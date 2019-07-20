#%% [markdown]
# Check core SDK version number
import azureml.core
print("SDK version:", azureml.core.VERSION)

#%% [markdown]
import logging
logging.basicConfig(level=logging.DEBUG)

#%% [markdown]
#Initialize Workspace
from azureml.core import Workspace
ws = Workspace.from_config()
print(ws.name, ws.resource_group, ws.location, ws.subscription_id, sep = '\n')

#%% [markdown]
#Inference config
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

from azureml.core.model import Model
model = Model(workspace=ws, name="aml-deploy-test-regression")

local_service = Model.deploy(ws, "aml-local-deployment", [model], inference_config, deployment_config)
local_service.wait_for_deployment(True)

#%% [markdown]
print(local_service.state)
print("scoring URI: " + local_service.scoring_uri)
print('Local service port: {}'.format(local_service.port))
#%% [markdown]
print(local_service.get_logs())

#%% [markdown]
#Test the endpoint
import json

sample_input = json.dumps({
    'data': [
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    ]
})

sample_input = bytes(sample_input, encoding='utf-8')

print(local_service.run(input_data=sample_input))

