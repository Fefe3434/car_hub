from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
import app.utils.database.absract_db_methode as DbConnexionAbstractMethode
import os

load_dotenv()

meta = MetaData()
Base = declarative_base()

ECHO_CONNEXION = False


class SessionObject:
    def __init__(self, objet_to_copy) -> None:
        try:
            self.session = getattr(objet_to_copy, 'session')
            self.bdd = getattr(objet_to_copy, 'bdd')
            self.engine = getattr(objet_to_copy, 'engine')

        except Exception as e:
            print(e.args)

    def get_session_object(self):
        return self


class DbConnexion(DbConnexionAbstractMethode.DbConnection):
    """ Connexion base de Données """
    __instance = None
    __session = None

    __instanceDict = {}
    # Singleton: Permet d'avoir une  connection

    @staticmethod
    def get_instance(service):
        """ Static access method. """
        return DbConnexion.__instanceDict[service]

    def __init__(self, bdd=os.getenv("MYSQL_DATABASE_CAR"), service='default'):
        self.bdd = bdd
        if service not in DbConnexion.__instanceDict:
            self.engine = self.connect()  # Methode de classe
            self.session = sessionmaker()
            self.session.configure(bind=self.engine)
            objet = SessionObject(self)
            singleton_session = objet.get_session_object()
            DbConnexion.__instanceDict[service] = singleton_session
            DbConnexion.__instanceDict[service].__session = None
        else:
            self.get_instance(service)

    def connect(self):
        INFO_CONNEXION = os.getenv("MYSQL_URL") + self.bdd
        engine = create_engine(INFO_CONNEXION, echo=ECHO_CONNEXION, pool_recycle=3600)
        return engine

    def get_session(self, bdd=None, service='default'):
        if bdd:
            self.bdd = bdd
        self.engine = self.connect()
        self.session = sessionmaker(bind=self.engine)()
        return self.session

    def execute(self, query):
        pass

    def close(self):
        session = self.get_session()
        session.close()
