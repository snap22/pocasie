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

# %% {"init_cell": true}
Stanice = pickle.load(open('stanice.pickle', 'rb'))  # 159 stanic
owkey = 'your_openweathermap_apikey'
wkeys = ('clouds', 'rain', 'wind', 'humidity', 'pressure', 'temperature')
tempkeys = ('day','night','min','max')
owm = OWM(owkey)
mgr = owm.weather_manager()


# %%
def weather_record(one_dict):
    wdict = {p: one_dict[p] for p in wkeys}
    wdict['wind'] = wdict['wind']['speed']
    wdict['rain'] = list(wdict['rain'].values())[0] if wdict['rain'] else 0
    wdict['pressure'] = wdict['pressure']['press']
    temp = wdict['temperature']
    wdict['temperature'] = temp['temp'] if 'temp' in temp.keys() else {p: temp[p] for p in tempkeys}
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
def weather_data(city,exclude='minutely'):
    latc, lonc = Stanice[city]
    one_call = mgr.one_call(lat=latc, lon=lonc, units='metric',exclude=exclude)
    return get_current(one_call), get_hourly(one_call), get_daily(one_call)

# %%
# martin_current, martin_hourly, martin_daily = weather_data('Martin')
