from flask import Flask, request, jsonify, render_template, url_for
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image

app = Flask(__name__)

# Load the trained model
model = load_model('D:/Rubix_hackathon/Rubix/flask/models/my_model.h5')

from flask import Flask, request, jsonify, render_template, url_for
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import os

app = Flask(__name__)

# Load the trained models
damage_model = load_model('D:/Rubix_hackathon/Rubix/flask/models/disaster_model.h5')
disaster_model = load_model('D:/Rubix_hackathon/Rubix/flask/models/my_model.h5')
regional_model = load_model('D:/Rubix_hackathon/Rubix/flask/models/damage_eval_model.h5')


damage_types = np.array(sorted(['disaster happened', 'no disaster happened']))
disaster_types = np.array(sorted(['volcano', 'flooding', 'earthquake', 'fire', 'wind', 'tsunami']))
damage_levels = np.array(['no damage', 'minor damage', 'major damage', 'destroyed'])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
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
    regional_damage_confidence = float(prediction_regional[max_index_regional])

    response = {
        'prediction_damage': damage_type,
        'prediction_disaster': disaster_type,
        'prediction_regional': regional_damage_type,
        'image_url': url_for('static', filename='image.jpg')
    }
    return jsonify(response)



if __name__ == '__main__':
    app.run(debug=True)
