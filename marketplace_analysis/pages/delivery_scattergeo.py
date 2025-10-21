import streamlit as st
import pandas as pd
from modules.navbar import navbar
from visuals.delivery_scattergeo_plots import delivery_scattergeo_plots


def delivery_scattergeo():
    navbar()

    st.set_page_config(
        page_title="E-Commerce Analysis",
        page_icon=":moneybag:",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    df = cached_df
    st.subheader("Impact of Location on Delivery Time")

    tab1, tab2, tab3 = st.tabs([":hourglass: Shipping Time", ":clock3: Delayed Orders", ":star: Review Score"])

    with tab1:
        # Remove missing carrier delivery times (1251 orders)
        df_carrier = df[~df['order_delivered_carrier'].isnull()].reset_index(drop=True)
        df_carrier['shipping_hours'] = (df_carrier['order_delivered_customer'] - df_carrier['order_delivered_carrier']).dt.total_seconds()/3600
        # Remove outliers time<0 and time>30 days (3323 orders)
        df_carrier = df_carrier[(df_carrier['shipping_hours'] > 0) & (df_carrier['shipping_hours'] <= 720)].reset_index(drop=True)
        df_carrier['shipping_days'] = df_carrier['shipping_hours']/24

        left_rev, gap_rev, right_rev = st.columns([8, 0.5, 3.5], vertical_alignment="top")
        with left_rev:
            shipping_map = delivery_scattergeo_plots(df_carrier, 'shipping', 'Average Order Shipping Time')
            st.plotly_chart(shipping_map, use_container_width=False)
        with right_rev:
            st.markdown("\n\n")
            st.markdown("\n\n")
            st.markdown("\n\n")
            st.markdown("""- In addition to paying more to get their orders delivered,
                        the customers in the Northeast have to wait longer for the delivery as well.
                        """)

    with tab2:
        df['delay_hours'] = (df['order_delivered_customer'] - df['order_estimated_delivery']).dt.total_seconds()/3600
        # Filter for only delayed orders
        delay_df = df[(df['delay_hours'] > 0) & (df['delay_hours'] <= 720)].reset_index(drop=True)
        delay_df['delay_days'] = delay_df['delay_hours']/24

        left_del, gap_del, right_del = st.columns([8, 0.5, 3.5], vertical_alignment="top")
        with left_del:
            delay_map = delivery_scattergeo_plots(delay_df, 'delays', 'Delayed Orders')
            st.plotly_chart(delay_map, use_container_width=False)
        with right_del:
            st.markdown("\n\n")
            st.markdown("\n\n")
            st.markdown("\n\n")
            st.markdown("""- Despite the long shipping times, the delayed orders are limited to
                        about 7.5% of all orders due to the conservative forecasting.
                        """)
            st.markdown("""- Forecasting seems to be taking the delivery distance into account
                        as well since the delayed orders are more distributed across Brazil.
                        """)

    with tab3:
        # upon first load, set the st.feedback value to a pre-defined
        if "min_score" not in st.session_state:
            st.session_state.min_score = 0
        if "max_score" not in st.session_state:
            st.session_state.max_score = 1

        left_sc, gap_sc, right_sc = st.columns([8, 0.5, 3.5], vertical_alignment="top")
        with right_sc:
            st.markdown("\n\n")
            st.markdown("\n\n")

            st.markdown("Select Min. Review Score")
            min_filter = st.feedback("stars", key="min_score")
            st.markdown("Select Max. Review Score")
            max_filter = st.feedback("stars", key="max_score")

            st.markdown("\n\n")
            st.markdown("""- Similar to the delayed orders, the negative reviews are not
                        observed more in a specific region than others.
                        """)
        with left_sc:
            if min_filter is None:
                min_filter = 0
            if max_filter is None:
                max_filter = 2
            score_df = df[(df['review_score']>=min_filter+1)&(df['review_score']<=max_filter+1)].reset_index(drop=True)
            score_map = delivery_scattergeo_plots(score_df, 'review', 'Average Review Score')
            st.plotly_chart(score_map, use_container_width=False)



if __name__ == '__main__':
    if "data" in st.session_state:
        cached_df = st.session_state["data"]
        delivery_scattergeo()
    else:
        st.switch_page('olistAnalysis.py')
