# app/services/user_service.py
"""
Servicio de Usuarios
Contiene toda la lógica de negocio relacionada con usuarios
Conecta con Supabase PostgreSQL
"""

import os
import httpx
from app.utils.validators import validar_email, validar_string_no_vacio, sanitizar_string

# Configuración de Supabase
SUPABASE_URL = os.getenv('SUPABASE_URL', '').rstrip('/')
SUPABASE_KEY = os.getenv('SUPABASE_KEY', '')

# Headers para Supabase
HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {SUPABASE_KEY}',
    'apikey': SUPABASE_KEY,
    'Prefer': 'return=representation'
}

# URL base para PostgREST
REST_URL = f"{SUPABASE_URL}/rest/v1"

print(f"DEBUG: SUPABASE_URL = {SUPABASE_URL}")
print(f"DEBUG: SUPABASE_KEY = {'*' * 10 if SUPABASE_KEY else 'NO ENCONTRADA'}")


def obtener_todos_usuarios():
    """
    Obtiene todos los usuarios desde Supabase
    
    Returns:
        list: Lista de todos los usuarios
    """
    try:
        response = httpx.get(
            f"{REST_URL}/users",
            headers=HEADERS
        )
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"Error al obtener usuarios: {e}")
        return []


def obtener_usuario_por_id(user_id):
    """
    Obtiene un usuario por su ID desde Supabase
    
    Args:
        user_id: ID (UUID) del usuario
        
    Returns:
        dict: Datos del usuario o None si no existe
    """
    try:
        response = httpx.get(
            f"{REST_URL}/users?id=eq.{user_id}",
            headers=HEADERS
        )
        if response.status_code == 200:
            data = response.json()
            return data[0] if data else None
        return None
    except Exception as e:
        print(f"Error al obtener usuario: {e}")
        return None


def obtener_usuario_por_email(email):
    """
    Obtiene un usuario por su email
    
    Args:
        email: Email del usuario
        
    Returns:
        dict: Datos del usuario o None si no existe
    """
    try:
        response = httpx.get(
            f"{REST_URL}/users?email=eq.{email}",
            headers=HEADERS
        )
        if response.status_code == 200:
            data = response.json()
            return data[0] if data else None
        return None
    except Exception as e:
        print(f"Error al buscar por email: {e}")
        return None


def crear_usuario(data):
    """
    Crea un nuevo usuario en Supabase
    
    Args:
        data: Diccionario con nombre, email, rol
        
    Returns:
        tuple: (usuario_dict, error_message)
    """
    try:
        # Validar datos
        if not data:
            return None, "No se enviaron datos"
        
        # Extraer campos
        nombre_raw = data.get('nombre')
        email_raw = data.get('email')
        
        if not nombre_raw:
            return None, "El nombre es requerido"
        if not email_raw:
            return None, "El email es requerido"
        
        # Limpiar datos
        nombre = sanitizar_string(nombre_raw)
        email = sanitizar_string(email_raw)
        
        if not validar_string_no_vacio(nombre):
            return None, "El nombre no puede estar vacío"
        
        if not validar_email(email):
            return None, "El email no es válido"
        
        # Verificar email único
        if obtener_usuario_por_email(email):
            return None, "El email ya está registrado"
        
        rol = data.get('rol', 'usuario').lower()
        roles_validos = ['administrador', 'usuario']
        if rol not in roles_validos:
            return None, f"Rol inválido. Debe ser: {', '.join(roles_validos)}"
        
        # Insertar en Supabase
        nuevo_usuario = {
            'nombre': nombre,
            'email': email,
            'rol': rol
        }
        response = httpx.post(
            f"{REST_URL}/users",
            headers=HEADERS,
            json=nuevo_usuario
        )
        
        if response.status_code == 201:
            resultado = response.json()
            return resultado[0] if isinstance(resultado, list) else resultado, None
        elif response.status_code == 409:
            return None, "El email ya está registrado en la base de datos"
        else:
            error_msg = f"Error Supabase ({response.status_code}): {response.text}"
            print(f"DEBUG: {error_msg}")
            return None, "Error al crear usuario"
    except Exception as e:
        error_msg = f"Excepción: {str(e)}"
        print(f"DEBUG: {error_msg}")
        return None, "Error interno al crear usuario"


def actualizar_usuario(user_id, data):
    """
    Actualiza un usuario en Supabase
    
    Args:
        user_id: ID del usuario
        data: Datos a actualizar
        
    Returns:
        tuple: (usuario_dict, error_message)
    """
    if not data:
        return None, "No se enviaron datos"
    
    # Verificar que existe
    if not obtener_usuario_por_id(user_id):
        return None, "Usuario no encontrado"
    
    # Validar datos si se envían
    if 'nombre' in data:
        nombre = sanitizar_string(data['nombre'])
        if not validar_string_no_vacio(nombre):
            return None, "El nombre no puede estar vacío"
    
    if 'email' in data:
        email = sanitizar_string(data['email'])
        if not validar_email(email):
            return None, "El email no es válido"
        
        # Verificar unicidad
        usuario_existente = obtener_usuario_por_email(email)
        if usuario_existente and usuario_existente.get('id') != user_id:
            return None, "El email ya está en uso"
    
    if 'rol' in data:
        rol = data['rol'].lower()
        if rol not in ['administrador', 'usuario']:
            return None, "Rol inválido"
    
    # Actualizar en Supabase
    try:
        response = httpx.patch(
            f"{REST_URL}/users?id=eq.{user_id}",
            headers=HEADERS,
            json=data
        )
        
        if response.status_code == 200:
            return response.json()[0] if isinstance(response.json(), list) else response.json(), None
        else:
            return None, f"Error: {response.text}"
    except Exception as e:
        return None, f"Error al actualizar: {str(e)}"


def eliminar_usuario(user_id):
    """
    Elimina un usuario de Supabase
    
    Args:
        user_id: ID del usuario
        
    Returns:
        tuple: (success, error_message)
    """
    # Verificar tareas asociadas
    from app.services.task_service import contar_tareas_por_usuario
    if contar_tareas_por_usuario(user_id) > 0:
        return False, "No se puede eliminar un usuario con tareas asignadas"
    
    try:
        response = httpx.delete(
            f"{REST_URL}/users?id=eq.{user_id}",
            headers=HEADERS
        )
        
        if response.status_code == 204:
            return True, None
        else:
            return False, f"Error: {response.text}"
    except Exception as e:
        return False, f"Error al eliminar: {str(e)}"


def verificar_usuario_existe(user_id):
    """
    Verifica si un usuario existe
    
    Args:
        user_id: ID del usuario
        
    Returns:
        bool: True si existe
    """
    return obtener_usuario_por_id(user_id) is not None
