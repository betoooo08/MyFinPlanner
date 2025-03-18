# MyFinPlanner 📊💰

**MyFinPlanner** es una aplicación web de gestión de finanzas personales que permite rastrear ingresos y gastos, establecer presupuestos y obtener información sobre hábitos de gasto.  
Incluye **MyFinancePal**, un asistente financiero impulsado por IA que proporciona visualizaciones y recomendaciones basadas en patrones de gasto.

## 🚀 Características

- 📊 **Seguimiento de ingresos y gastos** con reportes detallados.  
- 🎯 **Establecimiento de presupuestos** mensuales y personalizados.  
- 📈 **Análisis financiero** con visualizaciones interactivas.  
- 🤖 **MyFinancePal (Asistente IA)** que ofrece recomendaciones y análisis de hábitos de gasto.  
- 📡 **Soporte para inversiones** con actualización en tiempo real de precios de acciones usando la API de FinHub.  

---

## 🛠 Instalación y Configuración

### 1️⃣ Requisitos previos

Antes de iniciar el proyecto, asegúrate de tener instalado:

- Python 3.10+ 👉 [Descargar aquí](https://www.python.org/downloads/)
- Git 👉 [Descargar aquí](https://git-scm.com/)
- Virtualenv (opcional, pero recomendado)  

### 2️⃣ Clonar el repositorio

```bash
git clone https://github.com/tuusuario/MyFinPlanner.git
cd MyFinPlanner
```

### 3️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4️⃣ Aplicar migraciones y preparar la base de datos

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5️⃣ Iniciar el servidor de desarrollo

```bash
python manage.py runserver
```

### 📁 Estructura del Proyecto

```bash
MyFinPlanner/  
│── finances/                  # Aplicación principal de Django  
│   │── static/                 # Archivos estáticos (CSS, JS, imágenes)  
│   │── templates/              # Plantillas HTML para la interfaz  
│   │── __init__.py             # Archivo que indica que este directorio es un módulo de Python  
│   │── admin.py                # Configuración del panel de administración de Django  
│   │── apps.py                 # Configuración de la aplicación en Django  
│   │── forms.py                # Formularios para la entrada de datos del usuario  
│   │── models.py               # Modelos de la base de datos de la aplicación  
│   │── tests.py                # Pruebas unitarias de la aplicación  
│   │── urls.py                 # Definición de rutas de la aplicación  
│   │── views.py                # Lógica de la vista para manejar solicitudes  
│  
│── myFinPlanner/               # Configuración global del proyecto Django  
│   │── __pycache__/            # Archivos compilados de Python (ignorar)  
│   │── __init__.py             # Archivo que indica que este directorio es un módulo de Python  
│   │── asgi.py                 # Configuración para el servidor ASGI  
│   │── settings.py             # Configuración principal del proyecto  
│   │── urls.py                 # Definición de rutas a nivel del proyecto  
│   │── wsgi.py                 # Configuración para el servidor WSGI  
│  
│── .gitignore                  # Archivos y carpetas que Git debe ignorar  
│── db.sqlite3                   # Base de datos SQLite del proyecto  
│── manage.py                    # Archivo para gestionar el proyecto Django  
│── README.md                    # Documentación del proyecto  
│── requirements.txt              # Dependencias del proyecto  

```

---

🚀 **¡Gracias por usar MyFinPlanner!**  
  






