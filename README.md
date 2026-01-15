# TaskFlow Backend - Arquitectura MVC

Sistema de gestión de tareas con arquitectura profesional usando Flask y patrón MVC.

## 📁 Estructura del Proyecto

```
taskflow-mvc/
├── app.py                      # Punto de entrada
├── config.py                   # Configuraciones
├── requirements.txt            # Dependencias
└── app/
    ├── __init__.py            # Factory de la aplicación
    ├── models/                # Modelos de datos
    │   ├── __init__.py
    │   ├── user.py           # Modelo User
    │   └── task.py           # Modelo Task
    ├── services/              # Lógica de negocio
    │   ├── __init__.py
    │   ├── user_service.py   # Servicios de usuarios
    │   └── task_service.py   # Servicios de tareas
    ├── routes/                # Endpoints (Controllers)
    │   ├── __init__.py
    │   ├── users.py          # Rutas de usuarios
    │   └── tasks.py          # Rutas de tareas
    └── utils/                 # Utilidades
        ├── __init__.py
        └── validators.py     # Funciones de validación
```

## 🏗️ Arquitectura MVC

### Model (Modelos)
**Ubicación:** `app/models/`

Definen la estructura de los datos:
- `User`: Representa un usuario del sistema
- `Task`: Representa una tarea

**Responsabilidades:**
- Definir la estructura de datos
- Métodos de conversión (to_dict, from_dict)
- Métodos de utilidad específicos del modelo

### Service (Servicios)
**Ubicación:** `app/services/`

Contienen la lógica de negocio:
- `user_service`: Operaciones sobre usuarios
- `task_service`: Operaciones sobre tareas

**Responsabilidades:**
- Validaciones de negocio
- Procesamiento de datos
- Coordinación entre modelos
- Manejo de la "base de datos" (en memoria)

### Routes (Rutas/Controllers)
**Ubicación:** `app/routes/`

Definen los endpoints de la API:
- `users.py`: Endpoints de usuarios (users_bp)
- `tasks.py`: Endpoints de tareas (tasks_bp)

**Responsabilidades:**
- Recibir peticiones HTTP
- Extraer datos de la petición
- Llamar a los servicios correspondientes
- Devolver respuestas JSON

## 🚀 Instalación y Ejecución

### 1. Crear entorno virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Instalar dependencias

```bash
pip install flask flask-cors
```

O crear un archivo `requirements.txt`:
```
Flask==3.0.0
flask-cors==4.0.0
```

Y ejecutar:
```bash
pip install -r requirements.txt
```

### 3. Ejecutar la aplicación

```bash
python app.py
```

El servidor estará disponible en: `http://localhost:5000`

## 📚 Endpoints Disponibles

### Usuarios

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/users` | Lista todos los usuarios |
| GET | `/api/users/<id>` | Obtiene un usuario |
| POST | `/api/users` | Crea un usuario |
| PUT | `/api/users/<id>` | Actualiza un usuario |
| DELETE | `/api/users/<id>` | Elimina un usuario |
| GET | `/api/users/<id>/tasks` | Tareas del usuario |
| GET | `/api/users/<id>/stats` | Estadísticas del usuario |

### Tareas

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/tasks` | Lista todas las tareas |
| GET | `/api/tasks/<id>` | Obtiene una tarea |
| POST | `/api/tasks` | Crea una tarea |
| PUT | `/api/tasks/<id>` | Actualiza una tarea |
| PATCH | `/api/tasks/<id>/complete` | Marca tarea completada |
| DELETE | `/api/tasks/<id>` | Elimina una tarea |
| GET | `/api/tasks/completed` | Lista tareas completadas |
| GET | `/api/tasks/pending` | Lista tareas pendientes |

### Health Check

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/health` | Estado del servidor |

## 🧪 Ejemplos de Uso con Thunder Client

### Crear Usuario

```http
POST http://localhost:5000/api/users
Content-Type: application/json

{
  "nombre": "María García",
  "email": "maria@email.com",
  "rol": "usuario"
}
```

### Crear Tarea Asignada

```http
POST http://localhost:5000/api/tasks
Content-Type: application/json

{
  "titulo": "Implementar login",
  "descripcion": "Sistema de autenticación con JWT",
  "prioridad": "alta",
  "usuario_id": 1
}
```

### Obtener Tareas de un Usuario

```http
GET http://localhost:5000/api/users/1/tasks
```

### Marcar Tarea como Completada

```http
PATCH http://localhost:5000/api/tasks/1/complete
```

### Obtener Estadísticas de Usuario

```http
GET http://localhost:5000/api/users/1/stats
```

Respuesta:
```json
{
  "total": 5,
  "completadas": 2,
  "pendientes": 3,
  "por_prioridad": {
    "alta": 2,
    "media": 2,
    "baja": 1
  }
}
```

## 🔒 Validaciones Implementadas

### Usuarios
- ✅ Email debe ser válido y único
- ✅ Nombre no puede estar vacío
- ✅ Rol debe ser 'administrador' o 'usuario'
- ✅ No se puede eliminar usuario con tareas asignadas

### Tareas
- ✅ Título no puede estar vacío
- ✅ Prioridad debe ser 'alta', 'media' o 'baja'
- ✅ No se puede asignar a usuario inexistente

## 🎯 Ventajas de esta Arquitectura

### 1. Separación de Responsabilidades
- Cada capa tiene una función específica
- Fácil de entender qué hace cada archivo

### 2. Mantenibilidad
- Cambios en una capa no afectan a las demás
- Fácil agregar nuevas funcionalidades

### 3. Testabilidad
- Servicios y modelos se pueden probar independientemente
- No dependen de Flask para funcionar

### 4. Escalabilidad
- Fácil agregar nuevos recursos
- Estructura se mantiene consistente al crecer

### 5. Trabajo en Equipo
- Diferentes desarrolladores pueden trabajar en diferentes módulos
- Menos conflictos en Git

## 📝 Próximos Pasos

1. **Sesión 4:** Integrar con Supabase (PostgreSQL)
2. Implementar autenticación con JWT
3. Agregar tests unitarios
4. Implementar paginación
5. Agregar filtros avanzados
6. Crear documentación con Swagger

## 🐛 Troubleshooting

### Error: ModuleNotFoundError
**Problema:** No se encuentra el módulo 'app'

**Solución:** Asegúrate de estar en la carpeta raíz del proyecto y que existe `app/__init__.py`

### Error: Import Error
**Problema:** Error al importar modelos o servicios

**Solución:** Verifica que todos los archivos `__init__.py` existan en cada carpeta

### El servidor no arranca
**Problema:** Puerto 5000 ya está en uso

**Solución:** 
1. Detén otros servidores corriendo
2. O cambia el puerto en `config.py`

## 👨‍💻 Autor

**Ing. Jim Requena**  
Programación Web II | UPDS

## 📄 Licencia

Este proyecto es material educativo para el curso de Programación Web II.
