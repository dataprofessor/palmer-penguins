import streamlit as st
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(
    page_title='Palmer Penguins Predictor - Easy Mode',
    page_icon='🐧',
)

st.title('🐧 Palmer Penguins Predictor')
st.success('Easy Mode')

# User input features
st.subheader('Input features')
with st.container(border=True):
    island = st.selectbox('Island',('Biscoe','Dream','Torgersen'))
    gender = st.selectbox('Gender',('male','female'))
    bill_length_mm = st.slider('Bill length (mm)', 32.1,59.6,43.9)
    bill_depth_mm = st.slider('Bill depth (mm)', 13.1,21.5,17.2)
    flipper_length_mm = st.slider('Flipper length (mm)', 172.0,231.0,201.0)
    body_mass_g = st.slider('Body mass (g)', 2700.0,6300.0,4207.0)

data = {'island': island,
        'bill_length_mm': bill_length_mm,
        'bill_depth_mm': bill_depth_mm,
        'flipper_length_mm': flipper_length_mm,
        'body_mass_g': body_mass_g,
        'gender': gender}
input_df = pd.DataFrame(data, index=[0])

# Combines user input features with entire penguins dataset
# This will be useful for the encoding phase
penguins_raw = pd.read_csv('https://raw.githubusercontent.com/dataprofessor/data/master/penguins_cleaned.csv')
penguins = penguins_raw.drop('species', axis=1)
input_penguins = pd.concat([input_df,penguins],axis=0)

# Encoding ordinal features
encode = ['gender','island']
for col in encode:
    dummy = pd.get_dummies(input_penguins[col], prefix=col)
    df_penguins = pd.concat([input_penguins,dummy], axis=1)
    del df_penguins[col]
input_row = df_penguins[:1] # Selects only the first row (the user input data)

# ML model building
## Preparing the dataframe
target_mapper = {'Adelie':0, 'Chinstrap':1, 'Gentoo':2}
def target_encode(val):
    return target_mapper[val]
df = penguins_raw.copy()
df['species'] = df['species'].apply(target_encode)

## Separating X and y
X = df_penguins.drop('species', axis=1)
y = df_penguins['species']

st.write(X)

# Train ML model
# clf = RandomForestClassifier()
# clf.fit(X, y)

# Apply model to make predictions
# prediction = clf.predict(input_row)
# prediction_proba = clf.predict_proba(input_row)

#st.subheader('Prediction')
#penguins_species = np.array(['Adelie','Chinstrap','Gentoo'])
#st.write(penguins_species[prediction])

#st.subheader('Prediction Probability')
#st.write(prediction_proba)
