import sys
sys.path.append("../planettapper")
from planettapper.search import planets_from_table, search_planets_by_star, search_planets_by_params


table = search_planets_by_star('TRAPPIST-1')
print(table)

planets = planets_from_table(table)

print(planets)

for planet in planets:
    print(planet)

table = search_planets_by_params({'hostname': [], 'discoverymethod': [], 'sy_dist': [5,500]})

print(table)

planets = planets_from_table(table)

for planet in planets:
    print(planet)

