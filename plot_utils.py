# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.14.0
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import panel as pn
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import folium
from folium import plugins
import json

from get_weather import weather_data, Stanice, wkeys, nadpisy
#                  wkeys = ['clouds', 'rain',  'wind', 'humidity', 'pressure', 'temperature']
w_colors = dict(zip(wkeys,['green', 'darkblue', 'blue', 'magenta', 'darkgray', 'red']))


# %%
def weather_fig_vals(wdata, period, vals=['temperature','clouds']):
    df = wdata[period]
    nplots = len(vals) 
    fig = make_subplots(rows=nplots, cols=1,subplot_titles=[nadpisy[val] for val in vals], vertical_spacing=0.09)

    xval = df.index
    for ind,val in enumerate(vals):
        nrow = ind + 1
        if period == 'daily' and val == 'temperature':
            fig.add_trace(go.Bar(x=xval,y=df['temp_day'],
                                     marker_color='green',name='day'),row=nrow,col=1)
            fig.add_trace(go.Bar(x=xval,y=df['temp_night'],
                                     marker_color='darkblue',name='night'),row=nrow,col=1)
            fig.add_trace(go.Bar(x=xval,y=df['temp_max'],
                                     marker_color='red',name='max'),row=nrow,col=1)
            fig.add_trace(go.Bar(x=xval,y=df['temp_min'],
                                     marker_color='blue',name='min'),row=nrow,col=1)
        else:
            plot_function = go.Bar if val == 'rain' else go.Scatter
            fig.add_trace(plot_function(x=xval,y=df[val],marker_color=w_colors[val],
                                        name=nadpisy[val]), row=nrow,col=1)
        if period == 'hourly':
            fig.update_xaxes(dtick=60*60*1000*3, tickformat="%H\n%e.%b",row=nrow,col=1)
        else:   # daily
            fig.update_xaxes(dtick=60*60*1000*24, tickformat="%e.%b",
                             ticklabelmode="period", row=nrow,col=1)
    fig.update_layout(height=nplots * 250,width=1000,margin=dict(t=20, b=0, r=10, l=10),showlegend=False)
    return fig


# %%
# folium maps
def slovakia_map():
    map_slovakia = folium.Map(location=[48.7, 19.6], zoom_start=8)

    with open("slovakia.geojson", "r") as file:
        geo_data = json.load(file)

    style_fcn =  lambda x : {'fillColor': '#228B2255', 'color': '#228B22'}    
    folium.GeoJson(geo_data, name="slovakia",style_function=style_fcn).add_to(map_slovakia)

    polohy, popy = [], []
    for station in Stanice:
        lat, lon = Stanice[station]
        poptext = f"{station}"
        polohy.append([lat, lon])
        popy.append(poptext)
    
    plugins.MarkerCluster(polohy, popups=popy).add_to(map_slovakia)
    return map_slovakia


# %%
def choosen_onmap(station):
    map = slovakia_map()
    folium.CircleMarker(location=Stanice[station], radius=15, color='red',
                    fill_color='red', fill=True).add_to(map)
    return map
