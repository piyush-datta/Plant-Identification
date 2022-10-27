from flask import Flask, jsonify, request, json
import os
import tensorflow
import urllib.request
import numpy as np
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

app= Flask(__name__)

MODEL_PATH ='plants_69.42.h5'

model = load_model(MODEL_PATH)

UPLOAD_FOLDER = '/home/piyush/project/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def main():
    return "Plant Identification"

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'files[]' not in request.files:
        resp= jsonify({'message':'No file part in the request'})
        resp.status_code = 400
        return resp

    files= request.files.getlist('files[]')

    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath= os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            img = image.load_img(filepath, target_size=(331, 331))
            img = image.img_to_array(img, dtype=np.uint8)
            img = np.array(img)/255.0
            img = np.expand_dims(img, axis = 0)
        
    
            pred = model.predict(img)
            
            labels = {0 : 'aloevera', 1:'banana', 2:'bilimbi', 3:'cantaloupe', 4:'cassava', 5:'coconut',
                    6: 'corn', 7: 'cucumber', 8: 'curcuma', 9: 'daisy', 10: 'dandelion', 11: 'eggplant', 
                    12: 'galangal', 13:'ginger', 14: 'guava', 15: 'kale', 16: 'longbeans', 17: 'mango', 
                    18: 'melon', 19:'orange', 20:'paddy', 21: 'papaya', 22:'peper chili', 23:'pineapple', 
                    24:'pomelo',25:'rose',26: 'shallot', 27:'soybeans', 28: 'spinach', 29: 'sunflower', 
                    30:'sweet potatoes', 31:'tobacco', 32:'tulip',33:'waterapple', 34:'watermelon'}
            predicted_class = labels[np.argmax(pred[0], axis=-1)]
            Maximum_Probability= str(np.max(pred[0], axis=-1)*100)

            return jsonify({"result":predicted_class, "probability":Maximum_Probability})

        else:
            errors[file.filename] = 'File type is not allowed'
            resp = jsonify(errors)
            resp.status_code = 500
            return resp

if __name__=='__main__':
 app.run(port=6001, debug=True)        

        



        
