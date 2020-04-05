from sagemaker.sklearn.estimator import SKLearn
import sagemaker
from sagemaker import get_execution_role
import boto3
import os
import sys

def get_session_and_role():

    # Create a SM session and get an appropraiate role.
    sagemaker_session = sagemaker.Session()

    # This execution role can only be inferred when executing in a AWS notebook. If running locally, pull your own role's details.
    try:
        role = sagemaker.get_execution_role()
    except ValueError:
        iam = boto3.client('iam')
        role = iam.get_role(RoleName = os.environ['SAGEMAKER_ROLE_NAME'])['Role']['Arn']
    
    return sagemaker_session, role

# Get session and role
session, role = get_session_and_role()
script_path = os.path.join(sys.path[0], 'train_and_deploy.py')

# Uncomment the session code to run in AWS, while also picking a suitable instance size rather than local.
sklearn = SKLearn(
    entry_point=script_path,
    train_instance_type="local",
    role=role,
    # sagemaker_session=session,
    hyperparameters={'max_leaf_nodes': 30})

sklearn.fit({'train': os.environ['S3_TRAINING_DATA']})

