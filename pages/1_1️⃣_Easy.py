# Import libraries
import streamlit as st
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# Set page configuration
st.set_page_config(
    page_title='Palmer Penguins Predictor - Easy Mode',
    page_icon='🐧',
)

# Display title
st.title('🐧 Palmer Penguins Predictor')
st.success('Easy Mode')

# User provide input features
st.subheader('Input features')
with st.container(border=True):
    island = st.selectbox('Island',('Biscoe','Dream','Torgersen'))
    gender = st.selectbox('Gender',('male','female'))
    bill_length_mm = st.slider('Bill length (mm)', 32.1,59.6,43.9)
    bill_depth_mm = st.slider('Bill depth (mm)', 13.1,21.5,17.2)
    flipper_length_mm = st.slider('Flipper length (mm)', 172.0,231.0,201.0)
    body_mass_g = st.slider('Body mass (g)', 2700.0,6300.0,4207.0)

# Create a DataFrame from user input
data = {'island': island,
        'bill_length_mm': bill_length_mm,
        'bill_depth_mm': bill_depth_mm,
        'flipper_length_mm': flipper_length_mm,
        'body_mass_g': body_mass_g,
        'gender': gender}
input_df = pd.DataFrame(data, index=[0])

# Load data
penguins_raw = pd.read_csv('https://raw.githubusercontent.com/dataprofessor/palmer-penguins/master/data/penguins_cleaned.csv')

# Pre-process data
## Combine user input features with entire penguins dataset; useful for encoding phase
penguins = penguins_raw.drop('species', axis=1)
input_penguins = pd.concat([input_df, penguins],axis=0)

## Encode ordinal features
encode = ['island','gender']
df_penguins = pd.get_dummies(input_penguins, prefix=encode)
input_row = df_penguins[:1] # Selects only the first row (the user input data)

## Prepare dataframe
target_mapper = {'Adelie':0, 'Chinstrap':1, 'Gentoo':2}
def target_encode(val):
    return target_mapper[val]

## Separate X and y
X = df_penguins[1:]
y = penguins_raw['species'].apply(target_encode)

# Model training and inference
## Train ML model
clf = RandomForestClassifier()
clf.fit(X, y)

## Apply model to make predictions
prediction = clf.predict(input_row)
prediction_proba = clf.predict_proba(input_row)

## Display predicted species
st.subheader('Predicted Species')
penguins_species = np.array(['Adelie','Chinstrap','Gentoo'])
st.success(str(penguins_species[prediction][0]))
