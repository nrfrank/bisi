
class ECRConfig:

    def __init__(self, repositoryName: str, **kwargs):
        """Config class for creating an ECR repository
        All params get passed to https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr.html#ECR.Client.create_repository

        Args:
            repositoryName: the name of the repository to store an image to, bisi will create it if it doesn't exist
            **kwargs: extra arguments to pass to boto3.client('ecr').create_repository
        """
        self.repositoryName = repositoryName
        self.kwargs = kwargs

