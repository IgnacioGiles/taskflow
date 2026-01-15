# app/services/user_service.py
"""
Servicio de Usuarios
Contiene toda la lógica de negocio relacionada con usuarios
"""

from app.models.user import User
from app.utils.validators import validar_email, validar_string_no_vacio, sanitizar_string

# Base de datos en memoria (temporal)
users_db = [
    User(id=1, nombre='Admin', email='admin@taskflow.com', rol='administrador'),
    User(id=2, nombre='Juan Pérez', email='juan@email.com', rol='usuario')
]

# Contador para IDs
next_user_id = 3


def obtener_todos_usuarios():
    """
    Obtiene todos los usuarios
    
    Returns:
        list: Lista de todos los usuarios
    """
    return [user.to_dict() for user in users_db]


def obtener_usuario_por_id(user_id):
    """
    Obtiene un usuario por su ID
    
    Args:
        user_id: ID del usuario a buscar
        
    Returns:
        dict: Datos del usuario o None si no existe
    """
    for user in users_db:
        if user.id == user_id:
            return user.to_dict()
    return None


def obtener_usuario_por_email(email):
    """
    Obtiene un usuario por su email
    
    Args:
        email: Email del usuario a buscar
        
    Returns:
        User: Objeto User o None si no existe
    """
    for user in users_db:
        if user.email == email:
            return user
    return None


def crear_usuario(data):
    """
    Crea un nuevo usuario con validaciones
    
    Args:
        data: Diccionario con los datos del usuario
        
    Returns:
        tuple: (usuario_dict, error_message)
               Si exitoso: (datos_usuario, None)
               Si error: (None, mensaje_error)
    """
    global next_user_id
    
    # Validar que existan datos
    if not data:
        return None, "No se enviaron datos"
    
    # Validar nombre
    nombre = sanitizar_string(data.get('nombre'))
    if not validar_string_no_vacio(nombre):
        return None, "El nombre es requerido y no puede estar vacío"
    
    # Validar email
    email = sanitizar_string(data.get('email'))
    if not validar_email(email):
        return None, "El email no es válido"
    
    # Verificar email único
    if obtener_usuario_por_email(email):
        return None, "El email ya está registrado"
    
    # Validar rol (opcional)
    rol = data.get('rol', 'usuario').lower()
    roles_validos = ['administrador', 'usuario']
    if rol not in roles_validos:
        return None, f"El rol debe ser uno de: {', '.join(roles_validos)}"
    
    # Crear usuario
    nuevo_usuario = User(
        id=next_user_id,
        nombre=nombre,
        email=email,
        rol=rol
    )
    
    users_db.append(nuevo_usuario)
    next_user_id += 1
    
    return nuevo_usuario.to_dict(), None


def actualizar_usuario(user_id, data):
    """
    Actualiza un usuario existente
    
    Args:
        user_id: ID del usuario a actualizar
        data: Diccionario con los datos a actualizar
        
    Returns:
        tuple: (usuario_dict, error_message)
    """
    if not data:
        return None, "No se enviaron datos"
    
    # Buscar usuario
    usuario = None
    for user in users_db:
        if user.id == user_id:
            usuario = user
            break
    
    if not usuario:
        return None, "Usuario no encontrado"
    
    # Actualizar nombre si se envía
    if 'nombre' in data:
        nombre = sanitizar_string(data['nombre'])
        if not validar_string_no_vacio(nombre):
            return None, "El nombre no puede estar vacío"
        usuario.nombre = nombre
    
    # Actualizar email si se envía
    if 'email' in data:
        email = sanitizar_string(data['email'])
        if not validar_email(email):
            return None, "El email no es válido"
        
        # Verificar que el email no esté en uso por otro usuario
        if email != usuario.email:
            usuario_con_email = obtener_usuario_por_email(email)
            if usuario_con_email:
                return None, "El email ya está en uso"
        
        usuario.email = email
    
    # Actualizar rol si se envía
    if 'rol' in data:
        rol = data['rol'].lower()
        roles_validos = ['administrador', 'usuario']
        if rol not in roles_validos:
            return None, f"El rol debe ser uno de: {', '.join(roles_validos)}"
        usuario.rol = rol
    
    return usuario.to_dict(), None


def eliminar_usuario(user_id):
    """
    Elimina un usuario
    
    Args:
        user_id: ID del usuario a eliminar
        
    Returns:
        tuple: (success, error_message)
    """
    global users_db
    
    # Verificar si el usuario tiene tareas asignadas
    from app.services.task_service import contar_tareas_por_usuario
    
    if contar_tareas_por_usuario(user_id) > 0:
        return False, "No se puede eliminar un usuario con tareas asignadas"
    
    # Buscar y eliminar usuario
    for i, user in enumerate(users_db):
        if user.id == user_id:
            users_db.pop(i)
            return True, None
    
    return False, "Usuario no encontrado"


def verificar_usuario_existe(user_id):
    """
    Verifica si un usuario existe
    
    Args:
        user_id: ID del usuario a verificar
        
    Returns:
        bool: True si existe, False en caso contrario
    """
    return obtener_usuario_por_id(user_id) is not None
