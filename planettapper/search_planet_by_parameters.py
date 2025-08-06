import pyvo as vo
import numpy as np
from planettapper.celestialbodies import Planet, Star
import astropy.units as u

tap_service = vo.dal.TAPService("https://exoplanetarchive.ipac.caltech.edu/TAP")

def dict_to_adql_where(filters):
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


def search_planets_by_params(params, num_entries=5):

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
    params = {'pl_massj':[5,10], 'sy_dist':[1,100]}
    print(search_planets_by_params(params))
