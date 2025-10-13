import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def financial_scattergeo_plots(df, plot_type, plot_title = ""):
    """
    Creates a distribution of review scores with comments
    df = Dataframe with orders
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

    if plot_type == 'revenue':
        grouped_df = df.groupby(['customer_zipcode_prefix', 'customer_city']).agg({'price': 'sum', 'customer_latitude': 'mean', 'customer_longitude': 'mean'}).reset_index()
        grouped_df['marker_size'] = grouped_df['price']/3000
        grouped_df['marker_text'] = grouped_df['customer_city'].str.title() + '<br>Revenue: ' + round(grouped_df['price'],2).astype(str)
        colorbar_feature = 'price'
        colorbar_title = "Total Revenue (RBL)"
    elif plot_type == 'ticket':
        grouped_df = df.groupby(['order_id', 'customer_city']).agg({'price': 'sum', 'customer_zipcode_prefix': 'max', 'customer_latitude': 'mean', 'customer_longitude': 'mean'})\
            .groupby(['customer_zipcode_prefix', 'customer_city']).agg({'price': 'mean', 'customer_latitude': 'mean', 'customer_longitude': 'mean'}).reset_index()
        grouped_df['marker_size'] = grouped_df['price']/100
        grouped_df['marker_text'] = grouped_df['customer_city'].str.title() + '<br>Avg. Ticket: ' + round(grouped_df['price'],2).astype(str)
        colorbar_feature = 'price'
        colorbar_title = "Average Ticket (RBL)"
    elif plot_type == 'freight':
        step_df = df.groupby(['order_id', 'customer_city']).agg({'price': 'sum', 'freight_value': 'sum', 'customer_zipcode_prefix': 'max', 'customer_latitude': 'mean', 'customer_longitude': 'mean'})
        step_df['freight_ratio'] = 100*(step_df['freight_value'] / step_df['price'])
        grouped_df = step_df.groupby(['customer_zipcode_prefix', 'customer_city']).agg({'freight_ratio': 'mean', 'customer_latitude': 'mean', 'customer_longitude': 'mean'}).reset_index()
        grouped_df['marker_size'] = grouped_df['freight_ratio']/20
        grouped_df['marker_text'] = grouped_df['customer_city'].str.title() + '<br>Freight Ratio: ' + round(grouped_df['freight_ratio'],1).astype(str) + ' %'
        colorbar_feature = 'freight_ratio'
        colorbar_title = "Freight Ratio (%)"

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
                color = grouped_df[colorbar_feature],
                cmax = grouped_df[colorbar_feature].max(),
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
