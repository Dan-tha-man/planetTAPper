import pyvo as vo
import numpy as np
from celestialbodies import Planet, Star
import astropy.units as u
import pandas as pd


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
    if len(extras) > 0:
        ex_query = f"""
            SELECT TOP 1
            {', '.join(default_columns)}, {', '.join(extras)}
            FROM pscomppars
            WHERE pl_name = '{name}'
            """
    else:
        ex_query = f"""
            SELECT TOP 1
            {', '.join(default_columns)}
            FROM pscomppars
            WHERE pl_name = '{name}'
            """
    
    result = tap_service.search(ex_query).to_table()
    if len(result) == 0:
        raise ValueError(f'Planet "{name}" not found in database. Try putting "-" instead of spaces?')
    df = result.to_pandas().iloc[0]

    extra_df = result.to_pandas()
    for col in extra_df.columns:
        if col not in extras:
            extra_df.pop(col)


    star = Star(name=df['hostname'],
                mass=df['st_mass']*u.Msun if not pd.isna(df['st_mass']) else None,
                radius=df['st_rad']*u.Rsun if not pd.isna(df['st_rad']) else None,
                spectype=df['st_spectype'],
                teff=df['st_teff']*u.K if not pd.isna(df['st_teff']) else None,
                period=df['st_rotp']*u.day if not pd.isna(df['st_rotp']) else None,
                distance=df['sy_dist']*u.pc if not pd.isna(df['sy_dist']) else None
                )

    planet = Planet(name=df['pl_name'], 
                    mass=df['pl_massj']*u.Mjup if not pd.isna(df['pl_massj']) else None,
                    radius=df['pl_radj']*u.Rjup if not pd.isna(df['pl_radj']) else None,
                    period=df['pl_orbper']*u.day if not pd.isna(df['pl_orbper']) else None,
                    semi_major_axis=df['pl_orbsmax']*u.AU if not pd.isna(df['pl_orbsmax']) else None,
                    ecc=df['pl_orbeccen'] if not pd.isna(df['pl_orbeccen']) else None,
                    host=star,
                    extra=extra_df.iloc[0]
                    )
    return planet

if __name__ == "__main__":
    planet_name = "Kepler-334 b"
    extras = ['ra', 'dec']
    kepler = search_planet_by_name(planet_name, extras)
    print(kepler)
