import json

# Banco global
banco = {}

def cargar_banco():
    """Carga el banco desde el archivo banco.json"""
    global banco
    try:
        with open("banco.json", "r") as f:
            banco = json.load(f)
    except FileNotFoundError:
        banco = {}

def guardar_banco():
    """Guarda el banco en el archivo banco.json"""
    with open("banco.json", "w") as f:
        json.dump(banco, f)