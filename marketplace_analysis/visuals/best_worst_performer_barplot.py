import plotly.express as px


def best10_performer_plot(df, x_axis_title, x_range='Auto', plot_title = ""):
    """
    Plots the 10 best performers with product categories
    df = Top 10 product categories based on selected feature
    x_axis_title = Title of x axis
    x_range = Range of x axis values (Auto by default)
    plot_title = Title of plot (No title by default)
    """
    df.columns=['category', 'value']
    fig = px.bar(df, x='value', y='category', orientation='h', color='value', color_continuous_scale='Emrld',
                 text=[f"{row[1]} ({row[2]})" for row in df.itertuples()])
    fig.update_layout(plot_bgcolor="rgba(0, 0, 0, 0)",
                    title_text=plot_title, title_x=0.1,
                    coloraxis_showscale=False, autosize=False)
    if x_range == 'Auto':
        fig.update_xaxes(
            title=x_axis_title,
            ticks='outside',
            showline=True,
            linecolor='black',
            showgrid=False
        )
    else:
        fig.update_xaxes(
            title=x_axis_title,
            ticks='outside',
            showline=True,
            linecolor='black',
            showgrid=False,
            range=x_range
        )
    fig.update_yaxes(
        ticks='outside',
        showline=True,
        linecolor='black',
        showgrid=False,
        categoryorder='total ascending',
        visible=False
    )
    fig.update_traces(hovertemplate='%{y} (%{x})')

    return fig


def worst10_performer_plot(df, x_axis_title, x_range='Auto', plot_title=""):
    """
    Plots the 10 worst performers with product categories
    df = Bottom 10 product categories based on selected feature
    x_axis_title = Title of x axis
    x_range = Range of x axis values (Auto by default)
    plot_title = Title of plot (No title by default)
    """
    df.columns=['category', 'value']
    fig = px.bar(df, x='value', y='category', orientation='h', color='value', color_continuous_scale='solar',
                 text=[f"{row[1]} ({row[2]})" for row in df.itertuples()])
    fig.update_layout(plot_bgcolor="rgba(0, 0, 0, 0)",
                    title_text=plot_title, title_x=0.1,
                    coloraxis_showscale=False)
    if x_range == 'Auto':
        fig.update_xaxes(
            title=x_axis_title,
            ticks='outside',
            showline=True,
            linecolor='black',
            showgrid=False
        )
    else:
        fig.update_xaxes(
            title=x_axis_title,
            ticks='outside',
            showline=True,
            linecolor='black',
            showgrid=False,
            range=x_range
        )
    fig.update_yaxes(
        ticks='outside',
        showline=True,
        linecolor='black',
        showgrid=False,
        categoryorder='total descending',
        visible=False
    )
    fig.update_traces(hovertemplate='%{y} (%{x})')

    return fig
