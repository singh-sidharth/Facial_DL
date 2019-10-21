# @hidden_cell
# The following code contains the credentials for a file in your IBM Cloud Object Storage.
# You might want to remove those credentials before you share your notebook.
wml_credentials = { <PUT YOUR SERVICE CREDENTIALS HERE FOR WML>}

# NOTE: The model needs to be in .tgz format. Serialize the model with weights and then compress it with tar or gzip
!wget <link to the model to be deployed>

from watson_machine_learning_client import WatsonMachineLearningAPIClient
client = WatsonMachineLearningAPIClient( wml_credentials )

#This is the description of the platform the model was trained on
metadata = {
    client.repository.ModelMetaNames.NAME: "Mobile Detection",
    client.repository.ModelMetaNames.FRAMEWORK_NAME: "tensorflow",
    client.repository.ModelMetaNames.FRAMEWORK_VERSION: "1.11",
    client.repository.ModelMetaNames.FRAMEWORK_LIBRARIES: [{'name':'keras', 'version': '2.2.4'}]
}
model_details = client.repository.store_model( model="<MODEL_NAME>.tar.gz", meta_props=metadata )
#Deployment
model_id = model_details["metadata"]["guid"]
deployment_details = client.deployments.create( artifact_uid=model_id, name="Keras deployment" )
