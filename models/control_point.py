class ControlPoint():
    def __init__(self, id: str, logic_controller_id: str):
        self._id = id
        self._logic_controller_id = logic_controller_id

    @property
    def id(self) -> str:
        return self.id

    @property
    def logic_controller_id(self) -> str:
        return self._logic_controller_id
