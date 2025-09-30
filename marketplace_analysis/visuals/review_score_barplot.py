import plotly.express as px

def review_score_barplot(df, plot_title = ""):
    """
    Creates a distribution of review scores with comments
    df = Dataframe with orders
    x = Parameter to calculate the distribution
    x_title = Name of x axis
    y_title = Name of y axis
    plot_title = Title of plot (No title by default)
    """

    total_num_reviews = df.groupby('review_score')['review_id'].count()
    missing_reviews = df[df['review_comment'].isnull()].groupby('review_score')['review_id'].count()

    res = (100 - (missing_reviews / total_num_reviews).fillna(0)*100).reset_index().rename(columns={'review_id': 'perc'})

    fig = px.bar(res, x='review_score', y='perc')

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
        showgrid=False
    )
    fig.update_yaxes(
        title='Percentage of Reviews [%]',
        ticks='outside',
        showline=True,
        linecolor='black',
        showgrid=False,
        range=[0,100]
    )

    return fig
