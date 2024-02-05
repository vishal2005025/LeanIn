from plyer import notification
import time
import joblib  # Assuming you used joblib for model persistence

# Load your pre-trained model
model = joblib.load('D:/Rubix_hackathon/Rubix/flask/models/flood_prediction.pkl')

# List of lists with static data for attributes
static_data = [
    [1.3, 57, 18, 30, 65.7, 3.4, 25, 1.3, 3.4, 0.5, 0.5, 0.5, 0.5],
    [1.5, 60, 20, 35, 70.5, 3.6, 28, 1.4, 3.8, 0.6, 0.6, 0.6, 0.6],
    # Add more lists as needed
]

def predict_flood(attributes):
    # Assuming your model takes a list of features for prediction
    prediction = model.predict([attributes])[0]
    return prediction

def display_notification(prediction):
    title = 'Flood Prediction'
    if prediction == 'Flood':
        message = 'Danger detected! Flood is predicted.'
    else:
        message = 'No danger detected. No flood predicted.'

    # Display notification
    notification.notify(
        title=title,
        message=message,
        app_icon=None,  # e.g., 'C:\\icon_32x32.ico'
        timeout=10,  # seconds
    )

def periodically_predict():
    for attributes in static_data:
        prediction = predict_flood(attributes)
        print(f'Prediction for attributes {attributes}: {prediction}')
        display_notification(prediction)
        time.sleep(10)  # Sleep for 1 hour (3600 seconds) before the next prediction

if __name__ == '__main__':
    periodically_predict()