import plotly.express as px

def delivery_days_violinplot(df, plot_title = ""):
    """
    Creates a distribution of review scores with comments
    df = Dataframe with orders
    plot_title = Title of plot (No title by default)
    """
    df['delivery_days'] = (df['order_delivered_customer'] - df['order_purchase']).dt.days
    df['delivery_delay'] = (df['order_delivered_customer'] - df['order_estimated_delivery']).dt.days

    melted_df = df.melt(id_vars='review_score')
    delivery_df = melted_df[melted_df['variable'] == 'delivery_days'].reset_index(drop=True)
    delivery_df['value'] = delivery_df['value'].astype('float64')
    median_df = delivery_df.groupby(['review_score'])['value'].median().to_frame('median')

    fig = px.violin(df, y="delivery_days", x="review_score", box=True, points=False)

    fig.update_layout(
        plot_bgcolor="rgba(0, 0, 0, 0)",
        # width=800, height=400,
        title_text=plot_title, title_x=0.2
    )
    fig.update_xaxes(
        title='Review Score',
        ticks='outside',
        tickvals=[1,2,3,4,5],
        showline=True,
        linecolor='black',
        showgrid=False,
    )
    fig.update_yaxes(
        title='Delivery Time [days]',
        ticks='outside',
        showline=True,
        linecolor='black',
        showgrid=False,
        range=[0,50]
    )

    for (score, value) in median_df.itertuples(name=None):
        fig.add_annotation(
            dict(x=score,
                y=value,
                text="Median: "+str(int(value)),
                font=dict(color='red'),
                showarrow=False,
                xshift=40))

    return fig
