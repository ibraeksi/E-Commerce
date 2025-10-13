import streamlit as st

def navbar():
    with st.sidebar:
        st.header('Navigation')
        st.page_link('olistAnalysis.py', label='Overview')
        st.subheader('Exploratory Data Analysis')
        st.page_link('pages/review_scores.py', label='Review Scores')
        st.page_link('pages/delivery_time.py', label='Delivery Time')
        st.page_link('pages/product_category.py', label='Product Categories')
        st.subheader('Geospatial Analysis')
        st.page_link('pages/user_locations.py', label='User Locations')
        st.page_link('pages/financial_scattergeo.py', label='Spending Distribution')
