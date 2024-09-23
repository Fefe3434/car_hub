
from abc import ABC, abstractmethod
import json


class AbstractRequestDecomposeStrategy(ABC):
    @abstractmethod
    def __init__(self, model_strategy, prototype):
        self.model_strategy = model_strategy
        self.prototype = prototype

    @abstractmethod
    def decompose(self, request_body: json):
        data = json.loads(request_body)

        model_data = {}
        for properties in self.prototype.__dict__.keys():
            key = properties
            value = None
            if properties in data.keys():
                value = data[properties]
            model_data[key] = value

        data_model_instance = self.model_strategy(**model_data)
        return data_model_instance


class AbstractResponseComposeStrategy(ABC):
    @abstractmethod
    def __init__(self, model_strategy):
        self.model_strategy = model_strategy

    @abstractmethod
    def compose(self, data):
        model_data = {}
        try:
            if isinstance(data, list):
                model_data = [self._compose_single_item(item) for item in data]
            else:
                model_data = self._compose_single_item(data)
            return model_data
        except Exception as e:
            print(f"Exception occurred: {e}")
            return model_data

    def _compose_single_item(self, item):
        model_data = {}
        for attr_name, attr_value in item.__dict__.items():
            if attr_name in dir(self.model_strategy):  # .__dict__.keys():
                if (not (isinstance(attr_value, int) or isinstance(attr_value, float)
                         or isinstance(attr_value, bytearray))):
                    attr_value = str(attr_value)  # value.strftime('%H-%M-%S')
                if isinstance(attr_value, bytearray):
                    attr_value = attr_value.decode('utf8')
                model_data[attr_name] = attr_value
        return model_data
