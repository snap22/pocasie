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
from bokeh.plotting import figure, output_notebook, show

from get_weather import weather_data, Stanice
output_notebook()

# %%
current, hourly_DF, daily_DF = weather_data('Martin')


# %%
def hourly_figure(val="temp"):
    ph = figure(width=800, height=250, x_axis_type="datetime", tools = "pan,hover,reset",
               tooltips=[(val,"$x, $y")])
    ph.xaxis.formatter.days = '%d.%b'
    ph.xaxis.ticker.desired_num_ticks = 12
    ph.xaxis.major_label_text_font_style = 'bold'
    ph.xaxis.formatter.hours = '%H'
    return ph


# %%
# hourly forecast plot example
x, y = hourly_DF.index, hourly_DF['temperature']
ph = hourly_figure("temp")
ph.line(x, y)
show(ph)


# %%
def daily_figure(val="temp"):
    pd = figure(width=800, height=250, x_axis_type="datetime", tools = "pan,hover,reset")
    pd.xaxis.formatter.days = '%d.%b'
    pd.xaxis.ticker.desired_num_ticks = 8
    pd.xaxis.major_label_text_font_style = 'bold'
    return pd


# %%
# daily forecast plot example, bar plot
x, y = daily_DF.index, daily_DF['rain']
pd = daily_figure("rain")
pd.vbar(x, top=y, width=1000*3600*23) # in milliseconds
show(pd)

# %%
# daily forecast plot example, line plot
x, ymax = daily_DF.index, daily_DF['temp_max']
ymin = daily_DF['temp_min']

pd = daily_figure()
pd.line(x, ymax)
pd.line(x, ymin)
pd.circle(x,ymax)
show(pd)
