# app/utils/validators.py
"""
Validadores y funciones de utilidad
Funciones reutilizables para validación de datos
"""

import re

def validar_email(email):
    """
    Valida que el email tenga un formato correcto
    
    Args:
        email: Email a validar
        
    Returns:
        bool: True si el email es válido, False en caso contrario
    """
    if not email:
        return False
    
    # Patrón simple de email
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(patron, email))


def validar_string_no_vacio(texto):
    """
    Valida que un string no esté vacío después de quitar espacios
    
    Args:
        texto: Texto a validar
        
    Returns:
        bool: True si el texto no está vacío, False en caso contrario
    """
    if not texto or not isinstance(texto, str):
        return False
    return len(texto.strip()) > 0


def validar_prioridad(prioridad):
    """
    Valida que la prioridad sea válida
    
    Args:
        prioridad: Prioridad a validar
        
    Returns:
        bool: True si la prioridad es válida, False en caso contrario
    """
    if not prioridad:
        return False
    
    prioridades_validas = ['alta', 'media', 'baja']
    return prioridad.lower() in prioridades_validas


def validar_rol(rol):
    """
    Valida que el rol sea válido
    
    Args:
        rol: Rol a validar
        
    Returns:
        bool: True si el rol es válido, False en caso contrario
    """
    if not rol:
        return False
    
    roles_validos = ['administrador', 'usuario']
    return rol.lower() in roles_validos


def sanitizar_string(texto):
    """
    Limpia un string eliminando espacios extra
    
    Args:
        texto: Texto a limpiar
        
    Returns:
        str: Texto limpio o None si el input es inválido
    """
    if not texto or not isinstance(texto, str):
        return None
    return texto.strip()


def validar_id_positivo(id_value):
    """
    Valida que un ID sea un entero positivo
    
    Args:
        id_value: ID a validar
        
    Returns:
        bool: True si el ID es válido, False en caso contrario
    """
    try:
        return int(id_value) > 0
    except (ValueError, TypeError):
        return False
