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
        

    def __str__(self):
        return f'{self.name}'
    
