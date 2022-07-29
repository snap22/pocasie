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

# %% [markdown]
# ### Len na vytvorenie `stanice.pickle`

# %%
from pyowm.owm import OWM
import pandas as pd
import pickle
owm = OWM('a2a830c463a6745b0c8317cd01fed10d')
mgr = owm.geocoding_manager()

# %%
sk_stan = pd.read_csv('stations_sk_dia.csv')
mena = sk_stan['meno'].values

# %%
Stan_dict = {}
for miesto in mena:
    locations = mgr.geocode(miesto,country='SK')
    if locations:
        loc = locations[0]
        Stan_dict[loc.name] = (loc.lat, loc.lon)

# %%
pickle.dump(Stan_dict,open('stanice.pickle','wb'))

# %%
# sd = pickle.load(open('stanice.pickle','rb'))
