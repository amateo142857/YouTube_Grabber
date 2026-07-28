#!/usr/bin/env python3
"""
Descargador de YouTube con Interfaz Gráfica
Requisitos: pip install yt-dlp
"""

import yt_dlp
import os
import sys
import threading
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from pathlib import Path
from datetime import datetime

# Variables globales
url_var = None
calidad_var = None
tipo_var = None
formato_audio_var = None
ruta_var = None
descargando = False

COLORES = {
    'bg': '#0a1a1a',          # Fondo principal (verde azulado muy oscuro)
    'bg2': '#122a2a',         # Fondo secundario (verde profundo)
    'fg': '#d4fff4',          # Texto claro (verde-azulado muy suave)
    'acento': '#00bcd4',      # Azul brillante (acento principal)
    'acento_oscuro': '#006064', # Azul oscuro
    'acento_claro': '#4dd0e1',  # Azul claro
    'success': '#4caf50',     # Verde éxito
    'entry_bg': '#1a3d3d',    # Fondo de entrada (verde azulado)
    'button_bg': '#00796b',   # Fondo botón (verde intenso)
    'button_fg': '#ffffff',   # Texto botón
    'frame_bg': '#122a2a',    # Fondo frame
}

def setup_styles():
    """Configurar estilos de la interfaz"""
    style = ttk.Style()
    style.theme_use('clam')
    
    # Configurar colores para ttk
    style.configure('TFrame', background=COLORES['bg'])
    style.configure('TLabel', background=COLORES['bg'], foreground=COLORES['fg'])
    style.configure('TLabelframe', background=COLORES['bg'], foreground=COLORES['acento'])
    style.configure('TLabelframe.Label', background=COLORES['bg'], foreground=COLORES['acento'])
    style.configure('TButton', background=COLORES['button_bg'], foreground=COLORES['button_fg'])
    style.configure('Accent.TButton', background=COLORES['acento'], foreground=COLORES['button_fg'])
    style.map('Accent.TButton',
            background=[('active', COLORES['acento_claro']),
                        ('disabled', COLORES['acento_oscuro'])])
    style.configure('TEntry', fieldbackground=COLORES['entry_bg'], foreground=COLORES['fg'])
    style.configure('TCombobox', fieldbackground=COLORES['entry_bg'], foreground=COLORES['fg'])
    style.configure('TRadiobutton', background=COLORES['bg'], foreground=COLORES['fg'])
    style.map('TRadiobutton',
            background=[('active', COLORES['bg'])],
            foreground=[('active', COLORES['acento'])])
    style.configure('TProgressbar', background=COLORES['acento'])

def center_window(root):
    """Centrar la ventana en la pantalla"""
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

def pegar_url(root, log_text):
    """Pegar URL desde el portapapeles"""
    global url_var
    try:
        url = root.clipboard_get()
        if "https://youtu" in url:
            url_var.set(url)   # type: ignore
            log_info(log_text, f"📋 URL pegada: {url[:50]}...")
        else:
            log_error(log_text, "[!]  La url de su portapapeles no es valida")
    except:
        log_error(log_text, "❌ No se pudo obtener la URL del portapapeles")

def seleccionar_carpeta(log_text):
    """Abrir diálogo para seleccionar carpeta"""
    global ruta_var
    carpeta = filedialog.askdirectory(
        title="Seleccionar carpeta de descarga",
        initialdir=ruta_var.get() # type: ignore
    )
    if carpeta:
        ruta_var.set(carpeta) # type:ignore
        log_info(log_text, f"📁 Carpeta seleccionada: {carpeta}")

def actualizar_opciones(audio_frame):
    """Mostrar/ocultar opciones según el tipo de descarga"""
    global tipo_var
    if tipo_var.get() == "audio": #type: ignore
        audio_frame.pack(fill=tk.X, pady=5)
    else:
        audio_frame.pack_forget()

def log_info(log_text, mensaje):
    """Agregar mensaje informativo al log"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_text.insert(tk.END, f"[{timestamp}] ℹ️ {mensaje}\n")
    log_text.see(tk.END)

def log_error(log_text, mensaje):
    """Agregar mensaje de error al log"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_text.insert(tk.END, f"[{timestamp}] ❌ {mensaje}\n")
    log_text.see(tk.END)

def log_success(log_text, mensaje):
    """Agregar mensaje de éxito al log"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_text.insert(tk.END, f"[{timestamp}] ✅ {mensaje}\n")
    log_text.see(tk.END)

def limpiar_log(log_text):
    """Limpiar el log"""
    log_text.delete(1.0, tk.END)

def mostrar_info():
    """Mostrar información del programa"""
    info = """
Descargador de videos de Youtebe 

Características:
• Descarga de videos en múltiples calidades
• Extracción de audio en varios formatos
• Barra de progreso en tiempo real
• Selección de carpeta de destino
• Soporte para URLs de playlists

Requisitos:
• Python 3.6+
• yt-dlp
• ffmpeg (para audio)

Desarrollado por Alejandro Mateo
    """
    messagebox.showinfo("Información", info)

def actualizar_progreso(progress_bar, progress_label, valor):
    """Actualizar barra de progreso desde el hilo principal"""
    progress_bar['value'] = min(valor, 100)
    progress_label.config(text=f"Descargando... {int(valor)}%")
    progress_bar.update_idletasks()

def progreso_hook(progress_bar, progress_label, d):
    """Hook para actualizar la barra de progreso"""
    if d['status'] == 'downloading':
        if 'total_bytes' in d:
            porcentaje = (d['downloaded_bytes'] / d['total_bytes']) * 100
            actualizar_progreso(progress_bar, progress_label, porcentaje)
        elif 'total_bytes_estimate' in d:
            porcentaje = (d['downloaded_bytes'] / d['total_bytes_estimate']) * 100
            actualizar_progreso(progress_bar, progress_label, porcentaje)
    elif d['status'] == 'finished':
        actualizar_progreso(progress_bar, progress_label, 100)

def descargar_video(url, calidad, ruta, log_text, progress_bar, progress_label):
    """Descargar video con las opciones seleccionadas"""
    ydl_opts = {
        'outtmpl': f'{ruta}/%(title)s.%(ext)s',
        'progress_hooks': [lambda d: progreso_hook(progress_bar, progress_label, d)],
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
    
    log_info(log_text, f"📥 Iniciando descarga: {url}")
    log_info(log_text, f"📁 Carpeta: {ruta}")
    log_info(log_text, f"🎯 Calidad: {calidad}")
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl: # type: ignore
        info = ydl.extract_info(url, download=True)
        titulo = info.get('title', 'Desconocido')
        duracion = info.get('duration_string', 'Desconocida')
        
        log_success(log_text, f"✅ Video descargado: {titulo}")
        log_info(log_text, f"⏱️ Duración: {duracion}")

def descargar_audio(url, formato, ruta, log_text, progress_bar, progress_label):
    """Descargar solo el audio"""
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': formato,
            'preferredquality': '192',
        }],
        'outtmpl': f'{ruta}/%(title)s.%(ext)s',
        'progress_hooks': [lambda d: progreso_hook(progress_bar, progress_label, d)],
        'quiet': True,
        'no_warnings': True,
    }
    
    log_info(log_text, f"🎵 Iniciando descarga de audio: {url}")
    log_info(log_text, f"📁 Carpeta: {ruta}")
    log_info(log_text, f"🎵 Formato: {formato}")
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl: # type: ignore
        info = ydl.extract_info(url, download=True)
        titulo = info.get('title', 'Desconocido')
        
        log_success(log_text, f"✅ Audio descargado: {titulo}.{formato}")

def descargar(root, download_btn, progress_bar, progress_label, log_text):
    """Función de descarga ejecutada en hilo separado"""
    global descargando, url_var, calidad_var, tipo_var, formato_audio_var, ruta_var
    try:
        url = url_var.get().strip() # type: ignore
        calidad = calidad_var.get() # type: ignore
        tipo = tipo_var.get() # type: ignore
        ruta = ruta_var.get() # type: ignore
        
        # Crear carpeta si no existe
        Path(ruta).mkdir(parents=True, exist_ok=True)
        
        if tipo == "video":
            descargar_video(url, calidad, ruta, log_text, progress_bar, progress_label)
        else:
            formato = formato_audio_var.get() # type: ignore
            descargar_audio(url, formato, ruta, log_text, progress_bar, progress_label)
            
    except Exception as e:
        log_error(log_text, f"❌ Error: {str(e)}")
        messagebox.showerror("Error", f"Error al descargar:\n{str(e)}")
    finally:
        descargando = False
        download_btn.config(state=tk.NORMAL, text="⬇️ DESCARGAR")
        progress_label.config(text="✅ Descarga completada")
        progress_bar['value'] = 100

def iniciar_descarga(root, download_btn, progress_bar, progress_label, log_text):
    """Iniciar el proceso de descarga en un hilo separado"""
    global descargando, url_var
    
    if descargando:
        messagebox.showwarning("Advertencia", "Ya hay una descarga en progreso")
        return
        
    url = url_var.get().strip() # type: ignore
    if not url:
        messagebox.showerror("Error", "Por favor ingresa una URL válida")
        return
        
    # Deshabilitar botón
    download_btn.config(state=tk.DISABLED, text="⏳ Descargando...")
    descargando = True
    progress_bar['value'] = 0
    progress_label.config(text="Iniciando descarga...")
    
    # Iniciar hilo de descarga
    thread = threading.Thread(
        target=descargar,
        args=(root, download_btn, progress_bar, progress_label, log_text),
        daemon=True
    )
    thread.start()

def create_widgets(root):
    """Crear todos los widgets de la interfaz"""
    global url_var, calidad_var, tipo_var, formato_audio_var, ruta_var
    
    # Inicializar variables Tkinter después de crear la ventana
    url_var = tk.StringVar()
    calidad_var = tk.StringVar(value="best")
    tipo_var = tk.StringVar(value="video")
    formato_audio_var = tk.StringVar(value="mp3")
    ruta_var = tk.StringVar(value="./descargas")
    
    # Configurar estilo
    setup_styles()
    root.configure(bg=COLORES['bg'])
    
    # Frame principal con scroll
    main_frame = ttk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    # Título
    title_label = tk.Label(
        main_frame,
        text="📥 Descargador de videos de Youtube 📥",
        font=('Arial', 24, 'bold'),
        bg=COLORES['bg'],
        fg=COLORES['acento']
    )
    title_label.pack(pady=(0, 20))
    
    # Subtítulo
    subtitle_label = tk.Label(
        main_frame,
        text="Descarga tus videos favoritos con estilo",
        font=('Arial', 16),
        bg=COLORES['bg'],
        fg=COLORES['fg']
    )
    subtitle_label.pack(pady=(0, 15))
    
    # Frame de URL
    url_frame = ttk.LabelFrame(main_frame, text="🔗 URL del Video", padding=10)
    url_frame.pack(fill=tk.X,pady=(0, 15))
    
    url_entry = ttk.Entry(
        url_frame,
        textvariable=url_var,
        font=('Arial', 16)
    )
    url_entry.pack(fill=tk.X, ipady=5)
    url_entry.bind('<Return>', lambda e: iniciar_descarga(root, download_btn, progress_bar, progress_label, log_text))
    
    # Botón pegar
    paste_btn = ttk.Button(
        url_frame,
        text="📋 Portapapeles",
        command=lambda: pegar_url(root, log_text)
    )
    paste_btn.pack(pady=(5, 0))
    
    # Frame de opciones
    options_frame = ttk.LabelFrame(main_frame, text="⚙️ Opciones", padding=10)
    options_frame.pack(fill=tk.X, pady=(0, 15))
    
    # Tipo de descarga
    tipo_frame = ttk.Frame(options_frame)
    tipo_frame.pack(fill=tk.X, pady=5)
    
    ttk.Label(tipo_frame, text="Tipo:").pack(side=tk.LEFT, padx=(0, 10))
    
    video_radio = ttk.Radiobutton(
        tipo_frame,
        text="🎥 Video",
        variable=tipo_var,
        value="video",
        command=lambda: actualizar_opciones(audio_frame)
    )
    video_radio.pack(side=tk.LEFT, padx=(0, 10))
    
    audio_radio = ttk.Radiobutton(
        tipo_frame,
        text="🎵 Audio",
        variable=tipo_var,
        value="audio",
        command=lambda: actualizar_opciones(audio_frame)
    )
    audio_radio.pack(side=tk.LEFT)
    
    # Calidad
    calidad_frame = ttk.Frame(options_frame)
    calidad_frame.pack(fill=tk.X, pady=5)
    
    ttk.Label(calidad_frame, text="Calidad:").pack(side=tk.LEFT, padx=(0, 10))
    
    calidades = [
        ("Mejor", "best"),
        ("1080p", "1080p"),
        ("720p", "720p"),
        ("480p", "480p"),
        ("360p", "360p"),
        ("Peor", "worst")
    ]
    
    for texto, valor in calidades:
        rb = ttk.Radiobutton(
            calidad_frame,
            text=texto,
            variable=calidad_var,
            value=valor
        )
        rb.pack(side=tk.LEFT, padx=(0, 10))
    
    # Formato de audio (oculto inicialmente)
    audio_frame = ttk.Frame(options_frame)
    audio_frame.pack(fill=tk.X, pady=5)
    audio_frame.pack_forget()  # Ocultar inicialmente
    
    ttk.Label(audio_frame, text="Formato audio:").pack(side=tk.LEFT, padx=(0, 10))
    
    formatos_audio = ["mp3", "m4a", "wav", "flac", "aac"]
    audio_combo = ttk.Combobox(
        audio_frame,
        textvariable=formato_audio_var,
        values=formatos_audio,
        state="readonly",
        width=10
    )
    audio_combo.pack(side=tk.LEFT)
    audio_combo.set("mp3")
    
    # Carpeta de descarga
    ruta_frame = ttk.Frame(options_frame)
    ruta_frame.pack(fill=tk.X, pady=5)
    
    ttk.Label(ruta_frame, text="📁 Guardar en:").pack(side=tk.LEFT, padx=(0, 10))
    
    ruta_entry = ttk.Entry(
        ruta_frame,
        textvariable=ruta_var,
        width=50
    )
    ruta_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
    
    ruta_btn = ttk.Button(
        ruta_frame,
        text="📂",
        command=lambda: seleccionar_carpeta(log_text),
        width=5
    )
    ruta_btn.pack(side=tk.LEFT)
    
    # Botón de descarga
    download_btn = ttk.Button(
        main_frame,
        text="⬇️ DESCARGAR",
        command=lambda: iniciar_descarga(root, download_btn, progress_bar, progress_label, log_text),
        style="Accent.TButton"
    )
    download_btn.pack(fill=tk.X, pady=(0, 15), ipady=10)
    
    # Barra de progreso
    progress_frame = ttk.Frame(main_frame)
    progress_frame.pack(fill=tk.X, pady=(0, 10))
    
    progress_label = ttk.Label(
        progress_frame,
        text="🔥 Listo para descargar",
        foreground=COLORES['fg']
    )
    progress_label.pack()
    
    progress_bar = ttk.Progressbar(
        progress_frame,
        orient=tk.HORIZONTAL,
        length=100,
        mode='determinate'
    )
    progress_bar.pack(fill=tk.X, pady=5)
    
    # Log de eventos
    log_frame = ttk.LabelFrame(main_frame, text="📋 Registro de eventos", padding=5)
    log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
    
    log_text = scrolledtext.ScrolledText(
        log_frame,
        height=10,
        bg=COLORES['entry_bg'],
        fg=COLORES['fg'],
        font=('Consolas', 16),
        wrap=tk.WORD
    )
    log_text.pack(fill=tk.BOTH, expand=True)
    
    # Botones inferiores
    bottom_frame = ttk.Frame(main_frame)
    bottom_frame.pack(fill=tk.X)
    
    clear_btn = ttk.Button(
        bottom_frame,
        text="🗑️ Limpiar log",
        command=lambda: limpiar_log(log_text)
    )
    clear_btn.pack(side=tk.LEFT)
    
    info_btn = ttk.Button(
        bottom_frame,
        text="ℹ️ Información",
        command=mostrar_info
    )
    info_btn.pack(side=tk.RIGHT)
    
    return download_btn, progress_bar, progress_label, log_text

def main():
    """Función principal"""
    try:
        # Verificar que yt-dlp esté instalado
        import yt_dlp
    except ImportError:
        root = tk.Tk()
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
    root = tk.Tk()
    root.title("📥 Descargador de videos de Youtube")
    root.geometry("900x700")
    root.resizable(True, True)
    
    #Icono de la ventana
    icono1 = Image.open("img/icono1.png")
    icono_ventana = ImageTk.PhotoImage(icono1)
    root.iconphoto(False, icono_ventana) # type: ignore

    # Crear widgets
    download_btn, progress_bar, progress_label, log_text = create_widgets(root)
    
    # Centrar ventana
    center_window(root)
    
    # Log inicial
    log_info(log_text, "[+] Descargador de video de Youtube iniciado")
    log_info(log_text, "[+] Ingresa una URL y presiona Enter o haz clic en DESCARGAR")
    
    root.mainloop()

if __name__ == "__main__":
    main()
