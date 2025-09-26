import plotly.express as px

def histogram(df, x, x_title, y_title, plot_title = ""):
    """
    Creates a histogram from given data
    df = Dataframe with orders
    x = Parameter to calculate the distribution
    x_title = Name of x axis
    y_title = Name of y axis
    plot_title = Title of plot (No title by default)
    """

    fig = px.histogram(df, x=x)
    fig.update_layout(
        plot_bgcolor="rgba(0, 0, 0, 0)", bargap=0.2,
        #width=600, height=400,
        title_text=plot_title, title_x=0.2
    )
    fig.update_xaxes(
        title=x_title,
        ticks='outside',
        showline=True,
        linecolor='black',
        showgrid=False
    )
    fig.update_yaxes(
        title=y_title,
        ticks='outside',
        showline=True,
        linecolor='black',
        showgrid=False
    )

    return fig
