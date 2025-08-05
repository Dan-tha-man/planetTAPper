import pyvo as vo
import numpy as np
from planetTAPper import Planet, Star
import astropy.units as u


tap_service = vo.dal.TAPService("https://exoplanetarchive.ipac.caltech.edu/TAP")

default_columns = ['pl_name', 'pl_orbper', 'pl_radj', 'pl_massj', 
                   'pl_orbeccen', 'hostname', 'st_spectype', 'st_teff', 
                   'st_rad', 'st_mass', 'st_rotp', 'sy_dist']

def search_planet_by_name(name, extras=[]):
    
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

if __name__ == "__main__":
    planet_name = "Kepler-334 b"
    kepler = search_planet_by_name(planet_name)
    print(kepler.name)
    print(kepler.star.distance)
