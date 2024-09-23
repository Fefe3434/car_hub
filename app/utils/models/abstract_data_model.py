
class DataModel:
    def __init__(self, **kwargs):
        for field, value in kwargs.items():
            setattr(self, field, value)

class DataPrototype(dict):
    def __init__(self):
        for field, value in self.__dict__.items():
            self[field] = value
