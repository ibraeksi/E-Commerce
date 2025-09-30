import streamlit as st
import pandas as pd
from modules.navbar import navbar
from pathlib import Path

delivery_time_prediction_image = Path(__file__).parents[1] / 'data/images/delivery_time_prediction.png'
OLS_regression_image = Path(__file__).parents[1] / 'data/images/OLS_regression_delivery_time.png'

from visuals.delivery_days_violinplot import delivery_days_violinplot
from visuals.review_score_corr import review_score_corr
from visuals.delivery_time_stage import delivery_time_stage
from visuals.delay_dist_score import delay_dist_score
from visuals.delay_dist_score import delivery_status
from visuals.delay_dist_score import delay_donut

def delivery_time():
    navbar()

    st.set_page_config(
        page_title="Olist Analysis",
        page_icon=":moneybag:",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    df = cached_df
    st.subheader("Delivery Time Analysis")

    tab1, tab2, tab3 = st.tabs([":chart_with_upwards_trend: Analysis", ":clock3: Delivery Delays", ":bell: Estimated Delivery"])

    with tab1:
        st.markdown("""- Delivery time has a significant impact on customer satisfaction
                        as the review score increases with decreasing median delivery time.""")
        st.markdown("""- As seen, delays in delivery time are also negatively correlated
                        with customer review scores.""")

        left_violin, gap_violin, right_violin = st.columns([5, 0.5, 6.5], vertical_alignment="top")
        with left_violin:
            delivery_violin = delivery_days_violinplot(df, 'Delivery Duration by Review Score')
            st.plotly_chart(delivery_violin)
        with right_violin:
            corr_plot = review_score_corr(df, 'Correlation between Numerical Features')
            st.plotly_chart(corr_plot)

    with tab2:
        df['delivery_days'] = (df['order_delivered_customer'] - df['order_purchase']).dt.days
        df['delivery_delay'] = (df['order_delivered_customer'] - df['order_estimated_delivery']).dt.days
        df["Status"] = df.apply(delivery_status, axis=1)

        left_delay, gap_delay, right_delay = st.columns([7, 0.25, 4.75], vertical_alignment="top")
        with left_delay:
            delay_dist_plot = delay_dist_score(df, 'Score Distribution by Delivery Status')
            st.plotly_chart(delay_dist_plot)
        with right_delay:
            st.markdown("\n\n")
            st.markdown("\n\n")
            st.markdown("\n\n")
            delay_donut_plot = delay_donut(df)
            st.plotly_chart(delay_donut_plot, use_container_width=False)

            st.markdown("""- For orders with 1-star rating, 27% was delivered later than
                        the estimated delivery time, which is only 1.8% for orders
                        with 5-star rating.""")
            st.markdown("""- About 90% of orders are delivered early which suggests
                        that the estimated delivery time may be too conservative and
                        there may be room for improvement.""")


    with tab3:
        # Calculate delivery durations
        df['approval_time'] = df['order_approved'] - df['order_purchase']
        df['waiting_time'] = df['order_delivered_carrier'] - df['order_approved']
        df['shipping_time'] = df['order_delivered_customer'] - df['order_delivered_carrier']
        df['total_time'] = df['order_delivered_customer'] - df['order_purchase']
        df['estimated_time'] = df['order_estimated_delivery'] - df['order_purchase']

        # Filter for orders with realistic durations
        df = df[df['waiting_time'] >= pd.Timedelta(0)]
        df = df[df['shipping_time'] >= pd.Timedelta(0)]

        left_time, gap_time, right_time = st.columns([5.5, 0.5, 5], vertical_alignment="top")
        with left_time:
            delivery_stage_plot = delivery_time_stage(df, 'Median Delivery Time per Stage')
            st.plotly_chart(delivery_stage_plot)
        with right_time:
            st.markdown("\n\n")
            st.markdown("\n\n")
            st.markdown(":blue-background[Key Takeaways]")
            st.markdown("""Approval Time = Median is only 20 mins, which reflects the efficiency
                        of the frontend as most orders are instantly approved.""")
            st.markdown("""Waiting Time (From approval to handoff to logistics)
                        = Median is 1.9 days with a high standard deviation of 85 hours, which
                        shows inconsistency in seller responsiveness.""")
            st.markdown("""Shipping Time = Median is about 7.1 days with a large variance and
                        thus contributes the most to delays and user dissatisfaction.""")
            st.markdown("""Total Time (From approval to delivery) = Median is about 10.3 days
                        which is reasonable considering Brazil's size, but there is room for
                        improvement compared to global standards.""")

        st.markdown("**:blue-background[Improving Estimated Delivery Time]**")
        st.markdown("""Estimated Time of Arrival (ETA) is a key component of modern e-commerce
                    services. It allows companies to manage customer expectations by showing a
                    predicted date for customer delivery.""")
        st.markdown("""- The median value for Olist's estimated delivery time is 23.3 days
                    which is more than double the actual delivery time. The forecasting is so
                    conservative that majority of orders end up arriving early. This can affect
                    conversion rates especially among first-time or time-sensitive customers.""")
        st.markdown("""- Using an OLS multivariate model with numerical features related to the order
                    such as number of items, price and freight value can already provide better
                    predictions as a starting point.""")

        left_pre, gap_pre, right_pre = st.columns([6, 1, 5], vertical_alignment="top")
        with left_pre:
            st.image(delivery_time_prediction_image)
            st.markdown("\n\n")
            st.markdown("""- As seen, the resulting predictions with the linear OLS
                        regression model are much closer to the actual delivery time.""")
            st.markdown("""- The p-value for the selected variables confirms that the
                        relationship between these features and delivery time are
                        statistically significant.""")
        with right_pre:
            st.image(OLS_regression_image)


if __name__ == '__main__':
    if "data" in st.session_state:
        cached_df = st.session_state["data"]
        delivery_time()
    else:
        st.switch_page('olistAnalysis.py')
