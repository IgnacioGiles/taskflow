# app.py
"""
Punto de entrada de la aplicación TaskFlow
Arranca el servidor Flask con arquitectura MVC
"""

import os
from app import create_app

# Obtener configuración del entorno (default: development)
config_name = os.getenv('FLASK_ENV', 'development')

# Crear la aplicación
app = create_app(config_name)

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("🚀 TaskFlow API v2.0 - MVC Architecture")
    print("=" * 60)
    print(f"\n📋 Configuración: {config_name}")
    print(f"🌐 Servidor: http://localhost:{app.config['PORT']}")
    print(f"🐛 Debug: {app.config['DEBUG']}")
    print("\n📚 Documentación de Endpoints:")
    print("\n👤 USUARIOS:")
    print("  GET    /api/users              - Listar usuarios")
    print("  GET    /api/users/<id>         - Obtener usuario")
    print("  POST   /api/users              - Crear usuario")
    print("  PUT    /api/users/<id>         - Actualizar usuario")
    print("  DELETE /api/users/<id>         - Eliminar usuario")
    print("  GET    /api/users/<id>/tasks   - Tareas del usuario")
    print("  GET    /api/users/<id>/stats   - Estadísticas del usuario")
    
    print("\n📝 TAREAS:")
    print("  GET    /api/tasks              - Listar tareas")
    print("  GET    /api/tasks/<id>         - Obtener tarea")
    print("  POST   /api/tasks              - Crear tarea")
    print("  PUT    /api/tasks/<id>         - Actualizar tarea")
    print("  PATCH  /api/tasks/<id>/complete - Marcar completada")
    print("  DELETE /api/tasks/<id>         - Eliminar tarea")
    print("  GET    /api/tasks/completed    - Tareas completadas")
    print("  GET    /api/tasks/pending      - Tareas pendientes")
    
    print("\n❤️  SALUD:")
    print("  GET    /api/health             - Estado del servidor")
    
    print("\n" + "=" * 60)
    print("💡 Presiona Ctrl+C para detener el servidor")
    print("=" * 60 + "\n")
    
    # Arrancar servidor
    app.run(host=app.config['HOST'], port=app.config['PORT'])
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )
