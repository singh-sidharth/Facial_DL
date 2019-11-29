import io
import requests,json
from PIL import Image
import numpy as np
from picamera import PiCamera
from picamera.array import PiRGBArray
from time import sleep
#Creating an instance for the pi camera
camera = PiCamera(resolution=(100,100))
while True:    
    #camera.start_preview()
    sleep(5)
    with PiRGBArray(camera, size=(100,100)) as output:
        camera.capture(output,'rgb')   
        payload = { "values" : [output.array] }        
        # NOTE: Get the ml_instance id from service credentials of machine learning instance
        ml_instance_id="084b11f3-c072-4d12-b7a3-ec806f3500e3"
        # NOTE: Generate iam_token based on apikey
        # another apikey=<jGfi97h047faAAf7SBsGm6cAAFu_KbisQIX2IUCFqmE->
        print("Generating IAM Token")
        url="https://iam.cloud.ibm.com/identity/token"
        iam_header={'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'application/json'}
        data={"grant_type":"urn:ibm:params:oauth:grant-type:apikey", "apikey":"Ws-Y6SW7YIGIaM13N2HY2_hkoC1JuvuWYmpNqQYrjFhT"}
        resp = requests.post(url=url, data=data, headers=iam_header)
        iam_token=resp.json()["access_token"]
        iam_token='Bearer '+iam_token
        print("Received token is : ",iam_token)

        # NOTE: generate iam_token and retrieve ml_instance_id based on provided documentation  
        header ={'Content-Type' :'application/json', 'Authorization': iam_token, 'ML-Instance-ID': ml_instance_id}

        response_scoring = requests.post('https://jp-tok.ml.cloud.ibm.com/v3/wml_instances/084b11f3-c072-4d12-b7a3-ec806f3500e3/deployments/fa86647a-737b-4A93-aa5c-0da9957a32c4/online', json=payload, headers=header)
        print("Scoring response")
        response=json.loads(response_scoring.text)
        print(response)
        response=response['values']
        prediction=np.argmax(response)
        print(prediction)
        # Class 1 is mobile and Class 0 is not
        predicted_class = 'Mobile' if prediction==1 else 'Not Mobile'
        print(predicted_class)
        output.truncate(0)
        sleep(195)
        if prediction == 1:
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            print("WARNING: MOBILE SPOOFING DETECTED!!!!")
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            #camera.stop_preview()
            break
        
    

