from dataclasses import dataclass, field

from ..bases.joints.pistonjoint import PistonJoint
from ..constants import SHAPEID


@dataclass
class Piston5(PistonJoint):
    shapeId: str = field(kw_only=True, default=SHAPEID.PISTON5)
