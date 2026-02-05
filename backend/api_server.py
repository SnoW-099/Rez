# api_server.py - Servidor API para comunicación con el frontend

from flask import Flask, jsonify
from flask_cors import CORS
from threading import Thread
import os
import sys
import logging
from datetime import datetime

# Añadir el directorio backend al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config_backend import config

logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Habilitar CORS para peticiones desde el frontend

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
        {'name': '!ping', 'description': 'Verifica la latencia del bot', 'category': 'Utilidad'},
        {'name': '!help', 'description': 'Muestra todos los comandos disponibles', 'category': 'Utilidad'},
        {'name': '!profile [@usuario]', 'description': 'Muestra tu perfil o el de otro usuario', 'category': 'Economía'},
        {'name': '!balance [@usuario]', 'description': 'Consulta tu saldo o el de otro usuario', 'category': 'Economía'},
        {'name': '!work', 'description': 'Trabaja para ganar dinero (cooldown: 3 min)', 'category': 'Economía'},
        {'name': '!transfer @usuario cantidad', 'description': 'Transfiere dinero a otro usuario', 'category': 'Economía'},
        {'name': '!rob @usuario', 'description': 'Intenta robar dinero (50% de éxito)', 'category': 'Economía'},
        {'name': '!ranking', 'description': 'Top 5 usuarios más ricos', 'category': 'Economía'},
        {'name': '!warn @usuario', 'description': 'Advierte a un usuario (Mods)', 'category': 'Moderación'},
        {'name': '!clear cantidad', 'description': 'Elimina mensajes (Mods)', 'category': 'Moderación'},
        {'name': '!play canción', 'description': 'Reproduce música en tu canal', 'category': 'Música'},
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