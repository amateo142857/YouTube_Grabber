#!/usr/bin/env python3
"""
Descargador de YouTube con Interfaz CustomTkinter
Requisitos: pip install customtkinter yt-dlp pillow
"""

import yt_dlp
import os
import sys
import threading
import tkinter as tk
from tkinter import messagebox, filedialog
from pathlib import Path
from datetime import datetime
import customtkinter as ctk
from PIL import Image, ImageTk
import re

# ===== CONFIGURACIÓN DE COLORES MEJORADA =====
# Colores más claros y azules
COLOR_FONDO = "#1a1a2e"           # Fondo principal (azul oscuro suave)
COLOR_FONDO2 = "#16213e"          # Fondo secundario (azul más claro)
COLOR_FONDO3 = "#0f3460"          # Fondo terciario (azul medio)
COLOR_TARJETA = "#1a2744"         # Color de tarjetas
COLOR_TARJETA_HOVER = "#243b6e"   # Tarjeta hover
COLOR_TEXTO = "#e8f0fe"           # Texto principal (blanco azulado)
COLOR_TEXTO2 = "#a8c8ff"          # Texto secundario (azul claro)
COLOR_ACENTO = "#2196F3"          # Azul principal
COLOR_ACENTO2 = "#64B5F6"         # Azul claro
COLOR_ACENTO3 = "#1976D2"         # Azul oscuro
COLOR_ACENTO4 = "#BBDEFB"         # Azul muy claro
COLOR_BOTON = "#1e88e5"           # Botón principal (azul intenso)
COLOR_BOTON_HOVER = "#42a5f5"     # Botón hover (azul más claro)
COLOR_BOTON_DISABLED = "#546e7a"  # Botón deshabilitado
COLOR_SUCCESS = "#4CAF50"         # Verde éxito
COLOR_ERROR = "#EF5350"           # Rojo error
COLOR_WARNING = "#FFA726"         # Naranja warning
COLOR_BARRA_PROGRESO = "#42a5f5"  # Barra de progreso

# Configurar tema de CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ===== VARIABLES GLOBALES =====
root = None
main_frame = None

# Variables de control
url_var = None
calidad_var = None
tipo_var = None
formato_audio_var = None
ruta_var = None
descargando = False

# Variables para widgets que necesitamos modificar
url_entry = None
download_btn = None
progress_bar = None
progress_label = None
log_text = None
audio_frame = None
audio_combo = None

# ===== FUNCIONES DE UTILIDAD =====

def center_window():
    """Centrar la ventana en la pantalla"""
    global root
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

# ===== FUNCIONES DE LOG =====

def log_info(mensaje):
    """Agregar mensaje informativo al log"""
    global log_text
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_text.insert(tk.END, f"[{timestamp}] ℹ️ {mensaje}\n")
    log_text.see(tk.END)
    log_text.update_idletasks()

def log_error(mensaje):
    """Agregar mensaje de error al log"""
    global log_text
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_text.insert(tk.END, f"[{timestamp}] ❌ {mensaje}\n")
    log_text.see(tk.END)
    log_text.update_idletasks()

def log_success(mensaje):
    """Agregar mensaje de éxito al log"""
    global log_text
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_text.insert(tk.END, f"[{timestamp}] ✅ {mensaje}\n")
    log_text.see(tk.END)
    log_text.update_idletasks()

def limpiar_log():
    """Limpiar el log"""
    global log_text
    log_text.delete(1.0, tk.END)
    log_info("🗑️ Log limpiado")

# ===== FUNCIONES DE INTERFAZ =====

def actualizar_opciones():
    """Mostrar/ocultar opciones según el tipo de descarga"""
    global audio_frame, tipo_var
    if tipo_var.get() == "audio":
        audio_frame.pack(fill=tk.X, pady=10)
    else:
        audio_frame.pack_forget()

def pegar_url():
    """Pegar URL desde el portapapeles"""
    global root, url_var
    try:
        url = root.clipboard_get()
        if "youtu" in url.lower():
            url_var.set(url)
            log_info(f"📋 URL pegada: {url[:50]}...")
        else:
            log_error("❌ La URL del portapapeles no parece ser de YouTube")
            messagebox.showwarning("URL Inválida", 
                                "La URL del portapapeles no parece ser de YouTube")
    except:
        log_error("❌ No se pudo obtener la URL del portapapeles")
        messagebox.showerror("Error", "No se pudo acceder al portapapeles")

def seleccionar_carpeta():
    """Abrir diálogo para seleccionar carpeta"""
    global ruta_var
    carpeta = filedialog.askdirectory(
        title="Seleccionar carpeta de descarga",
        initialdir=ruta_var.get()
    )
    if carpeta:
        ruta_var.set(carpeta)
        log_info(f"📁 Carpeta seleccionada: {carpeta}")

def mostrar_info():
    """Mostrar información del programa"""
    info = """🎬 Descargador de Videos de Youtube

Características:
• ✨ Interfaz moderna con CustomTkinter
• 📥 Descarga videos en múltiples calidades
• 🎵 Extracción de audio en varios formatos
• 📊 Barra de progreso en tiempo real
• 📁 Selección de carpeta de destino
• 🔗 Soporte para URLs de playlists
• 📋 Pegado automático desde portapapeles
• 🎨 Diseño responsive y adaptativo

Requisitos:
• Python 3.6+
• customtkinter
• yt-dlp
• ffmpeg (para audio)
• Pillow

Tecnologías:
• CustomTkinter - Interfaz moderna
• yt-dlp - Descarga de YouTube
• threading - Descargas en segundo plano

Desarrollado por Alejandro Mateo"""
    
    messagebox.showinfo("ℹ️ Información", info)

# ===== FUNCIONES DE PROGRESO =====

def actualizar_progreso(valor):
    """Actualizar barra de progreso desde el hilo principal"""
    global progress_bar, progress_label
    progress_bar.set(min(valor / 100, 1.0))
    progress_label.configure(text=f"📥 Descargando... {int(valor)}%")
    root.update_idletasks()

def progreso_hook(d):
    """Hook para actualizar la barra de progreso"""
    if d['status'] == 'downloading':
        if 'total_bytes' in d:
            porcentaje = (d['downloaded_bytes'] / d['total_bytes']) * 100
            actualizar_progreso(porcentaje)
        elif 'total_bytes_estimate' in d:
            porcentaje = (d['downloaded_bytes'] / d['total_bytes_estimate']) * 100
            actualizar_progreso(porcentaje)
    elif d['status'] == 'finished':
        actualizar_progreso(100)

# ===== FUNCIONES DE DESCARGA =====

def descargar_video(url, calidad, ruta):
    """Descargar video con las opciones seleccionadas"""
    ydl_opts = {
        'outtmpl': f'{ruta}/%(title)s.%(ext)s',
        'progress_hooks': [progreso_hook],
        'ignoreerrors': True,
        'nooverwrites': True,
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
    }
    
    # Configurar calidad
    if calidad == 'best':
        ydl_opts['format'] = 'bestvideo+bestaudio/best'
    elif calidad == 'worst':
        ydl_opts['format'] = 'worst'
    else:
        height = calidad.replace('p', '')
        ydl_opts['format'] = f'bestvideo[height<={height}]+bestaudio/best[height<={height}]'
    
    log_info(f"📥 Iniciando descarga: {url}")
    log_info(f"📁 Carpeta: {ruta}")
    log_info(f"🎯 Calidad: {calidad}")
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        titulo = info.get('title', 'Desconocido')
        duracion = info.get('duration_string', 'Desconocida')
        
        log_success(f"✅ Video descargado: {titulo}")
        log_info(f"⏱️ Duración: {duracion}")
        log_info(f"📂 Ubicación: {ruta}")

def descargar_audio(url, formato, ruta):
    """Descargar solo el audio"""
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': formato,
            'preferredquality': '192',
        }],
        'outtmpl': f'{ruta}/%(title)s.%(ext)s',
        'progress_hooks': [progreso_hook],
        'quiet': True,
        'no_warnings': True,
    }
    
    log_info(f"🎵 Iniciando descarga de audio: {url}")
    log_info(f"📁 Carpeta: {ruta}")
    log_info(f"🎵 Formato: {formato}")
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        titulo = info.get('title', 'Desconocido')
        
        log_success(f"✅ Audio descargado: {titulo}.{formato}")
        log_info(f"📂 Ubicación: {ruta}")

def descargar():
    """Función de descarga ejecutada en hilo separado"""
    global descargando, download_btn, progress_bar, progress_label
    global url_var, calidad_var, tipo_var, formato_audio_var, ruta_var
    
    try:
        url = url_var.get().strip()
        calidad = calidad_var.get()
        tipo = tipo_var.get()
        ruta = ruta_var.get()
        
        # Crear carpeta si no existe
        Path(ruta).mkdir(parents=True, exist_ok=True)
        
        if tipo == "video":
            descargar_video(url, calidad, ruta)
        else:
            formato = formato_audio_var.get()
            descargar_audio(url, formato, ruta)
            
    except Exception as e:
        log_error(f"❌ Error: {str(e)}")
        messagebox.showerror("Error", f"Error al descargar:\n{str(e)}")
    finally:
        descargando = False
        download_btn.configure(state="normal", text="⬇️  DESCARGAR AHORA")
        progress_label.configure(text="✅ Descarga completada")
        progress_bar.set(1.0)

def iniciar_descarga():
    """Iniciar el proceso de descarga en un hilo separado"""
    global descargando, download_btn, progress_bar, progress_label, url_var
    
    if descargando:
        messagebox.showwarning("Advertencia", "Ya hay una descarga en progreso")
        return
    
    url = url_var.get().strip()
    if not url:
        messagebox.showerror("Error", "Por favor ingresa una URL válida")
        return
    
    # Validar URL
    if not re.match(r'^https?://(www\.)?(youtube\.com|youtu\.be)/', url):
        messagebox.showerror("Error", "URL de YouTube inválida")
        return
    
    # Deshabilitar botón
    download_btn.configure(state="disabled", text="⏳ DESCARGANDO...")
    descargando = True
    progress_bar.set(0)
    progress_label.configure(text="⏳ Iniciando descarga...")
    
    # Iniciar hilo de descarga
    thread = threading.Thread(target=descargar, daemon=True)
    thread.start()

# ===== CREACIÓN DE LA INTERFAZ =====

def create_widgets():
    """Crear todos los widgets de la interfaz"""
    global root, main_frame, url_var, calidad_var, tipo_var, formato_audio_var, ruta_var
    global url_entry, download_btn, progress_bar, progress_label, log_text
    global audio_frame, audio_combo
    
    # Inicializar variables
    url_var = ctk.StringVar()
    calidad_var = ctk.StringVar(value="best")
    tipo_var = ctk.StringVar(value="video")
    formato_audio_var = ctk.StringVar(value="mp3")
    ruta_var = ctk.StringVar(value="./descargas")
    
    # Frame principal con scroll
    main_frame = ctk.CTkScrollableFrame(
        root,
        fg_color="transparent"
    )
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    # ===== HEADER =====
    header_frame = ctk.CTkFrame(
        main_frame,
        fg_color=COLOR_TARJETA,
        corner_radius=15
    )
    header_frame.pack(fill=tk.X, pady=(0, 20), padx=10)
    
    # Título principal
    title_label = ctk.CTkLabel(
        header_frame,
        text="📥 Descargador de videos de Youtube",
        font=ctk.CTkFont(size=32, weight="bold"),
        text_color=COLOR_ACENTO2
    )
    title_label.pack(pady=(20, 5))
    
    # Subtítulo
    subtitle_label = ctk.CTkLabel(
        header_frame,
        text="Descarga videos y música de YouTube con estilo profesional",
        font=ctk.CTkFont(size=14),
        text_color=COLOR_TEXTO2
    )
    subtitle_label.pack(pady=(0, 20))
    
    # ===== SECCIÓN URL =====
    url_frame = ctk.CTkFrame(
        main_frame,
        fg_color=COLOR_TARJETA,
        corner_radius=15
    )
    url_frame.pack(fill=tk.X, pady=(0, 20), padx=10)
    
    url_label = ctk.CTkLabel(
        url_frame,
        text="📎 URL del Video",
        font=ctk.CTkFont(size=16, weight="bold"),
        text_color=COLOR_TEXTO
    )
    url_label.pack(pady=(15, 10))
    
    # Contenedor para entry y botón pegar
    url_container = ctk.CTkFrame(url_frame, fg_color="transparent")
    url_container.pack(fill=tk.X, padx=20, pady=(0, 15))
    
    url_entry = ctk.CTkEntry(
        url_container,
        textvariable=url_var,
        placeholder_text="https://www.youtube.com/watch?v=...",
        font=ctk.CTkFont(size=14),
        height=45,
        corner_radius=10,
        border_width=2,
        border_color=COLOR_ACENTO,
        fg_color=COLOR_FONDO2
    )
    url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
    url_entry.bind('<Return>', lambda e: iniciar_descarga())
    
    paste_btn = ctk.CTkButton(
        url_container,
        text="📋 Pegar",
        font=ctk.CTkFont(size=14, weight="bold"),
        height=45,
        width=100,
        corner_radius=10,
        fg_color=COLOR_ACENTO3,
        hover_color=COLOR_ACENTO,
        text_color=COLOR_TEXTO,
        command=pegar_url
    )
    paste_btn.pack(side=tk.RIGHT)
    
    # ===== SECCIÓN OPCIONES =====
    options_frame = ctk.CTkFrame(
        main_frame,
        fg_color=COLOR_TARJETA,
        corner_radius=15
    )
    options_frame.pack(fill=tk.X, pady=(0, 20), padx=10)
    
    options_label = ctk.CTkLabel(
        options_frame,
        text="⚙️ Configuración",
        font=ctk.CTkFont(size=16, weight="bold"),
        text_color=COLOR_TEXTO
    )
    options_label.pack(pady=(15, 15))
    
    # Grid para opciones
    options_grid = ctk.CTkFrame(options_frame, fg_color="transparent")
    options_grid.pack(fill=tk.X, padx=20, pady=(0, 15))
    
    # ===== TIPO DE DESCARGA =====
    tipo_frame = ctk.CTkFrame(options_grid, fg_color="transparent")
    tipo_frame.pack(fill=tk.X, pady=5)
    
    tipo_label = ctk.CTkLabel(
        tipo_frame,
        text="📂 Tipo:",
        font=ctk.CTkFont(size=14, weight="bold"),
        width=120,
        text_color=COLOR_TEXTO
    )
    tipo_label.pack(side=tk.LEFT, padx=(0, 20))
    
    # Radio buttons personalizados
    video_rb = ctk.CTkRadioButton(
        tipo_frame,
        text="🎥 Video",
        variable=tipo_var,
        value="video",
        font=ctk.CTkFont(size=14),
        command=actualizar_opciones,
        border_color=COLOR_ACENTO,
        fg_color=COLOR_ACENTO,
        hover_color=COLOR_ACENTO2,
        text_color=COLOR_TEXTO
    )
    video_rb.pack(side=tk.LEFT, padx=(0, 20))
    
    audio_rb = ctk.CTkRadioButton(
        tipo_frame,
        text="🎵 Audio",
        variable=tipo_var,
        value="audio",
        font=ctk.CTkFont(size=14),
        command=actualizar_opciones,
        border_color=COLOR_ACENTO,
        fg_color=COLOR_ACENTO,
        hover_color=COLOR_ACENTO2,
        text_color=COLOR_TEXTO
    )
    audio_rb.pack(side=tk.LEFT)
    
    # ===== CALIDAD =====
    calidad_frame = ctk.CTkFrame(options_grid, fg_color="transparent")
    calidad_frame.pack(fill=tk.X, pady=10)
    
    calidad_label = ctk.CTkLabel(
        calidad_frame,
        text="🎯 Calidad:",
        font=ctk.CTkFont(size=14, weight="bold"),
        width=120,
        text_color=COLOR_TEXTO
    )
    calidad_label.pack(side=tk.LEFT, padx=(0, 20))
    
    # Contenedor para botones de calidad
    calidad_container = ctk.CTkFrame(calidad_frame, fg_color="transparent")
    calidad_container.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    calidades = [
        ("⭐ Mejor", "best"),
        ("1080p", "1080p"),
        ("720p", "720p"),
        ("480p", "480p"),
        ("360p", "360p"),
        ("Peor", "worst")
    ]
    
    # Crear radio buttons de calidad
    for texto, valor in calidades:
        rb = ctk.CTkRadioButton(
            calidad_container,
            text=texto,
            variable=calidad_var,
            value=valor,
            font=ctk.CTkFont(size=13),
            border_color=COLOR_ACENTO,
            fg_color=COLOR_ACENTO,
            hover_color=COLOR_ACENTO2,
            text_color=COLOR_TEXTO
        )
        rb.pack(side=tk.LEFT, padx=(0, 15))
    
    # ===== FORMATO DE AUDIO (oculto inicialmente) =====
    audio_frame = ctk.CTkFrame(options_grid, fg_color="transparent")
    
    audio_label = ctk.CTkLabel(
        audio_frame,
        text="🎵 Formato:",
        font=ctk.CTkFont(size=14, weight="bold"),
        width=120,
        text_color=COLOR_TEXTO
    )
    audio_label.pack(side=tk.LEFT, padx=(0, 20))
    
    formatos_audio = ["mp3", "m4a", "wav", "flac", "aac", "opus"]
    audio_combo = ctk.CTkComboBox(
        audio_frame,
        variable=formato_audio_var,
        values=formatos_audio,
        font=ctk.CTkFont(size=14),
        width=150,
        state="readonly",
        corner_radius=10,
        border_width=2,
        border_color=COLOR_ACENTO,
        fg_color=COLOR_FONDO2,
        button_color=COLOR_ACENTO,
        button_hover_color=COLOR_ACENTO2
    )
    audio_combo.pack(side=tk.LEFT)
    audio_combo.set("mp3")
    
    # ===== CARPETA DE DESCARGA =====
    ruta_frame = ctk.CTkFrame(options_grid, fg_color="transparent")
    ruta_frame.pack(fill=tk.X, pady=10)
    
    ruta_label = ctk.CTkLabel(
        ruta_frame,
        text="📁 Guardar en:",
        font=ctk.CTkFont(size=14, weight="bold"),
        width=120,
        text_color=COLOR_TEXTO
    )
    ruta_label.pack(side=tk.LEFT, padx=(0, 20))
    
    ruta_entry = ctk.CTkEntry(
        ruta_frame,
        textvariable=ruta_var,
        font=ctk.CTkFont(size=14),
        height=40,
        corner_radius=10,
        border_width=2,
        border_color=COLOR_ACENTO,
        fg_color=COLOR_FONDO2
    )
    ruta_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
    
    ruta_btn = ctk.CTkButton(
        ruta_frame,
        text="📂",
        font=ctk.CTkFont(size=16),
        height=40,
        width=60,
        corner_radius=10,
        fg_color=COLOR_ACENTO3,
        hover_color=COLOR_ACENTO,
        text_color=COLOR_TEXTO,
        command=seleccionar_carpeta
    )
    ruta_btn.pack(side=tk.RIGHT)
    
    # ===== BOTÓN DE DESCARGA (MEJORADO) =====
    download_btn = ctk.CTkButton(
        main_frame,
        text="⬇️  DESCARGAR AHORA",
        font=ctk.CTkFont(size=20, weight="bold"),
        height=65,
        corner_radius=15,
        fg_color=COLOR_BOTON,
        hover_color=COLOR_BOTON_HOVER,
        text_color="white",
        border_width=2,
        border_color=COLOR_ACENTO4,
        command=iniciar_descarga
    )
    download_btn.pack(fill=tk.X, pady=(0, 15), padx=10)
    
    # ===== BARRA DE PROGRESO =====
    progress_frame = ctk.CTkFrame(
        main_frame,
        fg_color=COLOR_TARJETA,
        corner_radius=15
    )
    progress_frame.pack(fill=tk.X, pady=(0, 15), padx=10)
    
    progress_label = ctk.CTkLabel(
        progress_frame,
        text="💡 Listo para descargar",
        font=ctk.CTkFont(size=14),
        text_color=COLOR_TEXTO2
    )
    progress_label.pack(pady=(15, 10))
    
    progress_bar = ctk.CTkProgressBar(
        progress_frame,
        orientation="horizontal",
        height=22,
        corner_radius=10,
        fg_color=COLOR_FONDO2,
        progress_color=COLOR_BARRA_PROGRESO,
        border_width=1,
        border_color=COLOR_ACENTO
    )
    progress_bar.pack(fill=tk.X, padx=20, pady=(0, 15))
    progress_bar.set(0)
    
    # ===== LOG DE EVENTOS =====
    log_frame = ctk.CTkFrame(
        main_frame,
        fg_color=COLOR_TARJETA,
        corner_radius=15
    )
    log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15), padx=10)
    
    log_header = ctk.CTkFrame(log_frame, fg_color="transparent")
    log_header.pack(fill=tk.X, padx=20, pady=(15, 10))
    
    log_label = ctk.CTkLabel(
        log_header,
        text="📋 Registro de Eventos",
        font=ctk.CTkFont(size=16, weight="bold"),
        text_color=COLOR_TEXTO
    )
    log_label.pack(side=tk.LEFT)
    
    # Botones de control del log
    log_buttons = ctk.CTkFrame(log_header, fg_color="transparent")
    log_buttons.pack(side=tk.RIGHT)
    
    clear_btn = ctk.CTkButton(
        log_buttons,
        text="🗑️ Limpiar",
        font=ctk.CTkFont(size=12, weight="bold"),
        height=32,
        width=100,
        corner_radius=8,
        fg_color=COLOR_ACENTO3,
        hover_color=COLOR_ACENTO,
        text_color=COLOR_TEXTO,
        command=limpiar_log
    )
    clear_btn.pack(side=tk.LEFT, padx=(0, 10))
    
    info_btn = ctk.CTkButton(
        log_buttons,
        text="ℹ️ Información",
        font=ctk.CTkFont(size=12, weight="bold"),
        height=32,
        width=100,
        corner_radius=8,
        fg_color=COLOR_ACENTO3,
        hover_color=COLOR_ACENTO,
        text_color=COLOR_TEXTO,
        command=mostrar_info
    )
    info_btn.pack(side=tk.LEFT)
    
    # Área de log
    log_text = ctk.CTkTextbox(
        log_frame,
        font=ctk.CTkFont(family="Consolas", size=12),
        corner_radius=10,
        border_width=2,
        border_color=COLOR_ACENTO,
        fg_color=COLOR_FONDO2,
        text_color=COLOR_TEXTO
    )
    log_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

# ===== FUNCIÓN PRINCIPAL =====

def main():
    """Función principal"""
    global root
    
    try:
        import yt_dlp
    except ImportError:
        root = ctk.CTk()
        root.withdraw()
        messagebox.showerror(
            "Error",
            "❌ yt-dlp no está instalado.\n\n"
            "Instálalo con:\n"
            "pip install yt-dlp\n\n"
            "En entorno virtual: source venv/bin/activate"
        )
        sys.exit(1)
    
    # Crear ventana principal
    root = ctk.CTk()
    root.title("Descargador de videos de Youtube")
    root.geometry("1000x800")
    root.minsize(900, 700)
    root.configure(fg_color=COLOR_FONDO)

    # Icono de la ventana
    try:
        icono1 = Image.open("img/icono1.png")
        icono_ventana = ImageTk.PhotoImage(icono1)
        root.iconphoto(False, icono_ventana)
    except:
        pass  # Si no encuentra el icono, continúa sin él
    
    # Crear widgets
    create_widgets()
    
    # Centrar ventana
    center_window()
    
    # Log inicial
    log_info("🚀 Descargador de Videos iniciado")
    log_info("💡 Ingresa una URL y presiona Enter o haz clic en DESCARGAR")
    
    # Iniciar la aplicación
    root.mainloop()

if __name__ == "__main__":
    main()