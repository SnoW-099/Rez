import logging
from datetime import datetime
from database import database

logger = logging.getLogger(__name__)

class BankSystem:
    def __init__(self):
        self.db = database
        self.starting_balance = 1000

    def get_user_data(self, user_id):
        """Obtener datos de un usuario, crearlo si no existe"""
        user_id = str(user_id)
        user = self.db.users.find_one({'user_id': user_id})
        
        if not user:
            user = {
                'user_id': user_id,
                'balance': self.starting_balance,
                'warnings': 0,
                'total_earned': 0,
                'total_spent': 0,
                'created_at': datetime.utcnow(),
                'last_work': None
            }
            self.db.users.insert_one(user)
            logger.info(f"Nuevo usuario creado en MongoDB: {user_id}")
        
        return user

    def add_money(self, user_id, amount):
        """Añadir dinero a un usuario"""
        user_id = str(user_id)
        self.get_user_data(user_id)  # Asegurar que existe
        
        self.db.users.update_one(
            {'user_id': user_id},
            {
                '$inc': {'balance': amount, 'total_earned': amount},
                '$set': {'updated_at': datetime.utcnow()}
            }
        )
        logger.debug(f"Usuario {user_id}: +{amount}")

    def remove_money(self, user_id, amount):
        """Quitar dinero a un usuario (no permite negativo)"""
        user_id = str(user_id)
        user = self.get_user_data(user_id)
        
        actual_amount = min(amount, user['balance'])
        
        self.db.users.update_one(
            {'user_id': user_id},
            {
                '$inc': {'balance': -actual_amount, 'total_spent': actual_amount},
                '$set': {'updated_at': datetime.utcnow()}
            }
        )
        logger.debug(f"Usuario {user_id}: -{actual_amount}")
        return actual_amount

    def set_balance(self, user_id, amount):
        """Establecer balance exacto"""
        user_id = str(user_id)
        self.get_user_data(user_id)
        
        self.db.users.update_one(
            {'user_id': user_id},
            {'$set': {'balance': amount, 'updated_at': datetime.utcnow()}}
        )

    def get_top_users(self, count=10):
        """Obtener top usuarios por balance"""
        users = self.db.users.find().sort('balance', -1).limit(count)
        return [(user['user_id'], user) for user in users]

    def add_warning(self, user_id):
        """Añadir advertencia a un usuario"""
        user_id = str(user_id)
        self.get_user_data(user_id)
        
        result = self.db.users.find_one_and_update(
            {'user_id': user_id},
            {
                '$inc': {'warnings': 1},
                '$set': {'updated_at': datetime.utcnow()}
            },
            return_document=True
        )
        logger.info(f"Usuario {user_id}: advertencia añadida (total: {result['warnings']})")
        return result['warnings']

    def get_warnings(self, user_id):
        """Obtener número de advertencias"""
        user = self.get_user_data(user_id)
        return user['warnings']

    def reset_warnings(self, user_id):
        """Reiniciar advertencias"""
        user_id = str(user_id)
        self.db.users.update_one(
            {'user_id': user_id},
            {'$set': {'warnings': 0, 'updated_at': datetime.utcnow()}}
        )
        logger.info(f"Usuario {user_id}: advertencias reiniciadas")

    def update_last_work(self, user_id):
        """Actualizar timestamp del último trabajo"""
        user_id = str(user_id)
        self.db.users.update_one(
            {'user_id': user_id},
            {'$set': {'last_work': datetime.utcnow()}}
        )

    def get_last_work(self, user_id):
        """Obtener timestamp del último trabajo"""
        user = self.get_user_data(user_id)
        return user.get('last_work')

    def get_stats(self):
        """Obtener estadísticas globales del banco"""
        pipeline = [
            {
                '$group': {
                    '_id': None,
                    'total_users': {'$sum': 1},
                    'total_coins': {'$sum': '$balance'},
                    'avg_balance': {'$avg': '$balance'}
                }
            }
        ]
        result = list(self.db.users.aggregate(pipeline))
        if result:
            return result[0]
        return {'total_users': 0, 'total_coins': 0, 'avg_balance': 0}