import pyvo as vo
import numpy as np
import pandas as pd

tap_service = vo.dal.TAPService("https://exoplanetarchive.ipac.caltech.edu/TAP")

# --- Inputs ---
num_of_entries = 5
column_names = "pl_name, discoverymethod, pl_orbper, sy_dist" # see possible column names: https://exoplanetarchive.ipac.caltech.edu/docs/API_PS_columns.html 
table_name = "pscomppars" # for our project we don't change this
condition = "sy_dist BETWEEN 10 AND 500 AND discoverymethod = 'Transit'"
order_name = "sy_dist"

# --- Options for Query ---
# SELECT "insert number of entries"
# FROM "insert table name"
# WHERE "insert condition"
# ORDER "insert column name to order by"

ex_query = f"""
    SELECT TOP {num_of_entries}
    {column_names} 
    FROM {table_name} 
    WHERE {condition}
    ORDER BY {order_name}
    """

result = tap_service.search(ex_query)

# --- Print Results of Query ---
tabled_result = result.to_table()

df = tabled_result.to_pandas()
print(df)
