from flask import Flask, request
import numpy as np
import joblib

app = Flask(__name__)

# Load the model from the file
logreg = joblib.load('D:/Rubix_hackathon/Rubix/flask/models/flood_prediction.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    # Get the data from the POST request
    data = request.get_json(force=True)

    # Make sure the data is in the correct format
    input_data = [data['MonsoonIntensity'], data['TopographyDrainage'], data['RiverManagement'], 
                  data['Deforestation'], data['Urbanization'], data['ClimateChange'], 
                  data['AgriculturalPractices'], data['Encroachments'], data['DrainageSystems'], 
                  data['CoastalVulnerability'], data['Landslides'], data['Watersheds'], 
                  data['WetlandLoss']]

    # Make a prediction using the model
    prediction = logreg.predict([np.array(input_data)])

    # Map the prediction to the corresponding class label
    if prediction[0] == 1:
        output = "Flood"
    else:
        output = "No Flood"

    return output

if __name__ == '__main__':
    app.run(port=5000, debug=True)
