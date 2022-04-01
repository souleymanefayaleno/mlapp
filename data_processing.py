##############################################################################################
#                                    import Libraries                                        #
##############################################################################################

"""
Prerequisite:
-> install python3
-$ pip or pip3 install streamlit
-$ pip or pip3 install scikit-learn
-$ pip or pip3 install matplotlib
-$ streamlit hello
-> ctrl + c
-$ streamlit run main.py
-$ pip install streamlit-aggrid
-> from st_agrrid import AgGrid
-> import pandas as pd
"""
import joblib

import pandas as pd

import numpy as np

import streamlit as st

from sklearn.neighbors import KNeighborsClassifier

from sklearn.svm import SVC

from sklearn.ensemble import RandomForestClassifier

from st_aggrid import AgGrid

##############################################################################################
#                            Machine Learning Application Functions                          #
##############################################################################################

# Add title predefine function
st.title("Welcome To Machine Learning Models Tuning Application !")

# Select machine learning approach predefine function
approaches = ['Supervised Learning', 'Neural Network or Deep Learning', 'Reinforcement Learning']
ml_approach = st.sidebar.selectbox("Select The Machine Learning Approach", approaches)

# Select model predefine function
algorithms = ['Regressions', 'RNN', 'CNN', 'DQN']
ml_algorithm = st.sidebar.selectbox("Select Algorithm Type", algorithms)


# Load test dataset
def load_test_dataset():
    X_test = st.sidebar.file_uploader(label='Load your test features file', type='cvs, xlsx, json')
    y_test = st.sidebar.file_uploader(label='Load your test features file', type='cvs, xlsx, json')
    return X_test, y_test


X, y = load_test_dataset()
st.write("shape of dataset", X.shape)
st.write("number of classes", len(np.unique(y)))


# Load machine learning model
def load_prediction_model():
    file_name = st.sidebar.file_uploader(label='Load your model file')
    loaded_model = joblib.load(filename=file_name)
    return loaded_model


model = load_prediction_model()
st.write("Loaded model current params :", model)
st.write("Load model hyperparameters :", model.get_params())


# Machine Learning models hyperparameters tuning
def params_tuning(clf_name):
    param = dict()
    if clf_name == "KNN":
        K = st.sidebar.slider("K", 1, 15)
        param["K"] = K
    elif clf_name == "SVM":
        C = st.sidebar.slider("C", 0.01, 10.0)
        param["C"] = C
    else:
        max_depth = st.sidebar.slider("max", 2, 15)
        n_estimators = st.sidebar.slider("n_estimators", 1, 100)
        param["max_depth"] = max_depth
        param["n_estimators"] = n_estimators
    return param

gd = GridOptionsBuilder
##############################################################################################
#                        Running Machine Learning Application Functions                      #
##############################################################################################

