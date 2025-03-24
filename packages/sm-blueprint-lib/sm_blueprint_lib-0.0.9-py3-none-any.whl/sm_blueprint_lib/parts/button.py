from dataclasses import dataclass, field

from ..bases.parts.baseinteractablepart import BaseInteractablePart
from ..constants import SHAPEID, AXIS


@dataclass
class Button(BaseInteractablePart):
    shapeId: str = field(kw_only=True, default=SHAPEID.BUTTON)
