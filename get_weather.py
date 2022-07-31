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
from pyowm.owm import OWM
import pickle
from datetime import datetime
import pandas as pd

# %% {"init_cell": true}
Stanice = pickle.load(open('stanice.pickle', 'rb'))  # 159 stanic
owkey = 'your_openweathermap_apikey'
wkeys = ['clouds', 'rain', 'wind', 'humidity', 'pressure', 'temperature']
tempkeys = ['day','night','min','max','eve', 'morn']
owm = OWM(owkey)
mgr = owm.weather_manager()


# %%
def weather_record(one_dict):
    wdict = {p: one_dict[p] for p in wkeys}
    wdict['wind'] = wdict['wind']['speed']
    wdict['rain'] = list(wdict['rain'].values())[0] if wdict['rain'] else 0
    wdict['pressure'] = wdict['pressure']['press']
    temp = wdict['temperature']
    if 'temp' in temp.keys():
        wdict['temperature'] = temp['temp']
    else:
        for p in tempkeys:
            wdict['temp_' + p] = temp[p]
        wdict.pop('temperature',None)    
    return wdict


# %%
def get_current(one_call):
    one_dict = one_call.current.to_dict()
    return weather_record(one_dict)


# %%
def wlist_to_dict(wlist):
    wdict = {}
    for p in wlist:
        wdict[datetime.fromtimestamp(p.ref_time)] = weather_record(p.to_dict())
    return wdict


# %%
def get_hourly(one_call):
    wlist = one_call.forecast_hourly
    return wlist_to_dict(wlist)


# %%
def get_daily(one_call):
    wlist = one_call.forecast_daily
    return wlist_to_dict(wlist)


# %%
def weather_data(city, exclude='minutely'):
    latc, lonc = Stanice[city]
    one_call = mgr.one_call(lat=latc, lon=lonc, units='metric',exclude=exclude)
    current, hourly, daily = get_current(one_call), get_hourly(one_call), get_daily(one_call)
    hourly_DF = pd.DataFrame.from_dict(hourly, orient='index', columns=wkeys)
    daily_DF = pd.DataFrame.from_dict(daily, orient='index', 
                                      columns=wkeys[:-1] + ['temp_' + p for p in tempkeys])
    return current, hourly_DF, daily_DF
