from contextlib import suppress

import yt_dlp
import subprocess
import sys
from pathlib import Path
from termcolor import colored

def progreso_hook(d):
        subprocess.run(['clear'])
        print("\n\nDescargado ....")
        if d['status'] == 'downloading':
            if 'total_bytes' in d:
                porcentaje = (d['downloaded_bytes'] / d['total_bytes']) * 100
                barra = '█' * int(porcentaje // 5) + '░' * (20 - int(porcentaje // 5))
                print(f"\r⏳ Progreso: [{barra}] {porcentaje:.1f}%", end='')
        elif 'total_bytes_estimate' in d:
            porcentaje = (d['downloaded_bytes'] / d['total_bytes_estimate']) * 100
            barra = '█' * int(porcentaje // 5) + '░' * (20 - int(porcentaje // 5))
            print(f"\r⏳ Progreso: [{barra}] {porcentaje:.1f}% (estimado)", end='')
    
        elif d['status'] == 'finished':
            print("\n✅ Descarga completada, procesando...")

def descargar_playlist(url, calidad):


    ydl_opts = {
    'outtmpl': './descargas/%(playlist_title)s/%(title)s.%(ext)s',
    'progress_hooks': [progreso_hook],
    'ignoreerrors': True,
    'nooverwrites': True,
    }

    # Configurar calidad
    if calidad == 'best':
        ydl_opts['format'] = 'bestvideo+bestaudio/best'
    elif calidad == 'worst':
        ydl_opts['format'] = 'worst'
    elif calidad == '1080p':
        ydl_opts['format'] = 'bestvideo[height<=1080]+bestaudio/best[height<=1080]'
    elif calidad == '720p':
        ydl_opts['format'] = 'bestvideo[height<=720]+bestaudio/best[height<=720]'
    elif calidad == '480p':
        ydl_opts['format'] = 'bestvideo[height<=480]+bestaudio/best[height<=480]'
    elif calidad == '360p':
        ydl_opts['format'] = 'bestvideo[height<=360]+bestaudio/best[height<=360]'
    else:
        ydl_opts['format'] = 'bestvideo+bestaudio/best'


    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl: # type: ignore
            ydl.download([url])
            print("✅ Playlist descargada exitosamente!")
    except Exception as e:
        print(f"❌ Error al descargar playlist: {str(e)}")



def descargar_audio(url, formato, ruta_descarga='.descargas'):
    Path(ruta_descarga).mkdir(parents=True, exist_ok=True)

    ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': formato,
        'preferredquality': '192',
    }],
    'outtmpl': f'{ruta_descarga}/%(title)s.%(ext)s',
    'progress_hooks': [progreso_hook],
    'quiet': False,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl: # type: ignore
            print(f"\n🎵 Descargando audio: {url}")
            print(f"📁 Guardando en: {ruta_descarga}")
            print(f"🎵 Formato: {formato}")
            print("-" * 50)

            info = ydl.extract_info(url, download=True)

            print("-" * 50)
            print(f"✅ ¡Audio descargado!")
            print(f"🎵 Título: {info.get('title', 'Desconocido')}")

    except Exception as e:
        print(f"❌ Error al descargar audio: {str(e)}")
        return False
    return True




def descargar_video(url,calidad,ruta_descarga='./descargas/'):
    Path(ruta_descarga).mkdir(parents=True, exist_ok=True)

    ydl_opts = {
        'outtmpl': f'{ruta_descarga}/%(title)s.%(ext)s',  # Formato del nombre del archivo
        'progress_hooks': [progreso_hook],  # Hook para mostrar progreso
        'ignoreerrors': True,
        'nooverwrites': True,
        'quiet': False,  # Mostrar información
        'no_warnings': False,
        'extract_flat': False,
    }

    # Configurar calidad
    if calidad == 'best':
        ydl_opts['format'] = 'bestvideo+bestaudio/best'
    elif calidad == 'worst':
        ydl_opts['format'] = 'worst'
    elif calidad == '1080p':
        ydl_opts['format'] = 'bestvideo[height<=1080]+bestaudio/best[height<=1080]'
    elif calidad == '720p':
        ydl_opts['format'] = 'bestvideo[height<=720]+bestaudio/best[height<=720]'
    elif calidad == '480p':
        ydl_opts['format'] = 'bestvideo[height<=480]+bestaudio/best[height<=480]'
    elif calidad == '360p':
        ydl_opts['format'] = 'bestvideo[height<=360]+bestaudio/best[height<=360]'
    else:
        ydl_opts['format'] = 'bestvideo+bestaudio/best'
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:  # type: ignore
            print(f"\n📥 Descargando: {url}")
            print(f"📁 Guardando en: {ruta_descarga}")
            print(f"🎯 Calidad: {calidad}")
            print("-" * 50)

            info = ydl.extract_info(url, download=True)

            print("-" * 50)
            print(f"✅ ¡Descarga completada!")
            print(f"📹 Título: {info.get('title', 'Desconocido')}")
            print(f"⏱️ Duración: {info.get('duration_string', 'Desconocida')}")

    except Exception as e:
        print(f"❌ Error al descargar: {str(e)}")
        return False
    
    return True

def main():
    try:    
        while True:
            print("\n" + "=" * 50)
            print("🎬 DESCARGADOR DE YOUTUBE")
            print("=" * 50)
            print("1. Descargar video")
            print("2. Descargar solo audio")
            print("3. Descargar playlist")
            print("4. Salir")
            print("=" * 50)

            opcion = input("Selecciona una opción (1-4): ").strip()
            if opcion == '4':
                subprocess.run(['clear'])
                print(colored("\n\n\nSaliendo del programa ...","red"))
                sys.exit(1)
            
            if opcion == '1':
                url = input("\n🔗 Ingresa la URL del video: ").strip()
                if not url:
                    print("❌ URL no válida")
                    continue

                print("\n🎯 Calidades disponibles:")
                print("1. Mejor calidad (best)")
                print("2. 1080p")
                print("3. 720p")
                print("4. 480p")
                print("5. 360p")
                print("6. Peor calidad (worst)")
                calidad_opcion = input("Selecciona calidad (1-6): ").strip()

                calidades = {
                    '1': 'best',
                    '2': '1080p',
                    '3': '720p',
                    '4': '480p',
                    '5': '360p',
                    '6': 'worst'
                    }
                calidad = calidades.get(calidad_opcion, 'best')
                descargar_video(url, calidad)
            if opcion == '2':
                url = input("\n🔗 Ingresa la URL del video: ").strip()
                if not url:
                    print("❌ URL no válida")
                    continue
                
                formato = input("Formato de audio (mp3/m4a/wav) [m4a]: ").strip() or 'm4a'
                descargar_audio(url, formato)
            
            if opcion == '3':
                url = input("\n🔗 Ingresa la URL de la playlist: ").strip()
                if not url:
                    print("❌ URL no válida")
                    continue

                print("\n🎯 Calidades disponibles:")
                print("1. Mejor calidad (best)")
                print("2. 1080p")
                print("3. 720p")
                print("4. 480p")
                print("5. 360p")
                print("6. Peor calidad (worst)")
                calidad_opcion = input("Selecciona calidad (1-6): ").strip()

                calidades = {
                    '1': 'best',
                    '2': '1080p',
                    '3': '720p',
                    '4': '480p',
                    '5': '360p',
                    '6': 'worst'
                    }
                calidad = calidades.get(calidad_opcion, 'best')

                descargar_playlist(url, calidad)

        

            

    except KeyboardInterrupt:
        subprocess.run(['clear'])
        print(colored("\n\n\nSaliendo del programa ...","red"))
    except Exception as e:
        print("f\n❌  Error inesperado {str(e)}")



if __name__=='__main__':
    main()

