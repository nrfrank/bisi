
import os
import sys
import docker

from typing import Iterable

from bisi.providers import Provider
from bisi.resources import Resource, Dockerfile, Job

docker_client = docker.from_env()


class Local(Provider):

    def build(self) -> None:
        """Builds the resources that are specified locally"""
        dockerfiles = Resource.get_resources(resource_type=Dockerfile)
        for dockerfile in dockerfiles:
            self.build_dockerfile(dockerfile)

    def deploy(self) -> None:
        pass  # stub to make project work

    def build_dockerfile(self, dockerfile: Dockerfile) -> None:
        """Builds the dockerfile locally using docker

        Args:
            dockerfile: the dockerfile to build
        """
        print(f'Building {dockerfile}')
        build_args = ' '.join([f'--build-arg "{k}={dockerfile.build_args[k]}"' for k in dockerfile.build_args]) \
            if dockerfile.build_args is not None else ''
        secrets = ' '.join([f'--secret "{secret}"' for secret in dockerfile.secret]) \
            if dockerfile.secret is not None else ''
        ssh = f'--ssh {dockerfile.ssh}' if dockerfile.ssh is not None else ''

        ret_val = os.system(
            f'docker build '
            f'-f {os.path.join(self.project_root_dir, dockerfile.file)} '
            f'-t {dockerfile.latest_image_tag()} '
            f'{build_args} '
            f'{secrets} '
            f'{ssh} '
            f'{self.project_root_dir} '
        )

        if ret_val != 0:
            raise Exception(f'Failed to build Dockerfile, exit_code = {ret_val}')

        for tag in dockerfile.tags[1:]:
            ret_val = os.system(f'docker tag {dockerfile.name}:{dockerfile.tags[0]} {dockerfile.name}:{tag}')
            if ret_val != 0:
                raise Exception(f'Failed to tag docker image')

    def run(self, name: str, arguments: Iterable[str]):
        """Runs the given resource with the provided arguments

        Args:
            name: the name of the resource to run
            arguments: the arguments to run with
        """
        job = Resource.get_resources(resource_type=Job, name=name)
        if len(job) != 1:
            raise Exception(f'Could not find job with name={name}')
        self.run_job(job[0], arguments)

    @staticmethod
    def run_job(job: Job, arguments: Iterable[str]):
        """Runs the job with the specified arguments locally with py-docker

        Args:
            job: the job to run
            arguments: the arguments to run with
        """
        print(f'Running {job}')

        command = [job.entrypoint] + list(arguments) + job.local_config.extra_args
        if job.entrypoint.endswith('.py'):
            command = ['python'] + command

        environment = job.environment.copy()
        environment.update(job.local_config.environment)

        try:
            container = docker_client.containers.run(
                image=job.dockerfile.latest_image_tag(),
                command=command,
                environment=environment,
                detach=True,
                **job.local_config.kwargs
            )
            for log in container.logs(stream=True, stdout=True, stderr=True):
                print(log.decode('utf-8').strip('\n'))

            if job.local_config.remove:
                container.remove()

        except Exception as e:
            print('Job Failed', file=sys.stderr)
            raise e
