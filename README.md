# AI-Client-Agent-MCP

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Agente de gestión de clientes compatible con el protocolo MCP (Model Context Protocol).

## ✨ Características

- ✅ Gestión completa de clientes (CRUD)
- 🚀 API RESTful basada en FastAPI
- 🗃️ Base de datos PostgreSQL
- 🔄 Compatible con Cursor, Windsurf, Claude y otros agentes MCP modernos
- 🔐 Autenticación y autorización integradas
- 📊 Validación de datos con Pydantic
- ⚡ Asíncrono y de alto rendimiento

## 📦 Estructura del Proyecto

```
AI-Client-Agent-MCP/
├── .env                    # Variables de entorno (crear manualmente)
├── requirements.txt        # Dependencias de Python
├── backend/                # Código fuente del backend
│   ├── __init__.py         # Paquete Python
│   ├── server.py           # Punto de entrada de la aplicación
│   │
│   ├── api/               # Capa de API
│   │   └── tools/
│   │       └── client_tools.py  # Endpoints MCP
│   │
│   ├── models/           # Modelos de datos
│   │   └── client.py       # Modelos Pydantic
│   │
│   ├── services/         # Lógica de negocio
│   │   └── client_service.py
│   │
│   └── core/            # Utilidades y configuraciones
│       ├── __init__.py
│       ├── config.py       # Configuración de la app
│       └── database.py     # Conexión a la base de datos
└── README.md
```

## 🔄 Flujo de la Aplicación

1. `server.py` inicia la aplicación MCP
2. Las peticiones llegan a los endpoints en `api/tools/`
3. Las herramientas utilizan los servicios para la lógica de negocio
4. Los servicios interactúan con la base de datos
5. Los modelos validan los datos en cada paso

## 🛠️ Instalación

1. Clona el repositorio:
   ```bash
   git clone [URL_DEL_REPOSITORIO]
   cd AI-Client-Agent-MCP
   ```

2. Crea un entorno virtual (recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Configura el archivo .env:
   ```bash
   cp .env.example .env
   # Edita el archivo .env con tus credenciales
   ```

5. Inicia el servidor:
   ```bash
   python -m backend.server
   ```

## ⚙️ Configuración

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
# Aplicación
APP_ENV=development
APP_DEBUG=True
APP_SECRET_KEY=tu_clave_secreta_aqui

# Base de datos
POSTGRES_USER=postgres
POSTGRES_PASSWORD=tu_contraseña
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_DB=nombre_bd

# URL de conexión (se genera automáticamente)
DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_SERVER}:${POSTGRES_PORT}/${POSTGRES_DB}
```

## 🚀 Uso

### Ejecutar el servidor

```bash
python -m backend.server
```

### Ejecutar pruebas

```bash
pytest tests/
```

## 📚 Documentación

La documentación de la API estará disponible en `http://localhost:8000/docs` cuando el servidor esté en ejecución.

## 🤝 Contribución

Las contribuciones son bienvenidas. Por favor, lee nuestras [pautas de contribución](CONTRIBUTING.md) antes de enviar un pull request.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más información.

---

Desarrollado con ❤️ por David Salas
