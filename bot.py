import sys
import time
import json
import os

from menu import mostrar_menu
from economia import (
    procesar_trabajar, procesar_crimen, procesar_daily,
    procesar_depositar, procesar_retirar, procesar_banco,
    procesar_cofre, procesar_apostar
)

DB_FILE = "usuarios.json"

def cargar_todos_los_datos():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def guardar_todos_los_datos(datos):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    db = cargar_todos_los_datos()
    
    if len(sys.argv) > 2:
        usuario_id = str(sys.argv[1])
        cmd = str(sys.argv).sctrip().lower()

        # Helper seguro para extraer montos numéricos (si pasas .depositar 500)
        def obtener_monto():
            try:
                return int(sys.argv)
            except (ValueError, IndexError):
                return 0
        
        # Inicializar usuario si no existe
        if usuario_id not in db:
            db[usuario_id] = {
                "efectivo": 100, "banco": 0,
                "ultimo_trabajo": 0, "ultimo_crimen": 0,
                "ultimo_daily": 0, "ultimo_cofre": 0, "ultimo_apostar": 0
            }
        u = db[usuario_id]
        respuesta = "❌ Comando no reconocido."

        # 👉 PRIMERO DEBE SER UN 'if'
        if cmd in [".menu", ".help"]:
            respuesta = mostrar_menu()
        elif cmd == ".banco":
            _, _, respuesta = procesar_banco(u["efectivo"], u["banco"])
        elif cmd in [".trabajar", ".work", ".w"]:
             ef, ba, ts, resp = procesar_trabajar(usuario_id, u["efectivo"], u["banco"], u["ultimo_trabajo"])
             u["efectivo"], u["banco"], u["ultimo_trabajo"] = ef, ba, ts
             respuesta = resp

        elif cmd == ".crimen":
             ef, ba, ts, resp = procesar_crimen(usuario_id, u["efectivo"], u["banco"], u["ultimo_crimen"])
             u["efectivo"], u["banco"], u["ultimo_crimen"] = ef, ba, ts
             respuesta = resp

        elif cmd == ".diario":
            ef, ba, ts, resp = procesar_daily(usuario_id, u["efectivo"], u["banco"], u["ultimo_daily"])
            u["efectivo"], u["banco"], u["ultimo_daily"] = ef, ba, ts
            respuesta = resp

        elif cmd == ".cofre":
            ef, ba, ts, resp = procesar_cofre(usuario_id, u["efectivo"], u["banco"], u["ultimo_cofre"])
            u["efectivo"], u["banco"], u["ultimo_cofre"] = ef, ba, ts
            respuesta = resp

        elif cmd == ".apostar":
            ef, ba, ts, resp = procesar_apostar(usuario_id, u["efectivo"], u["ultimo_apostar"])
            u["efectivo"], u["ultimo_apostar"] = ef, ts
            respuesta = resp

        elif cmd == ".depositar":
            ef, ba, ts, resp = procesar_depositar(usuario_id, u["efectivo"], u["banco"], obtener_monto())
            u["efectivo"], u["banco"] = ef, ba
            respuesta = resp

        elif cmd == ".retirar":
            ef, ba, ts, resp = procesar_retirar(usuario_id, u["efectivo"], u["banco"], obtener_monto())
            u["efectivo"], u["banco"] = ef, ba
            respuesta = resp
            
        guardar_todos_los_datos(db)
        print(respuesta)
    else:
        print("Modo ejecución: Faltan argumentos.")