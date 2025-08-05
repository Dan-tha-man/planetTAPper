import pyvo as vo
import numpy as np
from planetTAPper import Planet
import astropy.units as u


tap_service = vo.dal.TAPService("https://exoplanetarchive.ipac.caltech.edu/TAP")

default_columns = ['pl_name', 'pl_orbper', 'pl_radj', 'pl_massj', 
                   'pl_orbeccen', 'hostname', 'st_spectype', 'st_teff', 
                   'st_rad', 'st_mass', 'st_rotp', 'sy_dist']

def search(name, extras=[]):
    
    ex_query = f"""
        SELECT TOP 1
        {', '.join(default_columns)}
        {', '.join(extras)}
        FROM pscomppars
        WHERE pl_name = '{name}'
        """
    result = tap_service.search(ex_query).to_table()
    planet = Planet(name=result['pl_name'][0], 
                    period=result['pl_orbper'][0]*u.day,
                    radius=result['pl_radj'][0]*u.Rjup,
                    mass=result['pl_massj'][0]*u.Mjup,
                    ecc=result['pl_orbeccen'][0],
                    )

                
    return planet

print(search("Kepler-334 b"))

""" # --- Inputs ---
num_of_entries = 5
table_name = "pscomppars"
condition = "sy_dist BETWEEN 500 AND 10000"
order_name = "sy_dist"

# --- Options for Query ---
# SELECT "insert number of entries"
# FROM "insert table name"
# WHERE "insert condition"
# ORDER "insert column name to order by"

ex_query = f
    SELECT TOP {num_of_entries}
    pl_name, discoverymethod, pl_orbper, sy_dist
    FROM {table_name} 
    WHERE {condition}
    ORDER BY {order_name}
    

result = tap_service.search(ex_query)

# --- Print Results of Query ---
print(result.to_table().colnames)
print(result.to_table())
print(np.array(result).shape)
"""