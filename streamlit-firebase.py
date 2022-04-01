
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
-$ pip or pip3 install pyrebase

"""

import pyrebase

import streamlit as st


# Configuration Key
firebaseConfig = {
  'apiKey': "AIzaSyCAjiyD-mO2DC4YVdaPu-go7Wt4wt70A_Q",
  'authDomain': "streamilt-database.firebaseapp.com",
  'projectId': "streamilt-database",
  'databaseURL': "https://streamilt-database-default-rtdb.europe-west1.firebasedatabase.app/",
  'storageBucket': "streamilt-database.appspot.com",
  'messagingSenderId': "687983585640",
  'appId': "1:687983585640:web:2b6fea5e15920dc13d4edd",
  'measurementId': "G-BX01DP9VR6"
}

# Firebase Authentication
fire = pyrebase.intialize_app(firebaseConfig)
auth = firebase.auth()

# Database
db = firebase.database()
storage = firebase.storage()

st.sidebar.title("Our community app")

# Authentication
choice = st.sidebar.selectbox('Login/Signup', ['Login', 'Sing Up'])

email = st.sidebar.text_input('Please enter your email address')
password = st.sidebar.text_input('Please enter password')

if choice == 'Sign Up':
  handle = st.sidebar.text_input('Please input your app handle name', value = 'Default')
  submit = st.sidebar.button('Create my account')

  if submit:
    user = auth.create_user_with_email_and_password(email, password)
    st.success('your account is created successfully')
