import folium
from folium.plugins import MarkerCluster

legend_html = f'''
<div style="
    position: fixed;
    top: 50px; right: 10px; width: 280px;
    z-index:9999; font-size:14px;
    background-color: rgba(0,0,0,0.3);
    border:2px solid grey;
    border-radius:6px;
    padding: 10px;
    box-shadow: 2px 2px 6px rgba(0,0,0,0.3);
    ">
  <p style="margin:0 0 5px 0;">Only cities with <b>100+ orders</b> included</p>
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
    100–499 orders
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
        lng=(f'{type}_longitude', 'median')
    ).reset_index()

    filtered_city_group = city_group[city_group['order_count'] >= 100]

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

        folium.CircleMarker(
            location=[row['lat'], row['lng']],
            radius=radius,
            popup=f"{row[f'{type}_city']}<br>Orders: {num_orders}<br>Avg payment: R$ {row['avg_payment']:.0f}",
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7
        ).add_to(marker_cluster)

    m.get_root().html.add_child(folium.Element(legend_html))

    return m
