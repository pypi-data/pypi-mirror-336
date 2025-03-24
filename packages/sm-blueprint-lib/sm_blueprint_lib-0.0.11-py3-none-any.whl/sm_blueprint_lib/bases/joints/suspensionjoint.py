from dataclasses import dataclass, field

from .basejoint import BaseJoint
from .suspensionjointcontroller import SuspensionJointController


@dataclass
class SuspensionJoin(BaseJoint):
    controller: SuspensionJointController

    def __post_init__(self):
        super().__post_init__()
        self.controller = SuspensionJointController(**self.controller)
