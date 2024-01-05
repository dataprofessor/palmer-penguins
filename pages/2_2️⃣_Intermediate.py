import streamlit as st
import pandas as pd

st.set_page_config(
    page_title='Palmer Penguins Predictor - Intermediate Mode',
    page_icon='🐧',
)

st.title('🐧 Palmer Penguins Predictor')
st.warning('Intermediate Mode')

st.subheader('Prediction Probability')
st.dataframe(prediction_proba, 
             column_config={
                '0': st.column_config.ProgressColumn(
                    'Adelie',
                    format='%f',
                    width='medium',
                    min_value=0,
                    max_value=1,
                ),
                '1': st.column_config.ProgressColumn(
                    'Chinstrap',
                    format='%f',
                    width='medium',
                    min_value=0,
                    max_value=1,
                ),
                '2': st.column_config.ProgressColumn(
                    'Gentoo',
                    format='%f',
                    width='medium',
                    min_value=0,
                    max_value=1,
                ),
             },
             hide_index=True,
          )
