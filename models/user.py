from models.vector import Vector


class User():

    def __init__(self, key_id: str, face_vector: Vector):  # TODO: выбрать: вектор как строка или как сущность
        self._key_id = key_id
        self._face_vector = face_vector

    def __repr__(self):
        return "<User('%s','%s')>" % (self._key_id, self._face_vector)

    @property
    def key_id(self) -> str:
        return self._key_id

    @property
    def face_vector(self) -> Vector:
        return self._face_vector
