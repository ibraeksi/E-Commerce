import plotly.express as px
import numpy as np

def review_score_corr(df, plot_title = ""):
    """
    Creates a distribution of review scores with comments
    df = Dataframe with orders
    plot_title = Title of plot (None by default)
    """

    df['delivery_time'] = (df['order_delivered_customer'] - df['order_purchase']).dt.days
    df['delay_vs_expected'] = (df['order_delivered_customer'] - df['order_estimated_delivery']).dt.days

    df_corr = df[['product_weight_grams',
        'product_length_cm', 'product_height_cm', 'product_width_cm',
        'payment_installments', 'payment_value',
        'review_score', 'delivery_time', 'delay_vs_expected']].corr(numeric_only=True).round(2)

    mask = np.zeros_like(df_corr, dtype=bool)
    mask[np.triu_indices_from(mask)] = True

    df_corr_viz = df_corr.mask(mask).dropna(how='all').dropna(axis='columns', how='all')
    fig = px.imshow(df_corr_viz, text_auto=True, range_color=[-1,1], color_continuous_scale="rdbu")

    fig.update_layout(
        plot_bgcolor="rgba(0, 0, 0, 0)",
        title_text=plot_title, title_x=0.2
    )
    fig.update_xaxes(
        ticks='outside',
        showline=False,
        linecolor='black',
        showgrid=False,
    )
    fig.update_yaxes(
        ticks='outside',
        showline=False,
        linecolor='black',
        showgrid=False
    )

    return fig
