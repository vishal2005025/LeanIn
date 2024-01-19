from flask import Flask, request, jsonify, render_template, url_for
from tensorflow.keras.models import load_model
import numpy as np
import joblib
from PIL import Image
import os
import pickle
import json
import pandas as pd
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import plotly
from plotly.graph_objs import Bar

app = Flask(__name__)

def tokenize(text):
    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()

    clean_tokens = []
    for tok in tokens:
        clean_tok = lemmatizer.lemmatize(tok).lower().strip()
        clean_tokens.append(clean_tok)

    return clean_tokens

df = pd.read_csv('D:/Rubix_hackathon/Rubix/flask/data/Disasters_messages.csv')

# Load the trained models
damage_model = load_model('D:/Rubix_hackathon/Rubix/flask/models/disaster_model.h5')
disaster_model = load_model('D:/Rubix_hackathon/Rubix/flask/models/my_model.h5')
regional_model = load_model('D:/Rubix_hackathon/Rubix/flask/models/damage_eval_model.h5')
logreg = joblib.load('D:/Rubix_hackathon/Rubix/flask/models/flood_prediction.pkl')
model=pickle.load(open('D:/Rubix_hackathon/Rubix/flask/models/fire_prediction_model.pkl','rb'))
analysis_model = joblib.load("D:/Rubix_hackathon/Rubix/flask/models/message_model.pkl")

damage_types = np.array(sorted(['disaster happened', 'no disaster happened']))
disaster_types = np.array(sorted(['volcano', 'flooding', 'earthquake', 'fire', 'wind', 'tsunami']))
damage_levels = np.array(['no damage', 'minor damage', 'major damage', 'destroyed'])

@app.route('/image')
def image():
    return render_template('satelliteImagery.html')

@app.route('/fire')
def fire():
    return render_template('firePredict.html')

@app.route('/flood')
def flood():
    return render_template('floodPredict.html')


@app.route('/predict_image', methods=['POST'])
def predict_image():
    data = request.files['file']
    img = Image.open(data)
    img = img.resize((1024, 1024))
    
    # Create the directory if it doesn't exist
    if not os.path.exists('static'):
        os.makedirs('static')

    # Save the image to a static directory
    img.save('static/image.jpg')

    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0)

    # Make predictions using the models
    prediction_damage = damage_model.predict(img_array)[0]
    prediction_disaster = disaster_model.predict(img_array)[0]
    prediction_regional = regional_model.predict(img_array)[0]

    # Get the disaster type with the highest prediction
    disaster_type = disaster_types[prediction_disaster.argmax()]

    # Get the damage type (disaster happened or not)
    damage_type = 'Disaster happened' if prediction_damage[1] > 0.5 else 'No disaster happened'

    # Get the regional damage type with the highest prediction
    max_index_regional = prediction_regional.argmax()
    regional_damage_type = damage_levels[max_index_regional]
    # regional_damage_confidence = float(prediction_regional[max_index_regional])

    response = {
        'prediction_damage': damage_type,
        'prediction_disaster': disaster_type,
        'prediction_regional': regional_damage_type,
        'image_url': url_for('static', filename='image.jpg')
    }
    return jsonify(response)

@app.route('/predict_fire', methods=['POST'])
def predict_fire():
    data = [float(x) for x in request.form.values()]
    final_features = [np.array(data)]
    output = model.predict(final_features)[0]
    if output == 0:
        output_text = 'No Fire'
    else:
        output_text = 'Fire'
    return render_template('firePredict.html', prediction_text=output_text)

@app.route('/predict_flood', methods=['POST'])
def predict_flood():
    # Get the data from the POST request
    data = request.form

    # Make sure the data is in the correct format
    input_data = [float(data['MI']), float(data['TD']), float(data['RM']), 
                  float(data['deforest']), float(data['urban']), float(data['CC']), 
                  float(data['AP']), float(data['encroach']), float(data['DS']), 
                  float(data['CV']), float(data['landslide']), float(data['watershed']), 
                  float(data['wetland'])]

    # Make a prediction using the model
    prediction = logreg.predict([np.array(input_data)])

    # Map the prediction to the corresponding class label
    if prediction[0] == 1:
        output = "Flood"
    else:
        output = "No Flood"

    return render_template('floodPredict.html', prediction_text=output)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
