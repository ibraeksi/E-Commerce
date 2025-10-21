import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
from modules.navbar import navbar
from modules.calculate_seller_revenue import seller_revenue
from visuals.order_count_city_map import order_count_city_map
from visuals.num_sellers_profit_lineplot import num_sellers_profit_lineplot
from visuals.removed_seller_scattergeo_plot import removed_seller_scattergeo_plot


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

    tab1, tab2, tab3 = st.tabs([":eyes: Customers", ":shopping_cart: Sellers", ":thinking: What If ?"])

    with tab1:
        st.markdown("""Customer Locations with Number of Orders""")
        st_folium(order_count_city_map(df, type='customer'), width=725, returned_objects=[])
    with tab2:
        st.markdown("""Seller Locations with Number of Orders""")
        st_folium(order_count_city_map(df, type='seller'), width=725, returned_objects=[])
    with tab3:
        st.markdown("""**:green-background[How to increase profitability ?]**""")
        left_time, gap_time, right_time = st.columns([5.5, 1, 5.5], vertical_alignment="top")
        with left_time:
            st.markdown("""**1) Improve Revenues**""")
            st.markdown("""There is only indirect influence on the sale of products,
                        as the only parameter that can be changed is the number of sellers on the marketplace.""")
            st.markdown("""**Assumptions:**""")
            st.markdown("""- ***Sales fees:*** Olist takes a 10% cut on
                        the product price (excl. freight) of each order delivered. (variable)""")
            st.markdown("""- ***Subscription fees:*** Olist charges 80 BRL per month per seller. (fixed)""")
        with right_time:
            st.markdown("""**2) Optimize Costs**""")
            st.markdown("""**Assumptions:**""")
            st.markdown("""- ***Estimated reputation costs:*** The monetary cost for negative reviews:""")
            st.markdown(""":red[1 star = 100], :orange[2 stars = 50], :orange[3 stars = 40],
                         :green[4 stars = 0], :green[5 stars = 0]""")
            st.markdown("""- ***IT costs:*** Total cumulated costs can be represented as:""")
            st.latex(r'''3157.27 * \sqrt{n\_sellers} + 978.23 * \sqrt{n\_items}''')
        st.markdown("\n\n")
        st.markdown("""- Bad customer experience has business implications: low repeat rate,
                    immediate customer support cost, refunds or unfavorable word of mouth communication.""")
        st.markdown("""- Both the number of sellers to manage and the number of sales transaction are costly
                    for IT systems. The formula suggests that Olist has lower IT costs with few sellers
                    selling a lot of items rather than the opposite.""")
        st.markdown("""- A better selection of sellers can reduce delays and the number of negative reviews.
                    The sellers that are not contributing to the profit can be identified as underperforming sellers.""")
        st.markdown("\n\n")
        st.markdown("**:green-background[How many underperforming sellers should Olist remove from its marketplace?]**")

        left_plot, gap_plot, right_plot = st.columns([8.25, 0.25, 3.5], vertical_alignment="top")
        with left_plot:
            unique_seller_df, plot_df = seller_revenue(df)
            num_sellers_plot = num_sellers_profit_lineplot(plot_df, 'Impact of Number of Sellers on Profit and IT Costs')
            st.plotly_chart(num_sellers_plot)
        with right_plot:
            st.markdown("\n\n")
            st.markdown("\n\n")
            st.markdown("""- In order to maximize revenue and market share, only the sellers
                        that haven't made any profit can be removed, i.e. the maximum total profit.""")
            st.markdown("""- That would result in removing 609 sellers from the marketplace, which would
                        mean an opportunity cost of 48720 BRL or only about 1.7% of the total profits.""")

        left_sc, gap_sc, right_sc = st.columns([6.5, 0.5, 5], vertical_alignment="top")
        with left_sc:
            removed_sellers_plot = removed_seller_scattergeo_plot(unique_seller_df, 'Locations of the Underperforming Sellers')
            st.plotly_chart(removed_sellers_plot, use_container_width=False)
        with right_sc:
            st.markdown("\n\n")
            st.markdown("\n\n")
            st.markdown("\n\n")
            st.markdown("\n\n")
            st.markdown("\n\n")
            st.markdown("\n\n")
            st.markdown("""- Removing the underperforming sellers would not have an impact on the
                        network of sellers since they are not concentrated in one region.""")
            st.markdown("""- Therefore it would not be expected to result in any major
                        changes to the logistics costs.""")


if __name__ == '__main__':
    if "data" in st.session_state:
        cached_df = st.session_state["data"]
        user_locations()
    else:
        st.switch_page('olistAnalysis.py')
