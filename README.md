To recreate this machine learning app, on your computer,
do the following steps:

Create a conda environment
Firstly, you need to create a conda environment called
mlapp 

$ conda create -n mlapp python=3.7.9

Secondly, we will login to the mlapp environment

$ conda activate mlapp

Install prerequisite libraries

Download requirements.txt file

$ wget https://raw.githubusercontent.com/dataprofessor/ml-auto-app/main/requirements.txt

$ pip install -r requirements.txt

Download and unzip mlapp repo

Launch the app

$ streamlit run app.py