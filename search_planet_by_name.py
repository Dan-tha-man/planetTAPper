import pyvo as vo
import numpy as np
from planetTAPper import Planet, Star
import astropy.units as u


tap_service = vo.dal.TAPService("https://exoplanetarchive.ipac.caltech.edu/TAP")

#Column names are planet properties:
default_columns = ['pl_name', 'pl_orbper', 'pl_radj', 'pl_massj', 
                   'pl_orbeccen', 'pl_orbsmax', 'hostname', 'st_spectype', 'st_teff', 
                   'st_rad', 'st_mass', 'st_rotp', 'sy_dist']
                    #All: https://exoplanetarchive.ipac.caltech.edu/docs/API_PS_columns.html

def search_planet_by_name(name, extras=[]):
    """Searches for planet by name

    Args:
        name: Name of the planet
        extras: Additional properties of the planet

    Returns:
        object: Returns an object from the planet class
    """
    ex_query = f"""
        SELECT TOP 1
        {', '.join(default_columns)}
        {', '.join(extras)}
        FROM pscomppars
        WHERE pl_name = '{name}'
        """
    result = tap_service.search(ex_query).to_table()
    if len(result) == 0:
        raise ValueError(f'Planet "{name}" not found in database. Try putting "-" instead of spaces?')
    df = result.to_pandas().iloc[0]

    star = Star(name=df['hostname'],
                mass=df['st_mass']*u.Msun if df['st_mass'] is not np.nan else None,
                radius=df['st_rad']*u.Rsun if df['st_rad'] is not np.nan else None,
                spectype=df['st_spectype'],
                teff=df['st_teff']*u.K if df['st_teff'] is not np.nan else None,
                period=df['st_rotp']*u.day if df['st_rotp'] is not np.nan else None,
                distance=df['sy_dist']*u.pc if df['sy_dist'] is not np.nan else None
                )

    planet = Planet(name=df['pl_name'], 
                    mass=df['pl_massj']*u.Mjup if df['pl_massj'] is not np.nan else None,
                    radius=df['pl_radj']*u.Rjup if df['pl_radj'] is not np.nan else None,
                    period=df['pl_orbper']*u.day if df['pl_orbper'] is not np.nan else None,
                    semi_major_axis=df['pl_orbsmax']*u.AU if df['pl_orbsmax'] is not np.nan else None,
                    ecc=df['pl_orbeccen'] if df['pl_orbeccen'] is not np.nan else None,
                    host=star,
                    extra=result
                    )

                
    return planet

if __name__ == "__main__":
    planet_name = "Kepler-334 b"
    kepler = search_planet_by_name(planet_name)
    print(kepler.host.distance)
    print(kepler.ecc)
