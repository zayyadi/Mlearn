from flask import Flask, request, jsonify, render_template
import json
import pickle
import numpy as np
from flask_cors import cross_origin

def load_gender():
    
    print("loading saved artifacts...start")

    with open("_bmi.json", "r") as f:
        data_columns = json.load(f)['data_columns']
        gender = data_columns[2:]  # first 3 columns are sqft, bath, bhk
    return gender

def load_model():
    model = None

    if model is None:
        with open('Bmi_model.pickle', 'rb') as f:
            model = pickle.load(f)

    return model


def get_estimated_bmi(gender,weight_in_kg,height_sqr):
    __data_columns=None
    __gender=None
    __model=None
    with open("_bmi.json", "r") as f:
        __data_columns = json.load(f)['data_columns']
        __gender = __data_columns[2:]
    if __model is None:
        with open('Bmi_model.pickle', 'rb') as f:
            __model = pickle.load(f)
    try:
        loc_index = __data_columns.index(gender.lower())
    except:
        loc_index = -1

    x = np.zeros(len(__data_columns))
    x[0] = weight_in_kg
    x[1] = height_sqr
    if loc_index>=0:
        x[loc_index] = 1

    return round(__model.predict([x])[0],1)



    # if model is None:
    #     with open('./artifacts/Bmi_model.pickle', 'rb') as f:
    #         model = pickle.load(f)
    # print("loading saved artifacts...done")


def gender():
    return load_gender()

app = Flask(__name__)
# CORS(app)

model = pickle.load(open('Bmi_model.pickle','rb'))

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/get_gender', methods=['GET'])
def get_gender():
    response =jsonify({
        'gender': gender()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/predict_bmi', methods=['GET', 'POST'])
@cross_origin()
def predict_bmi():
   
    gender = request.form['gender']
    weight_in_kg = int(request.form['weight'])
    height_sqr = float(request.form['height'])


    response = jsonify({
        'bmi': get_estimated_bmi(gender,weight_in_kg ,height_sqr)
    })
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")

    return response


if __name__ == "__main__":
    # print("Starting Python Flask Server For Home Price Prediction...")
    # utils.load_saved_artifacts()
    # # print(utils.get_gender())
    app.run(host='0.0.0.0')