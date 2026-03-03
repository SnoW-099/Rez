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
        # Utility
        {'name': '!ping', 'description': 'Check bot latency', 'category': 'Utility', 'role': 'user'},
        {'name': '!help', 'description': 'Shows all commands', 'category': 'Utility', 'role': 'user'},

        # Economy
        {'name': '!profile [@user]', 'description': 'Your complete profile with stats', 'category': 'Economy', 'role': 'user'},
        {'name': '!balance [@user]', 'description': 'Check your balance', 'category': 'Economy', 'role': 'user'},
        {'name': '!work', 'description': 'Work and earn $50-200 (3 min cd)', 'category': 'Economy', 'role': 'user'},
        {'name': '!daily', 'description': 'Daily reward $200-500 (24h cd)', 'category': 'Economy', 'role': 'user'},
        {'name': '!transfer @user $', 'description': 'Transfer money to another user', 'category': 'Economy', 'role': 'user'},
        {'name': '!rob @user', 'description': 'Attempt to rob (50% success)', 'category': 'Economy', 'role': 'user'},
        {'name': '!ranking', 'description': 'Top 5 richest users', 'category': 'Economy', 'role': 'user'},
        {'name': '!shop', 'description': 'Item and role shop', 'category': 'Economy', 'role': 'user'},
        {'name': '!buy [item]', 'description': 'Buy an item from the shop', 'category': 'Economy', 'role': 'user'},

        # Levels
        {'name': '!level [@user]', 'description': 'View level and XP', 'category': 'Levels', 'role': 'user'},
        {'name': '!leaderboard', 'description': 'Top 10 by XP', 'category': 'Levels', 'role': 'user'},

        # Casino
        {'name': '!coinflip $ heads/tails', 'description': 'Bet heads or tails', 'category': 'Casino', 'role': 'user'},
        {'name': '!slots $', 'description': 'Slot machine', 'category': 'Casino', 'role': 'user'},
        {'name': '!blackjack $', 'description': 'Play blackjack (21)', 'category': 'Casino', 'role': 'user'},
        {'name': '!roulette $ color/num', 'description': 'Casino roulette', 'category': 'Casino', 'role': 'user'},

        # Giveaways
        {'name': '!giveaway [time] [prize]', 'description': 'Create a giveaway', 'category': 'Giveaways', 'role': 'admin'},
        {'name': '!gend', 'description': 'End active giveaway', 'category': 'Giveaways', 'role': 'admin'},
        {'name': '!greroll [id]', 'description': 'Reroll giveaway winner', 'category': 'Giveaways', 'role': 'admin'},

        # Tickets
        {'name': '!ticket [reason]', 'description': 'Create support ticket', 'category': 'Tickets', 'role': 'user'},
        {'name': '!close', 'description': 'Close current ticket', 'category': 'Tickets', 'role': 'user'},

        # Moderation
        {'name': '!warn @user [reason]', 'description': 'Warn user (3 warns = kick)', 'category': 'Moderation', 'role': 'admin'},
        {'name': '!mute @user [time]', 'description': 'Mute user (10m, 1h, etc.)', 'category': 'Moderation', 'role': 'admin'},
        {'name': '!unmute @user', 'description': 'Unmute a user', 'category': 'Moderation', 'role': 'admin'},
        {'name': '!kick @user [reason]', 'description': 'Kick from server', 'category': 'Moderation', 'role': 'admin'},
        {'name': '!ban @user [reason]', 'description': 'Permanently ban user', 'category': 'Moderation', 'role': 'admin'},
        {'name': '!unban [id]', 'description': 'Unban by user ID', 'category': 'Moderation', 'role': 'admin'},
        {'name': '!clear [1-100]', 'description': 'Delete messages', 'category': 'Moderation', 'role': 'admin'},
        {'name': '!slowmode [sec]', 'description': 'Set channel slowmode', 'category': 'Moderation', 'role': 'admin'},

        # Music
        {'name': '!play [song]', 'description': 'Play music', 'category': 'Music', 'role': 'user'},
        {'name': '!join', 'description': 'Join voice channel', 'category': 'Music', 'role': 'user'},
        {'name': '!leave', 'description': 'Leave voice channel', 'category': 'Music', 'role': 'user'},

        # Owner
        {'name': '!addmoney @user $', 'description': 'Give money to user', 'category': 'Owner', 'role': 'owner'},
        {'name': '!removemoney @user $', 'description': 'Remove money from user', 'category': 'Owner', 'role': 'owner'},
        {'name': '!setbalance @user $', 'description': 'Set exact balance', 'category': 'Owner', 'role': 'owner'},
        {'name': '!setlevel @user level', 'description': 'Set user level', 'category': 'Owner', 'role': 'owner'},
        {'name': '!resetuser @user', 'description': 'Reset all user data', 'category': 'Owner', 'role': 'owner'},
        {'name': '!botstat', 'description': 'Detailed bot statistics', 'category': 'Owner', 'role': 'owner'},
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
        except Exception:
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