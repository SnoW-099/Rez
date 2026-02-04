import json
import os
from commands_manager import increment_command_count

class BankSystem:
    def __init__(self, filename='bank_data.json'):
        self.filename = filename
        self.data = self.load_data()

    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                return json.load(f)
        else:
            return {}

    def save_data(self):
        with open(self.filename, 'w') as f:
            json.dump(self.data, f, indent=4)

    def get_user_data(self, user_id):
        user_id = str(user_id)
        if user_id not in self.data:
            self.data[user_id] = {
                'balance': 1000,  # Saldo inicial
                'warnings': 0
            }
            self.save_data()
        return self.data[user_id]

    def add_money(self, user_id, amount):
        user_id = str(user_id)
        if user_id not in self.data:
            self.get_user_data(user_id)  # Crea la entrada si no existe
        
        self.data[user_id]['balance'] += amount
        self.save_data()
        increment_command_count()

    def remove_money(self, user_id, amount):
        user_id = str(user_id)
        if user_id not in self.data:
            self.get_user_data(user_id)  # Crea la entrada si no existe
        
        self.data[user_id]['balance'] -= amount
        if self.data[user_id]['balance'] < 0:
            self.data[user_id]['balance'] = 0
        self.save_data()
        increment_command_count()

    def get_top_users(self, count=10):
        sorted_users = sorted(self.data.items(), key=lambda x: x[1]['balance'], reverse=True)
        return sorted_users[:count]

    def add_warning(self, user_id):
        user_id = str(user_id)
        if user_id not in self.data:
            self.get_user_data(user_id)
        
        self.data[user_id]['warnings'] += 1
        self.save_data()
        increment_command_count()

    def get_warnings(self, user_id):
        user_id = str(user_id)
        user_data = self.get_user_data(user_id)
        return user_data['warnings']

    def reset_warnings(self, user_id):
        user_id = str(user_id)
        if user_id in self.data:
            self.data[user_id]['warnings'] = 0
            self.save_data()
            increment_command_count()