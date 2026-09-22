import os
import requests
import yt_dlp

os.makedirs("downloads", exist_ok=True)

def _descargar_con_ytdlp(enlace, extra_opts=None):
    if not enlace:
        return "⚠️ Especifica el enlace a descargar."
    try:
        ydl_opts = {
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'quiet': True,
        }
        if extra_opts:
            ydl_opts.update(extra_opts)
            
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(enlace, download=True)
            titulo = info.get('title', 'archivo')
        return f"✅ ¡Descargado con éxito: {titulo}!"
    except Exception as error:
        return f"⚠️ Error al descargar: {str(error)}"

def procesar_descargar(parametro):
    return _descargar_con_ytdlp(parametro)

def descargar_facebook(parametro):
    return _descargar_con_ytdlp(parametro)

def descargar_instagram(parametro):
    return _descargar_con_ytdlp(parametro)

def descargar_tiktok(parametro):
    return _descargar_con_ytdlp(parametro)

def descargar_youtube(parametro):
    return _descargar_con_ytdlp(parametro)

def procesar_mp3(parametro):
    opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    return _descargar_con_ytdlp(parametro, extra_opts=opts)

def procesar_mp4(parametro):
    opts = {'format': 'mp4/best[height<=720]'}
    return _descargar_con_ytdlp(parametro, extra_opts=opts)

def procesar_imagenes(parametro):
    if not parametro:
        return "⚠️ Especifica una URL de imagen."
    try:
        response = requests.get(parametro, timeout=10)
        if response.status_code == 200:
            nombre_archivo = f"downloads/img_{abs(hash(parametro))}.jpg"
            with open(nombre_archivo, 'wb') as f:
                f.write(response.content)
            return f"✅ Imagen descargada con éxito: {nombre_archivo}"
        return "⚠️ No se pudo descargar la imagen (código HTTP no 200)."
    except Exception as error:
        return f"⚠️ Error al descargar imagen: {str(error)}"

def procesar_sticker(parametro):
    return "✨ Para stickers, envía una imagen con el comando o usa la lógica de procesamiento de imagen a WebP."

def procesar_pinterest(parametro):
    return _descargar_con_ytdlp(parametro)

def procesar_Medifire(parametro):
    return "🔥 Mediafire requiere extracción de enlace directo (puedes usar scraping con BeautifulSoup o una API externa)."

def procesar_Mega(parametro):
    return "🟢 Mega requiere la librería `mega.py` o su CLI oficial para descargas directas."