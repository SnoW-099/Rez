# database.py - Conexión a MongoDB

import os
import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

logger = logging.getLogger(__name__)

class Database:
    _instance = None
    _client = None
    _db = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def connect(self):
        """Conectar a MongoDB"""
        if self._client is not None:
            return self._db

        mongodb_uri = os.getenv('MONGODB_URI')
        if not mongodb_uri:
            raise ValueError("MONGODB_URI no está definida en las variables de entorno")

        try:
            self._client = MongoClient(mongodb_uri)
            # Verificar conexión
            self._client.admin.command('ping')
            self._db = self._client['rez_bot']
            logger.info("✅ Conectado a MongoDB Atlas correctamente")
            return self._db
        except ConnectionFailure as e:
            logger.error(f"❌ Error al conectar a MongoDB: {e}")
            raise

    @property
    def db(self):
        if self._db is None:
            self.connect()
        return self._db

    @property
    def users(self):
        """Colección de usuarios"""
        return self.db['users']

    @property
    def config(self):
        """Colección de configuración"""
        return self.db['config']

    @property
    def logs(self):
        """Colección de logs"""
        return self.db['logs']

    def close(self):
        """Cerrar conexión"""
        if self._client:
            self._client.close()
            self._client = None
            self._db = None
            logger.info("Conexión a MongoDB cerrada")

# Instancia global
database = Database()
