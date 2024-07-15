import streamlit as st

st.set_page_config(
    page_title='Palmer Penguins Predictor',
    page_icon='🐧',
)

st.title('🐧 Palmer Penguins Predictor')

with st.expander('About this app'):
  st.markdown('**What can this app do?**')
  st.info('This tool allow users to predict the species of Palmer penguins as a function of their input features. It is built in 3 levels of difficulty that developers can use as inspiration for building their own!')

  st.markdown('**How to use the app?**')
  st.markdown('''1. Select a difficulty level either from the sidebar or click on buttons under this About expander.
2. From the selected page, adjust widgets for the Input features that will trigger a prediction output of the Penguin species.
3. As a result, this would initiate the ML model building process, display the model results as well as allow users to download the generated models and accompanying data.
''')

  st.markdown('**Under the hood**')
  st.markdown('Data sets:')
  st.markdown('- Palmer Penguins data set')
  
  st.markdown('Libraries used:')
  st.markdown('''- Pandas for data wrangling
- Scikit-learn for building a machine learning model
- Altair for chart creation
- Streamlit for user interface
- Streamlit-extras for its switch_page functionality
  ''')

st.write('👇 Choose a difficulty level:')

col = st.columns(3)
with col[0]:
    btn_easy = st.button('Easy')
    if btn_easy:
        st.page_link('pages/1_1️⃣_Easy.py')
with col[1]:
    btn_intermediate = st.button('Intermediate')
    if btn_intermediate:
        st.page_link('pages/2_2️⃣_Intermediate.py')
with col[2]:
    btn_advanced = st.button('Advanced')
    if btn_advanced:
        st.page_link('pages/3_3️⃣_Advanced.py')
