from dataclasses import dataclass, field

from ..bases.joints.suspensionjoint import SuspensionJoin
from ..constants import SHAPEID


@dataclass
class SportSuspension5(SuspensionJoin):
    shapeId: str = field(kw_only=True, default=SHAPEID.SPORT_SUSPENSION5)


@dataclass
class OffRoadSuspension5(SuspensionJoin):
    shapeId: str = field(kw_only=True, default=SHAPEID.OFFROAD_SUSPENSION5)
