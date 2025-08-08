import sys
sys.path.append("../planettapper")
import planettapper
import numpy as np
from astropy import units as u

result = planettapper.search_planets_by_star('TRAPPIST-1')
print(result)