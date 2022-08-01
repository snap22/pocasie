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
from plot_utils import weather_fig, daily_temp_fig

# %%
current, hourly_DF, daily_DF = weather_data('Martin')

# %%
# hourly, bar graph
fig1 = weather_fig(hourly_DF,'hourly',val='clouds',kind='Bar', color='darkblue')
fig1

# %%
# hourly, line graph
fig2 = weather_fig(hourly_DF, 'hourly', val='temperature',color='red')
fig2

# %%
# daily, bar graph
fig3 = weather_fig(daily_DF,'daily',val='clouds',kind='Bar',color='deepskyblue')
fig3

# %%
# daily, line graph
fig4 = weather_fig(daily_DF,'daily',val='pressure',color='blue')
fig4

# %%
# daily temperatures graph
fig5 = daily_temp_fig(daily_DF)
fig5
