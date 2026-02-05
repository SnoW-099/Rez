# api_server.py - Servidor API para comunicación con el frontend

from flask import Flask, jsonify
from flask_cors import CORS
from threading import Thread
import os
import sys
import logging
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config_backend import config

logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Variable global para almacenar el estado del bot
bot_status = {
    'status': 'offline',
    'last_heartbeat': None,
    'version': '2.0.0',
    'connected_servers': 0,
    'total_users': 0,
    'commands_used': 0
}

@app.route('/api/status', methods=['GET'])
def get_bot_status():
    """Obtener el estado actual del bot"""
    return jsonify(bot_status)

@app.route('/api/stats', methods=['GET'])
def get_bot_stats():
    """Obtener estadísticas del bot"""
    stats = {
        'servers': bot_status['connected_servers'],
        'users': bot_status['total_users'],
        'commandsUsed': bot_status['commands_used'],
        'uptime': calculate_uptime()
    }
    return jsonify(stats)

@app.route('/api/commands', methods=['GET'])
def get_commands():
    """Obtener lista de comandos disponibles"""
    commands = [
        # Utilidad
        {'name': '!ping', 'description': 'Verifica la latencia del bot', 'category': 'Utilidad'},
        {'name': '!help', 'description': 'Muestra todos los comandos', 'category': 'Utilidad'},
        
        # Economía
        {'name': '!profile [@user]', 'description': 'Tu perfil completo con stats', 'category': 'Economía'},
        {'name': '!balance [@user]', 'description': 'Consulta tu saldo', 'category': 'Economía'},
        {'name': '!work', 'description': 'Trabaja y gana $50-200 (3 min cd)', 'category': 'Economía'},
        {'name': '!daily', 'description': 'Recompensa diaria $200-500 (24h cd)', 'category': 'Economía'},
        {'name': '!transfer @user $', 'description': 'Transfiere dinero', 'category': 'Economía'},
        {'name': '!rob @user', 'description': 'Intenta robar (50% éxito)', 'category': 'Economía'},
        {'name': '!ranking', 'description': 'Top 5 más ricos', 'category': 'Economía'},
        {'name': '!shop', 'description': 'Tienda de items y roles', 'category': 'Economía'},
        {'name': '!buy [item]', 'description': 'Compra un item de la tienda', 'category': 'Economía'},
        
        # Niveles
        {'name': '!level [@user]', 'description': 'Ver nivel y XP', 'category': 'Niveles'},
        {'name': '!leaderboard', 'description': 'Top 10 por XP', 'category': 'Niveles'},
        
        # Moderación
        {'name': '!warn @user [razón]', 'description': 'Advierte (3 warns = kick)', 'category': 'Moderación'},
        {'name': '!mute @user [tiempo]', 'description': 'Silencia (ej: 10m, 1h)', 'category': 'Moderación'},
        {'name': '!unmute @user', 'description': 'Quita el silencio', 'category': 'Moderación'},
        {'name': '!kick @user [razón]', 'description': 'Expulsa del servidor', 'category': 'Moderación'},
        {'name': '!ban @user [razón]', 'description': 'Banea permanentemente', 'category': 'Moderación'},
        {'name': '!unban [id]', 'description': 'Desbanea por ID', 'category': 'Moderación'},
        {'name': '!clear [1-100]', 'description': 'Elimina mensajes', 'category': 'Moderación'},
        {'name': '!slowmode [seg]', 'description': 'Modo lento del canal', 'category': 'Moderación'},
        
        # Música
        {'name': '!play [canción]', 'description': 'Reproduce música', 'category': 'Música'},
        {'name': '!join', 'description': 'Entra al canal de voz', 'category': 'Música'},
        {'name': '!leave', 'description': 'Sale del canal de voz', 'category': 'Música'}
    ]
    return jsonify(commands)

@app.route('/api/bank-data', methods=['GET'])
def get_bank_data():
    """Obtener datos del sistema bancario desde MongoDB"""
    try:
        from bank_system import BankSystem
        bank = BankSystem()
        stats = bank.get_stats()
        top_users = bank.get_top_users(5)

        bank_data = {
            'totalUsers': stats.get('total_users', 0),
            'totalCoins': stats.get('total_coins', 0),
            'averageBalance': round(stats.get('avg_balance', 0), 2),
            'topUsers': [
                {'id': user_id, 'balance': data['balance']} 
                for user_id, data in top_users
            ]
        }
        return jsonify(bank_data)
    except Exception as e:
        logger.error(f"Error al obtener datos del banco: {e}")
        return jsonify({
            'totalUsers': 0,
            'totalCoins': 0,
            'averageBalance': 0,
            'topUsers': []
        })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'timestamp': datetime.utcnow().isoformat()})

def calculate_uptime():
    """Calcular el tiempo de actividad"""
    if bot_status['last_heartbeat']:
        try:
            start_time = datetime.fromisoformat(bot_status['last_heartbeat'].replace('Z', '+00:00'))
            now = datetime.now(start_time.tzinfo)
            diff = now - start_time
            
            days = diff.days
            hours, remainder = divmod(diff.seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            
            return f"{days}d {hours}h {minutes}m"
        except:
            pass
    return "0d 0h 0m"

def update_bot_status(status, servers=0, users=0, commands=0):
    """Actualizar el estado del bot"""
    global bot_status
    bot_status.update({
        'status': status,
        'last_heartbeat': datetime.utcnow().isoformat() + 'Z',
        'connected_servers': servers,
        'total_users': users,
        'commands_used': commands
    })

def run_api_server():
    """Ejecutar el servidor API en un hilo separado"""
    app.run(host=config.WEB_SERVER_HOST, port=config.WEB_SERVER_PORT, debug=False, use_reloader=False)

if __name__ == '__main__':
    run_api_server()