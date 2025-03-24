from dataclasses import dataclass, field
from typing import Optional

from ...constants import AXIS, SHAPEID
from ...pos import Pos
from ...id import ID


@dataclass
class BasePart:
    """Base class for all in-game parts
    """
    shapeId: str
    pos: Pos
    color: str
    joints: Optional[list[ID]] = field(kw_only=True, default=None)
    xaxis: int = field(kw_only=True, default=AXIS.DEFAULT_XAXIS)
    zaxis: int = field(kw_only=True, default=AXIS.DEFAULT_ZAXIS)

    def __post_init__(self):
        # if pos given as {"x": ..., "y": ..., "z": ...} or (x, y, z) then convert to Pos class
        if not isinstance(self.pos, Pos):
            try:
                self.pos = Pos(**self.pos)
            except TypeError:
                self.pos = Pos(self.pos[0], self.pos[1], self.pos[2])
        # if color given as (r, g, b) then convert to hex string
        if not isinstance(self.color, str):
            self.color = "%02X%02X%02X" % (
                self.color[0], self.color[1], self.color[2])
        if self.joints:
            self.joints = [ID(**id) for id in self.joints]

    def __init_subclass__(cls):
        super().__init_subclass__()
        try:
            SHAPEID.SHAPEID_TO_CLASS[cls.shapeId.default] = cls
        except AttributeError:
            pass
