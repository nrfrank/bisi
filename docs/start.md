# bisi

Bisi (**B**uild**I**t**S**hip**I**t) is a tool to help run workloads locally and in the cloud. 
Bisi lets you define and run all your containerized resources from one file stored at the root of your project all in python.

Currently supported providers are:
 - Locally with docker
 - AWS Batch
 
# Installation

## Prerequisites 
[Docker](https://docs.docker.com/get-docker/) is required to use bisi

The awscli and credentials are required to use the AWS Batch features.

```bash
pip install awscli
aws configure
```

## Install bisi

Install bisi from [pypi](https://pypi.org/project/bisi/)

```bash
pip install bisi
```

# Quickstart

Getting started with bisi is as simple as creating a Dockerfile and a bisi_resources.py file. 

Create a clean directory.

```bash
mkdir bisi_example
cd bisi_example
```

Run the following to create an example Dockerfile.

```bash
echo 'FROM python:slim
RUN pip install numpy
ADD . /bisi
WORKDIR /bisi' > Dockerfile
```

Next define an example workload as a python script.

```bash
echo 'import numpy
print(numpy.random.rand())' > workload.py
```

Finally create a bisi_resources.py file to tell bisi about our Dockerfile and how to run our workload.

```bash
echo 'import bisi.resources as bsr

df = bsr.Dockerfile(name="bisi_example", file="Dockerfile")

bsr.Job(name="numpy_example", entrypoint="workload.py", dockerfile=df)' > bisi_resources.py
```

Now you can use bisi to build your dockerfile and run it.

```bash
bisi build
bisi run numpy_example
```

From here you are free to use bisi to run anything from data processing to deep learning training in docker!
Check out the sections below for more detailed usage.

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
