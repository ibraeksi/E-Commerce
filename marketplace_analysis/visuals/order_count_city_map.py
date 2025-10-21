import folium
from folium.plugins import MarkerCluster


legend_html = f'''
<div style="
    position: fixed;
    top: 50px; right: 130px; width: 170px;
    z-index:9999; font-size:14px;
    background-color: rgba(0,0,0,0.3);
    border:2px solid grey;
    border-radius:6px;
    padding: 10px;
    box-shadow: 2px 2px 6px rgba(0,0,0,0.3);
    ">
  <p style="margin:0 0 5px 0;">Showing only cities with <b>10+ orders</b></p>
  <p style="margin:0;">
    <span style="display:inline-block; width:12px; height:12px; background-color:#e63946; border-radius:50%; margin-right:6px;"></span>
    1000+ orders
  </p>
  <p style="margin:0;">
    <span style="display:inline-block; width:12px; height:12px; background-color:#f4a261; border-radius:50%; margin-right:6px;"></span>
    500–999 orders
  </p>
  <p style="margin:0;">
    <span style="display:inline-block; width:12px; height:12px; background-color:#48cae4; border-radius:50%; margin-right:6px;"></span>
    10–499 orders
  </p>
</div>
'''

def order_count_city_map(df, type):
    """
    Creates a Folium map with number of orders per customer
    df = Dataframe with orders
    type = The name of the group for the locations (Customer or Seller)
    """
    city_group = df.groupby(f'{type}_city').agg(
        avg_payment=('payment_value', 'mean'),
        order_count=('order_id', 'count'),
        lat=(f'{type}_latitude', 'median'),
        lon=(f'{type}_longitude', 'median')
    ).reset_index()

    # Removing some outliers
    #Brazils most Northern spot is 5 deg 16′ 27.8″ N Lat
    city_group = city_group[city_group['lat'] <= 5.27438888]
    #it’s most Western spot is 73 deg, 58′ 58.19″W Long
    city_group = city_group[city_group['lon'] >= -73.98283055]
    #It’s most southern spot is 33 deg, 45′ 04.21″ S Lat
    city_group = city_group[city_group['lat'] >= -33.75116944]
    #It’s most Eastern spot is 34 deg, 47′ 35.33″ W Long
    city_group = city_group[city_group['lon'] <=  -34.79314722]

    # To apply a filter for minimum number of orders
    filtered_city_group = city_group[city_group['order_count'] >= 10]

    m = folium.Map(location=[-14.2350, -51.9253], zoom_start=4)
    marker_cluster = MarkerCluster().add_to(m)

    for _, row in filtered_city_group.iterrows():
        num_orders = row['order_count']

        if num_orders >= 1000:
            color = 'crimson'
            radius = 18
        elif num_orders >= 500:
            color = 'darkorange'
            radius = 13
        else:
            color = 'royalblue'
            radius = 9

        popuptext = f"{row[f'{type}_city'].title()}<br># of Orders: {num_orders}<br>Avg. Payment: {row['avg_payment']:.0f} BRL"
        popup = folium.Popup(popuptext, max_width=300,min_width=150)

        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=radius,
            popup=popup,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7
        ).add_to(marker_cluster)

    m.get_root().html.add_child(folium.Element(legend_html))

    return m
