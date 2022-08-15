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

from get_weather import weather_data, StaNames
from plot_utils import weather_fig_vals, choosen_onmap

pn.extension('plotly')

# %%
merania = {"Teplota": "temperature", "Tlak": "pressure", "Oblaky": "clouds", 
           "Vietor": "wind", "Zrážky": "rain", "Vlhkosť": "humidity"}

MAX_SELECTED_VALUES = 3

# %%
stanica_vyber = pnw.Select(options=list(StaNames),value="Bratislava")
merania_vyber = pnw.CheckBoxGroup(options=merania,value=["temperature","clouds"])


# %%
def set_merania(*events):
    for event in events:
        if event.type == "changed" and len(event.new) > MAX_SELECTED_VALUES:
            merania_vyber.value = event.old
            
watcher = merania_vyber.param.watch(set_merania, ['value'], onlychanged=True)            


# %%
@pn.depends(stanica_vyber)
def view_current(stanica_vyber):
    float_fmt = lambda s: '%.1f' %s
    df = weather_data(stanica_vyber)['current']
    return pn.pane.DataFrame(df, justify='center', width=240, float_format=float_fmt)


# %%
@pn.depends(stanica_vyber,merania_vyber)
def view_hourly(stanica_vyber,merania_vyber):
    fig = weather_fig_vals(weather_data(stanica_vyber), 'hourly', vals=merania_vyber)
    return fig


# %%
@pn.depends(stanica_vyber,merania_vyber)
def view_daily(stanica_vyber,merania_vyber):
    fig = weather_fig_vals(weather_data(stanica_vyber), 'daily', vals=merania_vyber)
    return fig


# %%
@pn.depends(stanica_vyber)
def view_map(stanica_vyber):
    return pn.pane.plot.Folium(choosen_onmap(stanica_vyber), width=1000, height=600)


# %%
global widgets

merania_row = pn.Row(merania_vyber,width=250,align='center')
widgets = pn.Column(pn.Row(stanica_vyber,width=250), merania_row, pn.Row(view_current), align='center')
nadpis_celkovy = pn.pane.Markdown("## Počasie na Slovensku<br/>", align='center')

# %%
tabs = pn.Tabs(("Predpoveď 48 hod.", pn.Column(view_hourly)), ("Predpoveď 8 dní", pn.Column(view_daily)),
               ("Stanice na mape", pn.Column(view_map, width=1000,height=600)), dynamic=True, tabs_location="above")


# %%
def enable_merania(*events):
    global widgets
    for event in events:
        active_tab = event.new
        if active_tab == 2:
            widgets.objects[1][0] = pn.Row(pn.pane.Markdown("<center><h3>Nemeriame, ukazujeme</h3></center>",
                                                            width=240, height=110, align="center"))
        else:
            widgets.objects[1][0] = pn.Row(merania_vyber, width=250, align='center')

tabs_watcher = tabs.param.watch(enable_merania, 'active', onlychanged=True)

# %%
weather_info = pn.Column(nadpis_celkovy,tabs)
app = pn.Column(pn.Row(widgets, pn.Spacer(width=20), weather_info)).servable(title="Počasie na Slovensku")
app
