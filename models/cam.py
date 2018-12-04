from models.control_point import ControlPoint


class Camera():
    def __init__(self, id: str, control_point: ControlPoint):
        self._id = id
        self._control_point = control_point

    @property
    def id(self) -> str:
        return self.id

    @property
    def control_point(self) -> ControlPoint:
        return self._control_point
