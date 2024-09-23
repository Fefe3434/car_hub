class DecodeRequete:
    def __init__(self, requete, list_key=[]) -> None:
        self.requete = requete
        self.list_key = list_key

    @property
    def decode_requete(self):
        temp = {}
        for key in self.requete.__dict__:
            if not key.startswith('_') and key != 'metadata' and key not in self.list_key:
                value = self.requete.__getattribute__(key)
                # print(type(value))
                if (not (isinstance(value, int) or isinstance(value, float) or isinstance(value, bytearray))):
                    value = str(value)
                if isinstance(value, bytearray):
                    value = value.decode('utf8')
                temp[key] = value
        return temp
