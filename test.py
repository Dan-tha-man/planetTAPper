import pyvo as vo
import numpy as np
import pandas
from planetTAPper import Planet

tap_service = vo.dal.TAPService("https://exoplanetarchive.ipac.caltech.edu/TAP")

def search(name):
    
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