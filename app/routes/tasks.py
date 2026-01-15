# app/routes/tasks.py
"""
Rutas de Tareas (Blueprint)
Endpoints para gestión de tareas
"""

from flask import Blueprint, jsonify, request
from app.services import task_service

# Crear Blueprint
tasks_bp = Blueprint('tasks', __name__)


@tasks_bp.route('/tasks', methods=['GET'])
def listar_tareas():
    """
    GET /api/tasks
    Lista todas las tareas
    
    Query params opcionales:
        - completada: true/false (filtra por estado)
        - prioridad: alta/media/baja (filtra por prioridad)
    
    Returns:
        JSON: Lista de tareas con código 200
    """
    # Filtros opcionales
    completada = request.args.get('completada')
    prioridad = request.args.get('prioridad')
    
    if completada is not None:
        if completada.lower() == 'true':
            tareas = task_service.obtener_tareas_completadas()
        else:
            tareas = task_service.obtener_tareas_pendientes()
    elif prioridad:
        tareas = task_service.obtener_tareas_por_prioridad(prioridad)
    else:
        tareas = task_service.obtener_todas_tareas()
    
    return jsonify(tareas), 200


@tasks_bp.route('/tasks/<int:task_id>', methods=['GET'])
def obtener_tarea(task_id):
    """
    GET /api/tasks/<id>
    Obtiene una tarea específica
    
    Args:
        task_id: ID de la tarea
    
    Returns:
        JSON: Datos de la tarea con código 200, o error 404
    """
    tarea = task_service.obtener_tarea_por_id(task_id)
    
    if not tarea:
        return jsonify({'error': 'Tarea no encontrada'}), 404
    
    return jsonify(tarea), 200


@tasks_bp.route('/tasks', methods=['POST'])
def crear_tarea():
    """
    POST /api/tasks
    Crea una nueva tarea
    
    Body JSON esperado:
        {
            "titulo": "string",
            "descripcion": "string" (opcional),
            "prioridad": "string" (opcional: alta/media/baja),
            "usuario_id": int (opcional)
        }
    
    Returns:
        JSON: Tarea creada con código 201, o error 400
    """
    data = request.get_json()
    
    tarea, error = task_service.crear_tarea(data)
    
    if error:
        return jsonify({'error': error}), 400
    
    return jsonify(tarea), 201


@tasks_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def actualizar_tarea(task_id):
    """
    PUT /api/tasks/<id>
    Actualiza una tarea existente
    
    Args:
        task_id: ID de la tarea
    
    Body JSON (campos opcionales):
        {
            "titulo": "string",
            "descripcion": "string",
            "completada": boolean,
            "prioridad": "string",
            "usuario_id": int
        }
    
    Returns:
        JSON: Tarea actualizada con código 200, o error 400/404
    """
    data = request.get_json()
    
    tarea, error = task_service.actualizar_tarea(task_id, data)
    
    if error:
        codigo = 404 if error == "Tarea no encontrada" else 400
        return jsonify({'error': error}), codigo
    
    return jsonify(tarea), 200


@tasks_bp.route('/tasks/<int:task_id>/complete', methods=['PATCH'])
def marcar_tarea_completada(task_id):
    """
    PATCH /api/tasks/<id>/complete
    Marca una tarea como completada
    
    Args:
        task_id: ID de la tarea
    
    Returns:
        JSON: Tarea actualizada con código 200, o error 404
    """
    tarea, error = task_service.marcar_tarea_completada(task_id)
    
    if error:
        return jsonify({'error': error}), 404
    
    return jsonify(tarea), 200


@tasks_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def eliminar_tarea(task_id):
    """
    DELETE /api/tasks/<id>
    Elimina una tarea
    
    Args:
        task_id: ID de la tarea
    
    Returns:
        JSON: Mensaje de confirmación con código 200, o error 404
    """
    exitoso, error = task_service.eliminar_tarea(task_id)
    
    if not exitoso:
        return jsonify({'error': error}), 404
    
    return jsonify({'message': 'Tarea eliminada exitosamente'}), 200


@tasks_bp.route('/tasks/completed', methods=['GET'])
def listar_tareas_completadas():
    """
    GET /api/tasks/completed
    Lista solo las tareas completadas
    
    Returns:
        JSON: Lista de tareas completadas con código 200
    """
    tareas = task_service.obtener_tareas_completadas()
    return jsonify(tareas), 200


@tasks_bp.route('/tasks/pending', methods=['GET'])
def listar_tareas_pendientes():
    """
    GET /api/tasks/pending
    Lista solo las tareas pendientes
    
    Returns:
        JSON: Lista de tareas pendientes con código 200
    """
    tareas = task_service.obtener_tareas_pendientes()
    return jsonify(tareas), 200
