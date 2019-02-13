from models.vector import Vector


class User():

    def __init__(self, key_id: str, full_name: str, face_vector: Vector):  # TODO: выбрать: вектор как строка или как сущность
        self._key_id = key_id
        self._face_vector = face_vector
        self._full_name = full_name

    def __repr__(self):
        return "<User('%s','%s','%s')>" % (self._key_id, self._full_name, self._face_vector)

    @property
    def key_id(self) -> str:
        return self._key_id

    @property
    def face_vector(self) -> Vector:
        return self._face_vector

    @property
    def full_name(self) -> str:
        return self._full_name

