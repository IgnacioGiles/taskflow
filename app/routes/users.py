# app/routes/users.py
"""
Rutas de Usuarios (Blueprint)
Endpoints para gestión de usuarios
"""

from flask import Blueprint, jsonify, request
from app.services import user_service

# Crear Blueprint
users_bp = Blueprint('users', __name__)


@users_bp.route('/users', methods=['GET'])
def listar_usuarios():
    """
    GET /api/users
    Lista todos los usuarios
    
    Returns:
        JSON: Lista de usuarios con código 200
    """
    usuarios = user_service.obtener_todos_usuarios()
    return jsonify(usuarios), 200


@users_bp.route('/users/<int:user_id>', methods=['GET'])
def obtener_usuario(user_id):
    """
    GET /api/users/<id>
    Obtiene un usuario específico
    
    Args:
        user_id: ID del usuario
        
    Returns:
        JSON: Datos del usuario con código 200, o error 404
    """
    usuario = user_service.obtener_usuario_por_id(user_id)
    
    if not usuario:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    
    return jsonify(usuario), 200


@users_bp.route('/users', methods=['POST'])
def crear_usuario():
    """
    POST /api/users
    Crea un nuevo usuario
    
    Body JSON esperado:
        {
            "nombre": "string",
            "email": "string",
            "rol": "string" (opcional)
        }
    
    Returns:
        JSON: Usuario creado con código 201, o error 400
    """
    data = request.get_json()
    
    usuario, error = user_service.crear_usuario(data)
    
    if error:
        return jsonify({'error': error}), 400
    
    return jsonify(usuario), 201


@users_bp.route('/users/<int:user_id>', methods=['PUT'])
def actualizar_usuario(user_id):
    """
    PUT /api/users/<id>
    Actualiza un usuario existente
    
    Args:
        user_id: ID del usuario
    
    Body JSON (campos opcionales):
        {
            "nombre": "string",
            "email": "string",
            "rol": "string"
        }
    
    Returns:
        JSON: Usuario actualizado con código 200, o error 400/404
    """
    data = request.get_json()
    
    usuario, error = user_service.actualizar_usuario(user_id, data)
    
    if error:
        codigo = 404 if error == "Usuario no encontrado" else 400
        return jsonify({'error': error}), codigo
    
    return jsonify(usuario), 200


@users_bp.route('/users/<int:user_id>', methods=['DELETE'])
def eliminar_usuario(user_id):
    """
    DELETE /api/users/<id>
    Elimina un usuario
    
    Args:
        user_id: ID del usuario
    
    Returns:
        JSON: Mensaje de confirmación con código 200, o error 400/404
    """
    exitoso, error = user_service.eliminar_usuario(user_id)
    
    if not exitoso:
        codigo = 404 if error == "Usuario no encontrado" else 400
        return jsonify({'error': error}), codigo
    
    return jsonify({'message': 'Usuario eliminado exitosamente'}), 200


@users_bp.route('/users/<int:user_id>/tasks', methods=['GET'])
def obtener_tareas_usuario(user_id):
    """
    GET /api/users/<id>/tasks
    Obtiene todas las tareas de un usuario
    
    Args:
        user_id: ID del usuario
    
    Returns:
        JSON: Lista de tareas del usuario con código 200, o error 404
    """
    # Verificar que el usuario existe
    if not user_service.verificar_usuario_existe(user_id):
        return jsonify({'error': 'Usuario no encontrado'}), 404
    
    from app.services import task_service
    tareas = task_service.obtener_tareas_por_usuario(user_id)
    
    return jsonify(tareas), 200


@users_bp.route('/users/<int:user_id>/stats', methods=['GET'])
def obtener_estadisticas_usuario(user_id):
    """
    GET /api/users/<id>/stats
    Obtiene estadísticas de tareas de un usuario
    
    Args:
        user_id: ID del usuario
    
    Returns:
        JSON: Estadísticas del usuario con código 200, o error 404
    """
    # Verificar que el usuario existe
    if not user_service.verificar_usuario_existe(user_id):
        return jsonify({'error': 'Usuario no encontrado'}), 404
    
    from app.services import task_service
    estadisticas = task_service.obtener_estadisticas_usuario(user_id)
    
    return jsonify(estadisticas), 200
