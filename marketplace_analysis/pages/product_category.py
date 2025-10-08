import streamlit as st
import pandas as pd
from modules.navbar import navbar
from visuals.ols_product_review_score_barplot import ols_product_review_score_barplot
from visuals.order_num_items_visuals import order_num_items_donut
from visuals.order_num_items_visuals import order_grouped_num_items_donut
from visuals.order_num_items_visuals import num_item_violinplot
from visuals.best_worst_performer_barplot import best10_performer_plot
from visuals.best_worst_performer_barplot import worst10_performer_plot


def product_category():
    navbar()

    st.set_page_config(
        page_title="E-Commerce Analysis",
        page_icon=":moneybag:",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    product_df = cached_df
    product_df['delivery_time'] = (product_df['order_delivered_customer'] - product_df['order_purchase']).dt.days
    product_df['delay_vs_expected'] = (product_df['order_delivered_customer'] - product_df['order_estimated_delivery']).dt.days
    product_df['product_volume_cm3'] = product_df['product_length_cm']*product_df['product_height_cm']*product_df['product_width_cm']

    st.subheader("Product Performance by Category")

    tab1, tab2 = st.tabs([":chart_with_upwards_trend: Analysis", ":keycap_ten: Best & Worst"])

    with tab1:
        order_sales = product_df[['product_id', 'price']].groupby('product_id').sum().rename(columns={'price': 'sales'})
        order_num_orders = product_df.groupby('product_id')['order_id'].nunique().reset_index().rename(columns={'order_id': 'num_orders'})
        order_num_items = product_df.groupby('order_id',as_index=False).agg({'order_item_id': 'count'}).rename(columns={'order_item_id':'num_items'})

        df = product_df.merge(order_num_orders, on='product_id').merge(order_num_items, on='order_id').merge(order_sales, on='product_id')

        left_ols, gap_ols, right_ols = st.columns([6, 0.5, 5.5], vertical_alignment="top")
        with left_ols:
            ols_product_review_plot = ols_product_review_score_barplot(df, 'Effects of Different Features on Review Score')
            st.plotly_chart(ols_product_review_plot)
            st.markdown("""- Product features such as price, number of photos and dimensions
                        do not influence the review score much.""")
            st.markdown("""- Delay and delivery time has a negative impact on review score
                        as analyzed in the previous step.""")
        with right_ols:
            df_std = df.copy()
            selected_features = ['delivery_time', 'delay_vs_expected', 'price', 'product_photos_qty', 'product_volume_cm3', 'num_items']

            for f in selected_features:
                mu = df[f].mean()
                sigma = df[f].std()
                df_std[f] = df[f].map(lambda x: (x - mu) / sigma)
            df_std[selected_features].head()

            ### The following calculation leads to slow execution for the deployed app
            # model = smf.ols(formula=f"review_score ~ {'+ '.join(selected_features)}", data=df_std).fit()
            # st.dataframe(return_significative_coef(model))

            st.markdown("\n\n")
            st.markdown("\n\n")
            st.dataframe(pd.DataFrame({'feature': ['product_photos_qty', 'price', 'product_volume_cm3',
                                                   'num_items', 'delay_vs_expected', 'delivery_time'],
                                       'p-value': [0.0000, 0.0001, 0.0205, 0.0000, 0.0000, 0.0000],
                                       'coeff': [0.02, 0.02, -0.01, -0.12, -0.14, -0.38]}))

            st.markdown("""- The p-values for the selected continuous features confirm
                        that the relationship with review scores are statistically significant.""")

        st.markdown("\n\n")
        st.markdown("**:blue-background[Impact of Number of Items]**")
        st.markdown("""- Number of items within an order has a negative impact on review
                            score as well suggesting increased complexity in logistics leading
                            to delayed orders.""")

        left_items, gap_items, right_items = st.columns([5.75, 0.5, 5.75], vertical_alignment="top")
        df['num_item_cat'] = df['num_items'].apply(lambda x: 3 if x>=3 else (2 if x>1 else 1))
        with left_items:
            st.markdown("""- Most orders are single item orders and only 10% of orders include
                        more than 2 items.""")
            all_num_items_donut = order_num_items_donut(df)
            st.plotly_chart(all_num_items_donut)
        with right_items:
            st.markdown("""- Therefore, the orders can be grouped into 3 categories for comparison:
                        single item, 2 items and 3+ items.""")
            grouped_num_items_donut = order_grouped_num_items_donut(df)
            st.plotly_chart(grouped_num_items_donut)

        st.markdown("""- The review score decreases for orders with more than 2 items, but the
                    delivery time stays the same. So the negative reviews might be related to the
                    product itself rather than the increased complexity in logistics. As the number
                    of items in an order increases, the expectation of the customer increases as well.""")
        left_violin, gap_violin, right_violin = st.columns([5.75, 0.5, 5.75], vertical_alignment="top")
        with left_violin:
            review_score_num_item_plot = num_item_violinplot(df, 'review_score', 'Review Score', [0,5.5], 'Score Distribution by Number of Items')
            st.plotly_chart(review_score_num_item_plot)
        with right_violin:
            delivery_time_num_item_plot = num_item_violinplot(df, 'delivery_time', 'Delivery Time [days]', [0,50], 'Delivery Duration by Number of Items')
            st.plotly_chart(delivery_time_num_item_plot)

    with tab2:
        delivered = product_df[product_df['order_status'] == 'delivered'].copy()
        delivered['category_translation'] = delivered['category_translation'].str.replace('fashion_childrens_clothes','fashion_children_clothing')
        delivered['category_translation'] = delivered['category_translation'].str.replace('auto','automotive')

        st.markdown(":blue-background[Sales Concentration]")
        st.markdown("""- There is a large discrepancy between the best-selling and least-selling
                    products, as everyday items from categories like bed_bath_table, beauty-health
                    and sports_leisure sell the most.""")
        best_sales = delivered['category_translation'].value_counts().nlargest(10).reset_index()
        worst_sales = delivered['category_translation'].value_counts().nsmallest(10).reset_index()

        left_sales, gap_sales, right_sales = st.columns([7, 1, 4], vertical_alignment="top")
        with left_sales:
            top10_sales = best10_performer_plot(best_sales, x_axis_title='Number of Orders', plot_title='Top 10 Best-Selling Categories')
            st.plotly_chart(top10_sales)
        with right_sales:
            bot10_sales = worst10_performer_plot(worst_sales, x_axis_title='Number of Orders', plot_title='Top 10 Least-Selling Categories')
            st.plotly_chart(bot10_sales)

        st.markdown(":blue-background[Customer Satisfaction]")
        st.markdown("""- Both extremes in terms of average review score are due to the
                    very low number of reviews as seen in the plots above and therefore
                    can be disregarded. Books across different categories seem to be getting high scores
                    and some common products such as office furnitures are reviewed poorly.""")
        best_rating = delivered.groupby('category_translation')['review_score'].mean().round(3).nlargest(10).reset_index()
        worst_rating = delivered.groupby('category_translation')['review_score'].mean().round(3).nsmallest(10).reset_index()

        left_score, gap_score, right_score = st.columns([5.5, 1, 5.5], vertical_alignment="top")
        with left_score:
            top10_score = best10_performer_plot(best_rating, x_axis_title='Average Review Score', x_range=[0,5.5], plot_title='Top 10 by Average Rating')
            st.plotly_chart(top10_score)
        with right_score:
            bot10_score = worst10_performer_plot(worst_rating, x_axis_title='Average Review Score', x_range=[0,5.5], plot_title='Bottom 10 by Average Rating')
            st.plotly_chart(bot10_score)

        st.markdown(":blue-background[Delivery Time]")
        st.markdown("""- The reason behind the low scores for office furnitures
                    might be delivery time as it takes nearly 3 weeks for a customer to
                    receive their order.""")
        best_delivery = delivered.groupby('category_translation')['delivery_time'].mean().round().astype('int64').nlargest(10).reset_index()
        worst_delivery = delivered.groupby('category_translation')['delivery_time'].mean().round().astype('int64').nsmallest(10).reset_index()

        left_delivery, gap_delivery, right_delivery = st.columns([5.5, 1, 5.5], vertical_alignment="top")
        with left_delivery:
            top10_delivery = best10_performer_plot(best_delivery, x_axis_title='Average Delivery Time [days]', x_range=[0,20.5], plot_title='Top 10 Slowest Delivery')
            st.plotly_chart(top10_delivery)
        with right_delivery:
            bot10_delivery = worst10_performer_plot(worst_delivery, x_axis_title='Average Delivery Time [days]', x_range=[0,20.5], plot_title='Top 10 Fastest Delivery')
            st.plotly_chart(bot10_delivery)

        st.markdown(":blue-background[Spending Behavior]")
        st.markdown("""- Computers and small home appliances seem to be the luxury items
                    in the marketplace as most product payment values are between 50 and 200 BRL.""")
        best_payment = delivered.groupby('category_translation')['payment_value'].median().round().astype('int64').nlargest(10).reset_index()
        worst_payment = delivered.groupby('category_translation')['payment_value'].median().round().astype('int64').nsmallest(10).reset_index()

        left_payment, gap_payment, right_payment = st.columns([5.5, 1, 5.5], vertical_alignment="top")
        with left_payment:
            top10_payment = best10_performer_plot(best_payment, x_axis_title='Median Payment Value [BRL]', x_range=[0,1250], plot_title='Top 10 Most Expensive')
            st.plotly_chart(top10_payment)
        with right_payment:
            bot10_payment = worst10_performer_plot(worst_payment, x_axis_title='Median Payment Value [BRL]', x_range=[0,1250], plot_title='Top 10 Least Expensive')
            st.plotly_chart(bot10_payment)

        st.markdown("""- It would be beneficial for the company to eliminate product categories
                    that are slow to deliver, receive poor reviews and have a low volume. The focus
                    needs to be on scaling fast-moving essential products that receive good reviews.""")

if __name__ == '__main__':
    if "data" in st.session_state:
        cached_df = st.session_state["data"]
        product_category()
    else:
        st.switch_page('olistAnalysis.py')
