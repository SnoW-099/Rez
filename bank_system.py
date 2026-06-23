import json

banco = {}


def cargar_banco():
    global banco
    try:
        with open("banco.json", "r", encoding="utf-8") as f:
            banco = json.load(f)
    except FileNotFoundError:
        banco = {}


def guardar_banco():
    with open("banco.json", "w", encoding="utf-8") as f:
        json.dump(banco, f)
