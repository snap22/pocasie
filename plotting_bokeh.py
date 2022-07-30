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
from bokeh.plotting import figure, output_notebook, show, ColumnDataSource

from get_weather import weather_data, Stanice
from datetime import datetime
output_notebook()

# %%
current, hourly, daily = weather_data('Martin')


# %%
def hourly_figure(val="temp"):
    ph = figure(width=800, height=250, x_axis_type="datetime", tools = "pan,hover,reset",
               tooltips=[(val,"$y")])
    ph.xaxis.formatter.days = '%d/%m'
    ph.xaxis.ticker.desired_num_ticks = 12
    ph.xaxis.major_label_text_font_style = 'bold'
    ph.xaxis.formatter.hours = '%H'
    return ph


# %%
# hourly forecast plot example
xy = [(h, hourly[h]['humidity']) for h in hourly.keys()]
x, y = zip(*xy)
ph = hourly_figure("hum")
ph.line(x, y)
show(ph)


# %%
def daily_figure(val="temp"):
    pd = figure(width=800, height=250, x_axis_type="datetime", tools = "pan,reset")
    pd.xaxis.formatter.days = '%d/%m'
    pd.xaxis.ticker.desired_num_ticks = 8
    pd.xaxis.major_label_text_font_style = 'bold'
    return pd


# %%
# daily forecast plot example, bar plot
xy = [(d, daily[d]['rain']) for d in daily.keys()]
x, y = zip(*xy)
pd = daily_figure("rain")
pd.vbar(x, top=y, width=1000*3600*23) # in milliseconds
show(pd)

# %%
# daily forecast plot example, line plot
pd = daily_figure()
xy = [(d, daily[d]['temperature']['day']) for d in daily.keys()]
x, y = zip(*xy)
pd.line(x, y)
pd.circle(x,y)
show(pd)
