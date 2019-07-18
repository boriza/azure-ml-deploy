#%% [markdown]
# Check core SDK version number
import azureml.core
print("SDK version:", azureml.core.VERSION)

#%% [markdown]
#Initialize Workspace
from azureml.core import Workspace
ws = Workspace.from_config()
print(ws.name, ws.resource_group, ws.location, ws.subscription_id, sep = '\n')

#%% [markdown]
#register model

from azureml.core.model import Model

model = Model.register(model_path = "sklearn_regression_model.pkl",
                       model_name = "aml-deploy-test-regression",
                       tags = {'area': "diabetes", 'type': "regression"},
                       description = "Ridge regression model to predict diabetes",
                       workspace = ws)

#%% [markdown]
#folder structure 
import os

source_directory = "deploy-source"

os.makedirs(source_directory, exist_ok = True)
os.makedirs("deploy-source/x/y", exist_ok = True)
os.makedirs("deploy-source/env", exist_ok = True)
os.makedirs("deploy-source/dockerstep", exist_ok = True)

#%% [markdown]
%%writefile deploy-source/dockerstep/customDockerStep.txt
RUN echo "this is test"

#%% [markdown]
#write a data file 
%%writefile deploy-source/extradata.json
{
    "people": [
        {
            "website": "microsoft.com", 
            "from": "Seattle", 
            "name": "Mrudula"
        }
    ]
}
