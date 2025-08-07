import sys
sys.path.append("../planettapper")


import planettapper
import pandas as pd

result2 = planettapper.search_planets_by_params({'hostname':'TRAPPIST-1'})
df = result2.to_pandas()
print(df)
planets = []
for planet_name in df['pl_name']:
    planet_obj = planettapper.search_planet_by_name(planet_name)
    planets.append(planet_obj)
for p in planets:
    print(p)
