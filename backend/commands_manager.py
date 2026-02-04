# commands_manager.py - Gestión del conteo de comandos

_command_count = 0

def increment_command_count():
    """Incrementar el contador de comandos"""
    global _command_count
    _command_count += 1

def get_command_count():
    """Obtener el contador de comandos"""
    return _command_count

def reset_command_count():
    """Reiniciar el contador de comandos"""
    global _command_count
    _command_count = 0