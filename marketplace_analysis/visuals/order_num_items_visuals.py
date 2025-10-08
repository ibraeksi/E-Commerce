import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

def order_num_items_donut(df, plot_title = ""):
    """
    Creates a donut chart showing number of orders per number of items
    df = Dataframe with number of items per order
    plot_title = Title of plot (None by default)
    """
    order_counts = df['num_items'].value_counts().reset_index().sort_values('num_items').reset_index(drop=True)
    donut_colors = ['#636EFA', '#EF553B', '#00CC96']

    fig = go.Figure(data=[go.Pie(labels=order_counts['num_items'], values=order_counts['count'],
                                direction ='clockwise', hole=.4, marker_colors=donut_colors, sort=False)])
    fig.update_layout(
        plot_bgcolor="rgba(0, 0, 0, 0)",
        margin=dict(t=25, b=0, l=0, r=0),
        height=200, width=200, legend_title='Num. Items',
        uniformtext_minsize=12, uniformtext_mode='hide'
    )
    fig.update_traces(textposition='inside')

    return fig


def order_grouped_num_items_donut(df, plot_title = ""):
    """
    Creates a donut chart showing number of orders per groups of number of items
    df = Dataframe with number of items per order
    plot_title = Title of plot (None by default)
    """
    order_counts = df['num_item_cat'].value_counts().reset_index().sort_values('num_item_cat').reset_index(drop=True)
    order_counts = order_counts.replace(3, '3+')
    donut_colors = ['#636EFA', '#EF553B', '#00CC96']

    fig = go.Figure(data=[go.Pie(labels=order_counts['num_item_cat'], values=order_counts['count'],
                                direction ='clockwise', hole=.4, marker_colors=donut_colors, sort=False)])
    fig.update_layout(
        plot_bgcolor="rgba(0, 0, 0, 0)",
        margin=dict(t=25, b=0, l=0, r=0),
        height=200, width=200,
        showlegend=True, legend_title='Num. Items',
    )

    return fig


def num_item_violinplot(df, feature, feature_title, feature_range, plot_title = ""):
    """
    Creates a distribution of selected feature with respect to number of items
    df = Dataframe with number of items
    feature = Name of feature to be used for distribution
    feature_title = Name of feature for y axis title
    feature_range = Range of values for y axis
    plot_title = Title of plot (No title by default)
    """
    melted_df = df.melt(id_vars='num_item_cat')
    delivery_df = melted_df[melted_df['variable'] == feature].reset_index(drop=True)
    delivery_df['value'] = delivery_df['value'].astype('float64')
    median_df = delivery_df.groupby(['num_item_cat'])['value'].median().to_frame('median').reset_index(drop=True)

    fig = px.violin(df, y=feature, x="num_item_cat", box=False, points=False)

    fig.update_layout(
        plot_bgcolor="rgba(0, 0, 0, 0)",
        # width=800, height=400,
        title_text=plot_title, title_x=0.2
    )
    fig.update_xaxes(
        title='Number of Items',
        ticks='outside',
        showline=True,
        linecolor='black',
        showgrid=False,
        categoryorder='array', categoryarray= [1, 2, 3]
    )
    fig.update_yaxes(
        title=feature_title,
        ticks='outside',
        showline=True,
        linecolor='black',
        showgrid=False,
        range=feature_range
    )

    for i in range(len(median_df)):
        fig.add_annotation(
            dict(x=i+1,
                y=median_df.loc[i,'median'],
                text="Median: "+str(int(median_df.loc[i,'median'])),
                font=dict(color='red'),
                showarrow=False,
                xshift=40))

    return fig
