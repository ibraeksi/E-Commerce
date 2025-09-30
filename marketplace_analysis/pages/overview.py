import streamlit as st
import pandas as pd
from modules.navbar import navbar
from pathlib import Path

order_data = Path(__file__).parents[1] / 'data/processed/processed_orders.csv'
schema_image = Path(__file__).parents[1] / 'data/images/data_schema.png'

def overview():
    navbar()

    st.set_page_config(
        page_title="E-Commerce Analysis",
        page_icon=":moneybag:",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.header("E-Commerce Analysis Using Olist Data")

    st.markdown("""In this project, I will be using the publicly available Olist
                dataset in order to conduct a detailed analysis with the goal of
                identifying ways to improve customer satisfaction while maintaining
                a healthy volume of orders.""")

    st.markdown("""The dataset can be found on Kaggle:
                https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce""")

    st.subheader("About the Dataset")

    st.markdown("""Olist is a Brazilian e-commerce marketplace that connects small
                businesses to customers. They provided the public
                with a dataset containing real information about more than 100k
                orders made on the platform between 2016 and 2018. The data consists
                of multiple datasets which are connected as depicted in the
                following schema:""")

    st.image(schema_image, caption="Olist Data Schema")

    st.markdown("""The individual datasets are merged and cleaned to have a
                 single orders table with all the necessary information required
                 for the analysis. The preprocessing steps can be found in the
                 notebook in the GitHub repository for this project:""")
    st.markdown("""https://github.com/ibraeksi/E-Commerce/tree/main/marketplace_analysis""")

    st.markdown("""The resulting table consists of 118,233 orders and 44 columns.
                There are no duplicates and the only missing values left in the table are: """)
    st.markdown("""- order_delivered_carrier_date = 1251 missing values for when the order
                was handed to the logistic partner mostly due to canceled or ongoing orders,
                will be kept in the dataset as is.""")
    st.markdown("""- review_id, review_score = 978 missing values, meaning 978 orders with no reviews,
                i.e, the customers did not provide any rating, which is to be expected
                in real-world data and therefore will be kept as is.""")
    st.markdown("""- review_comment_message = 68593 orders with missing review comments,
                i.e, the customers did not provide any comment with their rating,
                which is to be expected in real-world data.""")
    st.markdown("""- review_comment_title = 104346 orders with missing review titles,
                i.e, the customers did not provide any title with their rating,
                which is to be expected in real-world data.""")

    date_cols = ['order_purchase', 'order_approved', 'order_delivered_carrier', 'order_delivered_customer',
             'order_estimated_delivery', 'shipping_limit_date', 'review_create', 'review_answer']
    df = pd.read_csv(order_data, parse_dates=date_cols)
    st.session_state["data"] = df

#if __name__ == '__main__':
#    overview()
