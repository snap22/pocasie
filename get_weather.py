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
    wdict['pressure'] = wdict['pressure']['press']
    temp = wdict['temperature']
    wdict['temperature'] = temp.get('temp',{p: temp[p] for p in tempkeys})
    return wdict


# %%
def get_current(one_call):
    one_dict = one_call.current.to_dict()
    return weather_record(one_dict)


# %%
def wlist_to_dict(wlist):
    wdict = {}
    for p in wlist:
        wdict[p.ref_time] = weather_record(p.to_dict())
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
what_func = {'current': get_current, '48h': get_hourly, '8d': get_daily}


# %%
def weather_data(city,what='48h',exclude='minutely'):
    latc, lonc = Stanice[city]
    one_call = mgr.one_call(lat=latc, lon=lonc, units='metric',exclude=exclude)
    return what_func[what](one_call)

# %%
# martin_curr = weather_data('Martin',what='current')
# martin_hourly = weather_data('Martin',what='48h')
# martin_daily = weather_data('Martin',what='8d')
