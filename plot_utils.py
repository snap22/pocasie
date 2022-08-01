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

from get_weather import weather_data, Stanice


# %%
def weather_fig(df, period, val, color='indigo', kind='scatter'):
    fig = go.Figure()
    plot_function = go.Scatter if kind=='scatter' else go.Bar
    fig.add_trace(plot_function(x=df.index,y=df[val],marker_color=color))
    if period == 'hourly':
        fig.update_xaxes(dtick=60*60*1000*3, tickformat="%H\n%e.%b")
    else:   # daily
        fig.update_xaxes(dtick=60*60*1000*24, tickformat="%e.%b", ticklabelmode="period")
    return fig


# %%
def daily_temp_fig(df, kind='scatter'):
    fig = go.Figure()
    plot_function = go.Scatter if kind=='scatter' else go.Bar
    fig.add_trace(plot_function(x=df.index,y=df['temp_day'],marker_color='green',name='day'))
    fig.add_trace(plot_function(x=df.index,y=df['temp_night'],marker_color='darkblue',name='night'))
    fig.add_trace(plot_function(x=df.index,y=df['temp_max'],marker_color='red',name='max'))
    fig.add_trace(plot_function(x=df.index,y=df['temp_min'],marker_color='blue',name='min'))
    fig.update_xaxes(dtick=60*60*1000*24, tickformat="%e.%b", ticklabelmode="period")
    return fig
