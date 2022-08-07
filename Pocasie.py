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

from plotly.subplots import make_subplots

from get_weather import weather_data, StaNames, db
from plot_utils import weather_fig_vals

pn.extension('plotly')

# %%
merania = {"Teplota": "temperature", "Tlak": "pressure", "Oblaky": "clouds", 
           "Vietor": "wind", "Zrážky": "rain", "Vlhkosť": "humidity"}
casy = {"Aktuálne počasie": "current","Predpoveď 48 hod.": "hourly","Predpoveď 8 dní": "daily"}

MAX_SELECTED_VALUES = 3

# %%
stanica_vyber = pnw.Select(options=list(StaNames),size=8,value="Martin")

merania_vyber = pnw.CheckBoxGroup(options=merania,value=["temperature","clouds"])


# %%
def set_merania(*events):
    for event in events:
        if event.type == "changed" and len(event.new) > MAX_SELECTED_VALUES:
            merania_vyber.value = event.old
            
watcher = merania_vyber.param.watch(set_merania, ['value'], onlychanged=True)            


# %%
@pn.depends(stanica_vyber,merania_vyber)
def view_hourly(stanica_vyber,merania_vyber):
    return weather_fig_vals(weather_data(stanica_vyber),
                            'hourly', vals=merania_vyber)


# %%
@pn.depends(stanica_vyber,merania_vyber)
def view_daily(stanica_vyber,merania_vyber):
    return weather_fig_vals(weather_data(stanica_vyber),
                            'daily',vals=merania_vyber)


# %%
widgets = pn.Column(pn.Row(stanica_vyber,width=250),pn.Row(merania_vyber,width=250)) 

# %%
tabs = pn.Tabs(("Predpoveď 48 hod.",pn.Column(view_hourly)),("Predpoveď 8 dní",pn.Column(view_daily)),
                dynamic=True,tabs_location="above")

# %%
app = pn.Row(widgets, tabs).servable()
app
