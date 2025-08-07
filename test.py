import planettapper
import pandas as pd

run_search_by_name = False
run_search_by_parameters = True

# --- Input for Search By Name ---
object_name = 'Kepler-334 b' # could be star or planet


# --- Input for Search By Parameters ---
parameters = (dict)
num_entries = 10



if __name__ == '__main__':

    if run_search_by_name:
        object_with_properties = planettapper.search_planet_by_name(object_name)
        print(object_with_properties)
    if run_search_by_parameters:       
        result = planettapper.search_planets_by_params(parameters, num_entries=num_entries)

        pd.set_option('display.max_rows', None)
        df = result.to_pandas()
        print(df)
    else:
        print('nothing is running, check run_search_by_name and run_search_by_parameters!')