from dash import Dash, dcc, html, Input, Output
from data_script import id_df, zipcode_data, months
from dotenv import load_dotenv
from flask_caching import Cache
import os
import plotly.express as px
import re

load_dotenv()
MAPBOX_TOKEN = os.getenv('MAPBOX_TOKEN')

# Diskcache
# cache = diskcache.Cache("./cache")
# long_callback_manager = DiskcacheLongCallbackManager(cache)


app = Dash(name=__name__, eager_loading=True, title="ID ZHVI")
# cache = Cache(app.server, config={
#     'CACHE_TYPE': 'filesystem',
#     'CACHE_DIR': './cache'
# })
# TIMEOUT = 60

app.layout = html.Div([
    html.H4('Idaho Zillow Home Value Index (ZHVI) vs. Time'),
    html.P('Select a month:'),
    dcc.Dropdown(id='month', value='2022-01-31', options=months, clearable=False),
    dcc.Graph(id="graph"),
])


# @cache.memoize(timeout=TIMEOUT)
def get_figure(df, geojson, month):
    fig = px.choropleth_mapbox(
        data_frame=df,
        geojson=geojson,
        color=month,
        locations="ZIP",
        center={"lat": 45.3775, "lon": -114.9657},
        zoom=5,
        height=600,
        mapbox_style='carto-positron',
        opacity=0.9,
        range_color=[100000, 1150000],
    )
    fig.update_layout(
        margin={"r": 0, "t": 50, "l": 0, "b": 0},
        mapbox_accesstoken=MAPBOX_TOKEN)

    return fig


@app.callback(output=Output("graph", "figure"),
              inputs=Input("month", "value"),)
def display_choropleth(month):
    """
    mapbox_style options = ["carto-positron", "carto-darkmatter", "stamen-terrain", "stamen-toner", "stamen-watercolor"
    """
    df = id_df
    geojson = zipcode_data
    return get_figure(df, geojson, month)


app.run_server(debug=True)
