import os
import pandas as pd
from sagemaker_containers.beta.framework import worker
from sklearn.tree import DecisionTreeClassifier
import argparse
from sklearn.externals import joblib

def train_fn(train_dir):

    # Take the set of files and read them all into a single pandas dataframe
    input_files = [ os.path.join(train_dir, file) for file in os.listdir(args.train)]

    raw_data = [pd.read_csv(file, header=None) for file in input_files]
    train_data = pd.concat(raw_data)

    # labels are in the first column
    train_y = train_data.ix[:,0]
    train_X = train_data.ix[:,1:]

    # Now use scikit-learn's decision tree classifier to train the model.
    clf = DecisionTreeClassifier()
    clf = clf.fit(train_X, train_y)

    joblib.dump(clf, os.path.join(args.model_dir, "model.joblib"))


def model_fn(model_dir):
    clf = joblib.load(os.path.join(model_dir, "model.joblib"))
    return clf


def output_fn(prediction, accept):
    if accept == "application/json":
        return worker.Response(json.dumps(prediction), accept, mimetype=accept)

def predict_fn(input_data, model):
    # X = data_transformation(input_data)
    prediction = model.predict(input_data)
    return {'predicted-value': prediction}


if __name__ == '__main__':

    # Get Args
    parser = argparse.ArgumentParser()
    # Sagemaker specific arguments. Defaults are set in the environment variables - if you use that approach.
    parser.add_argument('--output-data-dir', type=str, default=os.environ['SM_OUTPUT_DATA_DIR'])
    parser.add_argument('--model-dir', type=str, default=os.environ['SM_MODEL_DIR'])
    parser.add_argument('--train', type=str, default=os.environ['SM_CHANNEL_TRAIN'])
    parser.add_argument('--max_leaf_nodes', type=int, default=-1)
    args = parser.parse_args()

    # Train
    clf = train_fn(args.train)

