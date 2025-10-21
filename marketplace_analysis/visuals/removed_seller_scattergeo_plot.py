import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def removed_seller_scattergeo_plot(df, plot_title = ""):
    """
    Creates a scattergeo plot showing the locations of the removed sellers
    df = Preprocessed dataframe with orders and seller revenues
    plot_title = Title of plot (No title by default)
    """
    # Removing some outliers
    #Brazils most Northern spot is 5 deg 16′ 27.8″ N Lat
    df = df[df['seller_latitude'] <= 5.27438888]
    #it’s most Western spot is 73 deg, 58′ 58.19″W Long
    df = df[df['seller_longitude'] >= -73.98283055]
    #It’s most southern spot is 33 deg, 45′ 04.21″ S Lat
    df = df[df['seller_latitude'] >= -33.75116944]
    #It’s most Eastern spot is 34 deg, 47′ 35.33″ W Long
    df = df[df['seller_longitude'] <=  -34.79314722]

    #df['seller_type'] = df['profits'].apply(lambda x: 'Removed' if x<0 else 'Remaining')
    #df['seller_type_color'] = df['seller_type'].apply(lambda x: 'red' if x == 'Removed' else 'forestgreen')

    removed_df = df[df['profits']<=0].reset_index(drop=True)
    remaining_df = df[df['profits']>0].reset_index(drop=True)

    fig = go.Figure(data=[go.Scattergeo(
        lat = remaining_df['seller_latitude'],
        lon = remaining_df['seller_longitude'],
        text = remaining_df['seller_city'],
        mode = 'markers', name = 'Net Positive',
        marker_color='forestgreen'), go.Scattergeo(
        lat = removed_df['seller_latitude'],
        lon = removed_df['seller_longitude'],
        text = removed_df['seller_city'],
        mode = 'markers', name = 'Underperforming',
        marker_color='red')])

    fig.update_layout(
        legend = dict(font = dict(size = 14, color='black'), yanchor="top", y=0.98, xanchor="right", x=0.95),
        legend_title = dict(font = dict(size = 14, color='black')),
        legend_bgcolor="rgba(0, 0, 0, 0)",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        legend_title_text='Seller Type',
        height=600, width=550,
        margin=dict(t=25, b=0, l=0, r=0),
        title = plot_title,
        geo = dict(
            projection_scale=1.75,
            center=dict(lat=-19, lon=-54),
            scope='south america',
            projection_type='mercator',
            showland = True,
            showocean = True,
            showrivers = True,
            landcolor = "rgb(242, 242, 242)",
            countrycolor = "rgb(217, 217, 217)",
            oceancolor = "rgb(179, 205, 227)",
            rivercolor = "rgb(179, 205, 227)",
        ),
    )

    return fig
