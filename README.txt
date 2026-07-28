# 📥 YouTube Downloader (yt-dlp)

Este proyecto contiene dos descargadores de YouTube:
1. **Versión Terminal (CLI)**: interactiva en consola, con menú y barra de progreso.
2. **Versión Tkinter (GUI)**: aplicación gráfica con botones, barra de progreso y opciones.

---

## 🚀 Características
- Descarga videos en múltiples calidades (best, 1080p, 720p, 480p, 360p, worst).
- Descarga solo audio en varios formatos (mp3, m4a, wav, flac, aac).
- Descarga playlists completas.
- Barra de progreso en tiempo real (CLI y GUI).
- Selección de carpeta de destino (GUI).
- Registro de eventos y mensajes claros.

---

## 📦 Dependencias
Instala las siguientes librerías antes de ejecutar:

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) → motor de descarga
- ffmpeg → requerido para extracción de audio
- termcolor → para colores en la versión terminal
- pillow → para manejo de iconos en la versión Tkinter
- tkinter → interfaz gráfica (ya incluido en Python estándar)

Instalación rápida:
```bash
pip install yt-dlp termcolor pillow

