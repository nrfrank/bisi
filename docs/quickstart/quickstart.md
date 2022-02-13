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

Finally create a bisi_resources.py file to tell bisi about your Dockerfile and how to run your workload.

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
