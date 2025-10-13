import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
from modules.navbar import navbar
from visuals.order_count_city_map import order_count_city_map


def user_locations():
    navbar()

    st.set_page_config(
        page_title="E-Commerce Analysis",
        page_icon=":moneybag:",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    df = cached_df

    st.subheader("Analysis based on User Locations")

    tab1, tab2 = st.tabs([":eyes: Customers", ":shopping_cart: Sellers"])

    with tab1:
        st.markdown("""Customer Locations with Number of Orders""")
        st_folium(order_count_city_map(df, type='customer'), width=725, returned_objects=[])
    with tab2:
        st.markdown("""Seller Locations with Number of Orders""")
        st_folium(order_count_city_map(df, type='seller'), width=725, returned_objects=[])


if __name__ == '__main__':
    if "data" in st.session_state:
        cached_df = st.session_state["data"]
        user_locations()
    else:
        st.switch_page('olistAnalysis.py')
