import streamlit as st
import pandas as pd
from pages.overview import overview
from pages.review_scores import review_scores
from pages.delivery_time import delivery_time
from pages.product_category import product_category
from pages.seller_locations import seller_locations
from pages.customer_locations import customer_locations


def main():
    st.session_state.update(st.session_state)

    #--- Initialize session_state
    if 'active_page' not in st.session_state:
        st.session_state.active_page = 'Overview'

    # Get current values of states
    st.session_state.active_page = st.session_state.active_page

    st.set_page_config(
        page_title="E-Commerce Analysis",
        page_icon=":moneybag:",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    #--- Run the active page
    if st.session_state.active_page == 'Overview':
        overview()
    elif st.session_state.active_page == 'Review Scores':
        review_scores()
    elif st.session_state.active_page == 'Delivery Time':
        delivery_time()
    elif st.session_state.active_page == 'Product Categories':
        product_category()
    elif st.session_state.active_page == 'Customer Locations':
        customer_locations()
    elif st.session_state.active_page == 'Seller Locations':
        seller_locations()

if __name__ == '__main__':
    main()
