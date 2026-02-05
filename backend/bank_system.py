import logging
from datetime import datetime, timedelta
from database import database

logger = logging.getLogger(__name__)

class BankSystem:
    def __init__(self):
        self.db = database
        self.starting_balance = 1000
        self.starting_xp = 0

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
                'xp': 0,
                'level': 0,
                'messages': 0,
                'cooldowns': {},
                'created_at': datetime.utcnow(),
                'last_work': None,
                'last_daily': None,
                'last_xp_gain': None
            }
            self.db.users.insert_one(user)
            logger.info(f"Nuevo usuario creado en MongoDB: {user_id}")
        
        return user

    # ============== ECONOMÍA ==============

    def add_money(self, user_id, amount):
        """Añadir dinero a un usuario"""
        user_id = str(user_id)
        self.get_user_data(user_id)
        
        self.db.users.update_one(
            {'user_id': user_id},
            {
                '$inc': {'balance': amount, 'total_earned': amount},
                '$set': {'updated_at': datetime.utcnow()}
            }
        )
        logger.debug(f"Usuario {user_id}: +${amount}")

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
        logger.debug(f"Usuario {user_id}: -${actual_amount}")
        return actual_amount

    def get_top_users(self, count=10):
        """Obtener top usuarios por balance"""
        users = self.db.users.find().sort('balance', -1).limit(count)
        return [(user['user_id'], user) for user in users]

    # ============== COOLDOWNS PERSISTENTES ==============

    def get_cooldown(self, user_id, command):
        """Obtener cooldown de un comando para un usuario"""
        user_id = str(user_id)
        user = self.get_user_data(user_id)
        cooldowns = user.get('cooldowns', {})
        
        if command in cooldowns:
            expires_at = cooldowns[command]
            if isinstance(expires_at, str):
                expires_at = datetime.fromisoformat(expires_at)
            
            if expires_at > datetime.utcnow():
                remaining = (expires_at - datetime.utcnow()).total_seconds()
                return remaining
        
        return 0  # No hay cooldown activo

    def set_cooldown(self, user_id, command, seconds):
        """Establecer cooldown para un comando"""
        user_id = str(user_id)
        expires_at = datetime.utcnow() + timedelta(seconds=seconds)
        
        self.db.users.update_one(
            {'user_id': user_id},
            {'$set': {f'cooldowns.{command}': expires_at}}
        )
        logger.debug(f"Usuario {user_id}: cooldown '{command}' = {seconds}s")

    def clear_cooldown(self, user_id, command):
        """Limpiar cooldown de un comando"""
        user_id = str(user_id)
        self.db.users.update_one(
            {'user_id': user_id},
            {'$unset': {f'cooldowns.{command}': ''}}
        )

    # ============== SISTEMA DE XP/NIVELES ==============

    def add_xp(self, user_id, amount):
        """Añadir XP a un usuario y verificar subida de nivel"""
        user_id = str(user_id)
        user = self.get_user_data(user_id)
        
        new_xp = user.get('xp', 0) + amount
        new_level = self.calculate_level(new_xp)
        old_level = user.get('level', 0)
        
        self.db.users.update_one(
            {'user_id': user_id},
            {
                '$set': {
                    'xp': new_xp,
                    'level': new_level,
                    'last_xp_gain': datetime.utcnow()
                },
                '$inc': {'messages': 1}
            }
        )
        
        leveled_up = new_level > old_level
        logger.debug(f"Usuario {user_id}: +{amount} XP (nivel {new_level})")
        
        return leveled_up, new_level

    def calculate_level(self, xp):
        """Calcular nivel basado en XP: nivel = sqrt(xp / 100)"""
        import math
        return int(math.sqrt(xp / 100))

    def xp_for_level(self, level):
        """XP necesario para un nivel específico"""
        return level * level * 100

    def get_xp_leaderboard(self, count=10):
        """Obtener top usuarios por XP"""
        users = self.db.users.find().sort('xp', -1).limit(count)
        return list(users)

    def can_gain_xp(self, user_id, cooldown_seconds=60):
        """Verificar si el usuario puede ganar XP (cooldown de mensajes)"""
        user_id = str(user_id)
        user = self.get_user_data(user_id)
        
        last_xp = user.get('last_xp_gain')
        if last_xp is None:
            return True
        
        if isinstance(last_xp, str):
            last_xp = datetime.fromisoformat(last_xp)
        
        elapsed = (datetime.utcnow() - last_xp).total_seconds()
        return elapsed >= cooldown_seconds

    # ============== ADVERTENCIAS ==============

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

    # ============== ESTADÍSTICAS ==============

    def get_stats(self):
        """Obtener estadísticas globales del banco"""
        pipeline = [
            {
                '$group': {
                    '_id': None,
                    'total_users': {'$sum': 1},
                    'total_coins': {'$sum': '$balance'},
                    'avg_balance': {'$avg': '$balance'},
                    'total_xp': {'$sum': '$xp'}
                }
            }
        ]
        result = list(self.db.users.aggregate(pipeline))
        if result:
            return result[0]
        return {'total_users': 0, 'total_coins': 0, 'avg_balance': 0, 'total_xp': 0}