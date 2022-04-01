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

import streamlit as st

import matplotlib.pyplot as plt

from PIL import Image

from st_aggrid import AgGrid

from st_aggrid import GridOptionsBuilder

import sqlite3 as sql

conn = sql.connect('data.db')
curs = conn.cursor()


###############################################################################################
#                                definition of script functions                               #
###############################################################################################
def create_usertable():
    curs.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT, password TEXT)')


def add_userdata(username, password):
    curs.execute('INSERT INTO userstable(username, password) VALUES (?,?)', (username, password))
    conn.commit()


def login_user(username, password):
    curs.execute('SELECT * FROM userstable WHERE username = ? AND password = ?', (username, password))
    data = curs.fetchall()
    return data


def view_all_users():
    curs.execute('SELECT * FROM userstable')
    data = curs.fetchall()
    return data


def regression_model():
    return 0


def rnn_cnn_model():
    return 0


def dqn_reinforcement_model():
    return 0


# us columns to display elements
col1, col2 = st.columns(2)


def connection_option():
    menu = ["Home", "Login", "SignUp"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.markdown(
            "<h1 style='text-align: center; color: #494a63;'>Machine Learning Models Hyperparameters Tracking Application</h1>",
            unsafe_allow_html=True)
        img = Image.open(
            "/Users/souleymanefayaleno/Desktop/mlapp/images/mlapp0.png")
        st.image(img, width=700, caption="")
        st.markdown(
            "<h3 style='text-align: center; color: #494a63;'>Learn how to tune hyperparameters to make models work as expected</h3>",
            unsafe_allow_html=True)

    elif choice == "Login":
        st.markdown(
            "<h3 style='text-align: center; color: #494a63;'>Login to start prediction and hyperparameters tuning</h3>",
            unsafe_allow_html=True)
        img = Image.open(
            "/Users/souleymanefayaleno/Desktop/mlapp/images/mlapp1.jpg")
        st.image(img, width=700, caption="")

        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type='password')
        if st.sidebar.checkbox("Login"):
            # if username == "admin" and password == "admin":
            create_usertable()
            result = login_user(username, password)
            if result:
                success = st.success("Logged in as {}".format(username))
                if success:
                    button = st.checkbox('Get Started')
                    if button:
                        st.markdown(
                            "<h1 style='text-align: center; color: #5072A7;'>Track and tune a machine learning model hyperparameters!</h1>",
                            unsafe_allow_html=True)

                        st.write('**1. Model Configuration :**')

                        # Select machine learning approach predefine function
                        approaches = ['Supervised Learning', 'Neural Network or Deep Learning',
                                      'Reinforcement Learning']
                        ml_approach = st.selectbox("select the machine learning approach", approaches)

                        # Select model predefine function
                        algorithms = ['Regressions', 'RNN', 'CNN', 'DQN']
                        ml_algorithm = st.selectbox("select the machine learning algorithm", algorithms)

                        # Upload machine learning model file
                        file_name = st.file_uploader(label='upload your machine learning model file')

                        st.write('**2. Dataset Configuration :**')
                        # Upload test dataset (features and targets)
                        X_test = st.file_uploader(label='upload your test features file')
                        y_test = st.file_uploader(label='upload your test targets file')

                        # Load machine learning model file
                        if file_name:
                            st.write('**3. Model Tracking :**')
                            st.info('The model current hyperparameters')
                            loaded_model = joblib.load(filename=file_name)
                            st.write(loaded_model)
                            st.info('The whole model hyperparameters')
                            st.write(loaded_model.get_params())

                        # Features information
                        if X_test:
                            st.write('**4. Dataset Tracking :**')
                            st.write('X_test (rows, columns)')
                            features = pd.read_csv(X_test)
                            st.info(features.shape)

                            gd = GridOptionsBuilder.from_dataframe(features)
                            gd.configure_pagination(enabled=True)
                            gd.configure_default_column(editable=True, groupable=True)

                            sel_mode = st.radio('select type', options=['single', 'multiple'])
                            gd.configure_selection(selection_mode=sel_mode, use_checkbox=True)
                            gridoptions = gd.build()
                            grid_table1 = AgGrid(features, gridOptions=gridoptions)

                        # Targets information
                        if y_test:
                            st.write('y_test (rows, columns)')
                            targets = pd.read_csv(y_test)
                            st.info(targets.shape)

                            gd = GridOptionsBuilder.from_dataframe(targets)
                            gd.configure_pagination(enabled=True)
                            gd.configure_default_column(editable=True, groupable=True)

                            gd.configure_selection(selection_mode=sel_mode, use_checkbox=True)
                            gridoptions = gd.build()
                            grid_table2 = AgGrid(targets, gridOptions=gridoptions)

            else:
                st.warning("Username or Password Incorrect!")

    elif choice == "SignUp":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')

        if st.button('Signup'):
            create_usertable()
            add_userdata(new_user, new_password)
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to login!")


# -----------------------------------------------------------------------------------------------------------
# col1, col2 = st.columns(2)

# st.write(password)
# st.code(copy)
# st.info("Results")
# st.download_button('Download', str(results))

# img = Image.open(
# "C:/Users/soule/OneDrive/Bureau/Thesis_files/Dev_And_ML/stack-overflow-developer-survey-2021/mlapp2.jpg")
# col2.image(img, width=300, caption="Simple Image!")
# -----------------------------------------------------------------------------------------------------------
# task = st.selectbox("Task", ["Add Post", "Analytics", "Profiles"])
# if task == "Add Post":
#     st.subheader("Add Your Post")
# elif task == "Analytics":
#     st.subheader("Analytics")
# elif task == "Profiles":
#     st.subheader("User Profiles")
#     user_result = view_all_users()
#     clean_db = pd.DataFrame(user_result, columns=["Username", "Password"])
#     st.dataframe(clean_db)

# ----------------------------------------------------------------------------------------------------------
# st.multiselect("",['col1', 'col2', 'col3', 'col4', '...', 'coln'])
# st.write('You selected:', options)

# st.slider('slide me', min_value=0, max_value=10)
# age = st.slider('How old are you', 0, 110, 25)
# st.write('I'm', age, 'years old')
# values = st.slider('Select a range of values', 0.0, 100.0, (25.0, 75.0))
# st.write('values:', values)
# import time
# with st.spinner('wait for it ...'):
#   time.sleep(1.8)
# st.success('Done!')

# st.write('Progress bar widget')

# my_bar = st.progress(0)
# for p in range(100):
#   time.sleep(0.1)
#   my_bar.progress(p+1)

# ----------------------------------------------------------------------------------------------------------


hide_menu = """
<style>
#MainMenu {
     visibility:hidden;
}

footer {
     visibility:hidden;
}
</style>
"""

show_menu = """
#MainMenu {
     visibility:visible;
}
"""

###############################################################################################
#                                script execution                                             #
###############################################################################################


if __name__ == "__main__":
    connection_option()
