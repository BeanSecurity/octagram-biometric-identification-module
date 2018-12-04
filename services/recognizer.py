from models.vector import Vector
from services.service_interfaces import IRecognizer


class Recognizer(IRecognizer):  # TODO: обращение к серверу
    def __init__(self):
        pass

    def extract(self, picture) -> Vector:
        return Vector('asrtastsrt')

    def compare_vectors(self, user_vector: Vector, extracted_vector: Vector) -> float:
        return 0.9
