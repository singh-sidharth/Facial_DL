import requests,json
from PIL import Image
import numpy as np

img = Image.open( "img.jpg" )
img = img.resize((100,100))
img_as_arr  = np.asarray( img )
img_as_list = img_as_arr.tolist()
payload = { "values" : [ img_as_list ] }

# NOTE: Get the ml_instance id from service credentials of machine learning instance
ml_instance_id="c2165c94-7bb3-45fc-ae23-79a26021a531"
# NOTE: Generate iam_token based on apikey
# another apikey=<jGfi97h047faAAf7SBsGm6cAAFu_KbisQIX2IUCFqmE->
print("Generating IAM Token")
url="https://iam.cloud.ibm.com/identity/token"
iam_header={'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'application/json'}
data={"grant_type":"urn:ibm:params:oauth:grant-type:apikey", "apikey":"pRjsn8ZCMWPvKAxtXMYtT0iyYSw5_I2eyuHcy-yGnj1P"}
resp = requests.post(url=url, data=data, headers=iam_header)
iam_token=resp.json()["access_token"]
iam_token='Bearer '+iam_token
print("Received token is : ",iam_token)

# NOTE: generate iam_token and retrieve ml_instance_id based on provided documentation	
header ={'Content-Type' :'application/json', 'Authorization': iam_token, 'ML-Instance-ID': ml_instance_id}

response_scoring = requests.post('https://jp-tok.ml.cloud.ibm.com/v3/wml_instances/c2165c94-7bb3-45fc-ae23-79a26021a531/deployments/d2b2eb68-ea76-4ee0-a254-bc12801437d1/online', json=payload, headers=header)
print("Scoring response")
response=json.loads(response_scoring.text)
print(response)
response=response['values']
prediction=np.argmax(response)
print(prediction)
# Class 0 is mobile and Class 1 is not
predicted_class = 'Mobile' if response==1 else 'Not Mobile'
print(predicted_class)