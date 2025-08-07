import sys
sys.path.append("../planettapper")


import planettapper
import numpy as np
from astropy import units as u

result2 = planettapper.search_planets_by_params({'hostname':'TRAPPIST-1'})
df = result2.to_pandas()
print(df)
planets = []
for planet_name in df['pl_name']:
    planet_obj = planettapper.search_planet_by_name(planet_name)
    planets.append(planet_obj)
for p in planets:
    print(p)
    a_Rs = (p.semi_major_axis.to(u.m)) / (p.radius.to(u.m))
    b = np.random.uniform(0, 1)
    inc_deg = np.degrees(np.arccos((b / a_Rs)))
    print(inc_deg)
