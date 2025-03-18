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
│── myfinplanner/        # Carpeta principal del proyecto Django
│   ├── settings.py      # Configuración del proyecto
│   ├── urls.py          # Definición de rutas
│   ├── wsgi.py          # Entrada WSGI para despliegue
│   ├── asgi.py          # Entrada ASGI (para WebSockets y más)
│── core/                # Aplicación principal del proyecto
│   ├── models.py        # Definición de modelos de base de datos
│   ├── views.py         # Lógica de vistas
│   ├── urls.py          # Rutas de la app
│   ├── templates/       # Archivos HTML para el frontend
│── static/              # Archivos estáticos como CSS y JS
│── templates/           # Plantillas HTML compartidas
│── db.sqlite3           # Base de datos SQLite (si se usa por defecto)
│── manage.py            # Comando principal de Django
│── requirements.txt     # Dependencias del proyecto
```

---

🚀 **¡Gracias por usar MyFinPlanner!**  
  






