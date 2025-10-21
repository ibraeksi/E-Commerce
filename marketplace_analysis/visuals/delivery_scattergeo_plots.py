import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def delivery_scattergeo_plots(df, plot_type, plot_title = ""):
    """
    Creates a scattergeo plot based on delivery KPIs
    df = Dataframe with orders
    plot_type = Feature to calculate distribution (Shipping Time, Delayed Orders or Review Score)
    plot_title = Title of plot (No title by default)
    """
    # Removing some outliers
    #Brazils most Northern spot is 5 deg 16′ 27.8″ N Lat
    df = df[df['customer_latitude'] <= 5.27438888]
    #it’s most Western spot is 73 deg, 58′ 58.19″W Long
    df = df[df['customer_longitude'] >= -73.98283055]
    #It’s most southern spot is 33 deg, 45′ 04.21″ S Lat
    df = df[df['customer_latitude'] >= -33.75116944]
    #It’s most Eastern spot is 34 deg, 47′ 35.33″ W Long
    df = df[df['customer_longitude'] <=  -34.79314722]

    # getting the first 3 digits of customer zipcode
    df['customer_zipcode_prefix'] = df['customer_zipcode'].astype(str).str.zfill(5).str[0:3]
    df['customer_zipcode_prefix'] = df['customer_zipcode_prefix'].astype(int)

    if plot_type == 'shipping':
        grouped_df = df.groupby(['customer_zipcode_prefix', 'customer_city']).agg({'shipping_days': 'mean', 'customer_latitude': 'mean', 'customer_longitude': 'mean'}).reset_index()
        grouped_df['marker_size'] = grouped_df['shipping_days']/2
        grouped_df['marker_text'] = grouped_df['customer_city'].str.title() + '<br>Shipping Time: ' + round(grouped_df['shipping_days'],2).astype(str) + ' days'
        colorbar_feature = 'shipping_days'
        colorbar_title = "Shipping Time (days)"
        colorbar_max = 30
    elif plot_type == 'delays':
        grouped_df = df.groupby(['customer_zipcode_prefix', 'customer_city']).agg({'delay_days': 'mean', 'customer_latitude': 'mean', 'customer_longitude': 'mean'}).reset_index()
        grouped_df['marker_size'] = grouped_df['delay_days']/2
        grouped_df['marker_text'] = grouped_df['customer_city'].str.title() + '<br>Delay: ' + round(grouped_df['delay_days'],2).astype(str) + ' days'
        colorbar_feature = 'delay_days'
        colorbar_title = "Delay Time (days)"
        colorbar_max = 30
    elif plot_type == 'review':
        grouped_df = df.groupby(['customer_zipcode_prefix', 'customer_city']).agg({'review_score': 'mean', 'customer_latitude': 'mean', 'customer_longitude': 'mean'}).reset_index()
        grouped_df['marker_size'] = 10
        grouped_df['marker_text'] = grouped_df['customer_city'].str.title() + '<br>Avg. Score: ' + round(grouped_df['review_score'],2).astype(str)
        colorbar_feature = 'review_score'
        colorbar_title = "Review Score"
        colorbar_max = 5

    fig = go.Figure(data=go.Scattergeo(
        lat = grouped_df['customer_latitude'],
        lon = grouped_df['customer_longitude'],
        text = grouped_df['marker_text'],
        mode = 'markers',
        marker = dict(
                size = grouped_df['marker_size'],
                opacity = 0.8,
                autocolorscale = False,
                line = dict(
                    width=1,
                    color='rgba(102, 102, 102)'
                ),
                colorscale = 'thermal',
                cmin = 0,
                cmax = colorbar_max,
                color = grouped_df[colorbar_feature],
                colorbar=dict(
                    title=dict(
                        text=colorbar_title
                    )
                )
            )))

    fig.update_layout(
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
