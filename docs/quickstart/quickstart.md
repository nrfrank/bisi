# Quickstart

Getting started with bisi is as simple as creating a Dockerfile and a bisi_resources.py file. 

1. Create a clean directory.

    ```bash
    mkdir bisi_example
    cd bisi_example
    ```

2. Run the following to create an example Dockerfile.

    ```bash
    echo 'FROM python:slim
    RUN pip install numpy
    ADD . /bisi
    WORKDIR /bisi' > Dockerfile
    ```

3. Next define an example workload as a python script.

    ```bash
    echo 'import numpy
    import sys
    print(numpy.add(1, int(sys.argv[1])))' > workload.py  # This scripts prints the output 1 + the first argument passed to it.
    ```

4. Finally create a bisi_resources.py file to tell bisi about your Dockerfile and how to run your workload.

    ```bash
    echo 'import bisi.resources as bsr
    
    df = bsr.Dockerfile(name="bisi_example", file="Dockerfile")
    
    bsr.Job(name="numpy_example", entrypoint="workload.py", dockerfile=df)' > bisi_resources.py
    ```

5. Now you can use bisi to build your dockerfile and run it with arguments.

    ```bash
    bisi build
    bisi run numpy_example -- 2  # Bisi will pass everything after the `--` marker to your script as arguments
    ```

From here you are free to use bisi to run anything from data processing to deep learning training with docker!
