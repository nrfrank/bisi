# Infrastructure setup for AWS Batch

This guide walks through setting up the required infrastruce to use bisi with AWS Batch.

Prerequisites: 
 - awscli installed (`pip install awscli`)
 - AWS credentials configured (`aws configure`)

## IAM Permission Requirements

AWS Managed Policies
- AWSBatchFullAccess
- AWSCloudFormationFullAccess
- AmazonElasticContainerRegistryPublicFullAccess

- Extra inline policy:
    ```json
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": "ecr:*",
                "Resource": "*"
            },
            {
                "Sid": "VisualEditor0",
                "Effect": "Allow",
                "Action": "iam:PassRole",
                "Resource": "*"
            }
        ]
    }
    ```

# Cloudformation Stack

A minimal setup can be achieved with a cloudformation stack. 
The stack requires two parameters for what subnets and security groups to use for the AWS Batch compute environment.
You can navigate the VPC AWS console to get values for these parameters. 
Replace the variables below with your parameters and run the code in your terminal to create the infrastructure.

```bash
SUBNETS='YOUR_SUBNET1\,YOUR_SUBNET2\,YOUR_SUBNET3'
SECURITYGROUPS=YOUR_SECURITYGROUP

echo 'Parameters:
  Subnets:
    Type: CommaDelimitedList
  SecurityGroups:
    Type: CommaDelimitedList

Resources:
  ComputeEnvironment:
    Type: AWS::Batch::ComputeEnvironment
    Properties:
      Type: MANAGED
      ServiceRole: aws-service-role/batch.amazonaws.com/AWSServiceRoleForBatch
      ComputeEnvironmentName: bisi-test-ce
      ComputeResources:
        MaxvCpus: 4
        Type: EC2
        MinvCpus: 0
        Subnets:
          Ref: Subnets
        SecurityGroupIds:
          Ref: SecurityGroups
        InstanceRole: ecsInstanceRole
        InstanceTypes:
          - optimal
        DesiredvCpus: 0
      State: ENABLED

  JobQueue:
    Type: AWS::Batch::JobQueue
    Properties:
      ComputeEnvironmentOrder:
        - Order: 1
          ComputeEnvironment: bisi-test-ce
      State: ENABLED
      Priority: 1
      JobQueueName: bisi-test-jq
    DependsOn: ComputeEnvironment' > ./aws_batch_stack.yaml

aws cloudformation create-stack --stack-name bisi-batch-minimal \
    --template-body "$(cat ./aws_batch_stack.yaml)" \
    --parameters ParameterKey=Subnets,ParameterValue="$SUBNETS" \
    ParameterKey=SecurityGroups,ParameterValue="$SECURITYGROUPS"
```
