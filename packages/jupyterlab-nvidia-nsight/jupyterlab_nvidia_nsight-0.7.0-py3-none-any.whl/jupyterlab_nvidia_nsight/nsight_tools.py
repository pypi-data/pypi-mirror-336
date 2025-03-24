# SPDX-FileCopyrightText: Copyright (c) 2025 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

from abc import ABC, abstractmethod
import shutil
from pathlib import Path
import tempfile
import shlex
import socket
from typing import List, Optional, Set
from jupyter_server.serverapp import ServerApp


class NsightTool(ABC):
    class VersionError(Exception):
        pass

    class ArgumentError(Exception):
        pass

    def __init__(self, kernel_id: str, installation_path: str, args: str):
        self.kernel_id = kernel_id
        self.installation_path = installation_path
        self.args = shlex.split(args)
        self.target_exe = shutil.which(self.target_exe_name(), path=self.target_exe_dir())
        self.host_exe = shutil.which(self.host_exe_name(), path=self.host_exe_dir())

    @abstractmethod
    def target_exe_name(self) -> str:
        """
        Returns the name of the tool executable
        """

    @abstractmethod
    def target_exe_dir(self) -> Optional[Path]:
        """
        Returns the path to the directory of the tool executable.
        """

    @abstractmethod
    def host_exe_name(self) -> str:
        """
        Returns the name of the tool's host executable
        """

    @abstractmethod
    def host_exe_dir(self, installation_path: str) -> Optional[Path]:
        """
        Returns the path to the directory of the tool's host executable.
        """

    @abstractmethod
    def launch_kernel_cmd(self) -> List[str]:
        """
        Returns the tool command to inject to the kernel launch command.
        """

    @abstractmethod
    def set_version(self, version: str) -> Optional[str]:
        """
        Set and validate the version of the tool.
        The version argument is the output of the tool executable when called with --version.
        The optional returned string is a warning that should be displayed to the user.
        Raises NsightTool.VersionError if the version is not supported.
        """

    @abstractmethod
    def get_start_code(self, **kwargs) -> str:
        """
        Returns the Python code to start the tool (to be executed by the kernel).
        """

    @abstractmethod
    def get_stop_code(self, **kwargs) -> str:
        """
        Returns the Python code to stop the tool (to be executed by the kernel).
        """

    @abstractmethod
    def cleanup(self):
        pass

    @abstractmethod
    def get_not_allowed_options(self):
        """
        Returns a set of options that are not allowed to be used with the tool.
        """

    @staticmethod
    def normalize_path(path: str):
        path = Path(path).expanduser()
        if not path.is_absolute():
            path = Path(ServerApp.instance().root_dir) / path
        return path.resolve()

    def _check_supported_args(self, args: Set[str]):
        not_allowed = args & self.get_not_allowed_options()
        if not_allowed:
            return 'The following options are not supported by Nsight extension: ' \
                f'{list(not_allowed)}. '
        return ''


class NsysProfiler(NsightTool):
    # TODO: DTSP-16323
    # TODO: DTSP-16324
    nsys_target_dir_name = 'target-linux-x64'
    nsys_host_dir_name = 'host-linux-x64'
    min_supported_version = '2024.1.1'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.requested_stats_report_path: Optional[Path] = None
        error_message = self._check_supported_args(set(self.args))
        if error_message:
            raise NsightTool.ArgumentError(error_message)

    def target_exe_name(self) -> str:
        return 'nsys'

    def target_exe_dir(self) -> Optional[Path]:
        if self.installation_path:
            return Path(self.installation_path) / self.nsys_target_dir_name

    def host_exe_name(self) -> str:
        return 'nsys-ui'

    def host_exe_dir(self) -> Optional[Path]:
        if self.installation_path:
            return Path(self.installation_path) / self.nsys_host_dir_name

    def launch_kernel_cmd(self) -> List[str]:
        return [self.target_exe, 'launch', f'--session={self.kernel_id}'] + self.args

    def set_version(self, version: str):
        version = version.split()[-1]
        if version != socket.gethostname():
            version = version.split('-')[0]
            if tuple(map(int, version.split('.'))) < tuple(map(int, self.min_supported_version.split('.'))):
                raise self.VersionError(f'jupyterlab-nvidia-nsight requires nsys >= "{self.min_supported_version}".'
                                        f' Found: "{version}"')

    def get_start_code(self, report_path: str, args: str) -> str:
        error_message = self._check_supported_args(set(shlex.split(args)))
        if error_message:
            raise self.ArgumentError(error_message)

        report_path = self.normalize_path(report_path)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        args = shlex.split(args)
        if '--stats=true' in args or \
           ('--stats' in args and len(args) > args.index('--stats') + 1 and args[args.index('--stats') + 1] == 'true'):
            self.requested_stats_report_path = report_path

        return f"""
subprocess.check_call(
    ['{self.target_exe}', 'start', '--session={self.kernel_id}', '--output={report_path}'] + {args})
"""

    def get_stop_code(self) -> str:
        code = f"""subprocess.check_call(
            ['{self.target_exe}', 'stop', '--session={self.kernel_id}'], stderr=subprocess.PIPE)
"""
        if self.requested_stats_report_path:
            code += f"""
if pathlib.Path('{self.requested_stats_report_path}').exists():
    subprocess.check_call(
        ['{self.target_exe}', 'stats', '{self.requested_stats_report_path}', '--force-export=true'])
"""
        self.requested_stats_report_path = None
        return code

    def cleanup(self):
        pass

    def get_not_allowed_options(self):
        return {
            '--help', '-h',
            '--hotkey-capture',
            '--output', '-o',
            '--session-new',
            '--session',
            '--stop-on-exit', '-x',
        }


class NcuProfiler(NsightTool):
    nvtx_domain = 'JupyterLabNvidiaNsight'
    min_supported_version = '2024.3'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validate_enable_args()
        self.ncu_ui_support = True

        # self.report_path contains the profiling results during the whole kernel lifecycle.
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.report_path = Path(self.tmp_dir.name) / 'report.ncu-rep'
        self.tmp_report_path = Path(self.tmp_dir.name) / 'tmp_report.ncu-rep'

    def target_exe_name(self) -> str:
        return 'ncu'

    def target_exe_dir(self) -> Optional[Path]:
        if self.installation_path:
            return Path(self.installation_path)

    def host_exe_name(self) -> str:
        return 'ncu-ui'

    def host_exe_dir(self) -> Optional[Path]:
        return self.target_exe_dir()

    def launch_kernel_cmd(self) -> List[str]:
        return [self.target_exe,
                '-o', str(self.report_path),
                '--nvtx-exclude', f'{self.nvtx_domain}@exclude'] + self.args

    def set_version(self, version: str):
        version = version.strip().splitlines()[-1].split()[1]
        if tuple(map(int, version.split('.'))) < tuple(map(int, self.min_supported_version.split('.'))):
            self.ncu_ui_support = False
            return f'''jupyterlab-nvidia-nsight requires ncu >= "{self.min_supported_version}" for full support.
Found: "{version}". Using console output only.'''

    def get_start_code(self, args: str) -> str:
        self.validate_start_args(set(shlex.split(args)))

    def get_stop_code(self, report_path: str, args: str, range_id: str) -> str:
        if not self.report_path.exists():
            return ''
        if not self.ncu_ui_support:
            # NCU < 2024.3
            return f"""
subprocess.check_call(
    '{self.target_exe} -i {self.report_path} --nvtx-include {self.nvtx_domain}@{range_id} {args}',
    shell=True)
"""

        report_path = self.normalize_path(report_path)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        return f"""
# First, filter from the full report the last cell(s) profiling results.
# This prevents flag conflict when the user uses "--nvtx-include".
subprocess.check_call(
    ['{self.target_exe}', '-i', '{self.report_path}',
     '--nvtx-include', '{self.nvtx_domain}@{range_id}', '-o', '{self.tmp_report_path}', '-f'],
    stdout=subprocess.DEVNULL)

# Export the new report, using the CLI flags provided by the user.
subprocess.check_call(
    '{self.target_exe} -i {self.tmp_report_path} -o {report_path} -f --log-file stderr {args}',
    shell=True)

# Generate console output of the new report, using the CLI flags provided by the user.
subprocess.check_call('{self.target_exe} -i {self.tmp_report_path} {args}', shell=True)
"""

    def cleanup(self):
        self.tmp_dir.cleanup()

    def validate_enable_args(self):
        if '--nvtx' not in self.args:
            self.args.append('--nvtx')

        args = set(self.args)
        error_message = self._check_supported_args(args)

        not_allowed_on_enable = args & self.NOT_ALLOWED_OPTIONS_ON_ENABLE
        if not_allowed_on_enable:
            error_message += 'The following options can be used only when profiling cells, ' \
                f'not when enabling ncu: {list(not_allowed_on_enable)}. '

        if error_message:
            raise self.ArgumentError(error_message)

    def validate_start_args(self, args: Set[str]):
        error_message = self._check_supported_args(args)

        not_allowed_on_start = args & self.NOT_ALLOWED_OPTIONS_ON_START
        if not_allowed_on_start:
            error_message += 'The following options can be used only when enabling NCU tool ' \
                + str(list(not_allowed_on_start))

        if error_message:
            raise self.ArgumentError(error_message)

    def get_not_allowed_options(self):
        return {
            '--app-replay-buffer',
            '--app-replay-match',
            '--app-replay-mode',
            '--check-exit-code',
            '--chips',
            '--config-file-path',
            '--config-file',
            '--export', '-o',
            '--force-overwrite', '-f',
            '--help', '-h',
            '--hostname',
            '--import', '-i',
            '--kill',
            '--list-chips',
            '--list-metrics',
            '--list-rules',
            '--list-sections',
            '--list-sets',
            '--log-file',
            '--mode',
            '--null-stdin',
            '--open-in-ui',
            '--profile-from-start',
            '--query-metrics-collection',
            '--query-metrics-mode',
            '--query-metrics',
            '--quiet',
            '--range-filter',
            '--range-replay-options',
            '--rename-kernels-export',
            '--replay-mode',
            '--section-folder-restore',
            '--version', '-v',
        }

    NOT_ALLOWED_OPTIONS_ON_ENABLE = {
        '--csv',
        '--devices',
        '--disable-extra-suffixes',
        '--filter-mode',
        '--kernel-id',
        '--kernel-name-base',
        '--kernel-name', '-k',
        '--launch-count', '-c',
        '--launch-skip-before-match',
        '--launch-skip', '-s',
        '--nvtx-exclude',
        '--nvtx-include',
        '--page',
        '--print-details',
        '--print-fp',
        '--print-kernel-base',
        '--print-metric-attribution',
        '--print-metric-instances',
        '--print-metric-name',
        '--print-nvtx-rename',
        '--print-rule-details',
        '--print-source',
        '--print-summary',
        '--print-units',
        '--rename-kernels-path',
        '--rename-kernels',
        '--resolve-source-file',
    }

    NOT_ALLOWED_OPTIONS_ON_START = {
        '--apply-rules',
        '--cache-control',
        '--call-stack-type',
        '--call-stack',
        '--clock-control',
        '--disable-profiler-start-stop',
        '--graph-profiling',
        '--import-source',
        '--injection-path-32',
        '--injection-path-64',
        '--max-connections',
        '--metrics',
        '--pm-sampling-buffer-size',
        '--pm-sampling-interval',
        '--pm-sampling-max-passes',
        '--port', '-p',
        '--preload-library',
        '--rule',
        '--section-folder-recursive',
        '--section-folder',
        '--section',
        '--set',
        '--source-folders',
        '--support-32bit',
        '--target-processes-filter',
        '--target-processes',
        '--verbose',
        '--warp-sampling-buffer-size',
        '--warp-sampling-interval',
        '--warp-sampling-max-passes',
    }


tools = {
    'nsys': NsysProfiler,
    'ncu': NcuProfiler
}
