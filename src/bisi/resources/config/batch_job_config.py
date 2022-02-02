
from typing import Dict, List


class BatchJobConfig:

    def __init__(self, jobQueue: str, jobDefinitionName: str = None, containerProperties: dict = None,
                 extra_args: List[str] = None, environment: Dict[str, str] = None, **kwargs):
        """Config class for configuring batch jobs
        most arguments are passed to https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch.html#Batch.Client.register_job_definition

        Args:
            jobQueue: The batch job queue to submit the job to
            jobDefinitionName: the name to give the job definition
            containerProperties: The container properties to set for the job, defaults to 2 vcpus and 1GB of memory,
                when running with bisi, image, command, and environment are overridden
            extra_args: a list of extra arguments to call the entrypoint with
            environment: a dictionary of environment variables to set for batch jobs
            **kwargs: extra args to pass to boto3.client('batch').register_job_definition
        """
        self.jobQueue = jobQueue
        self.jobDefinitionName = jobDefinitionName
        self.type = 'container'
        if containerProperties is None:
            self.containerProperties = {
                'vcpus': 2,
                'memory': 1024
            }
        else:
            self.containerProperties = containerProperties

        self.extra_args = extra_args if extra_args else list()
        self.environment = environment if environment else dict()
        self.kwargs = kwargs
