from dataclasses import dataclass, field
from typing import Optional, Dict, Any
import astropy.units as u

@dataclass
class Planet:
    name: str
    mass: Optional[u.Quantity] = None
    radius: Optional[u.Quantity] = None
    period: Optional[u.Quantity] = None
    semi_major_axis: Optional[u.Quantity] = None
    ecc: Optional[float] = None
    host_star: Optional[str] = None

    extra: Dict[str, Any] = field(default_factory=dict)

    def __getitem__(self, key):
        return getattr(self, key, self.extra.get(key))
    
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
        if self.ecc is not None and not type(self.ecc) == float and 0 < self.ecc < 1:
            raise ValueError(f'Eccentricity must be float between 0 and 1, got {self.ecc}')


    def __str__(self):
        return f'{self.name}'




