import plotly.express as px
import pandas as pd

def delivery_time_stage(df, plot_title = ""):
    """
    Creates a distribution of review scores with comments
    df = Dataframe with order delivery times
    plot_title = Title of plot (None by default)
    """

    summary = pd.DataFrame({
        'median': [
            df['approval_time'].median(),
            df[df['waiting_time'].notna()]['waiting_time'].median(),
            df[df['shipping_time'].notna()]['shipping_time'].median(),
            df['total_time'].median(),
            df['estimated_time'].median()
        ],
        'std': [
            df['approval_time'].std(),
            df[df['waiting_time'].notna()]['waiting_time'].std(),
            df[df['shipping_time'].notna()]['shipping_time'].std(),
            df['total_time'].std(),
            df['estimated_time'].std()
        ]
    }, index=['Approval', 'Waiting', 'Shipping', 'Total', 'Estimated'])

    summary = summary.map(lambda x: pd.to_timedelta(x.round('s'))).reset_index()

    summary['median_hours'] = summary['median'].dt.total_seconds() / 3600
    summary['std_hours'] = summary['std'].dt.total_seconds() / 3600
    summary['label'] = summary['median_hours'].apply(lambda h: f"{h:.0f}h\n({h/24:.1f}d)")

    fig = px.scatter(summary, x="index", y="median_hours",
                 error_x="std_hours", error_y="std_hours")
    fig.update_layout(
        plot_bgcolor="rgba(0, 0, 0, 0)",
        width=600, height=400,
        title_text=plot_title, title_x=0.2
    )
    fig.update_xaxes(
        title='',
        ticks='outside',
        showline=True,
        linecolor='black',
        showgrid=False,
    )
    fig.update_yaxes(
        title='Delivery Time [hours]',
        ticks='outside',
        showline=True,
        linecolor='black',
        showgrid=False,
        range=[0,800]
    )

    for i in range(len(summary)):
        if i == 0:
            fig.add_annotation(
                dict(x=summary.loc[i,'index'],
                    y=summary.loc[i,'median_hours'],
                    text=str(int(summary.loc[i,'median_hours']*60))+'min.',
                    font=dict(color='blue'),
                    showarrow=False,
                    xshift=0,
                    yshift=15))
        else:
            fig.add_annotation(
                dict(x=summary.loc[i,'index'],
                    y=summary.loc[i,'median_hours'],
                    text=summary.loc[i,'label'] ,
                    font=dict(color='blue'),
                    showarrow=False,
                    xshift=0,
                    yshift=15))

    return fig
