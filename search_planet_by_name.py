import pyvo as vo
import numpy as np
import pandas
from planetTAPper import Planet, Star

tap_service = vo.dal.TAPService("https://exoplanetarchive.ipac.caltech.edu/TAP")

def search_planet_by_name(name):
    ex_query = f"""
        SELECT TOP 1
        pl_name,pl_orbper,pl_radj,pl_massj,pl_orbeccen, hostname,st_spectype,st_teff,st_rad,st_mass,st_rotp,sy_dist
        FROM pscomppars
        WHERE pl_name = '{name}'
        """
    result = tap_service.search(ex_query)
    planet = Planet()
    planet.star = Star()
    columns = result.to_table().colnames
    print(result)
    for column in columns:
        match column:
            case 'pl_name':
                planet.name = result.to_table()['pl_name'][0]
            case 'pl_orbper':
                planet.period = result.to_table()['pl_orbper'][0]
            case 'pl_radj':
                planet.radius = result.to_table()['pl_radj'][0]
            case 'pl_massj':
                planet.mass = result.to_table()['pl_massj'][0]
            case 'pl_orbeccen':
                planet.ecc = result.to_table()['pl_orbeccen'][0]
            case 'hostname':
                planet.star.name = result.to_table()['hostname'][0]
            case 'st_spectype':
                planet.star.type = result.to_table()['st_spectype'][0]
            case 'st_teff':
                planet.star.temp = result.to_table()['st_teff'][0]
            case 'st_rad':
                planet.star.radius = result.to_table()['st_rad'][0]
            case 'st_mass':
                planet.star.mass = result.to_table()['st_mass'][0]
            case 'st_rotp':
                planet.star.period = result.to_table()['st_rotp'][0]
            case 'sy_dist':
                planet.star.distance = result.to_table()['sy_dist'][0]
    return planet
if __name__ == "__main__":
    planet_name = "Kepler-334 b"
    kepler = search_planet_by_name(planet_name)
    print(kepler.name)
    print(kepler.star.distance)
