# Azure ML - Local Debugging and Deployment
Deploy azure ml models  to a local container for debugging purposes 


#### Mac compatibility bug:
Model deployment fails due to Docker environment compatibility. As a temp workaround remove /private shared folder and add /var/folder

####Inspired by 
https://github.com/Azure/MachineLearningNotebooks/blob/master/how-to-use-azureml/deploy-to-local/register-model-deploy-local-advanced.ipynb
