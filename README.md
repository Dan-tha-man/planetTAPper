DOI: 10.5281/zenodo.16755131

# planetTAPper:
[![A rectangular badge, half black half purple containing the text Made at Code/Astro](https://img.shields.io/badge/Made%20at-Code/Astro-blueviolet.svg)](https://semaphorep.github.io/codeastro/) ![python](https://shields.io/badge/python-3.10-blue) ![python](https://img.shields.io/badge/UC-Irvine-yellow)

The planetTAPper package can be used to search for a planet's attributes given its name.  planetTAPper relies on the the pyvo library in addition to the IVOA Table Access Protocol (TAP) and IVOA Astronomical Data Query Language.  Data is taken from the Planetary Systems Composite Data from the Nasa Exoplanet Archive

All names can be found at: [Data Column Definitions](https://exoplanetarchive.ipac.caltech.edu/docs/API_PS_columns.html)

## Requirements & Installation:
```
pip install pyvo
```
The pyvo library requires affiliate libraries be installed
```
pip install numpy astropy requests
```
or install all required packages with 
```
pip install -r requirements.txt
```

