# 🧾 OCR App - Extracción de texto desde imágenes y PDFs

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green?style=flat-square&logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-Ready-blue?style=flat-square&logo=docker)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)
![Status](https://img.shields.io/badge/Status-Production_Ready-brightgreen?style=flat-square)

**Trabajo Final Integrador - Técnicas de Procesamiento Digital de Imágenes**

📅 Año: 2025

👨🏻‍🏫 Profesor: Juan Ignacio Bonini (@ioanne)

🏫 Institución: IFTS 18

� Alumnos:
- Juan Jose Albornoz (@juanjoalbornoz)
- Estefany Herrera Martinez (@hmestefany)
- Carolina Linares (@carolinares03)
- Gonzalo Rey del Castillo (@King-Zalogon)

---

## ✨ Descripción del proyecto

**OcrAPP** es una aplicación web completa que permite subir imágenes o PDFs escaneados y devuelve el texto extraído en formatos `.docx` y `.txt`. 

La aplicación incluye un **sistema completo de usuarios** con autenticación, gestión de presets personalizados, y un innovador sistema de recuperación de contraseñas basado en verificación de identidad.

Su objetivo es facilitar la digitalización de apuntes, estudios médicos, facturas y otros documentos escaneados, combinando procesamiento digital de imágenes avanzado con una interfaz profesional y segura.

---

## 🚀 Funcionalidades

### 📄 Procesamiento de Documentos
- ✅ Extracción de texto desde imágenes (`.jpg`, `.png`) y `.pdf`  
- ✅ Preprocesamiento avanzado configurable por el usuario
- ✅ Vista previa de la imagen procesada para diagnóstico
- ✅ Soporte multilenguaje para OCR (incluye español e inglés)  
- ✅ Exportación del texto extraído a archivos `.txt` y `.docx` 

### 🔐 Sistema de Usuarios
- ✅ **Registro y autenticación** con hash seguro de contraseñas
- ✅ **Gestión de presets personalizados** - guarda tus configuraciones favoritas
- ✅ **Sistema único de recuperación de contraseña** usando presets como verificación de identidad
- ✅ **Protección anti-ataques** con bloqueo temporal de 10 minutos
- ✅ **Redirección inteligente** que preserva el contexto del usuario

### 🎨 Experiencia de Usuario
- ✅ **Interfaz adaptativa** que cambia según el estado de autenticación
- ✅ **Navegación consistente** con barra superior unificada
- ✅ **Selector visual de presets** para cargar configuraciones guardadas
- ✅ **Notificaciones en tiempo real** para todas las acciones
- ✅ **Diseño responsivo** optimizado para móviles y desktop

---

## 🧪 Transformaciones disponibles

Al cargar una imagen, podés elegir aplicar una o más de las siguientes transformaciones:

- 🔘 **Color y Contraste**: Escala de grises, inversión de colores, brillo, contraste, CLAHE.
- 🔘 **Filtros y Suavizado**: Desenfoque Gaussiano y Filtro de Mediana.
- 🔘 **Transformaciones Geométricas**: Corrección de inclinación (Deskew), Rotación manual.
- 🔘 **Detección de Bordes**: Filtro de Canny con umbrales ajustables.
- 🔘 **Binarización y Morfología**: Métodos adaptativos y operaciones morfológicas configurables.

Estas herramientas permiten **mejorar la precisión del OCR**, adaptándose a distintas calidades y formatos de documentos.

---

## 🛠️ Tecnologías utilizadas

### Backend y Core:
- **Python 3.11+** - Lenguaje principal con soporte moderno
- **FastAPI** - Framework web moderno con validación automática
- **SQLite** - Base de datos ligera con inicialización automática
- **Uvicorn** - Servidor ASGI de alto rendimiento

### Procesamiento de Imágenes y OCR:
- **OpenCV (cv2)** - Biblioteca avanzada para preprocesamiento de imágenes
- **Tesseract OCR** - Motor de reconocimiento óptico de caracteres (incluye español)
- **PyMuPDF (fitz)** - Extracción y conversión de archivos PDF
- **Pillow (PIL)** - Manipulación adicional de imágenes
- **python-multipart** - Manejo de uploads de archivos

### Frontend y UI/UX:
- **Jinja2** - Motor de templates con lógica condicional avanzada
- **Tailwind CSS** - Framework CSS utility-first para diseño responsivo
- **HTML5 y JavaScript** - Interfaz moderna y reactiva

### Seguridad y Autenticación:
- **bcrypt** - Hash seguro de contraseñas con salt automático
- **python-jose** - Manejo de tokens JWT para sesiones
- **passlib** - Biblioteca robusta para autenticación

### Despliegue y Contenedores:
- **Docker** - Empaquetado y distribución de la aplicación
- **Render** - Plataforma de hosting en la nube con CI/CD
- **Git** - Control de versiones con workflow de desarrollo

### Generación de Documentos:
- **python-docx** - Creación de archivos Word (.docx)
- **ReportLab** - Generación avanzada de PDFs (futuras versiones)

---

## 🐳 Despliegue con Docker (Render)

Esta app ahora puede ejecutarse y desplegarse usando contenedores Docker.

### Archivos agregados:

- `Dockerfile`: contiene las instrucciones para construir la imagen con Tesseract y Poppler
- `render.yaml`: configuración para despliegue automático en Render

### Despliegue en la nube

La app está desplegada en:  
🔗 [https://ocrapp.data-bi.ar](https://ocrapp.data-bi.ar)

---

## ⚙️ Instalación y ejecución local

> ⚠️ **Importante**: La aplicación ahora incluye un sistema de base de datos que se inicializa automáticamente al arrancar.

### 1. Clonar el repositorio

```bash
https://github.com/juanjoalbornoz/OcrApp.git
cd ocr-app
```

### 2. Crear y activar el entorno virtual

```bash
python3 -m venv env

# Linux/macOS:
source env/bin/activate

# Windows:
env\Scripts\activate
```

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 4. Instalar Tesseract OCR

#### macOS:

```bash
brew install tesseract
```

#### Ubuntu:

```bash
sudo apt install tesseract-ocr tesseract-ocr-spa
```

#### Windows:

Descargar desde [https://github.com/UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki)

### 5. Instalar Poppler (para PDFs)

#### macOS:

```bash
brew install poppler
```

#### Ubuntu:

```bash
sudo apt install poppler-utils
```

### 6. Configurar base de datos (Automático)

La aplicación creará automáticamente la base de datos SQLite y todas las tablas necesarias al arrancar por primera vez. No necesitás configuración manual.

---

## 🚀 Ejecutar la aplicación

```bash
uvicorn app.main:app --reload
```

📎 Luego ingresá a: http://localhost:8000

### 🎯 Primeros pasos

1. **Acceso sin registro**: Podés usar la app inmediatamente para procesar documentos
2. **Crear cuenta** (opcional): Para guardar presets y acceder a funciones avanzadas
3. **Configurar presets**: Guarda tus configuraciones de preprocesamiento favoritas
4. **Procesar documentos**: Subí imágenes o PDFs y descargá los resultados

---

## 🔐 Funcionalidades de Usuario

### Para usuarios no registrados:
- ✅ Procesamiento completo de documentos
- ✅ Descarga de resultados (.txt y .docx)
- ✅ Acceso a todas las herramientas de preprocesamiento

### Para usuarios registrados:
- ✅ **Todo lo anterior**, más:
- ✅ Guardar presets de configuración personalizados
- ✅ Cargar configuraciones guardadas con un clic
- ✅ Recuperación de contraseña mediante verificación de presets
- ✅ Historial persistente de configuraciones

---

## � Consideraciones de Seguridad

### Medidas implementadas:
- **Contraseñas hasheadas** con bcrypt y salt automático
- **Cookies HTTP-only** para prevenir ataques XSS
- **Protección anti-fuerza bruta** con bloqueo temporal de 10 minutos
- **Validación de redirecciones** para evitar ataques de redirect abierto
- **Sistema único de recuperación** basado en presets conocidos por el usuario
- **Inicialización automática de BD** sin credenciales hardcodeadas

### Recuperación de contraseña innovadora:
En lugar de emails, usamos un sistema donde el usuario debe **reconocer sus presets guardados** entre opciones mezcladas. Esto garantiza que solo el dueño real de la cuenta pueda recuperar el acceso.

---

## �📂 Estructura del proyecto

```bash
OcrAPP/
│
├── app/
│   ├── main.py                # Lógica principal, rutas FastAPI y autenticación
│   ├── database.py            # Gestión de base de datos SQLite
│   ├── ocr.py                 # Funciones de OCR usando Tesseract
│   ├── preprocess.py          # Funciones de preprocesamiento de imágenes
│   ├── ocrapp.db              # Base de datos SQLite (se crea automáticamente)
│   └── templates/
│       ├── form.html          # Interfaz principal de procesamiento
│       ├── resultados.html    # Página de resultados OCR
│       ├── login.html         # Formulario de login
│       ├── register.html      # Formulario de registro
│       ├── forgot_password.html           # Inicio de recuperación
│       ├── password_recovery_challenge.html  # Desafío de presets
│       └── reset_password.html           # Nueva contraseña
│
├── diagnostics/               # Imágenes preprocesadas para diagnóstico 
├── outputs/                   # Archivos de texto y DOCX generados
├── static/                    # Estilos CSS y otros recursos estáticos
├── uploads/                   # Archivos temporales subidos por usuarios
│
├── Dockerfile                 # Imagen Docker optimizada para producción
├── render.yaml                # Configuración para despliegue en Render
├── requirements.txt           # Dependencias del proyecto
├── README.md                  # Documentación completa del proyecto
└── CHANGELOG.md               # Historial detallado de versiones
```

---

## 🌟 ¿Por qué elegir OCR App?

### Para estudiantes y profesionales:
- **Sin configuración técnica**: Funciona desde el navegador
- **Gratuito y sin límites**: Procesa tantos documentos como necesites
- **Calidad profesional**: Algoritmos avanzados de preprocesamiento
- **Privacidad**: Tus documentos se procesan localmente en el servidor

### Para desarrolladores:
- **Código abierto**: Contribuye y personaliza según tus necesidades
- **Documentación completa**: CHANGELOG detallado y README exhaustivo
- **Fácil despliegue**: Docker + Render para deploy en minutos
- **Arquitectura moderna**: FastAPI + SQLite + Docker

---

## 🤝 Para usuarios de GitHub

Si encontraste este repositorio y querés usar o contribuir:

### 🚀 Deploy rápido:
1. **Fork** este repositorio
2. **Conecta** tu fork con Render
3. **Deploy automático** usando el archivo `render.yaml` incluido
4. ¡**Listo!** Tu propia instancia estará funcionando

### 🛠️ Desarrollo local:
1. **Clona** el repositorio
2. **Sigue** las instrucciones de instalación arriba
3. **Ejecuta** `uvicorn app.main:app --reload`
4. **Navega** a http://localhost:8000

### 📋 Consideraciones importantes:
- La BD SQLite se **crea automáticamente** - no necesitás configuración previa
- Incluye **datos de prueba** y **documentación** para que entiendas el flujo
- El sistema está **listo para producción** con todas las medidas de seguridad

---

## 🔌 API y Endpoints

### Endpoints principales:
- `GET /` - Página principal con formulario de carga
- `POST /upload` - Procesamiento de archivos (imágenes/PDFs)
- `GET /resultados/{filename}` - Visualización de resultados
- `GET /download/{filename}` - Descarga de archivos procesados

### Autenticación:
- `GET /login` - Formulario de login
- `POST /login` - Autenticación de usuario
- `GET /register` - Formulario de registro
- `POST /register` - Creación de nueva cuenta
- `POST /logout` - Cerrar sesión

### Gestión de presets:
- `POST /save_preset` - Guardar configuración personalizada
- `GET /load_preset/{preset_id}` - Cargar preset específico

### Recuperación de contraseña:
- `GET /forgot_password` - Inicio del proceso de recuperación
- `POST /forgot_password` - Envío de solicitud
- `GET /password_recovery_challenge/{token}` - Desafío de presets
- `POST /password_recovery_challenge/{token}` - Validación del desafío
- `POST /reset_password/{token}` - Establecer nueva contraseña

### Utilidades:
- `GET /health` - Health check para monitoreo
- `GET /static/{path}` - Archivos estáticos (CSS, JS, imágenes)

---

## 🎯 Roadmap y mejoras futuras

### Versión 2.0 (Ideas para contribuciones):
- 📧 **Notificaciones por email** para recovery y registro
- 🌐 **Soporte multi-idioma** en la interfaz
- 📊 **Dashboard de estadísticas** de uso por usuario
- 🔄 **API REST** documentada para integraciones
- 💾 **Historial de documentos** procesados por usuario
- 🧠 **IA mejorada** para detección automática de tipo de documento

### Contribuir al proyecto:
1. **Fork** el repositorio
2. **Crea** una rama para tu feature: `git checkout -b feature/nueva-funcionalidad`
3. **Commit** tus cambios: `git commit -m 'Agrega nueva funcionalidad'`
4. **Push** a la rama: `git push origin feature/nueva-funcionalidad`
5. **Abre** un Pull Request con descripción detallada

---

## 📞 Soporte y contacto

### 🐛 Encontraste un bug?
- **Issues**: Abre un issue en GitHub con detalles del problema
- **Logs**: Incluye los logs relevantes y pasos para reproducir

### 💡 ¿Tenés una idea?
- **Feature Request**: Describe tu idea en un issue
- **Discusión**: Usa las Discussions para propuestas grandes

### 📧 Contacto directo:
- **Equipo de desarrollo**: [Información en los perfiles de GitHub]
- **Profesor**: @ioanne (IFTS 18)

---

## ❤️ Créditos

Este proyecto fue desarrollado con amor, pruebas, mate y muchas líneas de código por **Juanjo**, **Estefy**, **Carito** y **Gonza** como parte del trabajo final para la materia **Técnicas de Procesamiento Digital de Imágenes**.

### Agradecimientos especiales:
- 🎓 **Prof. Juan Ignacio Bonini** (@ioanne) por la guía, apoyo y por meterse de lleno a potenciarnos
- 🏫 **IFTS 18** por el espacio de aprendizaje
- 🌍 **Comunidad Open Source** por las herramientas increíbles que usamos
- ☕ **El café y el mate** por las horas de código

---

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Podés usar, modificar y distribuir libremente.

**¡Esperamos que esta herramienta te sea útil! Besitooos! 🚀**
