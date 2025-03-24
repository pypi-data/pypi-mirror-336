from dataclasses import dataclass, field

from ..bases.joints.basejoint import BaseJoint
from ..constants import SHAPEID


@dataclass
class Bearing(BaseJoint):
    shapeId: str = field(kw_only=True, default=SHAPEID.BEARING)
