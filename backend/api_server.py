# api_server.py - Servidor API para comunicación con el frontend

from flask import Flask, jsonify
from threading import Thread
import json
import os
import sys
from datetime import datetime

# Añadir el directorio backend al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config_backend import config

app = Flask(__name__)

# Variable global para almacenar el estado del bot
bot_status = {
    'status': 'offline',
    'last_heartbeat': None,
    'version': '1.0.0',
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
        {'name': '/ping', 'description': 'Verifica la latencia del bot'},
        {'name': '/help', 'description': 'Muestra esta ayuda'},
        {'name': '/play [cancion]', 'description': 'Reproduce música en tu canal de voz'},
        {'name': '/moderate', 'description': 'Herramientas de moderación'},
        {'name': '/profile', 'description': 'Muestra tu perfil de usuario'},
        {'name': '/balance', 'description': 'Consulta tu saldo'},
        {'name': '/work', 'description': 'Trabaja para ganar dinero'},
        {'name': '$balance', 'description': 'Consulta tu saldo actual en el banco'},
        {'name': '$trabajar', 'description': 'Trabaja para ganar dinero (cooldown de 3 minutos)'},
        {'name': '$robar <@usuario>', 'description': 'Intenta robar dinero a otro usuario (riesgo de multa)'},
        {'name': '$donar <@usuario> <cantidad>', 'description': 'Donar una cantidad específica de dinero a otro usuario'},
        {'name': '$ranking', 'description': 'Ver el ranking de los 5 usuarios con más dinero'},
        {'name': '$perfil [@usuario]', 'description': 'Ver tu perfil o el de otro usuario con información bancaria'}
    ]
    return jsonify(commands)

@app.route('/api/bank-data', methods=['GET'])
def get_bank_data():
    """Obtener datos del sistema bancario"""
    from bank_system import banco

    total_users = len(banco)
    total_coins = sum(banco.values())
    average_balance = total_coins / total_users if total_users > 0 else 0

    # Obtener top 5 usuarios
    top_users = sorted(banco.items(), key=lambda x: x[1], reverse=True)[:5]

    bank_data = {
        'totalUsers': total_users,
        'totalCoins': total_coins,
        'averageBalance': round(average_balance, 2),
        'topUsers': [{'id': user_id, 'balance': balance} for user_id, balance in top_users]
    }

    return jsonify(bank_data)

def calculate_uptime():
    """Calcular el tiempo de actividad"""
    if bot_status['last_heartbeat']:
        start_time = datetime.fromisoformat(bot_status['last_heartbeat'].replace('Z', '+00:00'))
        now = datetime.now(start_time.tzinfo)
        diff = now - start_time
        
        days = diff.days
        hours, remainder = divmod(diff.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        
        return f"{days}d {hours}h {minutes}m"
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
    # Iniciar el servidor API
    run_api_server()