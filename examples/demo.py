import sys
sys.path.append("../planettapper")

import planettapper
import pandas as pd
import matplotlib.pyplot as plt

run_search_by_name = False
run_search_by_parameters = True
enable_plot = False

# --- Input for Search By Name ---
object_name = 'Kepler-334 b' # could be star or planet
# SWEEPS-11 b (Hank's choice)
# J1470B (Kai's Choice)


# --- Input for Search By Parameters ---
parameters = dict()
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
        if enable_plot:
            mass = [mass for mass in result['pl_massj']]
            rad = [radius for radius in result['pl_radj']]
            names = [names for names in result['pl_name']]
            fig, ax = plt.subplots(1,1)
            ax.scatter(mass, rad)
            for i, name in enumerate(names):
                ax.annotate(name, (mass[i], rad[i]))
            ax.set_xlabel('Jupiter Mass')
            ax.set_ylabel('Jupiter Radius')
            ax.set_title('Planets')
            plt.show()
    else:
        print('nothing is running, check run_search_by_name and run_search_by_parameters!')
