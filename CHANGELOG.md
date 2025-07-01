# 📓 Changelog

Todos los cambios relevantes de este proyecto se documentan acá.

---

## [1.5.0] - 2025-06-30

### 🔐 Autenticación y Usuarios
- **Sistema completo de usuarios**: Registro, login y logout con hash de contraseñas
- **Gestión de presets por usuario**: Cada usuario puede guardar y gestionar sus propias configuraciones
- **Recuperación de contraseña innovadora**: Sistema único que usa los presets guardados del usuario como método de verificación de identidad
- **Sistema de seguridad avanzado**: Bloqueo temporal de 10 minutos después de fallar en la verificación de preset durante recuperación de contraseña
- **Redirección inteligente**: Los usuarios que se loguean desde la página de resultados regresan automáticamente a ver sus resultados

### 🎨 Mejoras de Interfaz
- **Navegación consistente**: Barra superior unificada en todas las páginas con estado de login
- **Selector de presets**: Los usuarios autenticados pueden cargar configuraciones guardadas anteriormente
- **Notificaciones visuales**: Mensajes de éxito al guardar presets y feedback claro en todas las acciones
- **Diseño responsivo mejorado**: Alineación perfecta y experiencia visual profesional en toda la aplicación
- **Templates especializados**: Páginas dedicadas para login, registro, recuperación de contraseña y desafío de verificación

### 🎯 Experiencia de Usuario
- **Condicionamiento inteligente de UI**: La interfaz se adapta según el estado de autenticación del usuario
- **Preservación de contexto**: Los usuarios no logueados pueden procesar imágenes y luego autenticarse sin perder su trabajo
- **Invitación a registro**: Mensajes amigables que invitan a crear cuenta para acceder a funciones premium
- **Sistema de presets mejorado**: Carga fácil de configuraciones con un clic desde un selector visual

### 🛡️ Seguridad
- **Verificación de identidad única**: Sistema de recuperación de contraseña basado en presets del usuario (5+ opciones mezcladas con señuelos)
- **Protección contra ataques**: Bloqueo automático después de intentos fallidos de recuperación
- **Validación robusta**: Múltiples capas de verificación en todos los formularios
- **Gestión segura de sesiones**: Cookies HTTP-only y redirecciones validadas

### 🚀 Deploy y Producción
- **Inicialización automática de BD**: La base de datos se crea automáticamente al arrancar la aplicación
- **Compatibilidad con Render**: Configuración completa para deploy en la nube
- **Servicio de archivos estáticos**: Soporte completo para CSS y assets
- **Health check endpoint**: Monitoreo del estado de la aplicación para plataformas cloud
- **Rutas optimizadas**: Todas las rutas son relativas y funcionan en cualquier entorno

### 🛠️ Interno
- **Arquitectura modular**: Separación clara entre autenticación, base de datos y lógica de negocio
- **Gestión de errores mejorada**: Manejo robusto de excepciones y validaciones
- **Base de datos optimizada**: Nuevas tablas para usuarios, presets y sistemas de seguridad
- **Dockerfile mejorado**: Soporte para Tesseract en español y optimizaciones de producción

---

## [1.4.0] - 2025-06-25

### ✨ Nuevo
- Gracias a @ioanne, se incorporó el **Editor Experto** de preprocesamiento personalizado.
- Los usuarios ahora pueden configurar cada paso del preprocesamiento de forma manual:
  - 🔘 Color y Contraste: Escala de grises, inversión de colores, brillo, contraste, CLAHE.
  - 🔘 Filtros y Suavizado: Desenfoque Gaussiano y Filtro de Mediana.
  - 🔘 Transformaciones Geométricas: Corrección de inclinación (Deskew), Rotación manual.
  - 🔘 Detección de Bordes: Filtro de Canny con umbrales ajustables.
  - 🔘 Binarización y Morfología: Métodos adaptativos y operaciones morfológicas configurables.
- Se agregó una nueva interfaz intuitiva y ordenada, en forma de acordeones, para activar/desactivar secciones.

### 🛠️ Interno
- Mejoras en el frontend para permitir personalización total del flujo de preprocesamiento.
- Nuevas rutas y lógica en backend para procesar transformaciones de forma dinámica según configuración del usuario.

---

## [1.3.0] - 2025-05-16
### ✨ Agregado
- Configuración Docker (`Dockerfile`) para contenerizar OcrAPP
- Archivo `render.yaml` para despliegue automático en Render
- Configuración de subdominio personalizado: `ocrapp.data-bi.ar`

### 🚀 Despliegue
- OcrAPP ahora está online con FastAPI corriendo desde un contenedor con soporte completo para OCR en la nube

---

## [1.2.0] - 2025-05-16
### ✨ Agregado
- Checkbox en la interfaz para activar o desactivar el preprocesamiento de imagen
- Mejora del preprocesamiento: aumento de contraste, binarización con Otsu y reducción de ruido
- Cambio del parámetro Tesseract a `--psm 4` para mejor segmentación de texto
- Actualización del README con tabla comparativa sobre cuándo aplicar mejoras

---

## [1.1.0] - 2025-05-16
### ✨ Agregado
- Funcionalidad para exportar el texto también en formato `.txt`
- Pantalla intermedia luego del procesamiento con botones de descarga
- Estilos CSS para mejorar la experiencia del usuario

---

## [1.0.0] - 2025-05-15
### 🚀 Creado
- Versión inicial de la app OCR
- Subida de imagen o PDF escaneado
- Extracción de texto con Tesseract OCR
- Generación automática de documento `.docx`
- Interfaz HTML básica
