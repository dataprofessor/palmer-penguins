import streamlit as st
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import altair as alt
import matplotlib.pyplot as plt
from itertools import product

st.set_page_config(
    page_title='Palmer Penguins Predictor - Advanced Mode',
    page_icon='🐧',
)

st.title('🐧 Palmer Penguins Predictor')
st.error('Advanced Mode')

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

st.write('DataFrame of Input features:')
st.dataframe(input_df, hide_index=True)

# Model settings

with st.sidebar:
    st.header('⚙️ Model Settings')
    parameter_n_estimators = st.slider('Number of estimators (n_estimators)', 0, 1000, 200, 100)
    parameter_max_features = st.slider('Max features (max_features)', 1, 5, 5, 1)

# Data pre-processing

## Combines user input features with entire penguins dataset
## This will be useful for the encoding phase
penguins_raw = pd.read_csv('https://raw.githubusercontent.com/dataprofessor/palmer-penguins/master/data/penguins_cleaned.csv')
penguins = penguins_raw.drop('species', axis=1)
input_penguins = pd.concat([input_df, penguins],axis=0)

## Encoding ordinal features
encode = ['island','gender']
df_penguins = pd.get_dummies(input_penguins, prefix=encode)

input_row = df_penguins[:1] # Selects only the first row (the user input data)

## Preparing the dataframe
target_mapper = {'Adelie':0, 'Chinstrap':1, 'Gentoo':2}
def target_encode(val):
    return target_mapper[val]

## Separating X and y
X = df_penguins[1:]
y = penguins_raw['species'].apply(target_encode)

# Train ML model
clf = RandomForestClassifier(n_estimators=parameter_n_estimators,
                             max_features=parameter_max_features,)
clf.fit(X, y)

# Apply model to make predictions
prediction = clf.predict(input_row)
prediction_proba = clf.predict_proba(input_row)
df_prediction = pd.DataFrame(prediction_proba, columns=['Adelie','Chinstrap','Gentoo'])

st.subheader('Prediction')

st.write('Predicted Species:')
penguins_species = np.array(['Adelie','Chinstrap','Gentoo'])
st.success(str(penguins_species[prediction][0]))

st.write('Prediction Probability:')

st.dataframe(df_prediction,
            column_config={
                'Adelie': st.column_config.ProgressColumn(
                    'Adelie',
                    format='%f',
                    width='medium',
                    min_value=0,
                    max_value=1,
                ),
                'Chinstrap': st.column_config.ProgressColumn(
                    'Chinstrap',
                    format='%f',
                    width='medium',
                    min_value=0,
                    max_value=1,
                ),
                'Gentoo': st.column_config.ProgressColumn(
                    'Gentoo',
                    format='%f',
                    width='medium',
                    min_value=0,
                    max_value=1,
                ),
             },
             hide_index=True,
          )

st.subheader('Download')
df_output = pd.concat([input_df, df_prediction, pd.Series(penguins_species[prediction], name='prediction')], axis=1)
st.dataframe(df_output, hide_index=True)
st.download_button(
    label="Download results as CSV",
    data=df_output.to_csv().encode('utf-8'),
    file_name='prediction.csv',
    mime='text/csv',
)


st.subheader('Model details')

# Display feature importance plot
st.write('Feature importance:')
importances = clf.feature_importances_
feature_names = list(X.columns)
forest_importances = pd.Series(importances, index=feature_names)
df_importance = forest_importances.reset_index().rename(columns={'index': 'feature', 0: 'value'})
    
bars = alt.Chart(df_importance).mark_bar(size=40).encode(
             x='value:Q',
             y=alt.Y('feature:N', sort='-x')
           ).properties(height=500)

st.altair_chart(bars, theme='streamlit', use_container_width=True)

# Display confusion matrix plot
st.write('Confusion matrix:')
predictions = clf.predict(X)
cm = confusion_matrix(y, predictions, labels=clf.classes_)

labels = np.unique(y)
cm = [y for i in cm for y in i]
roll = list(product(np.unique(y), repeat = 2))
columns = ["actual", "predicted", "confusion_matrix"]

data_list = [{'actual': roll[i][0], 'predicted': roll[i][1], 'confusion_matrix': cm[i]} for i in range(len(roll))]
df_cm = pd.DataFrame(data_list, columns=columns)

species = ['Adelie','Chinstrap','Gentoo']
cm_plot = alt.Chart(df_cm).mark_rect().encode(
                x=alt.X("predicted:N", axis=alt.Axis(values=species, title='Predicted Species')) ),
                y="actual:N",
                color='confusion_matrix'
            ).properties(
                width=600,
                height=480
            ).add_selection(
                alt.selection_interval(encodings=['x'], empty='none')
            )
st.altair_chart(cm_plot)
