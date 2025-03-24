from dataclasses import dataclass, field

from ..bases.parts.baselogicpart import BaseLogicPart
from ..constants import SHAPEID


@dataclass
class Switch(BaseLogicPart):
    shapeId: str = field(kw_only=True, default=SHAPEID.SWITCH)
