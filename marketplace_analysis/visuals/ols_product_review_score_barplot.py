import plotly.express as px
import pandas as pd

def ols_product_review_score_barplot(df, plot_title = ""):
    """
    Creates a distribution of review scores with comments
    df = Dataframe with orders
    plot_title = Title of plot (No title by default)
    """
    ols_coeff_dict = {'delivery_time':-0.378510, 'num_items':-0.118329,
                      'delay_vs_expected':-0.136321, 'product_volume_cm3':-0.009264,
                      'price':0.015781, 'product_photos_qty':0.018586}

    coeff_df = pd.DataFrame.from_dict(ols_coeff_dict, orient='index').reset_index().rename(columns={0:'value'})

    fig = px.bar(coeff_df, x="value", y="index", orientation='h')

    fig.update_layout(
        plot_bgcolor="rgba(0, 0, 0, 0)",
        height=300,
        title_text=plot_title, title_x=0.2
    )
    fig.update_xaxes(
        title='OLS Regression Coefficient',
        ticks='outside',
        showline=True,
        linecolor='black',
        showgrid=False
    )
    fig.update_yaxes(
        title='Feature',
        ticks='outside',
        showline=True,
        linecolor='black',
        showgrid=False,
    )

    return fig
