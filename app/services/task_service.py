# app/services/task_service.py
"""
Servicio de Tareas
Contiene toda la lógica de negocio relacionada con tareas
"""

from app.models.task import Task
from app.utils.validators import validar_string_no_vacio, validar_prioridad, sanitizar_string
from app.services.user_service import verificar_usuario_existe

# Base de datos en memoria (temporal)
tasks_db = [
    Task(id=1, titulo='Diseñar base de datos', descripcion='Crear el modelo ER de TaskFlow',
         completada=True, prioridad='alta', usuario_id=1),
    Task(id=2, titulo='Implementar API REST', descripcion='Crear endpoints CRUD',
         completada=False, prioridad='alta', usuario_id=1),
    Task(id=3, titulo='Crear frontend con React', descripcion='Interfaces de usuario',
         completada=False, prioridad='media', usuario_id=2)
]

# Contador para IDs
next_task_id = 4


def obtener_todas_tareas():
    """
    Obtiene todas las tareas
    
    Returns:
        list: Lista de todas las tareas
    """
    return [task.to_dict() for task in tasks_db]


def obtener_tarea_por_id(task_id):
    """
    Obtiene una tarea por su ID
    
    Args:
        task_id: ID de la tarea a buscar
        
    Returns:
        dict: Datos de la tarea o None si no existe
    """
    for task in tasks_db:
        if task.id == task_id:
            return task.to_dict()
    return None


def obtener_tareas_por_usuario(user_id):
    """
    Obtiene todas las tareas de un usuario
    
    Args:
        user_id: ID del usuario
        
    Returns:
        list: Lista de tareas del usuario
    """
    tareas_usuario = [task.to_dict() for task in tasks_db 
                      if task.usuario_id == user_id]
    return tareas_usuario


def contar_tareas_por_usuario(user_id):
    """
    Cuenta cuántas tareas tiene asignadas un usuario
    
    Args:
        user_id: ID del usuario
        
    Returns:
        int: Cantidad de tareas
    """
    return len([task for task in tasks_db if task.usuario_id == user_id])


def crear_tarea(data):
    """
    Crea una nueva tarea con validaciones
    
    Args:
        data: Diccionario con los datos de la tarea
        
    Returns:
        tuple: (tarea_dict, error_message)
    """
    global next_task_id
    
    # Validar que existan datos
    if not data:
        return None, "No se enviaron datos"
    
    # Validar título
    titulo = sanitizar_string(data.get('titulo'))
    if not validar_string_no_vacio(titulo):
        return None, "El título es requerido y no puede estar vacío"
    
    # Validar prioridad (opcional)
    prioridad = data.get('prioridad', 'media').lower()
    if not validar_prioridad(prioridad):
        return None, "La prioridad debe ser: alta, media o baja"
    
    # Validar usuario_id (opcional)
    usuario_id = data.get('usuario_id')
    if usuario_id is not None:
        if not verificar_usuario_existe(usuario_id):
            return None, "El usuario asignado no existe"
    
    # Crear tarea
    nueva_tarea = Task(
        id=next_task_id,
        titulo=titulo,
        descripcion=sanitizar_string(data.get('descripcion', '')),
        completada=data.get('completada', False),
        prioridad=prioridad,
        usuario_id=usuario_id
    )
    
    tasks_db.append(nueva_tarea)
    next_task_id += 1
    
    return nueva_tarea.to_dict(), None


def actualizar_tarea(task_id, data):
    """
    Actualiza una tarea existente
    
    Args:
        task_id: ID de la tarea a actualizar
        data: Diccionario con los datos a actualizar
        
    Returns:
        tuple: (tarea_dict, error_message)
    """
    if not data:
        return None, "No se enviaron datos"
    
    # Buscar tarea
    tarea = None
    for task in tasks_db:
        if task.id == task_id:
            tarea = task
            break
    
    if not tarea:
        return None, "Tarea no encontrada"
    
    # Actualizar título si se envía
    if 'titulo' in data:
        titulo = sanitizar_string(data['titulo'])
        if not validar_string_no_vacio(titulo):
            return None, "El título no puede estar vacío"
        tarea.titulo = titulo
    
    # Actualizar descripción si se envía
    if 'descripcion' in data:
        tarea.descripcion = sanitizar_string(data['descripcion'])
    
    # Actualizar completada si se envía
    if 'completada' in data:
        tarea.completada = bool(data['completada'])
    
    # Actualizar prioridad si se envía
    if 'prioridad' in data:
        prioridad = data['prioridad'].lower()
        if not validar_prioridad(prioridad):
            return None, "La prioridad debe ser: alta, media o baja"
        tarea.prioridad = prioridad
    
    # Actualizar usuario_id si se envía
    if 'usuario_id' in data:
        usuario_id = data['usuario_id']
        if usuario_id is not None and not verificar_usuario_existe(usuario_id):
            return None, "El usuario asignado no existe"
        tarea.usuario_id = usuario_id
    
    return tarea.to_dict(), None


def marcar_tarea_completada(task_id):
    """
    Marca una tarea como completada
    
    Args:
        task_id: ID de la tarea
        
    Returns:
        tuple: (tarea_dict, error_message)
    """
    # Buscar tarea
    for task in tasks_db:
        if task.id == task_id:
            task.marcar_completada()
            return task.to_dict(), None
    
    return None, "Tarea no encontrada"


def eliminar_tarea(task_id):
    """
    Elimina una tarea
    
    Args:
        task_id: ID de la tarea a eliminar
        
    Returns:
        tuple: (success, error_message)
    """
    global tasks_db
    
    # Buscar y eliminar tarea
    for i, task in enumerate(tasks_db):
        if task.id == task_id:
            tasks_db.pop(i)
            return True, None
    
    return False, "Tarea no encontrada"


def obtener_tareas_completadas():
    """
    Obtiene solo las tareas completadas
    
    Returns:
        list: Lista de tareas completadas
    """
    return [task.to_dict() for task in tasks_db if task.completada]


def obtener_tareas_pendientes():
    """
    Obtiene solo las tareas pendientes
    
    Returns:
        list: Lista de tareas pendientes
    """
    return [task.to_dict() for task in tasks_db if not task.completada]


def obtener_tareas_por_prioridad(prioridad):
    """
    Obtiene tareas filtradas por prioridad
    
    Args:
        prioridad: Prioridad a filtrar (alta, media, baja)
        
    Returns:
        list: Lista de tareas con esa prioridad
    """
    if not validar_prioridad(prioridad):
        return []
    
    return [task.to_dict() for task in tasks_db 
            if task.prioridad == prioridad.lower()]


def obtener_estadisticas_usuario(user_id):
    """
    Obtiene estadísticas de tareas de un usuario
    
    Args:
        user_id: ID del usuario
        
    Returns:
        dict: Estadísticas del usuario
    """
    tareas_usuario = [task for task in tasks_db if task.usuario_id == user_id]
    
    total = len(tareas_usuario)
    completadas = len([t for t in tareas_usuario if t.completada])
    pendientes = total - completadas
    
    # Contar por prioridad
    alta = len([t for t in tareas_usuario if t.prioridad == 'alta'])
    media = len([t for t in tareas_usuario if t.prioridad == 'media'])
    baja = len([t for t in tareas_usuario if t.prioridad == 'baja'])
    
    return {
        'total': total,
        'completadas': completadas,
        'pendientes': pendientes,
        'por_prioridad': {
            'alta': alta,
            'media': media,
            'baja': baja
        }
    }
