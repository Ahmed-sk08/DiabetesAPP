import os
from flask import Flask,jsonify, request, render_template
from flask_cors import CORS
import urllib.request
from io import BytesIO
import requests
import io
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app, resources = {r'/*':{'origins': '*'}})


@app.route('/', methods=['GET'])
def load():
    return render_template('index.html')
    # return render_template('index.html', user=user)
    # {{ user }} --> html

@app.route('/get-result', methods=['GET'])
def get_result():
    pregnancies =  request.args.get("pregnancies")
    glucose =  request.args.get("glucose")
    blood =  request.args.get("blood")
    skin =  request.args.get("skin")
    insulin =  request.args.get("insulin")
    bmi =  request.args.get("bmi")
    pedigree =  request.args.get("pedigree")
    age =  request.args.get("age")

    def shekale(data):
        path = "diabetes.csv"
        diabetes = pd.read_csv(path)

        X = diabetes.drop('Outcome', axis =1)
        X = X.values
        y = diabetes['Outcome']
        y = y.values
        X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2)
        tree = DecisionTreeClassifier(max_depth=3)
        tree.fit(X_train, y_train)

        X_form = [data] # will be replaced by data from the website
        y_form_yes = [1]
        y_form_no = [0]
        yes = tree.score(X_form, y_form_yes)
        no = tree.score(X_form, y_form_no)
        if no > yes:
            return "unlikely"
        else:
            return "likely"
    data_received = [pregnancies, glucose, blood, skin, insulin, bmi, pedigree, age]
    outcome = shekale(data_received) # e.g. [6, 148, 72, 35, 0, 33.6, 0.627, 50]
    return render_template('outcome.html', outcome=outcome)

if __name__ == '__main__':
    app.run()