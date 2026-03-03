import logging
import json
import math
import os
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# ─── Storage backend selection ────────────────────────────────
_USE_MONGO = False
_mongo_db = None
_JSON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bank_data.json')
_json_cache = {}

def _init():
    global _USE_MONGO, _mongo_db, _json_cache
    uri = os.getenv('MONGODB_URI', '').strip()
    if uri:
        try:
            from pymongo import MongoClient
            client = MongoClient(uri, serverSelectionTimeoutMS=3000)
            client.admin.command('ping')
            _mongo_db = client['rez_bot']
            _USE_MONGO = True
            logger.info("✅ BankSystem: Using MongoDB")
            return
        except Exception as e:
            logger.warning(f"⚠️  MongoDB failed ({e}), falling back to JSON")
    # JSON fallback
    if os.path.exists(_JSON_PATH):
        try:
            with open(_JSON_PATH, 'r', encoding='utf-8') as f:
                _json_cache = json.load(f)
        except Exception:
            _json_cache = {}
    logger.info("📁 BankSystem: Using local JSON (bank_data.json)")

_init()

# ─── JSON helpers ─────────────────────────────────────────────
def _save():
    try:
        with open(_JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(_json_cache, f, indent=2, default=str)
    except Exception as e:
        logger.error(f"JSON save error: {e}")

def _default_user(uid):
    return {
        'user_id': uid,
        'balance': 1000,
        'warnings': 0,
        'total_earned': 0,
        'total_spent': 0,
        'xp': 0,
        'level': 0,
        'messages': 0,
        'cooldowns': {},
        'created_at': datetime.utcnow().isoformat(),
    }

# ─── BankSystem ───────────────────────────────────────────────
class BankSystem:
    def __init__(self):
        self.starting_balance = 1000

    # ── User data ──────────────────────────────────────────
    def get_user_data(self, user_id):
        uid = str(user_id)
        if _USE_MONGO:
            user = _mongo_db.users.find_one({'user_id': uid})
            if not user:
                user = {**_default_user(uid), 'created_at': datetime.utcnow()}
                _mongo_db.users.insert_one(user)
            return user
        else:
            if uid not in _json_cache:
                _json_cache[uid] = _default_user(uid)
                _save()
            return _json_cache[uid]

    # ── Economy ────────────────────────────────────────────
    def add_money(self, user_id, amount):
        uid = str(user_id)
        if _USE_MONGO:
            self.get_user_data(uid)
            _mongo_db.users.update_one(
                {'user_id': uid},
                {'$inc': {'balance': amount, 'total_earned': amount}}
            )
        else:
            u = self.get_user_data(uid)
            u['balance'] = u.get('balance', 0) + amount
            u['total_earned'] = u.get('total_earned', 0) + amount
            _save()

    def remove_money(self, user_id, amount):
        uid = str(user_id)
        if _USE_MONGO:
            u = self.get_user_data(uid)
            actual = min(amount, u['balance'])
            _mongo_db.users.update_one(
                {'user_id': uid},
                {'$inc': {'balance': -actual, 'total_spent': actual}}
            )
            return actual
        else:
            u = self.get_user_data(uid)
            actual = min(amount, u.get('balance', 0))
            u['balance'] = u.get('balance', 0) - actual
            u['total_spent'] = u.get('total_spent', 0) + actual
            _save()
            return actual

    def get_top_users(self, count=10):
        if _USE_MONGO:
            users = _mongo_db.users.find().sort('balance', -1).limit(count)
            return [(u['user_id'], u) for u in users]
        else:
            sorted_u = sorted(_json_cache.items(), key=lambda x: x[1].get('balance', 0), reverse=True)
            return sorted_u[:count]

    # ── Cooldowns ──────────────────────────────────────────
    def get_cooldown(self, user_id, command):
        uid = str(user_id)
        u = self.get_user_data(uid)
        cooldowns = u.get('cooldowns', {})
        if command in cooldowns:
            try:
                exp = cooldowns[command]
                if isinstance(exp, str):
                    exp = datetime.fromisoformat(exp)
                if isinstance(exp, datetime) and exp > datetime.utcnow():
                    return (exp - datetime.utcnow()).total_seconds()
            except Exception:
                pass
        return 0

    def set_cooldown(self, user_id, command, seconds):
        uid = str(user_id)
        exp = datetime.utcnow() + timedelta(seconds=seconds)
        if _USE_MONGO:
            _mongo_db.users.update_one(
                {'user_id': uid},
                {'$set': {f'cooldowns.{command}': exp}}
            )
        else:
            u = self.get_user_data(uid)
            if 'cooldowns' not in u:
                u['cooldowns'] = {}
            u['cooldowns'][command] = exp.isoformat()
            _save()

    def clear_cooldown(self, user_id, command):
        uid = str(user_id)
        if _USE_MONGO:
            _mongo_db.users.update_one({'user_id': uid}, {'$unset': {f'cooldowns.{command}': ''}})
        else:
            u = self.get_user_data(uid)
            u.get('cooldowns', {}).pop(command, None)
            _save()

    # ── XP/Levels ──────────────────────────────────────────
    def calculate_level(self, xp):
        return int(math.sqrt(xp / 100))

    def xp_for_level(self, level):
        return level * level * 100

    def add_xp(self, user_id, amount):
        uid = str(user_id)
        u = self.get_user_data(uid)
        old_level = u.get('level', 0)
        new_xp = u.get('xp', 0) + amount
        new_level = self.calculate_level(new_xp)
        if _USE_MONGO:
            _mongo_db.users.update_one(
                {'user_id': uid},
                {'$set': {'xp': new_xp, 'level': new_level}, '$inc': {'messages': 1}}
            )
        else:
            u['xp'] = new_xp
            u['level'] = new_level
            u['messages'] = u.get('messages', 0) + 1
            _save()
        return new_level > old_level, new_level

    def get_xp_leaderboard(self, count=10):
        if _USE_MONGO:
            return list(_mongo_db.users.find().sort('xp', -1).limit(count))
        else:
            sorted_u = sorted(_json_cache.values(), key=lambda x: x.get('xp', 0), reverse=True)
            return sorted_u[:count]

    # ── Warnings ───────────────────────────────────────────
    def add_warning(self, user_id):
        uid = str(user_id)
        if _USE_MONGO:
            r = _mongo_db.users.find_one_and_update(
                {'user_id': uid}, {'$inc': {'warnings': 1}}, return_document=True
            )
            return r['warnings']
        else:
            u = self.get_user_data(uid)
            u['warnings'] = u.get('warnings', 0) + 1
            _save()
            return u['warnings']

    def get_warnings(self, user_id):
        return self.get_user_data(str(user_id)).get('warnings', 0)

    def reset_warnings(self, user_id):
        uid = str(user_id)
        if _USE_MONGO:
            _mongo_db.users.update_one({'user_id': uid}, {'$set': {'warnings': 0}})
        else:
            u = self.get_user_data(uid)
            u['warnings'] = 0
            _save()

    # ── Stats ──────────────────────────────────────────────
    def get_stats(self):
        if _USE_MONGO:
            pipeline = [{'$group': {'_id': None, 'total_users': {'$sum': 1},
                                    'total_coins': {'$sum': '$balance'},
                                    'avg_balance': {'$avg': '$balance'}}}]
            r = list(_mongo_db.users.aggregate(pipeline))
            return r[0] if r else {'total_users': 0, 'total_coins': 0, 'avg_balance': 0}
        else:
            if not _json_cache:
                return {'total_users': 0, 'total_coins': 0, 'avg_balance': 0}
            bals = [u.get('balance', 0) for u in _json_cache.values()]
            return {'total_users': len(_json_cache), 'total_coins': sum(bals),
                    'avg_balance': sum(bals) / len(bals)}

    # ── Direct DB access (legacy compat) ───────────────────
    @property
    def db(self):
        if _USE_MONGO:
            return _mongo_db
        # Return a minimal shim for leaderboard queries
        return _JSONShim()


class _JSONShim:
    """Minimal compatibility shim for code that accesses bank.db.users.find()"""
    class _Users:
        def find(self):
            return sorted(_json_cache.values(), key=lambda x: x.get('xp', 0), reverse=True)
        def find_one(self, q):
            uid = q.get('user_id')
            return _json_cache.get(str(uid))
        def insert_one(self, doc):
            _json_cache[str(doc['user_id'])] = doc
            _save()
        def update_one(self, q, update):
            uid = q.get('user_id')
            if uid and uid in _json_cache:
                inc = update.get('$inc', {})
                for k, v in inc.items():
                    _json_cache[uid][k] = _json_cache[uid].get(k, 0) + v
                set_ = update.get('$set', {})
                _json_cache[uid].update(set_)
                _save()
        def find_one_and_update(self, q, update, return_document=False):
            self.update_one(q, update)
            return _json_cache.get(str(q.get('user_id')))
        def aggregate(self, pipeline):
            return []
        def sort(self, field, direction):
            return self
        def limit(self, n):
            return list(_json_cache.values())[:n]

    @property
    def users(self):
        return self._Users()