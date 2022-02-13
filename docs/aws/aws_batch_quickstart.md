# AWS Batch

With [AWS Batch](https://aws.amazon.com/batch/) you can run your batch workloads in the cloud at any scale and bisi makes that easy for you.
To get started follow the [AWS Batch Setup Guide](docs/aws_batch_setup.md) to stand up a minimal Batch infrastructure setup running on CPU instances.

Once you have a batch job queue, you can configure bisi to utilize your batch infrastructure to run jobs. 
Assuming you ran the quickstart guide you can run the following to update your `bisi_resources.py` file.

```bash
echo 'import bisi.resources as bsr
from bisi.resources.config import BatchJobConfig, ECRConfig

df = bsr.Dockerfile(name="bisi_example", file="Dockerfile", ecr_config=ECRConfig("bisi_example"))

bsr.Job(name="numpy_example", entrypoint="workload.py", dockerfile=df, 
        batch_config=BatchJobConfig(jobQueue="bisi-test-jq"))' > bisi_resources.py
```

This configures bisi to upload your docker image to [Amazon ECR](https://aws.amazon.com/ecr/) and tells bisi where to submit your batch job.
Next you can deploy your container and run it in batch.

```bash
bisi deploy
bisi run --provider aws numpy_example
```

At this point you can navigate to https://console.aws.amazon.com/batch/home to see your pending job. 
From there you can also navigate to the job to see the logs for the job.

# Contact

* Open an issue at https://github.com/nrfrank/bisi 
* Contact bisi1.user@gmail.com about any questions/reports.
