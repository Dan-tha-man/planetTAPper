import pyvo as vo
from planettapper.celestialbodies import Planet, Star
import astropy.units as u
import pandas as pd


tap_service = vo.dal.TAPService("https://exoplanetarchive.ipac.caltech.edu/TAP")

#Column names are planet properties:
default_columns = ['pl_name', 'pl_bmassj', 'pl_orbper', 'pl_radj', 'pl_massj', 
                   'pl_orbeccen', 'pl_orbsmax', 'hostname', 'st_spectype', 'st_teff', 
                   'st_rad', 'st_mass', 'st_rotp', 'sy_dist']
                    #All: https://exoplanetarchive.ipac.caltech.edu/docs/API_PS_columns.html

def search_planet_by_name(name:str, extras:list=[]) -> Planet:
    """Searches for planet by name and returns the corresponding planet object

    Args:
        name (str): Name of the planet
        extras (list): List of additional parameter strings to be included in the planet object

    Returns:
        planet (Planet): a planet object containing relevant planetary parameters, a host star object with it's relevant stellar parameters, and any extra parameters specified
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
    
    try:
        result = tap_service.search(ex_query).to_table()
    except vo.dal.exceptions.DALQueryError as error:
        raise ValueError(f"ERROR {error.reason[11:]} column. Refer to https://exoplanetarchive.ipac.caltech.edu/docs/API_PS_columns.html for list of valid columns")
    
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
                    mass=df['pl_massj']*u.Mjup if not pd.isna(df['pl_massj']) else df['pl_bmassj']*u.Mjup,
                    radius=df['pl_radj']*u.Rjup if not pd.isna(df['pl_radj']) else None,
                    period=df['pl_orbper']*u.day if not pd.isna(df['pl_orbper']) else None,
                    semi_major_axis=df['pl_orbsmax']*u.AU if not pd.isna(df['pl_orbsmax']) else None,
                    ecc=df['pl_orbeccen'] if not pd.isna(df['pl_orbeccen']) else None,
                    host=star,
                    extra=extra_df.iloc[0]
                    )
    return planet

def dict_to_adql_where(filters: dict):
    '''Takes a dictionary of {key: value} pairs of {column names: restrictions} and returns a formatted where clause for ADQL
    
    Args:
        filters (dict): key/value pairs of column names and ranges or exact matches for those columns

    Returns:
        str: ADQL formatted WHERE clause
    
    '''
    clauses = []

    for key, value in filters.items():
        if isinstance(value, list) and len(value) == 2:
            low, high = value
            clauses.append(f"{key} BETWEEN {low} AND {high}")
        elif isinstance(value, (int, float)):
            clauses.append(f"{key} = {value}")
        elif isinstance(value, str):
            clauses.append(f"{key} = '{value}'")
        else:
            raise ValueError(f"Unsupported value type for key '{key}': {value}")
    
    return " AND ".join(clauses)


def search_planets_by_params(params:list, num_entries:int=5):
    """Searches for planets by parameters and returns a table of planets that fit the constraints of the chosen params

    Args:
        params (list): the parameters used to filter to the search
        num_entries (int): the amount of planets displayed that fit the parameter constraints

    Returns:
        result (table): a table with a specifed number of entrires that fit the constraints of the specified parameters
    """

    ex_query = f'''
        SELECT TOP {num_entries}
        pl_name, {', '.join(params.keys())}
        FROM pscomppars
        WHERE {dict_to_adql_where(params)}
        ORDER BY {list(params.keys())[0]}
        '''

    result = tap_service.search(ex_query)

    return result.to_table()


if __name__ == '__main__':
    kepler = search_planet_by_name('Kepler-334 b')
    print(kepler)
