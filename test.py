import pyvo as vo
import numpy as np

tap_service = vo.dal.TAPService("https://exoplanetarchive.ipac.caltech.edu/TAP")

ex_query = """
    SELECT top 1
    *
    FROM pscomppars 
    """
result = tap_service.search(ex_query)

print(result.to_table().colnames)
print(result.to_table())
print(np.array(result).shape)