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

"""

import pandas as pd

import numpy as np

import matplotlib.pyplot as plt

import streamlit as st

import seaborn as sns

from sklearn import datasets

from sklearn.neighbors import KNeighborsClassifier

from sklearn.svm import SVC

from sklearn.ensemble import RandomForestClassifier

from sklearn.model_selection import train_test_split

from sklearn.metrics import accuracy_score

from sklearn.decomposition import PCA

##############################################################################################
#                            Machine Learning Application Functions                          #
##############################################################################################

# Add title predefine function
st.title("Prediction Application With Machine Learning Approaches")

# Write text predefine function
st.write("""
# Explore different classifier
Which one is the best?
""")

# Select dataset predefine function
dataset_name = st.sidebar.selectbox("Select Dataset",
                                    ("Iris", "Breast Cancer", "Wine dataset", "Dataset_1", "Dataset_2",
                                     "Dataset_3", "Dataset_3", "Dataset_4", "Dataset_5"))

# Write the selected dataset name under the selection box
# st.write(dataset_name)

# Select machine learning approach predefine function
machine_learning_approach = st.sidebar.selectbox("Select Machine Learning Approach", ("Supervised Learning",
                                                                                      "Semi-supervised Learning",
                                                                                      "Unsupervised Learning",
                                                                                      "Ensemble Learning",
                                                                                      "Neural Network or Deep Learning",
                                                                                      "Reinforcement Learning"))

# Select model predefine function
observation_type = st.sidebar.selectbox("Select Observation Type", ("Classification", "Regression", "Clustering",
                                                                    "Associate Rule Learning",
                                                                    "Dimensionality Reduction",
                                                                    "CNN", "RNN", "GAN", "Autoencoders", "Perceptron",
                                                                    "Boosting", "Bagging", "Stacking"))

# Select model predefine function
model_name = st.sidebar.selectbox("Select Model", ("KNN", "SVM", "Random Forest", "Model_5", "Model_6",
                                                   "Model_7", "Model_8", "Model_9", "Model_10"))


def get_dataset(dataset_name):
    if dataset_name == "Iris":
        data = datasets.load_iris()
    elif dataset_name == "Breast Cancer":
        data = datasets.load_breast_cancer()
    else:
        data = datasets.load_wine()
    X = data.data
    y = data.target
    return X, y


X, y = get_dataset(dataset_name)
st.write("shape of dataset", X.shape)
st.write("number of classes", len(np.unique(y)))


def add_parameter_ui(clf_name):
    params = dict()
    if clf_name == "KNN":
        K = st.sidebar.slider("K", 1, 15)
        params["K"] = K
    elif clf_name == "SVM":
        C = st.sidebar.slider("C", 0.01, 10.0)
        params["C"] = C
    else:
        max_depth = st.sidebar.slider("max", 2, 15)
        n_estimators = st.sidebar.slider("n_estimators", 1, 100)
        params["max_depth"] = max_depth
        params["n_estimators"] = n_estimators
    return params


params = add_parameter_ui(model_name)


def get_classifier(clf_name, params):
    if clf_name == "KNN":
        clf = KNeighborsClassifier(n_neighbors=params["K"])
    elif clf_name == "SVM":
        clf = SVC(C=params["C"])
    else:
        clf = RandomForestClassifier(n_estimators=params["n_estimators"],
                                     max_depth=params["max_depth"],
                                     random_state=1234)
    return clf


clf = get_classifier(model_name, params)


def get_external_dataset():
    df = pd.read_csv('')
    return df


def upload_files():
    menu = ["Home", "Dataset", "DocumentFiles", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home")
        image_file = st.file_uploader("Upload Images", type=["png", "jpg", "jpeg"])
        if image_file is not None:
            st.write(type(image_file))
            file_details = {"filename": image_file.name, "filetype": image_file.type, "filesize": image_file.size}

    elif choice == "Dataset":
        st.subheader("Dataset")
    elif choice == "DocumentFiles":
        st.subheader("DocumentFiles")
    else:
        st.subheader("About")


upload_files()

##############################################################################################
#                        Running Machine Learning Application Functions                      #
##############################################################################################

# display content in two column
col1, col2 = st.columns(2)

# importation of .csv files
# dataset = pd.read_csv('survey_results_public.csv')

# display the seaborn dataset list
sns.get_dataset_names()

# importation of titanic dataset
df = sns.load_dataset('titanic')

# display the dataset columns
# df.columns

# display the dataset head
# df.head()

# display the whole dataset
st.write(df)

# delete the repeated columns (NB: axis = 0 for lines, axis = 1 for les columns)
df = df.drop(['alive', 'who', 'embarked', 'class', 'deck'], axis=1)
df.head()

# display dataset information
df.info()


# Univariate analysis (in this type of analysis each variable is visualized alone)
# visualization of the 'survived' variable with a bar
fig = plt.figure(figsize=(10, 5))
sns.countplot(x="survived", data=df)
col1.pyplot(fig)

# visualization of survived variable imbalance
df['survived'].value_counts(normalize=True)

# display the contingency table between 'sex' and 'adult_male' variables
pd.crosstab(df['sex'], df['adult_male'])

# visualization of the 'survived' variable with a bar
fig = plt.figure(figsize=(10, 5))
sns.countplot(x="embark_town", data=df)
col2.pyplot(fig)





