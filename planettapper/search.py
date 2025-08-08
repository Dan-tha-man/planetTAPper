import pyvo as vo
from planettapper.celestialbodies import Planet, Star
import astropy.units as u
import pandas as pd
from astropy.table import QTable

tap_service = vo.dal.TAPService("https://exoplanetarchive.ipac.caltech.edu/TAP")
#Column names are planet properties:

default_planet_columns = ['pl_name', 'pl_orbper', 'pl_radj', 'pl_massj', 
                'pl_orbeccen', 'pl_orbsmax']

default_star_columns = ['hostname', 'st_spectype', 'st_teff', 
                'st_rad', 'st_mass', 'st_rotp', 'sy_dist']

default_columns = default_planet_columns + default_star_columns

pscomppars_to_planettapper = {'pl_name': ['name', None], 'pl_massj': ['mass', u.Mjup], 
                              'pl_orbper': ['period', u.day], 'pl_radj': ['radius', u.Rjup], 'pl_orbeccen': ['ecc', None], 
                              'pl_orbsmax': ['semi_major_axis', u.AU], 'hostname': ['name', None], 'st_spectype': ['spectype', None],
                              'st_teff': ['teff', u.K], 'st_rad': ['radius', u.Rsun], 'st_mass': ['mass', u.Msun], 'st_rotp': ['period', u.day],
                              'sy_dist': ['distance', u.pc]}
                    #All: https://exoplanetarchive.ipac.caltech.edu/docs/API_PS_columns.html


def search_planets_by_star(star_name: str, extras:list=['pl_bmassj'], num_entries=10):
    """Searches for a star by name and returns a table of the corresponding planets

    Args:
        star_name (str): name of the star
        extras (list): List of additional parameter strings to be included in the search
    
    Returns:
        result (table): a table with all planets up to specifed number of entrires
    """

    if not isinstance(star_name, str):
        raise ValueError('Planet name must be a string')

    if len(extras) > 0:
        ex_query = f"""
            SELECT TOP {num_entries}
            {', '.join(default_columns)}, {', '.join(extras)}
            FROM pscomppars
            WHERE hostname = '{star_name}'
            """
    else:
        ex_query = f"""
            SELECT TOP {num_entries}
            {', '.join(default_columns)}
            FROM pscomppars
            WHERE hostname = '{star_name}'
            """

    try:
        result = tap_service.search(ex_query).to_table()
    except vo.dal.exceptions.DALQueryError as error:
        raise ValueError(f"ERROR {error.reason[11:]} column. Refer to https://exoplanetarchive.ipac.caltech.edu/docs/API_PS_columns.html for list of valid columns")

    return result


def search_planet_by_name(name:str, extras:list=[]) -> Planet:
    """Searches for planet by name and returns the corresponding planet object

    Args:
        name (str): Name of the planet
        extras (list): List of additional parameter strings to be included in the planet object

    Returns:
        planet (Planet): a planet object containing relevant planetary parameters, a host star object with it's relevant stellar parameters, and any extra parameters specified
    """
    
    if not isinstance(name, str):
        raise ValueError('Planet name must be a string')
    
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


def planets_from_table(table):

    # TODO Incorporate the extras in the planet objects
    # TODO Set values to nan if it's not a number

    for col in table.keys():
        if col in pscomppars_to_planettapper.keys():
            table[col].unit = pscomppars_to_planettapper[col][1]

    extras = [col for col in table.keys() if col not in default_columns]

    star_params = [col for col in default_star_columns if col in table.keys()]
    planet_params = [col for col in default_planet_columns if col in table.keys()]
    
    star_table = table[star_params].copy()
    planet_table = table[planet_params].copy()    

    for old,[new, units] in pscomppars_to_planettapper.items():
        if old in star_table.keys():
            star_table.unit = units
            star_table.rename_column(old,new)
        if old in planet_table.keys():
            planet_table.unit = units
            planet_table.rename_column(old,new)
    
    star_table = QTable(star_table)
    planet_table = QTable(planet_table)

    star_list = [dict(row) for row in star_table]
    planet_list = [dict(row) for row in planet_table]

    stars = [Star(**kwargs) for kwargs in star_list]
    for planet, star in zip(planet_list, stars):
        planet['host'] = star

    return [Planet(**kwargs) for kwargs in planet_list]
        


            

