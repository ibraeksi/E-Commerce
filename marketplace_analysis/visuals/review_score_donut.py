import plotly.graph_objects as go

def review_score_donut(df, x, plot_title = "", legend_title="Score"):
    """
    Creates a donut chart from given data
    df = Dataframe with orders
    x = Parameter to calculate the distribution
    plot_title = Title of plot (No title by default)
    legend_title = Title of legend ('Score' by default)
    """
    score_counts = df[x].value_counts().reset_index().sort_values(x).reset_index(drop=True)
    donut_colors = ['maroon', 'tomato', 'lightgrey', 'yellowgreen', 'forestgreen']
    fig = go.Figure(data=[go.Pie(labels=score_counts[x], values=score_counts['count'],
                                direction ='clockwise', hole=.4, marker_colors=donut_colors, sort=False)])
    fig.update_layout(
        plot_bgcolor="rgba(0, 0, 0, 0)",
        margin=dict(t=25, b=0, l=0, r=0),
        height=200, width=250,
        title_text=plot_title, title_x=0.5,
        legend_title_text=legend_title
    )

    return fig
