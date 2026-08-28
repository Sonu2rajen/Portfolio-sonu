from flask import Flask, render_template, request #render template function will use this template folder#
import joblib
import os
import numpy as np
import pickle

app= Flask(__name__) #that's how you initialize an app#

@app.route("/") #to create the homepage
def index():
    return render_template("home.html")

@app.route("/result",methods=['POST','GET']) #post means when the user post anything and GET means when user wants to get any data#
def result():
    gender=int(request.form['gender'])
    age=int(request.form['age'])
    hypertension=int(request.form['hypertension'])
    heart_disease = int(request.form['heart_disease'])
    ever_married = int(request.form['ever_married'])
    work_type = int(request.form['work_type'])
    Residence_type = int(request.form['Residence_type'])
    avg_glucose_level = float(request.form['avg_glucose_level'])
    bmi = float(request.form['bmi'])
    smoking_status = int(request.form['smoking_status'])

    x=np.array([gender,age,hypertension,heart_disease,ever_married,work_type,Residence_type,
                avg_glucose_level,bmi,smoking_status]).reshape(1,-1) ##to scale down the data and reshape the array into 2d array or it will through an error#

    scaler_path=os.path.join('C:/Users/Sneha/Documents/A/MSC 5th sem project/heart-stroke-prediction/heart-stroke-classifier/heart-stroke-classifier/Stroke-Risk-Prediction-using-Machine-Learning','models/scaler.pkl')
    scaler=None
    with open(scaler_path,'rb') as scaler_file: #rb means read binary
        scaler=pickle.load(scaler_file)

    x=scaler.transform(x) #transformed our values

    model_path=os.path.join('C:/Users/Sneha/Documents/A/MSC 5th sem project/heart-stroke-prediction/heart-stroke-classifier/heart-stroke-classifier/Stroke-Risk-Prediction-using-Machine-Learning','models/rf.sav')
    rf=joblib.load(model_path)

    Y_pred=rf.predict(x) #it will store the data in y_pred#

    # for No Stroke Risk
    if Y_pred==0:
        return render_template('nostroke.html')
    else:
        return render_template('stroke.html')

if __name__=="__main__":
    app.run(debug=True,port=5000) #debu=true means if any error occurs let us know#