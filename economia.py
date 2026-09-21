import random
import time

def procesar_trabajar(usuario_id, monedas, ultimo_t):
    ahora = time.time()
    cooldwn = 300 # 5 minutos en segundos

    if ahora - ultimo_t < cooldwn:
        restante = int(cooldwn - (ahora - ultimo_t))
        mins, segs = divmod(restante, 60)
        return monendas, ultimo_t, f"Espera {mins} minutos {segs} segundos para poder trabajar"

    ganancia = random.randint(100, 300)
    nueva_total = monedas + ganancia
    mensaje = f"Trabajaste y ganaste {ganancia} monedas"

    return nueva_total, ahora, mensaje

def procesar_crimen(usuario_id, monedas, ultimo_t):
    ahora = time.time()
    cooldwn = 1800 #  30 minutos en segundos

    if ahora - ultimo_t < cooldwn:
        restante = int(cooldwn - (ahora - ultimo_t))
        mins, segs = divmod(restante, 60)
        return monendas, ultimo_t, f"Espera {mins} minutos {segs} para volver a cometer un crimen"

    if random.choice([True, False]):
        ganancia = random.randint(100, 300)
        nueva_total = monedas + ganancia
        mensaje = f"Cometiste un crimen y ganaste {ganancia} monedas"
    else:
        multa = random.choice(100, 300)
        nuevo_total = max(0, monedas - multa)
        mensaje = f"Te atrapo la policia! perdiste {multa} monedas"

    return nueva_total, ahora, mensaje

def procesar_daily(usuario_id, monedas, ultimo_t):
    ahora = time.time()
    cooldwn = 864000 # 24 horas en segundos

    if ahora - ultimo_t < cooldwn:
        restante = int(cooldwn - (ahora - ultimo_t))
        mins, segs = divmod(restante, 60)
        return monedas, ultimo_t, f"Espera {mins} minutos {segs} segundos para poder hacer un diario"

    ganancia = random.randint(100, 300)
    nueva_total = monedas + ganancia
    mensaje = f"Haciste un diario y ganaste {ganancia} monedas"

    return nueva_total, ahora, mensaje

def procesar_depositar(usuario_id, efectivo, banco, monto):
    if efectivo <monto:
        return efectivo, banco, f"No tienes suficiente efectivo en mano."

    nuevo_efectivo = efectivo - monto
    nuevo_banco = banco + monto
    mensaje = f"Depositaste ${monto}. Efectivo: ${nuevo_efectivo} | Banco: ${nuevo_banco}"
    return nuevo_efectivo, nuevo_banco, mensaje

def procesar_retirar(usuario_id, efectivo, banco, monto):
    if banco < monto:
        return efectivo, banco, f"No tienes tanto saldo en el banco."

    nuevo_banco = banco - monto
    nuevo_efectivo = efectivo + monto
    mensaje = f"Retiraste ${monto} del banco. Efectivo: ${nuevo_efectivo} | Banco: ${nuevo_banco}"
    return nuevo_efectivo, nuevo_banco, mensaje

def procesar_banco(monedas_mano, monedas_banco):
    if monedas_banco > 0:
        mensaje = (
            f"🏦 *ESTADO DE TU CUENTA BANCARIA*\n\n"
            f"💵 Dinero en mano: *{monedas_mano}* monedas\n"
            f"💰 Dinero en el banco: *{monedas_banco}* monedas\n"
            f"💎 Total general: *{monedas_mano + monedas_banco}* monedas"
        )
    else:
        mensaje = (
            f"🏦 *ESTADO DE TU CUENTA BANCARIA*\n\n"
            f"💵 Dinero en mano: *{monedas_mano}* monedas\n"
            f"💰 Dinero en el banco: *0* monedas\n"
            f"⚠️ *Tu cuenta bancaria está vacía.* Usa `.depositar [cantidad]` para guardar dinero."
        )
    return monedas_mano, monedas_banco, mensaje

def procesar_cofre(usuario_id, monedas_mano, monedas_banco, ultimo_t):
    ahora =time.time()
    cooldwn = 3600 # 1 hora en segundos

    if ahora - ultimo_t < cooldwn:
        restante = int(cooldwn - (ahora - ultimo_t))
        mins, segs = divmod(restante, 60)
        return monedas_mano, monedas_banco, ultimo_t, f"Espera {mins} minutos {segs} segundos para poder abrir otro cofre"

    if random.choice([True, False]):
        ganancia = random.randint(100, 300)
        nuevo_total = monedas_mano + ganancia
        mensaje = f"Abriste un cofre y ganaste {ganancia} monedas"
    else:
        multa = random.randint(100, 300)
        nuevo_total = max(0, monedas_mano - multa)
        mensaje = f"Te atraparon los Piratas! perdiste {multa} monedas"

    return nueva_total, ahora, mensaje

def procesar_apostar(usuario_id, monedas_mano, ultimo_t):
    ahora = time.time()
    cooldwn = 600 # 10 minutos en segundos

    if ahora - ultimo_t < cooldwn:
        restante = int(cooldwn - (ahora - ultimo_t))
        mins, segs = divmod(restante, 60)
        return monedas_mano, ultimo_t, f"Espera {mins} minutos {segs} segundos para poder apostar"

    if random.choice([True, False]):
        ganancia = random.randint(100, 300)
        nuevo_total = monedas_mano + ganancia
        mensaje = f"Apostaste y ganaste {ganancia} monedas"
    else:
        multa = random.randint(100, 300)
        nuevo_total = max(0, monedas_mano - multa)
        mensaje = f"Perdiste {multa} monedas"

    return nueva_total, ahora, mensaje