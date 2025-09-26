import streamlit as st

def navbar():
    with st.sidebar:
        st.header('Navigation')
        st.page_link('olistAnalysis.py', label='Overview')
        st.subheader('Exploratory Data Analysis')
        st.page_link('pages/review_scores.py', label='Review Scores')
        st.page_link('pages/delivery_time.py', label='Delivery Time')
