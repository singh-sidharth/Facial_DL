from flask import Flask, flash, request, redirect, url_for, render_template, session
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import os

app = Flask(__name__)
TEMP_FOLDER='./temp'
app.config['UPLOAD_FOLDER']=TEMP_FOLDER
app.secret_key = "My secret key"
CORS(app)
prediction = None
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
#load the model before starting server
resnet_model = load_model("resnet.h5")

#Predicting the value and removing the temp
def predict_image(file):
    filename=secure_filename(file.filename)
    location=os.path.join(app.config['UPLOAD_FOLDER'],filename)
    file.save(location)
    test_image=load_img(location,color_mode='rgb', target_size = (100, 100))
    test_image = img_to_array(test_image)
    test_image=np.array([test_image])
    prediction = resnet_model.predict(test_image)
    os.remove(location)
    prediction = prediction.argmax(axis=-1)

#Check for the allowed file extensions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#The main web page to be served
@app.route('/')
def index():
    return render_template("index.html")

#Exposed api to predict
@app.route("/predict", methods=['POST'])
def predict():
    print(request.headers)
    # Check the request parameters
    if request.method == 'POST':
        file = request.files['image']

        if 'image' not in request.files:
            flash("No file received")
            return "No file received"

        if file and allowed_file(file.filename):
            predict_image(file)
            flash (True if prediction == 1 else False)
            return True if prediction == 1 else False
        else:
            flash('No selected file')
            return redirect(request.url)
    return "Unidentified Error Occured at server!!"

# start the flask app, allow remote connections
if __name__ == '__main__':
    app.run(host='127.0.0.5', debug = True)