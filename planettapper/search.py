import pyvo as vo
from .celestialbodies import Planet, Star
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
    if not isinstance(name, str):
        raise ValueError('Planet name must be a string')
    if len(result) == 0:
        raise ValueError(f'Planet "{name}" not found in database. Try putting "-" instead of spaces?')
    df = result.to_pandas().iloc[0]

    extra_df = result.to_pandas()
    for col in extra_df.columns:
        if col not in extras:
            extra_df.pop(col)


    star = Star(name=df['hostname'],
                mass=df['st_mass']*u.Msun if not pd.isna(df['st_mass']) and (df['st_mass'] not in [' ', '']) else None,
                radius=df['st_rad']*u.Rsun if not pd.isna(df['st_rad']) and (df['st_rad'] not in [' ', '']) else None,
                spectype=df['st_spectype'] if not pd.isna(df['st_spectype']) and (df['st_spectype'] not in [' ', '']) else None,
                teff=df['st_teff']*u.K if not pd.isna(df['st_teff']) and (df['st_teff'] not in [' ', '']) else None,
                period=df['st_rotp']*u.day if not pd.isna(df['st_rotp']) and (df['st_rotp'] not in [' ', '']) else None,
                distance=df['sy_dist']*u.pc if not pd.isna(df['sy_dist']) and (df['sy_dist'] not in [' ', '']) else None
                )

    planet = Planet(name=df['pl_name'], 
                    mass=df['pl_massj']*u.Mjup if not pd.isna(df['pl_massj']) and (df['pl_massj'] not in [' ', '']) else df['pl_bmassj']*u.Mjup,
                    radius=df['pl_radj']*u.Rjup if not pd.isna(df['pl_radj']) and (df['pl_radj'] not in [' ', '']) else None,
                    period=df['pl_orbper']*u.day if not pd.isna(df['pl_orbper']) and (df['pl_orbper'] not in [' ', '']) else None,
                    semi_major_axis=df['pl_orbsmax']*u.AU if not pd.isna(df['pl_orbsmax']) and (df['pl_orbper'] not in [' ', '']) else None,
                    ecc=df['pl_orbeccen'] if not pd.isna(df['pl_orbeccen']) and (df['pl_orbeccen'] not in [' ', '']) else None,
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
        if isinstance(value, list):
            if len(value) == 0:
                pass
            elif all(isinstance(v, str) for v in value):
                value_list = ", ".join(f"'{v}'" for v in value)
                clauses.append(f"{key} IN ({value_list})")

            elif len(value) == 2 and all(isinstance(v, (int, float)) for v in value):
                low, high = value
                clauses.append(f"{key} BETWEEN {low} AND {high}")
            
        elif isinstance(value, (int, float)):
            clauses.append(f"{key} = {value}")
        elif isinstance(value, str):
            clauses.append(f"{key} = '{value}'")
        else:
            raise ValueError(f"Unsupported value type for key '{key}': {value}")
    
    if len(clauses) == 0:
        return
    else:
        return "WHERE " + " AND ".join(clauses)


def search_planets_by_params(params:dict, sort_by='pl_massj', num_entries:int=5):
    """Searches for planets by parameters and returns a table of planets that fit the constraints of the chosen params

    Args:
        params (dict): the parameters used to filter to the search, and the desired value range
        num_entries (int): the amount of planets displayed that fit the parameter constraints

    Returns:
        result (table): a table with a specifed number of entrires that fit the constraints of the specified parameters
    """

    query_params = {'pl_name': [], 'pl_massj': [], 'pl_radj': []}

    query_params.update(params)

    ex_query = f"""
        SELECT TOP {num_entries}
        {', '.join(query_params.keys())}
        FROM pscomppars
        {dict_to_adql_where(query_params)}
        ORDER BY {sort_by}
        """

    result = tap_service.search(ex_query)

    return result.to_table()

