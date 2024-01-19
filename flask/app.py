import pickle
from flask import Flask,request,app,jsonify,url_for,render_template
import numpy as np
import pandas as pd

app=Flask(__name__)
model=pickle.load(open('D:/Rubix_hackathon/Rubix/flask/models/fire_prediction_model.pkl','rb'))
@app.route('/')
def home():
    #return 'Hello World'
    return render_template('home.html')

@app.route('/predict_api',methods=['POST'])
def predict_api():

    data=request.json['data']
    print(data)
    new_data=[list(data.values())]
    output=model.predict(new_data)[0]
    if output == 0:
        output_text = 'No Fire'
    else:
        output_text = 'Fire'
    return jsonify(output_text)

@app.route('/predict',methods=['POST'])
def predict():

    data=[float(x) for x in request.form.values()]
    final_features = [np.array(data)]
    print(data)
    
    output=model.predict(final_features)[0]
    print(output)
    if output == 0:
        output_text = 'No Fire'
    else:
        output_text = 'Fire'
    #output = round(prediction[0], 2)
    return render_template('home.html', prediction_text="Output is  {}".format(output_text))



if __name__=="__main__":
    app.run(debug=True)

