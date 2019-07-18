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

#%% [markdown]

from azureml.core.model import InferenceConfig

inference_config = InferenceConfig(source_directory="deploy-source",
                                   runtime= "python", 
                                   entry_script="x/y/score.py",
                                   conda_file="env/myenv.yml", 
                                   extra_docker_file_steps="dockerstep/customDockerStep.txt")


#%% [markdown]
# Deploy to Docker local 
from azureml.core.webservice import LocalWebservice

#this is optional, if not provided we choose random port
deployment_config = LocalWebservice.deploy_configuration(port=6789)

model_list = Model.list(workspace=ws)

local_service = Model.deploy(ws, "aml-deploy-test-regression", model_list[:1], inference_config, deployment_config)
local_service.wait_for_deployment()

#%% [markdown]
print('Local service port: {}'.format(local_service.port))

#%% [markdown]
print(local_service.get_logs())

#%% [markdown]
import json

sample_input = json.dumps({
    'data': [
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    ]
})

sample_input = bytes(sample_input, encoding='utf-8')

print(local_service.run(input_data=sample_input))

#%% [markdown]
