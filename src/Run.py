import time
import uuid
from dataclasses import dataclass, field

import numpy as np


@dataclass
class Run:
    session: str
    name: str
    circ_radius: float
    circ_std: float
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    time: str = field(default_factory=lambda: time.strftime("%Y-%m-%d %H:%M"))
    coords: np.ndarray = field(default_factory=lambda: np.zeros((), dtype=np.float64))

    def __str__(self) -> str:
        return f"{self.session}," f"{self.id},{self.time},{self.name}," f"{self.circ_radius},{self.circ_std},"

    @property
    def unit_circle_coords(self) -> np.ndarray:
        return self.coords / self.circ_radius
