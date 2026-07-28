# 🎬 YouTube Downloader

[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![yt-dlp](https://img.shields.io/badge/yt--dlp-latest-orange.svg)](https://github.com/yt-dlp/yt-dlp)

## 📋 Descripción

YouTube Downloader es una aplicación completa para descargar videos y audio de YouTube. Ofrece tanto una **interfaz gráfica** (GUI) como una **interfaz de línea de comandos** (CLI), permitiendo a los usuarios elegir su método preferido de descarga.

### ✨ Características Principales

- 🎥 **Descarga de videos** en múltiples calidades (1080p, 720p, 480p, 360p)
- 🎵 **Extracción de audio** en diversos formatos (MP3, M4A, WAV, FLAC, AAC)
- 📁 **Descarga de playlists** completas
- 📊 **Barra de progreso** en tiempo real
- 🎯 **Selección de calidad** personalizada
- 📂 **Carpeta de destino** configurable
- 🔄 **Soporte para múltiples URLs**
- 🖥️ **Interfaz gráfica intuitiva**
- ⌨️ **Interfaz CLI simple y efectiva**

## 📸 Capturas de Pantalla

### Interfaz Gráfica (GUI)

![[Pasted image 20260728125558.png]]
### Interfaz CLI

![[Pasted image 20260728125803.png]]

## 🔧 Requisitos del Sistema

- Python 3.6 o superior
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [FFmpeg](https://ffmpeg.org/) (necesario para descargas de audio y videos de alta calidad)
- [Pillow](https://python-pillow.org/) (para la interfaz gráfica)

## 📦 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/amateo142857/YouTube_Grabber.git
cd YouTube_Grabber
```

### 2. Crear un entorno virtual (recomendado)

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Instalar FFmpeg (obligatorio)

#### Windows
1. Descargar FFmpeg desde [ffmpeg.org](https://ffmpeg.org/download.html)
2. Agregar la carpeta `bin` de FFmpeg al PATH del sistema

#### Linux
```bash
sudo apt update
sudo apt install ffmpeg
```

#### MacOS
```bash
brew install ffmpeg
```

## 🚀 Uso

### Interfaz Gráfica (GUI)

Ejecutar el script principal:

```bash
python descargador_tkinter.py
```

#### Pasos para descargar:
1. **Ingresar URL**: Pega o escribe la URL del video/playlist
2. **Seleccionar tipo**: Video o Audio
3. **Elegir calidad**: Best, 1080p, 720p, 480p, 360p o Worst
4. **Configurar carpeta**: Selecciona dónde guardar el archivo
5. **¡Descargar!**: Haz clic en el botón de descarga

### Interfaz CLI

Ejecutar el script de línea de comandos:

```bash
python descargador_terminal.py
```

#### Menú interactivo:
```
==================================================
🎬 DESCARGADOR DE YOUTUBE
==================================================
1. Descargar video
2. Descargar solo audio
3. Descargar playlist
4. Salir
==================================================
```

## 📖 Guía de Uso Detallada

### Opciones de Calidad

| Calidad | Descripción |
|---------|-------------|
| **Best** | Mejor calidad disponible |
| **1080p** | Resolución 1920x1080 |
| **720p** | Resolución 1280x720 |
| **480p** | Resolución 854x480 |
| **360p** | Resolución 640x360 |
| **Worst** | Peor calidad disponible |

### Formatos de Audio

| Formato | Descripción | Uso Recomendado |
|---------|-------------|-----------------|
| **MP3** | MP3 estándar | Compatibilidad universal |
| **M4A** | AAC en contenedor MP4 | Mejor calidad/compresión |
| **WAV** | Audio sin comprimir | Edición de audio |
| **FLAC** | Compresión sin pérdida | Calidad máxima |
| **AAC** | Audio avanzado | Streaming/Dispositivos Apple |

## 🛠️ Estructura del Proyecto

```
youtube-downloader/
├── img/                        # Iconos y recursos gráficos
│   └── icono1.png
├── screenshots                 # Carpeta de imágens del proyecto 
│   └── imagenes del proyecto   
├── descargas/                  # Carpeta por defecto para descargas
├── descargador_terminal.py   # Interfaz de línea de comandos
├── descargador_tkinter.py   # Interfaz gráfica
├── requirements.txt            # Dependencias del proyecto
├── README.md                   # Este archivo
├── LICENSE                     # Licencia del proyecto
└── .gitignore                  # Archivos ignorados por Git
```

## 📦 Dependencias

### Requerimientos (`requirements.txt`)

```
yt-dlp>=2023.10.13
Pillow>=10.0.0
termcolor>=2.3.0
```


## 🐛 Reporte de Errores

Si encuentras algún error, por favor:

1. Verifica que tienes instaladas todas las dependencias
2. Asegúrate de tener FFmpeg instalado y configurado
3. Abre un issue en el repositorio con:
   - Descripción detallada del problema
   - Pasos para reproducirlo
   - Mensajes de error completos
   - Sistema operativo y versiones

## ⚠️ Notas Importantes

- **Uso Ético**: Esta herramienta está diseñada para descargar contenido con fines educativos y personales. Asegúrate de respetar los derechos de autor y los términos de servicio de YouTube.
- **Actualizaciones**: YouTube cambia frecuentemente su estructura, por lo que es importante mantener yt-dlp actualizado:
  ```bash
  pip install --upgrade yt-dlp
  ```
- **Errores de FFmpeg**: Si experimentas problemas con el audio o videos de alta calidad, verifica que FFmpeg esté correctamente instalado.

## 🎯 Próximas Características

- [ ] Descarga por lotes desde archivo de texto
- [ ] Soporte para otras plataformas (Vimeo, Dailymotion, etc.)
- [ ] Integración con gestores de descarga
- [ ] Conversión de formatos de video
- [ ] Interfaz web

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 👤 Autor

**Alejandro Mateo**

[![GitHub](https://img.shields.io/badge/GitHub-AlejandroMateo-181717?style=for-the-badge&logo=github)](https://github.com/AlejandroMateo)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-AlejandroMateo-0077B5?style=for-the-badge&logo=linkedin)](https://linkedin.com/in/alejandromateo)

## 🙏 Agradecimientos

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) por la increíble biblioteca de descarga
- [FFmpeg](https://ffmpeg.org/) por el procesamiento de audio y video
- A toda la comunidad de código abierto

---

⭐ **Si este proyecto te fue útil, ¡no olvides darle una estrella!** ⭐
