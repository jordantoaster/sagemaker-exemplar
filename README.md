# sagemaker-exemplar

This repository is intended to act as an example end to end in which you can use Sagemaker to...

- Train a model using a model training job with SM.
- Deploy the trained model to an endpoint, and make predictions against it.
- Monitor the endpoint for data drift, using the built in sagemaker functionality.

These tasks were acheived using the 'studio' variant of sagemaker, which essentially offers a portal on top of a Jupyter instance which attempts to enable ease of collaboration while bringing all the SM functionality together into a UI. Due to these reasons it exceeds the standard managed notebook approach. 

Sagemaker studio is setup using IAM permissions and the default domain.

## Pros / Cons of using SM

### Pros

- If you need to keep your data in S3, away from local machines then SM is a solid option for building solutions in an AWS eco-system.
- The addition of a command line makes it quite flexible for environment management and tooling like DVC.
- Integration with Git is quite straightforward, which means you can use SM for dev as CI can still be built of the repository.
- You can setup a Sagemaker instance by either using pip driven installs or bringing along a docker image, which is a good option.
- The ability to switch instance type with a click of a button if you need to scale up notebook compute.
- Ease of integration with GPU driven notebooks, with some sensible instance defaults.
- Jump start materials for stock ML problems and starter code for things like BERT.
- You can submit training jobs to Sagemaker outside the notebook, to run concurrenctly or overnight as required.
- Able to unit test via command line and pytest, as well as lint checks etc.
- SM will continue to improve and grow.
- Different parts of the deployment flow seem like lego bricks, You can train a custom model normally, dump in S3 and create a model object for deployment from that artifact rather than creating a SM estimator.

### Cons

- Handling actual Python files has limitations regarding debugging and intellisense within SM, which makes sense given its a notebook environment.
- .gitignore file is hidden from the UI.
- Integration pattern of SM pushes towards an endpoint, although you can write custom code if you want to do normal ML EDA or experimentation,
- It is unclear how this fits into a Infra as code workflow generally.
- SM documentation can suck, out of date tutorials, especially in regard to studio UI.
- There seems to be different ways to do things, for example using the old sagemaker approach of 'fn' functions in scripts versus deploying using only the prediction objects.
- Experiments / Trails does not feel overly dev friendly compared to say MLFlow tracking.

## Observations of SM 

- Built in SM algorithms want the label columns to always be first in the dataframe.
- SM may not make total sense as a deployment tool when an ever running endpoint is not required, for example in one off monthly bach jobs.

### Local model

This allows you to use an IDE to write code and kick off sagemaker jobs, enabling IDE friendly features like debugging. It basically lets you use Sagemaker through the python package and configuring the AWS CLI to test/debug your code. It seems to involve changing how you reference your session object in code as well.

https://aws.amazon.com/blogs/machine-learning/use-the-amazon-sagemaker-local-mode-to-train-on-your-notebook-instance/
https://github.com/aws-samples/amazon-sagemaker-local-mode

"Amazon SageMaker Python SDK to test your algorithm locally, just by changing a single line of code.  This means that you can iterate and test your work without having to wait for a new training or hosting cluster to be built each time.  Iterating with a small sample of the dataset locally and then scaling to train on the full dataset in a distributed manner is common in machine learning.  Typically this would mean rewriting the entire process and hoping not to introduce any bugs.  The Amazon SageMaker local mode allows you to switch seamlessly between local and distributed, managed training by simply changing one line of code. Everything else works the same."

Local mode essentially lets you decide whether training happens on the local instance or in a training instance that SM spins up. This means you can jump from local laptop development in VS code to running the same code in sagemaker on a training instance or endpoint easily (aka on a server/cluster SM provisions).

## Tools

### DVC

You can install DVC as usual and point to a data store in S3 as required, the DVC workflow would then operate as normal.

### Poetry

The value of poetry is generally decreased if using sagemaker, but if the end goal is a package, it remains the right tool to use.

## SM in a theoritical ML workflow

### SM for model development, not deployment.

**Phase 1**

- Data resides in S3.
- Data processing and version for modelling occurs in a notebook, standard usage.
- EDA occurs in the same manner.
- Model building occurs as per typical development workflow.
- Model evaluation.
- output is a modelling artifact.

**Phase 2**

- The model artifact can be stored in S3.
- Production inference code can be written using VS code or other tool, to be deployed as a package or picked up by CI in the repository.

### Other Thoughts

- In a CI process (Jenkins) it is possible to install the Sagemaker pypi, add aws credentials and then setup a Sagemaker training job or endpoint using code written in Python files as well. Training as part of CI is probably not great idea, but endpoint deployment through models in S3 and versioned in env variables could be effective if a SM endpoint is required. With suitable monitoring as part of SM endpoint setup, which could be used to for cloudwatch logs / watching data drift over time.
