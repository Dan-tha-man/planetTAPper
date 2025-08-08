import sys
sys.path.append("../planettapper")
import planettapper
import pandas as pd

result = planettapper.search_planets_by_star('TRAPPIST-1')
print(result)
