
import os
import boto3
import base64
import docker
import botocore.exceptions

from typing import Iterable

from bisi.providers.provider import CloudMixin
from bisi.resources import Resource, Dockerfile, Job
from bisi.providers import Provider

ecr_client = boto3.client('ecr')
batch_client = boto3.client('batch')
docker_client = docker.from_env()


class Aws(Provider, CloudMixin):

    def build(self) -> None:
        pass

    def deploy(self) -> None:
        """Deploys the jobs with a BatchJobConfig to AWS Batch and pushes their dockerfiles to ECR"""
        jobs = Resource.get_resources(resource_type=Job)

        for job in jobs:
            if job.batch_config is not None:
                full_repo_name = self.push_to_ecr(dockerfile=job.dockerfile)
                self.create_batch_job_definition(job=job, full_repo_name=full_repo_name)

    @staticmethod
    def ensure_repository_exists(repository_name, **kwargs) -> str:
        """Checks if the repository exists and creates if it doesn't

        Args:
            repository_name: the name of the repository to check/create
            **kwargs: extra args to pass to the create_repository function

        Returns:
            the full repository name
        """
        try:
            repos = ecr_client.describe_repositories(repositoryNames=[repository_name])
            return repos['repositories'][0]['repositoryUri']
        except botocore.exceptions.ClientError:
            repo = ecr_client.create_repository(repositoryName=repository_name, **kwargs)
            return repo['repository']['repositoryUri']

    @staticmethod
    def ensure_ecr_authenticated(server):
        """Logs into ECR so we can push docker images

        Args:
            server: the server to log in to
        """
        auth_creds = ecr_client.get_authorization_token()['authorizationData'][0]
        username, password = base64.b64decode(auth_creds['authorizationToken']).decode('utf-8').split(':')
        ret_val = os.system(f'docker login --username {username} --password {password} '
                            f'{server}')
        if ret_val != 0:
            raise Exception('Failed to login to ECR')

    @staticmethod
    def push_to_ecr(dockerfile: Dockerfile):
        """Pushes the dockerfile to ECR

        Args:
            dockerfile: the dockerfile to push
        """
        full_repo_name = Aws.ensure_repository_exists(dockerfile.ecr_config.repositoryName,
                                                      **dockerfile.ecr_config.kwargs)
        Aws.ensure_ecr_authenticated(full_repo_name.split('/')[0])
        for tag in dockerfile.tags:
            result = docker_client.api.tag(f'{dockerfile.name}:{tag}', full_repo_name, tag=tag, force=True)
            if result is False:
                raise Exception('Failed to tag docker image')

            ret_val = os.system(f'docker push {full_repo_name}:{tag}')
            if ret_val != 0:
                raise Exception('Failed to push docker image')
        return full_repo_name

    @staticmethod
    def get_ecr_image_digest(repo_name, tag):
        paginator = ecr_client.get_paginator('list_images')

        for images in paginator.paginate(repositoryName=repo_name):
            for image in images['imageIds']:
                if image.get('imageTag', None) == tag:
                    return image['imageDigest']
        raise Exception('Could not find ECR image')

    @staticmethod
    def create_batch_job_definition(job: Job, full_repo_name: str):
        """Registers a batch job definition for this job

        Args:
            job: the job to create a definition for
            full_repo_name: the ECR repo name for this job to pull from
        """
        image_digest = Aws.get_ecr_image_digest(job.dockerfile.ecr_config.repositoryName, job.dockerfile.tags[0])
        container_properties = job.batch_config.containerProperties.copy()
        container_properties['image'] = f'{full_repo_name}@{image_digest}'
        batch_client.register_job_definition(
            jobDefinitionName=job.batch_config.jobDefinitionName,
            type=job.batch_config.type,
            containerProperties=container_properties,
            **job.batch_config.kwargs
        )

    def run(self, name: str, arguments: Iterable[str]):
        """Runs the given resources with the given arguments

        Args:
            name: the name of the resource to run
            arguments: a list of arguments to run with
        """
        job = Resource.get_resources(resource_type=Job, name=name)
        if len(job) != 1:
            raise Exception(f'Could not find job with name={name}')
        self.run_job(job[0], arguments)

    @staticmethod
    def run_job(job: Job, arguments: Iterable[str]):
        """Runs the given job with the specified arguments in AWS Batch

        Args:
            job: the job to run
            arguments: a list of arguments to run with
        """
        assert job.batch_config is not None, 'batch_config is required for running a batch job'

        print(f'Running {job}')

        command = [job.entrypoint] + list(arguments) + job.batch_config.extra_args
        if job.entrypoint.endswith('.py'):
            command = ['python'] + command

        environment = job.environment.copy()
        environment.update(job.batch_config.environment)

        batch_client.submit_job(
            jobName=job.name,
            jobQueue=job.batch_config.jobQueue,
            jobDefinition=job.batch_config.jobDefinitionName,
            containerOverrides={
                'command': command,
                'environment': [{'name': key, 'value': value} for key, value in environment.items()]
            }
        )
