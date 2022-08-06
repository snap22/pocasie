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
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from get_weather import weather_data, Stanice
w_colors = {'temperature':'red','rain':'darkblue','wind':'blue','clouds':'yellow',
            'pressure':'darkgray','humidity':'blue'}
nadpisy = {'temperature': 'Teplota', 'pressure': 'Tlak', 'clouds': 'Oblaky',
           'wind': 'Vietor', 'rain': 'Zrážky', 'humidity': 'Vlhkosť'}


# %%
def weather_fig_vals(wdata, period, vals=['temperature','clouds']):
    df = wdata[period]
    nplots = len(vals) 
    fig = make_subplots(rows=nplots, cols=1,subplot_titles=[nadpisy[val] for val in vals], vertical_spacing=0.09)

    xval = df.index
    for ind,val in enumerate(vals):
        nrow = ind + 1
        if period == 'daily' and val == 'temperature':
            fig.add_trace(go.Scatter(x=xval,y=df['temp_day'],
                                     marker_color='green',name='day'),row=nrow,col=1)
            fig.add_trace(go.Scatter(x=xval,y=df['temp_night'],
                                     marker_color='darkblue',name='night'),row=nrow,col=1)
            fig.add_trace(go.Scatter(x=xval,y=df['temp_max'],
                                     marker_color='red',name='max'),row=nrow,col=1)
            fig.add_trace(go.Scatter(x=xval,y=df['temp_min'],
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
