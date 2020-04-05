import numpy as np
import os
from sklearn import datasets

# S3 prefix for reuse later.
s3_prefix = 'sagemaker-exemplar'

# Create a SM session and get an appropraiate role.
sagemaker_session = sagemaker.Session()

def get_and_upload_data(s3_prefix, sagemaker_session):

    # Load Iris dataset, then join labels and features
    iris = datasets.load_iris()
    joined_iris = np.insert(iris.data, 0, iris.target, axis=1)

    # Create directory and write csv
    os.makedirs('./data', exist_ok=True)
    np.savetxt('./data/iris.csv', joined_iris, delimiter=',', fmt='%1.1f, %1.3f, %1.3f, %1.3f, %1.3f')

    DATA_DIRECTORY = 'data'
    train_input = sagemaker_session.upload_data(DATA_DIRECTORY, key_prefix="{}/{}".format(s3_prefix, DATA_DIRECTORY))


# Setup data - Brute Force, assume data does not exist on S3 yet.
get_and_upload_data(s3_prefix, sagemaker_session)