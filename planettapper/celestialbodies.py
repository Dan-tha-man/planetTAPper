from dataclasses import dataclass, field
from typing import Optional
import astropy.units as u
from astropy.table import Table

@dataclass
class Planet:
    """
    Represents an exoplanet and its key physical and orbital properties.

    Attributes:
        name (str): Name of the planet
        mass (Optional[u.Quantity]): Mass of the planet (with units)
        radius (Optional[u.Quantity]): Radius of the planet (with units)
        period (Optional[u.Quantity]): Orbital period (with units)
        semi_major_axis (Optional[u.Quantity]): Semi-major axis of the orbit (with units)
        ecc (Optional[float]): Orbital eccentricity
        host (Optional[Star]): Host star object
        extra (table): Additional properties as an Astropy Table
    """
    name: str
    mass: Optional[u.Quantity] = None
    radius: Optional[u.Quantity] = None
    period: Optional[u.Quantity] = None
    semi_major_axis: Optional[u.Quantity] = None
    ecc: Optional[float] = None
    host: Optional['Star'] = None

    extra: Table = field(default_factory=lambda: Table())

    def __getitem__(self, key):
        if hasattr(self, key):
            return getattr(self, key)
        elif key in self.extra.colnames:
            return self.extra[key][0]
        else:
            raise KeyError(f"{key} not found in Planet attributes or extras.")
    
    def __setitem__(self, key, value):
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            self.extra[key] = value
        
    def __post_init__(self):
        if self.mass is not None and not self.mass.unit.is_equivalent(u.kg):
            raise u.UnitsError(f'Mass must have units of mass, got {self.mass.unit}')
        if self.radius is not None and not self.radius.unit.is_equivalent(u.m):
            raise u.UnitsError(f'Radius must have units of length, got {self.radius.unit}')
        if self.period is not None and not self.period.unit.is_equivalent(u.s):
            raise u.UnitsError(f'Period must have units of time, got {self.period.unit}')
        if self.semi_major_axis is not None and not self.semi_major_axis.unit.is_equivalent(u.m):
            raise u.UnitsError(f'Semi-major axis must have units of distance, got {self.semi_major_axis.unit}')
        if self.ecc is not None and not type(self.ecc) == float and not 0 <= self.ecc < 1:
            raise ValueError(f'Eccentricity must be float between 0 and 1, got {self.ecc}')


    def __str__(self):
        # Planet main attributes
        planet_attrs = [
            f"Name: {self.name}",
            f"Mass: {self.mass}" if self.mass is not None else "Mass: N/A",
            f"Radius: {self.radius}" if self.radius is not None else "Radius: N/A",
            f"Period: {self.period}" if self.period is not None else "Period: N/A",
            f"Semi-major axis: {self.semi_major_axis}" if self.semi_major_axis is not None else "Semi-major axis: N/A",
            f"Eccentricity: {self.ecc}" if self.ecc is not None else "Eccentricity: N/A",
        ]
        # Host star info
        star_attrs = [
            f"Name: {self.host.name}",
            f"Mass: {self.host.mass}" if self.host.mass is not None else "Mass: N/A",
            f"Radius: {self.host.radius}" if self.host.radius is not None else "Radius: N/A",
            f"Spectral Type: {self.host.spectype}" if self.host.spectype is not None else "Spectral Type: N/A",
            f"Teff: {self.host.teff}" if self.host.teff is not None else "Teff: N/A",
            f"Period: {self.host.period}" if self.host.period is not None else "Period: N/A",
            f"Distance: {self.host.distance}" if self.host.distance is not None else "Distance: N/A",
        ]
        star_section = "Star:\n  " + "\n  ".join(star_attrs)
        # Extra data
        return (
            "Planet:\n  " + "\n  ".join(planet_attrs) + "\n" +
            star_section + "\n"
        )


@dataclass
class Star:
    """
    Represents a star and its key physical properties.

    Attributes:
        name (str): Name of the star
        mass (Optional[u.Quantity]): Mass of the star (with units)
        radius (Optional[u.Quantity]): Radius of the star (with units)
        spectype (Optional[str]): Spectral type of the star
        teff (Optional[u.Quantity]): Effective temperature (with units)
        period (Optional[u.Quantity]): Rotation period (with units)
        distance (Optional[u.Quantity]): Distance to the star from earth (with units)
    """
    name: str
    mass: Optional[u.Quantity] = None
    radius: Optional[u.Quantity] = None
    spectype: Optional[str] = None
    teff: Optional[u.Quantity] = None
    period: Optional[u.Quantity] = None
    distance: Optional[u.Quantity] = None

    def __getitem__(self, key):
        return getattr(self, key, self.extra.get(key))
    
    def __setitem__(self, key, value):
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            self.extra[key] = value

