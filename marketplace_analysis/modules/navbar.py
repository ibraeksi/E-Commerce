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
        st.page_link('pages/customer_locations.py', label='Customer Locations')
        st.page_link('pages/seller_locations.py', label='Seller Locations')
