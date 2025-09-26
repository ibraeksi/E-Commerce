import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

def delivery_status(row):
    if pd.isna(row["delivery_delay"]):
        return "missing"
    if row["delivery_delay"] < 0:
        return "Early"
    elif row["delivery_delay"] > 0:
        return "Late"
    else:
        return "On Time"

def delay_dist_score(df, plot_title = ""):
    """
    Creates a distribution of review scores with comments
    df = Dataframe with orders
    plot_title = Title of plot (No title by default)
    """
    df['delivery_days'] = (df['order_delivered_customer'] - df['order_purchase']).dt.days
    df['delivery_delay'] = (df['order_delivered_customer'] - df['order_estimated_delivery']).dt.days

    df["Status"] = df.apply(delivery_status, axis=1)

    stacked_data = df.groupby(['review_score', 'Status']).size().unstack().fillna(0)
    stacked_data = stacked_data.div(stacked_data.sum(axis=1), axis=0) * 100
    stacked_data_df = stacked_data.reset_index().melt(id_vars=["review_score"])
    stacked_data_df['Status'] = pd.Categorical(stacked_data_df['Status'], categories=['Early', 'On Time', 'Late'], ordered=True)
    stacked_data_df = stacked_data_df.sort_values('Status').reset_index(drop=True)

    fig = px.bar(stacked_data_df, x='review_score', y='value', color='Status',
             color_discrete_sequence = ['green', 'yellow', 'red'])
    fig.update_layout(
        plot_bgcolor="rgba(0, 0, 0, 0)",
        bargap=0.2,
        title_text=plot_title, title_x=0.2
    )
    fig.update_xaxes(
        title='Review Score',
        ticks='outside',
        showline=True,
        linecolor='black',
        showgrid=False,
    )
    fig.update_yaxes(
        title='Percentage of Reviews [%]',
        ticks='outside',
        showline=True,
        linecolor='black',
        showgrid=False,
    )

    return fig

def delay_donut(df, x='Status'):
    """
    Creates a donut chart from given data
    df = Dataframe with orders
    x = Parameter to calculate the distribution
    plot_title = Title of plot (No title by default)
    legend_title = Title of legend ('Score' by default)
    """
    score_counts = df[x].value_counts().reset_index().sort_values(x).reset_index(drop=True)
    donut_colors = ['green', 'yellow', 'red']
    fig = go.Figure(data=[go.Pie(labels=score_counts[x], values=score_counts['count'],
                                direction ='clockwise', hole=.4, marker_colors=donut_colors, sort=False)])
    fig.update_layout(
        plot_bgcolor="rgba(0, 0, 0, 0)",
        margin=dict(t=25, b=0, l=0, r=0),
        height=150, width=150,
        showlegend=False
    )

    return fig
