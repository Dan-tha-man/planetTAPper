import pyvo as vo
import numpy as np
import pandas
from planetTAPper import Planet

tap_service = vo.dal.TAPService("https://exoplanetarchive.ipac.caltech.edu/TAP")

def search_planet_by_name(name):
    
    ex_query = f"""
        SELECT TOP 1
        pl_name,pl_orbper,pl_radj,pl_massj,pl_orbeccen, hostname,st_spectype,st_teff,st_rad,st_mass,st_rotp,sy_dist
        FROM pscomppars
        WHERE pl_name = '{name}'
        """
    result = tap_service.search(ex_query)
    planet = Planet()
    columns = result.to_table().colnames
    print(result)
    for column in columns:
        match column:
            case 'pl_name':
                planet.name = result.to_table()['pl_name'][0] 
            case 'pl_orbper':
                planet.period = result.to_table()['pl_orbper'][0]
                

search("Kepler-334 b")

# --- Inputs ---
num_of_entries = 5
column_names = "pl_name discoverymethod pl_orbper sy_dist"
table_name = "pscomppars" # for our project we don't change this
condition = "sy_dist BETWEEN 10 AND 500"
order_name = "sy_dist"

# --- Options for Query ---
# SELECT "insert number of entries"
# FROM "insert table name"
# WHERE "insert condition"
# ORDER "insert column name to order by"

ex_query = f"""
    SELECT TOP {num_of_entries}
    {column_names}
    FROM {table_name} 
    WHERE {condition}
    ORDER BY {order_name}
    """

result = tap_service.search(ex_query)

# --- Print Results of Query ---
print(result.to_table().colnames)
print(result.to_table())
print(np.array(result).shape)
