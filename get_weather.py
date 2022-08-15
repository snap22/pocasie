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
from sqlitedict import SqliteDict
from os import environ
from time import time

# %% {"init_cell": true}
Stanice = pickle.load(open('stanice.pickle', 'rb'))  # 159 stanic
StaNames = sorted(list(Stanice.keys()))
owkey =  environ["OWM_APIKEY"]                       # key for PyCon SK 2022
wkeys = ['clouds', 'rain', 'wind', 'humidity', 'pressure', 'temperature']
nadpisy = dict(zip(wkeys,['Oblaky', 'Zrážky', 'Vietor', 'Vlhkosť', 'Tlak', 'Teplota']))
tempkeys = ['day', 'night', 'min', 'max', 'eve', 'morn']
owm = OWM(owkey)
mgr = owm.weather_manager()
db = SqliteDict("one_call.sqlite", autocommit=True, tablename='weather')


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
    wd = weather_record(one_dict)
    res = {}
    for w_val in wd.keys():
        res[nadpisy[w_val]] = wd[w_val]
    res['Čas'] = datetime.fromtimestamp(one_dict['reference_time']).strftime("%-d.%b %H:%M") 
    return res    


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
def make_one_call(city,latc, lonc, exclude='minutely'):
    one_call = mgr.one_call(lat=latc, lon=lonc, units='metric',exclude=exclude)
    ref_time = one_call.current.ref_time
    db[city] = (ref_time, one_call)    
    return one_call


def weather_data(city, exclude='minutely', autoupdate=60*60*4):
    latc, lonc = Stanice[city]
    if city in db.keys():
        ref_time, one_call = db[city]
        if (int(time()) - ref_time > autoupdate):
            one_call = make_one_call(city, latc, lonc)
    else:
        one_call = make_one_call(city, latc, lonc)
    current, hourly, daily = get_current(one_call), get_hourly(one_call), get_daily(one_call)
    current_DF = pd.DataFrame.from_dict(current, orient='index',columns=['Aktuálne počasie'])
    hourly_DF = pd.DataFrame.from_dict(hourly, orient='index', columns=wkeys)
    daily_DF = pd.DataFrame.from_dict(daily, orient='index', 
                                      columns=wkeys[:-1] + ['temp_' + p for p in tempkeys])
    return {'current': current_DF, 'hourly': hourly_DF, 'daily': daily_DF}
