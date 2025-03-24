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
from pathlib import Path
from http import HTTPStatus
import functools
import json
import socket
import docker.errors
from typing import Dict, List
from jupyter_server.base.handlers import APIHandler
from jupyter_server.utils import url_path_join
import tornado
from jupyter_client.provisioning import KernelProvisionerFactory
from jupyter_client.provisioning.provisioner_base import KernelProvisionerBase

from .nsight_tools import NsightTool, tools
from .webrtc_container import WebRTCManager


kernel_id_to_nsight_tool: Dict[str, NsightTool] = {}
default_host = socket.getfqdn()


def wrap_provisioner(provisioner: KernelProvisionerBase):
    def launch_kernel_wrapper(func):
        @functools.wraps(func)
        def launch_kernel(cmd: List[str], **kwargs):
            tool = kernel_id_to_nsight_tool.get(provisioner.kernel_id, None)
            if tool is not None:
                cmd = tool.launch_kernel_cmd() + cmd
            return func(cmd, **kwargs)
        return launch_kernel

    provisioner.launch_kernel = launch_kernel_wrapper(provisioner.launch_kernel)


def wrap_kernel_provisioner_factory():
    def create_provisioner_instance_wrapper(func):
        @functools.wraps(func)
        def create_provisioner_instance(*args, **kwargs):
            provisioner = func(*args, **kwargs)
            wrap_provisioner(provisioner)
            return provisioner
        return create_provisioner_instance
    KernelProvisionerFactory.create_provisioner_instance = create_provisioner_instance_wrapper(
        KernelProvisionerFactory.create_provisioner_instance)


class HandlerBase(APIHandler, ABC):
    @abstractmethod
    def post_impl(self, **kwargs):
        pass

    @tornado.web.authenticated
    def post(self):
        try:
            self.post_impl(**(self.get_json_body() or {}))
        except BaseException as e:
            self.set_status(HTTPStatus.INTERNAL_SERVER_ERROR.value)
            self.finish(json.dumps({'message': str(e)}))


class DoIsInsideDockerHandler(HandlerBase):
    def post_impl(self):
        self.finish(json.dumps({'inside_docker': WebRTCManager.inside_docker}))


class DoEnableHandler(HandlerBase):
    def post_impl(self, *,
                  tool_type: str, kernel_id: str, args: str = '', installation_path: str = ''):
        tool = tools[tool_type](kernel_id, installation_path, args)
        if tool.target_exe is None:
            message = f'Could not find {tool_type} executable. ' \
                'Please set the installation path in jupyterlab-nvidia-nsight extension settings'
            self.set_status(HTTPStatus.INTERNAL_SERVER_ERROR.value)
            self.finish(json.dumps({'message': message}))
            return
        kernel_id_to_nsight_tool[kernel_id] = tool
        self.finish(json.dumps({'target_exe': tool.target_exe or '',
                    'launch_kernel_cmd': str(tool.launch_kernel_cmd())}))


class DoDisableHandler(HandlerBase):
    def post_impl(self, *, kernel_id: str):
        tool = kernel_id_to_nsight_tool.pop(kernel_id)
        tool.cleanup()
        self.finish()


class DoSetVersionHandler(HandlerBase):
    def post_impl(self, *, kernel_id: str, version: str):
        try:
            warning = kernel_id_to_nsight_tool[kernel_id].set_version(version)
            if warning:
                self.finish(json.dumps({'warning': warning}))
            else:
                self.finish()
        except NsightTool.VersionError as e:
            self.set_status(HTTPStatus.INTERNAL_SERVER_ERROR.value)
            self.finish(json.dumps({'message': str(e)}))


class DoGetStartCodeHandler(HandlerBase):
    def post_impl(self, *, kernel_id: str, **start_kwargs):
        code = kernel_id_to_nsight_tool[kernel_id].get_start_code(**start_kwargs)
        self.finish(json.dumps({'code': code}))


class DoGetStopCodeHandler(HandlerBase):
    def post_impl(self, *, kernel_id, **stop_kwargs):
        code = kernel_id_to_nsight_tool[kernel_id].get_stop_code(**stop_kwargs)
        self.finish(json.dumps({'code': code}))


class DoStartWebRTCHandler(HandlerBase):
    def post_impl(self, *, report_path: str, tool_type: str, host: str = default_host):
        try:
            port = WebRTCManager.run(tool_type, NsightTool.normalize_path(report_path), host)
            if port is None:
                self.set_status(HTTPStatus.INTERNAL_SERVER_ERROR.value)
                self.finish(json.dumps({'message': 'Failed to start WebRTC container'}))
            else:
                self.finish(json.dumps({'url': f'http://{host}:{port}'}))
        except Exception as e:
            self.set_status(HTTPStatus.INTERNAL_SERVER_ERROR.value)
            self.finish(json.dumps({'message': repr(e)}))


class DoStopWebRTCHandler(HandlerBase):
    def post_impl(self, *, report_path: str):
        WebRTCManager.stop(NsightTool.normalize_path(report_path))
        self.finish()


class DoIsFileExistsHandler(HandlerBase):
    def post_impl(self, *, path: str):
        self.finish(json.dumps({'exists': NsightTool.normalize_path(path).exists()}))


class DoIsWebRTCPulledHandler(HandlerBase):
    def post_impl(self, *, tool_type: str):
        try:
            WebRTCManager.get_docker_image(WebRTCManager.get_docker_client(), tool_type)
            self.finish(json.dumps({'pulled': True}))
        except docker.errors.ImageNotFound as e:
            self.finish(json.dumps({'pulled': False, 'message': e.explanation}))


class DoPullWebRTCHandler(HandlerBase):
    def post_impl(self, *, tool_type: str):
        WebRTCManager.pull_image(tool_type)
        self.finish()


class DoCheckOutputDir(HandlerBase):
    def post_impl(self, *, path: str):
        path = NsightTool.normalize_path(path)
        if not path.exists():
            self.set_status(HTTPStatus.INTERNAL_SERVER_ERROR.value)
            self.finish(json.dumps({'message': f'Output directory does not exist: "{path}"'}))
            return
        if not path.is_dir():
            self.set_status(HTTPStatus.INTERNAL_SERVER_ERROR.value)
            self.finish(json.dumps({'message': f'Output directory is not a directory: "{path}"'}))
            return

        # Verify permissions
        test_path = path / 'jupyterlab_nvidia_nsight_permission_test.txt'
        try:
            test_path.touch()
            test_path.unlink()
            self.finish()
        except PermissionError:
            self.set_status(HTTPStatus.INTERNAL_SERVER_ERROR.value)
            self.finish(json.dumps({'message': f'Output directory is not writable: "{path}"'}))

def setup_handlers(web_app):
    base_route_pattern = url_path_join(web_app.settings['base_url'], 'jupyterlab-nvidia-nsight')
    handlers = [
        (url_path_join(base_route_pattern, name), handler)
        for name, handler in (
            ('is-inside-docker', DoIsInsideDockerHandler),
            ('enable', DoEnableHandler),
            ('disable', DoDisableHandler),
            ('set-version', DoSetVersionHandler),
            ('get-start-code', DoGetStartCodeHandler),
            ('get-stop-code', DoGetStopCodeHandler),
            ('start-webrtc', DoStartWebRTCHandler),
            ('stop-webrtc', DoStopWebRTCHandler),
            ('is-file-exists', DoIsFileExistsHandler),
            ('is-webrtc-pulled', DoIsWebRTCPulledHandler),
            ('pull-webrtc', DoPullWebRTCHandler),
            ('check-output-directory', DoCheckOutputDir),
        )
    ]
    web_app.add_handlers('.*$', handlers)
    wrap_kernel_provisioner_factory()
