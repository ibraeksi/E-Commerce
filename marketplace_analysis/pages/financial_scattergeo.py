import streamlit as st
import pandas as pd
from modules.navbar import navbar
from visuals.financial_scattergeo_plots import financial_scattergeo_plots


def financial_scattergeo():
    navbar()

    st.set_page_config(
        page_title="E-Commerce Analysis",
        page_icon=":moneybag:",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    df = cached_df
    st.subheader("Analysis based on the Amount of Spending in each City")

    tab1, tab2, tab3 = st.tabs([":moneybag: Revenue", ":money_with_wings: Average Ticket", ":truck: Freight Ratio"])

    with tab1:
        left_rev, gap_rev, right_rev = st.columns([8, 0.5, 3.5], vertical_alignment="top")
        with left_rev:
            revenue_map = financial_scattergeo_plots(df, 'revenue', 'Where does the most revenue come from ?')
            st.plotly_chart(revenue_map, use_container_width=False)
        with right_rev:
            st.markdown("\n\n")
            st.markdown("\n\n")
            st.markdown("\n\n")
            st.markdown("""- As expected, most of the revenue (21% of total) comes from São Paulo
                        and Rio de Janeiro, which are the 2 largest cities in Brazil,
                        where about 16.6% of the population lives.
                        """)
            st.markdown("""- In fact, the most populous region in Brazil is the Southeast,
                        where the 3 states São Paulo, Minas Gerais and Rio de Janeiro include
                        about 40% of the population. Therefore, the majority of the orders,
                        and hence the revenue come from the Southeast, where most users are also located.""")
    with tab2:
        left_ticket, gap_ticket, right_ticket = st.columns([8, 0.5, 3.5], vertical_alignment="top")
        with left_ticket:
            ticket_map = financial_scattergeo_plots(df, 'ticket', 'What is the average amount of money a customer spends per transaction ?')
            st.plotly_chart(ticket_map, use_container_width=False)
        with right_ticket:
            st.markdown("\n\n")
            st.markdown("\n\n")
            st.markdown("\n\n")
            st.markdown("""- In contrast to the revenue, customers in the Southeast region
                        tend to have lower average ticket, i.e. lower amount of money spent per order,
                        than the customers in the Northeast region.
                        """)
            st.markdown("""- This is likely due to not having enough sellers in the Northeast,
                        which leads to higher freight costs for the customers there.
                        """)
    with tab3:
        left_freight, gap_freight, right_freight = st.columns([8, 0.5, 3.5], vertical_alignment="top")
        with left_freight:
            freight_map = financial_scattergeo_plots(df, 'freight', 'Who pays more to get their order delivered ?')
            st.plotly_chart(freight_map, use_container_width=False)
        with right_freight:
            st.markdown("\n\n")
            st.markdown("\n\n")
            st.markdown("\n\n")
            st.markdown("Freight Ratio = $$ \\frac{Freight Value}{Order Price} $$")
            st.markdown("""- For example, if a product costs 100 R\$ and the freight value
                        is 20 R\$, then the Freight Ratio is 20%.""")
            st.markdown("""- As seen, the freight ratio is higher in the sparsely populated
                        North, in some cases costing up to 4 times more than the product itself
                        due to increased logistics costs.""")
            st.markdown("""- High freight ratios can be expected to stop customers from completing
                        the purchase and therefore need to be minimized.""")


if __name__ == '__main__':
    if "data" in st.session_state:
        cached_df = st.session_state["data"]
        financial_scattergeo()
    else:
        st.switch_page('olistAnalysis.py')
