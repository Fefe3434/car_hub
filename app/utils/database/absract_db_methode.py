"""
Fichier de Modules des Fonctions Abstraite
"""

from abc import ABC, abstractmethod


PROTOCOL_MQTT = 1
PROTOCOL_HTTP = 2


class DbConnection(ABC):
    """
    Methode Abstraite Connexion BDD
    """

    def __init__(self):
        self.connection = None
        self.cursor = None

    @abstractmethod
    def connect(self):
        """ Methode de Connexion """
        pass

    @abstractmethod
    def get_session(self):
        """Methode Execution"""
        pass

    @abstractmethod
    def execute(self, query):
        """Methode Execution"""
        pass

    @abstractmethod
    def close(self):
        """Close Connexion """
        pass



class DbRouteConnection(ABC):
    def __init__(self,topic):
        self.topic = topic
        self.bdd = {
        }
        self.bdd_name ={
        }
    @abstractmethod
    def get_db_connexion(self):
        return (self.bdd[self.topic],self.bdd_name[self.topic])
    @abstractmethod
    def get_db_name(self):
        return self.bdd_name[self.topic]
    @abstractmethod
    def get_db_route_error(self):
        raise NameError("Base de Données Non Accessible")
