# SPDX-FileCopyrightText: Copyright (c) 2025 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

import atexit
import socket
import docker
import json
import urllib.request
from pathlib import Path
from typing import Optional
import tarfile
from io import BytesIO
from functools import lru_cache

from docker.models.containers import Container
from docker.models.images import Image


class WebRTCManager:
    http_port = 8080
    report_path_to_container = {}
    image_name = 'nvidia/devtools/nsight-streamer-{}'
    timeout = 10     # seconds
    inside_docker = Path('/.dockerenv').exists()

    atexit.register(
        lambda: [container.stop() for container in WebRTCManager.report_path_to_container.values()])

    @classmethod
    def get_docker_client(cls):
        try:
            return docker.DockerClient()
        except docker.errors.DockerException as e:
            if cls.inside_docker:
                message = 'Failed to start docker client. Is the docker socket mounted? ' \
                    '(try adding "-v /var/run/docker.sock:/var/run/docker.sock" ' \
                    'to the docker run command).'
            else:
                message = 'Failed to start docker client. Is the docker service running? ' \
                    '(start it with "systemctl start docker").'

            message += ' Also make sure you have sufficient permissions, see: ' \
                'https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user'
            raise RuntimeError(message) from e

    @classmethod
    def get_docker_image(cls, docker_client: docker.DockerClient, tool_type: str):
        version = cls.get_latest_image_version(tool_type)
        image = f'nvcr.io/{cls.image_name.format(tool_type)}'
        return docker_client.images.get(f'{image}:{version}')

    @classmethod
    def create_container(cls, tool_type: str, report_path: Path, host: str):
        client = cls.get_docker_client()
        image = cls.get_docker_image(client, tool_type)

        if cls.inside_docker:
            http_port, turn_port = cls._get_free_ports_for_container(client, image)
        else:
            http_port, turn_port = None, cls._get_free_port()

        devtool_cmd = cls.get_image_env_var(image, 'DEVTOOL_CMD')
        ports = {cls.http_port: http_port, turn_port: turn_port}
        environment = {
            'DEVTOOL_CMD': f'{devtool_cmd} /mnt/host/{report_path.name}',
            'HOST_IP': host,
            'TURN_PORT': str(turn_port),
            'WEB_USERNAME': ''
        }

        container = client.containers.create(
            image=image,
            ports=ports,
            environment=environment,
            detach=True,
            auto_remove=True,
        )

        cls._copy_to_container(container, report_path)

        container.start()
        cls.report_path_to_container[report_path] = container

    @classmethod
    def run(cls, tool_type: str, report_path: Path, host: str):
        if report_path not in cls.report_path_to_container:
            cls.create_container(tool_type, report_path, host)
        container = cls.report_path_to_container[report_path]
        return cls.get_docker_client().api.port(container.id, cls.http_port)[0]["HostPort"]

    @classmethod
    def stop(cls, report_path: Path):
        cls.report_path_to_container[report_path].stop()
        del cls.report_path_to_container[report_path]

    @staticmethod
    def _get_free_port() -> int:
        with socket.socket() as s:
            s.bind(('', 0))
            return s.getsockname()[1]

    @staticmethod
    def _get_free_ports_for_container(client: docker.DockerClient, image: Image):
        """
        Get two free ports from the docker host (to be used as HTTP and TURN ports).
        This method is used when running inside a docker container.
        Since we can't get the host's ports directly, we start a container
        and let docker assign the ports. We then stop the container and return the ports,
        to be used when creating the actual container.
        """
        container: Container = client.containers.run(
            image=image, command='sleep infinity', detach=True, remove=True, stop_signal='SIGKILL',
            ports={WebRTCManager.http_port: None, WebRTCManager.http_port + 1: None})
        http_port = client.api.port(container.id, WebRTCManager.http_port)[0]["HostPort"]
        turn_port = client.api.port(container.id, WebRTCManager.http_port + 1)[0]["HostPort"]
        container.stop()
        return http_port, turn_port

    @staticmethod
    def _copy_to_container(container: Container, src: Path, arcname: Optional[str] = None):
        stream = BytesIO()
        with tarfile.open(fileobj=stream, mode='w|') as tar:
            tar.add(src, arcname=arcname or src.name)

        container.put_archive('/mnt/host', stream.getvalue())

    @staticmethod
    def get_image_env_var(image: Image, env_var: str) -> str:
        return next(filter(lambda x: x.startswith(f'{env_var}='), image.attrs['Config']['Env'])
               ).split('=')[1]

    @classmethod
    @lru_cache(maxsize=None)
    def get_latest_image_version(cls, tool_type: str):
        with urllib.request.urlopen(
            f'https://api.ngc.nvidia.com/v2/repos/{cls.image_name.format(tool_type)}'
        ) as response:
            return json.loads(response.read().decode())['latestTag']

    @classmethod
    def pull_image(cls, tool_type: str):
        cls.get_docker_client().images.pull(
            f'nvcr.io/{cls.image_name.format(tool_type)}:'
            + cls.get_latest_image_version(tool_type))
