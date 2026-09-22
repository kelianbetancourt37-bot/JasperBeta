import random

def procesar_perfil(datos_usuario):
    nombre = datos_usuario.get("nombre", "Sin nombre")
    genero = datos_usuario.get("genero", "No especificado")
    edad = datos_usuario.get("edad", "No especificada")
    nacimiento = datos_usuario.get("nacimiento", "No especificado")
    nivel = datos_usuario.get("nivel", 1)
    nivel_progreso = datos_usuario.get("nivel_progreso", "[░░░░░░░░░░] 0%")
    monedas = datos_usuario.get("monedas", 500)
    banco = datos_usuario.get("banco", 0)
    racha = datos_usuario.get("racha", 0)
    descripcion = datos_usuario.get("descripcion", "Sin biografía.")

    return (
        f"╭─ 👤 *TARJETA DE PERFIL* 👤 ─╮\n"
        f"│\n"
        f"│   🏷️ *Nombre:* {nombre}\n"
        f"│   🚻 *Género:* {genero}\n"
        f"│   🎂 *Edad:* {edad} años\n"
        f"│   📅 *Nacimiento:* {nacimiento}\n\n"
        f"│   ⭐ *Nivel:* Nivel {nivel}\n"
        f"│   📈 *Progreso de nivel:* {nivel_progreso}\n"
        f"│\n"
        f"├─ 💰 *ECONOMÍA & RACHA* ─┤\n"
        f"│   💵 *Cartera:* {monedas} monedas\n"
        f"│   🏦 *Banco:* {banco} monedas\n"
        f"│   🔥 *Racha diaria:* {racha} días\n"
        f"│\n"
        f"├─ 📝 *BIOGRAFÍA* ─┤\n"
        f"│   _{descripcion}_\n"
        f"│\n"
        f"╰──────────────────────────╯\n"
        f"💡 _Usa `.setname`, `.setage`, etc., para editar tus datos._"
    )

def procesar_setname(param, datos_usuario, guardar_fn, base_datos):
    if not param:
        return "⚠️ Por favor escribe el nuevo nombre. Ejemplo: `.setname Juan`"
    datos_usuario["nombre"] = param
    guardar_fn(base_datos)
    return f"✅ Nombre actualizado correctamente a: *{param}*"

def procesar_setdesc(param, datos_usuario, guardar_fn, base_datos):
    if not param:
        return "⚠️ Escribe tu nueva biografía."
    datos_usuario["descripcion"] = param
    guardar_fn(base_datos)
    return f"📝 Biografía actualizada correctamente."

def procesar_setage(param, datos_usuario, guardar_fn, base_datos):
    if not param:
        return "⚠️ Especifica tu edad."
    datos_usuario["edad"] = param
    guardar_fn(base_datos)
    return f"🎂 Edad configurada a: *{param}* años."

def procesar_setbirth(param, datos_usuario, guardar_fn, base_datos):
    if not param:
        return "⚠️ Especifica tu fecha de nacimiento."
    datos_usuario["nacimiento"] = param
    guardar_fn(base_datos)
    return f"📅 Fecha de nacimiento guardada: *{param}*."

def procesar_setgene(param, datos_usuario, guardar_fn, base_datos):
    if not param:
        return "⚠️ Especifica tu género. Ejemplo: `.setgene Masculino`"
    datos_usuario["genero"] = param
    guardar_fn(base_datos)
    return f"🚻 Género actualizado a: *{param}*."

def procesar_level(datos_usuario):
    nivel = datos_usuario.get("nivel", 1)
    progreso = datos_usuario.get("nivel_progreso", "[░░░░░░░░░░] 0%")
    return f"📊 Tu nivel actual en el bot es: *Nivel {nivel}*.\n📈 Progreso: {progreso}"

def procesar_sublevel(param=""):
    return "📈 Progreso de nivel actualizado."

def procesar_levelup(datos_usuario=None):
    if isinstance(datos_usuario, dict):
        nivel = datos_usuario.get("nivel", 1)
        progreso = datos_usuario.get("nivel_progreso", "[░░░░░░░░░░] 0%")
        return f"🎉 Revisa tu estado: *Nivel {nivel}* | Progreso: {progreso}"
    return "🎉 ¡Felicidades! Has subido de nivel."

def agregar_experiencia(datos_usuario, cantidad):
    if "nivel" not in datos_usuario:
        datos_usuario["nivel"] = 1
    if "experiencia" not in datos_usuario:
        datos_usuario["experiencia"] = 0

    xp_necesaria = datos_usuario["nivel"] * 100
    datos_usuario["experiencia"] += cantidad

    sub_nivel = False
    while datos_usuario["experiencia"] >= xp_necesaria:
        datos_usuario["experiencia"] -= xp_necesaria
        datos_usuario["nivel"] += 1
        xp_necesaria = datos_usuario["nivel"] * 100
        sub_nivel = True

    porcentaje = min(datos_usuario["experiencia"] / xp_necesaria, 1.0)
    bloques_llenos = int(porcentaje * 10)
    barrita = "█" * bloques_llenos + "░" * (10 - bloques_llenos)
    porcentaje_num = int(porcentaje * 100)
    nivel_progreso = f"[{barrita}] {porcentaje_num}%"

    datos_usuario["nivel_progreso"] = nivel_progreso
    return nivel_progreso, sub_nivel