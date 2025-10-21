import plotly.express as px

def num_sellers_profit_lineplot(df, plot_title = ""):
    """
    Creates a line plot showing total revenue with respect to number of sellers
    df = Preprocessed dataframe with orders and seller revenues
    plot_title = Title of plot (No title by default)
    """
    max_profit = df['Total Profits'].max()
    max_profit_after_IT = df['Net Profits'].max()

    max_profit_row = len(df)-df['Total Profits'].idxmax()
    max_profit_after_IT_row = len(df)-df['Net Profits'].idxmax()

    fig = px.line(df, x='num_sellers', y=['IT Costs', 'Total Profits', 'Net Profits'],
                  color_discrete_sequence=['red', 'blue', 'forestgreen'])

    fig.add_hline(y=max_profit, line_width=1, line_dash="dash", line_color="blue")
    fig.add_hline(y=max_profit_after_IT, line_width=1, line_dash="dash", line_color="forestgreen")

    fig.add_vline(x=max_profit_row, line_width=1, line_dash="dash", line_color="blue")
    fig.add_vline(x=max_profit_after_IT_row, line_width=1, line_dash="dash", line_color="forestgreen")

    fig.add_annotation(x=max_profit_row, y=max_profit,
                text=f"# of Sellers = {max_profit_row}",
                showarrow=False,
                xshift=30, yshift=10)

    fig.add_annotation(x=max_profit_after_IT_row, y=max_profit_after_IT,
                text=f"# of Sellers = {max_profit_after_IT_row}",
                showarrow=False,
                xshift=30, yshift=10)

    fig.add_annotation(x=len(df),
                       y=df.loc[0,'Total Profits'],
                text=f"# of Sellers = {len(df)}",
                showarrow=False, yshift=-10)

    fig.update_layout(
        legend_title_text='',
        plot_bgcolor="rgba(0, 0, 0, 0)",
        title_text=plot_title, title_x=0
    )
    fig.update_xaxes(
        title='Number of Sellers',
        ticks='outside',
        showline=True,
        linecolor='black',
        showgrid=False,
        range=[0,3250]
    )
    fig.update_yaxes(
        title='Total Amount [BRL mil.]',
        ticks='outside',
        showline=True,
        linecolor='black',
        showgrid=False,
        range=[0,1.6]
    )

    return fig
