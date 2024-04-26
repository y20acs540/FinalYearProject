from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# Load the saved model
with open('cb_model.pkl', 'rb') as file:
    model = pickle.load(file)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Get the form input values
    city = int(request.form['city'])
    PM2p5 = float(request.form['textbox1'])
    PM10 = float(request.form['textbox2'])
    NO = float(request.form['textbox3'])
    NO2 = float(request.form['textbox4'])
    NOx = float(request.form['textbox5'])
    NH3 = float(request.form['textbox6'])
    CO = float(request.form['textbox7'])
    SO2 = float(request.form['textbox8'])
    O3 = float(request.form['textbox9'])
    Benzene = float(request.form['textbox10'])
    Toluene = float(request.form['textbox11'])
    Xylene = float(request.form['textbox12'])
    Temperature = float(request.form['textbox13'])
    Humidity = float(request.form['textbox14'])
    WindSpeed = float(request.form['textbox15'])
    Pressure = float(request.form['textbox16'])
    def get_AQI_bucket(x):
        if x <= 50:
            return "Good"
        elif x > 50 and x <= 100:
            return "Satisfactory"
        elif x > 100 and x <= 200:
            return "Moderate"
        elif x > 200 and x <= 300:
            return "Poor"
        elif x > 300 and x <= 400:
            return "Very Poor"
        elif x > 400:
            return "Severe"
        else:
            return '0'
    
    def suggestion(x):
        if x == 'Good':
            return 'Air Quality is good.Enjoy outdoor activities!..'
        elif x == 'Satisfactory':
            return 'Air Quality is currently satisfactory. Enjoy the fresh air and make the most of your day!..'
        elif x == 'Moderate':
            return 'Air Quality is moderate. Limit prolonged outdoor exertion.'
        elif x == 'Poor':
            return 'Air Quality is poor. Its advisable to limit outdoor activities and stay indoors as much as possible to avoid health issues related to poor air quality.'
        elif x == 'Very Poor':
            return 'Air Quality is Very Poor.Stay indoors with windows closed, use air purifiers,stay informed, and seek medical advice if symptomatic."'
        elif x == 'Severe':
            return 'Air Quality is Severe. Take Precautions such as wearing masks, reducing outdoor activities.'
        

    # Prepare input features for prediction
    input_data = np.array([[city,PM2p5, PM10, NO, NO2, NOx, NH3, CO, SO2, O3, Benzene, Toluene, Xylene, Temperature, Humidity, WindSpeed, Pressure]])

    # Make prediction
    prediction = np.exp(model.predict(input_data))-1

    rounded_prediction = round(prediction[0], 2)

    pred_qual = get_AQI_bucket(rounded_prediction)

    sug_msg = suggestion(pred_qual)

    # Render res.html template passing textbox values and prediction as arguments
    return render_template('res.html', PM2p5=PM2p5, PM10=PM10, NO=NO, NO2=NO2, NOx=NOx, NH3=NH3, CO=CO, SO2=SO2, O3=O3, Benzene=Benzene,
                           Toluene=Toluene, Xylene=Xylene, Temperature=Temperature, Humidity=Humidity, WindSpeed=WindSpeed,
                           Pressure=Pressure, rounded_prediction=rounded_prediction,pred_qual=pred_qual,sug_msg = sug_msg)


if __name__ == '__main__':
    app.run(debug=True)
