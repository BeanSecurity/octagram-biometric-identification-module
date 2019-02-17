class Vector():

    def __init__(self, value):
        self._value = value

    def __repr__(self):
        return "Vector('%s')" % (self._value, )

    @property
    def value(self):
        return self._value