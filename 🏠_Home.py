import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(
    page_title='Palmer Penguins Predictor',
    page_icon='🐧',
)

st.title('🐧 Palmer Penguins Predictor')
st.info('This tool allows one to predict the species of Palmer penguins as a function of their input features. It is built in 3 levels of difficulty!')

st.write('👇 Choose one:')

col = st.columns(3)
with col[0]:
    btn_easy = st.button('Easy')
    if btn_easy:
        switch_page('Easy')
with col[1]:
    btn_intermediate = st.button('Intermediate')
    if btn_intermediate:
        switch_page('Intermediate')
with col[2]:
    btn_advanced = st.button('Advanced')
    if btn_advanced:
        switch_page('Advanced')
