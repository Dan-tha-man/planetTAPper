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
    df = result.to_pandas().iloc[0]
    planet = Planet(name=df['pl_name'], 
                    period=df['pl_orbper']*u.day if df['pl_orbper'] is not np.nan else None,
                    radius=df['pl_radj']*u.Rjup if df['pl_radj'] is not np.nan else None,
                    mass=df['pl_massj']*u.Mjup if df['pl_massj'] is not np.nan else None,
                    ecc=df['pl_orbeccen'] if df['pl_orbeccen'] is not np.nan else None,
                    extra=result
                    )

                
    return planet

if __name__ == "__main__":
    planet_name = "Kepler-334 b"
    kepler = search_planet_by_name(planet_name)
    print(kepler.name)
    print(kepler.extra)
