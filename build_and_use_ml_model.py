###############################################################################################
#                                import of script libraries                                   #
###############################################################################################

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


###############################################################################################
#                                definition of script functions                               #
###############################################################################################

def import_data():
    file_type = 'none'
    """file import based on file type"""
    if file_type == 'cvs':
        dataset = pd.read_csv('file_path/file.csv')
    elif file_type == 'excel':
        dataset = pd.read_excel('file_path/file.xlsx')
    elif file_type == 'json':
        dataset = pd.read_json('file_path/file.json')
    else:
        print("=" * 100)
        print(" " * 23 + "Let's us use one of the Seaborn predefine dataset !")
        print("=" * 100)
        print("Seaborn datasets array :", sns.get_dataset_names())
        dataset = sns.load_dataset('titanic')
    return dataset


# Using import data function
df = import_data()


def dataset_manipulation_f1(data):
    print("-" * 100 + "\nDisplaying dataset head :")
    print(data.head())
    print("-" * 100 + "\nDisplaying dataset number of rows and columns :")
    print(data.shape)
    print("-" * 100 + "\nDisplaying dataset information :")
    print(data.info())
    print("-" * 100 + "\nDelete dataset redundant columns :")
    print("....")
    data = data.drop(['alive', 'who', 'embarked', 'class', 'deck'], axis=1)
    print("done!")
    print("-" * 100 + "\nDisplaying the new dataset head")
    print(data.head())
    print("-" * 100 + "\nVisualize 'survived' target variable using bar diagram :")
    print(sns.countplot(x='survived', data=data))
    print("-" * 100 + "\nVisualize 'sibsp' variable using bar diagram :")
    print(sns.countplot(x='sibsp', data=data))
    return data


def dataset_manipulation_f2(data):
    print("-" * 100 + "\nVisualize 'fare' variable using  mustache diagram :")
    print(sns.boxplot(x='fare', data=data))
    print("-" * 100 + "\nVisualize 'age' variable using  mustache diagram :")
    print(sns.boxplot(x='age', data=data))
    print("-" * 100 + "\nVisualize of the correlations between target variable and rest of the variables :")
    corr = df.corr(method='spearman')
    corr.sort_values(["survived"], ascending=False, inplace=True)
    print(corr.survived)
    print("-" * 100 + "\nDescribe the dataset statistics :")
    print(data.describe)


# Using dataset manipulation function
dataset_manipulation_f1(df)

###############################################################################################
#                                script execution                                             #
###############################################################################################

# if __name__ == "__main__":
# df = import_data()
