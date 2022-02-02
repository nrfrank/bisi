FROM python:slim

ADD . /project_data
WORKDIR /project_data

ARG TEST_BUILD_ARG
RUN echo $TEST_BUILD_ARG > build_arg.txt
