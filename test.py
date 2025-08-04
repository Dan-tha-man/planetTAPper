import pyvo as vo
import numpy as np

tap_service = vo.dal.TAPService("https://exoplanetarchive.ipac.caltech.edu/TAP")

ex_query = """
    SELECT TOP 5
    pl_name, discoverymethod, pl_orbper,sy_dist
    FROM pscomppars 
    """
result = tap_service.search(ex_query)

print(result.to_table().colnames)
print(np.array(result).shape)
print(result)