# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     cell_metadata_json: true
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

# %% {"init_cell": true}
import panel as pn
import panel.widgets as pnw
pn.extension('plotly')
from plotly.subplots import make_subplots
from functools import lru_cache

from get_weather import weather_data, Stanice, StaNames
from plot_utils import weather_fig_vals


# %%
@lru_cache(maxsize=20)
def weather_cached(stanica):
    return weather_data(stanica)


# %%
merania = {"Teplota": "temperature", "Tlak": "pressure", "Oblaky": "clouds", 
           "Vietor": "wind", "Zrážky": "rain", "Vlhkosť": "humidity"}
casy = {"Aktuálne počasie": "current","Predpoveď 48 hod.": "hourly","Predpoveď 8 dní": "daily"}

# %%
stanica_vyber = pnw.Select(options=list(StaNames),size=8,value="Martin")

merania_vyber = pnw.CheckBoxGroup(options=merania,value=["temperature","clouds"])


# %%
@pn.depends(stanica_vyber,merania_vyber)
def view_hourly(stanica_vyber,merania_vyber):
    fig = weather_fig_vals(weather_cached(stanica_vyber),'hourly',vals=merania_vyber)
    return pn.pane.Plotly(fig)


# %%
@pn.depends(stanica_vyber,merania_vyber)
def view_daily(stanica_vyber,merania_vyber):
    fig = weather_fig_vals(weather_cached(stanica_vyber),'daily',vals=merania_vyber)
    return pn.pane.Plotly(fig)


# %%
widgets = pn.Column(pn.Row(stanica_vyber,width=250),pn.Row(merania_vyber,width=250)) 

# %%
tabs = pn.Tabs(("Predpoveď 48 hod.",pn.Column(view_hourly)),("Predpoveď 8 dní",pn.Column(view_daily)),
                dynamic=True,tabs_location="above")

# %%
app = pn.Row(widgets, tabs).servable()
