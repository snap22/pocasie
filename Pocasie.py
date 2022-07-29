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
pn.extension()
import param
from bokeh.plotting import curdoc

from get_weather import weather_data, Stanice

# %%
merania = ["Teplota", "Tlak", "Oblaky", "Vietor", "Zrážky", "Vlhkosť"]
casy = ["Aktuálne počasie","Predpoveď 48 hod.","Predpoveď 8 dní"]


# %%
class Predpoved(param.Parameterized):
    StanicaVyber = param.Selector(objects=sorted(list(Stanice.keys())))
    Co_kreslit = param.ListSelector(default=["Teplota","Vietor"], objects=merania,precedence=0.5)
    Casy_vyber = param.Selector(objects=casy,default="Predpoveď 48 hod.")

    @param.depends("StanicaVyber","Co_kreslit")
    def view(self):
        # dorobit pre bokeh
        pass

# %%
PP = Predpoved(name="")
pn.Param(PP, widgets={'Co_kreslit': pn.widgets.CheckBoxGroup})

prehlad = pn.Column(pn.pane.Markdown("## Predpoveď počasia na 5 dní",align='center'),PP.param,PP.view)
prehlad[1][1].param.set_param(name="Výber meteostanice",width=200)
prehlad[1][2].param.set_param(name = "Čo nakresliť",width=150)
stan,velic = prehlad[1][1:]
curdoc().title="Počasie (5dní)"

znazornit = pn.Column(prehlad[0],pn.Row(pn.Spacer(width=160),stan, pn.Spacer(width=130),velic),PP.view)
znazornit.servable(target="main")
