import json

# Diccionarios globales
banco = {}
avisos_usuarios = {}

def cargar_datos():
    """Carga el banco y los avisos desde sus archivos JSON"""
    global banco, avisos_usuarios
    
    # Cargar Banco
    try:
        with open("banco.json", "r") as f:
            banco = json.load(f)
    except FileNotFoundError:
        banco = {}

    # Cargar Avisos
    try:
        with open("avisos.json", "r") as f:
            # Convertimos las llaves a int porque JSON las guarda como string
            data = json.load(f)
            avisos_usuarios = {int(k): v for k, v in data.items()}
    except FileNotFoundError:
        avisos_usuarios = {}

def guardar_datos():
    """Guarda el banco y los avisos en sus archivos JSON"""
    with open("banco.json", "w") as f:
        json.dump(banco, f)
    
    with open("avisos.json", "w") as f:
        json.dump(avisos_usuarios, f)