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
current, hourly_DF, daily_DF = weather_data('Martin')

# %%
# hourly, bar graph
fig1 = go.Figure() 
fig1.add_trace(go.Bar(x=hourly_DF.index,y=hourly_DF['rain'],marker_color="indigo"))
fig1.update_xaxes(dtick=60*60*1000*3, tickformat="%H\n%e.%b")
fig1

# %%
# hourly, line graph
fig2 = go.Figure() 
fig2.add_trace(go.Scatter(x=hourly_DF.index,y=hourly_DF['temperature'],marker_color="red"))
fig2.update_xaxes(dtick=60*60*1000*3, tickformat="%H\n%e.%b")
fig2

# %%
# daily, bar graph
fig3 = go.Figure() 
fig3.add_trace(go.Bar(x=daily_DF.index,y=daily_DF['rain'],marker_color="indigo"))
fig3.update_xaxes(dtick=60*60*1000*24, tickformat="%e.%b", ticklabelmode="period")
fig3

# %%
# daily, line graph
fig4 = go.Figure() 
fig4.add_trace(go.Scatter(x=daily_DF.index,y=daily_DF['temp_max'],marker_color="red", name="tmax"))
fig4.add_trace(go.Scatter(x=daily_DF.index,y=daily_DF['temp_min'],marker_color="blue", name="tmin"))
fig4.update_xaxes(dtick=60*60*1000*24, tickformat="%e.%b", ticklabelmode="period")
fig4
