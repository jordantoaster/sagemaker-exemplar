# sagemaker-exemplar

## TODO

- Need model_fn, predict_fn, input_fn code.
- Need code to create estimator.
- Based on examples I am seeing, the general worker is the training script.


## Ideas

Env Variables could be packaged in the CI pipeline, which then drives training and deployment if Master.

You can also run computation locally.

----
Putting iluoyi's solution in code

try:
    role = sagemaker.get_execution_role()
except ValueError:
    iam = boto3.client('iam')
    role = iam.get_role(RoleName='AmazonSageMaker-ExecutionRole-20191205T100050')['Role']['Arn']
A SageMaker execution role exists if you ever ran a job before, if not:

Log onto the console -> IAM -> Roles -> Create Role
Create a service-linked role with sagemaker.amazonaws.com
Give the role AmazonSageMakerFullAccess
Give the role AmazonS3FullAccess (<-- scope down if reasonable)
Then use the name in RoleName= like above

A potential long term solution would be to create a function that checks for an existing execution service role, if it does not exist, then create the new role.....but service-role creation with managed policies through boto3 IAM requires......patience....

I used a sagemaker default role that AWS gave me an option to select
----

https://github.com/awslabs/amazon-sagemaker-examples/blob/master/sagemaker-python-sdk/scikit_learn_iris/Scikit-learn%20Estimator%20Example%20With%20Batch%20Transform.ipynb
