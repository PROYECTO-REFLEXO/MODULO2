#!/usr/bin/env python3
"""
Script de pruebas para verificar los endpoints de HU02 y HU05
Ejecutar: python test_endpoints.py
"""

import requests
import json
import os
from datetime import datetime

# Configuración
BASE_URL = "http://127.0.0.1:8000/api"
TOKEN = None  # Se obtendrá después del login

def print_test_result(test_name, success, message=""):
    """Imprime el resultado de una prueba"""
    status = "✅ PASÓ" if success else "❌ FALLÓ"
    print(f"{status} {test_name}")
    if message:
        print(f"   {message}")
    print()

def test_server_connection():
    """Prueba la conexión básica al servidor"""
    try:
        response = requests.get(f"{BASE_URL.replace('/api', '')}")
        return True, "Servidor respondiendo"
    except requests.exceptions.ConnectionError:
        return False, "No se puede conectar al servidor. Asegúrate de que Django esté corriendo."

def test_login():
    """Prueba el endpoint de login"""
    global TOKEN
    
    # Datos de prueba (ajusta según tu base de datos)
    login_data = {
        "username": "admin@example.com",  # Cambia por un usuario real
        "password": "admin123"  # Cambia por la contraseña real
    }
    
    try:
        response = requests.post(f"{BASE_URL}/profile/login/", data=login_data)
        
        if response.status_code == 200:
            data = response.json()
            TOKEN = data.get('token') or data.get('access')  # Depende de la implementación
            return True, f"Login exitoso. Token obtenido: {TOKEN[:20]}..."
        else:
            return False, f"Login falló. Status: {response.status_code}, Response: {response.text}"
    except Exception as e:
        return False, f"Error en login: {str(e)}"

def test_get_profile():
    """Prueba obtener el perfil del usuario"""
    if not TOKEN:
        return False, "No hay token disponible"
    
    headers = {"Authorization": f"Bearer {TOKEN}"}
    
    try:
        response = requests.get(f"{BASE_URL}/profile/me/", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            return True, f"Perfil obtenido: {data.get('first_name', 'N/A')} {data.get('last_name', 'N/A')}"
        else:
            return False, f"Error al obtener perfil. Status: {response.status_code}, Response: {response.text}"
    except Exception as e:
        return False, f"Error: {str(e)}"

def test_update_profile():
    """Prueba actualizar el perfil del usuario"""
    if not TOKEN:
        return False, "No hay token disponible"
    
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Datos de prueba
    update_data = {
        "first_name": "Test",
        "last_name": "User",
        "phone": "+1234567890"
    }
    
    try:
        response = requests.put(f"{BASE_URL}/profile/me/", 
                              headers=headers, 
                              data=json.dumps(update_data))
        
        if response.status_code == 200:
            data = response.json()
            return True, f"Perfil actualizado: {data.get('message', 'OK')}"
        else:
            return False, f"Error al actualizar perfil. Status: {response.status_code}, Response: {response.text}"
    except Exception as e:
        return False, f"Error: {str(e)}"

def test_search_users():
    """Prueba la búsqueda de usuarios"""
    if not TOKEN:
        return False, "No hay token disponible"
    
    headers = {"Authorization": f"Bearer {TOKEN}"}
    
    # Parámetros de búsqueda
    params = {
        "search": "test",
        "per_page": 10,
        "page": 1
    }
    
    try:
        response = requests.get(f"{BASE_URL}/users/search/", 
                              headers=headers, 
                              params=params)
        
        if response.status_code == 200:
            data = response.json()
            total = data.get('total', 0)
            results = data.get('results', [])
            return True, f"Búsqueda exitosa. Total: {total}, Resultados: {len(results)}"
        else:
            return False, f"Error en búsqueda. Status: {response.status_code}, Response: {response.text}"
    except Exception as e:
        return False, f"Error: {str(e)}"

def test_get_all_users():
    """Prueba obtener todos los usuarios"""
    if not TOKEN:
        return False, "No hay token disponible"
    
    headers = {"Authorization": f"Bearer {TOKEN}"}
    
    try:
        response = requests.get(f"{BASE_URL}/users/", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            total = data.get('total', 0)
            results = data.get('results', [])
            return True, f"Usuarios obtenidos. Total: {total}, Resultados: {len(results)}"
        else:
            return False, f"Error al obtener usuarios. Status: {response.status_code}, Response: {response.text}"
    except Exception as e:
        return False, f"Error: {str(e)}"

def test_upload_photo():
    """Prueba subir una foto de perfil"""
    if not TOKEN:
        return False, "No hay token disponible"
    
    headers = {"Authorization": f"Bearer {TOKEN}"}
    
    # Crear un archivo de prueba simple
    test_image_path = "test_image.jpg"
    try:
        # Crear una imagen de prueba (1x1 pixel JPEG)
        with open(test_image_path, "wb") as f:
            f.write(b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342\xff\xc0\x00\x11\x08\x00\x01\x00\x01\x01\x01\x11\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00\x3f\x00\xaa\xff\xd9')
        
        with open(test_image_path, "rb") as f:
            files = {"photo": f}
            response = requests.put(f"{BASE_URL}/profile/photo/1/upload/", 
                                  headers=headers, 
                                  files=files)
        
        # Limpiar archivo de prueba
        if os.path.exists(test_image_path):
            os.remove(test_image_path)
        
        if response.status_code == 200:
            data = response.json()
            return True, f"Foto subida: {data.get('message', 'OK')}"
        else:
            return False, f"Error al subir foto. Status: {response.status_code}, Response: {response.text}"
    except Exception as e:
        # Limpiar archivo de prueba en caso de error
        if os.path.exists(test_image_path):
            os.remove(test_image_path)
        return False, f"Error: {str(e)}"

def test_delete_photo():
    """Prueba eliminar una foto de perfil"""
    if not TOKEN:
        return False, "No hay token disponible"
    
    headers = {"Authorization": f"Bearer {TOKEN}"}
    
    try:
        response = requests.delete(f"{BASE_URL}/profile/photo/1/delete/", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            return True, f"Foto eliminada: {data.get('message', 'OK')}"
        elif response.status_code == 404:
            return True, "No hay foto para eliminar (esperado)"
        else:
            return False, f"Error al eliminar foto. Status: {response.status_code}, Response: {response.text}"
    except Exception as e:
        return False, f"Error: {str(e)}"

def run_all_tests():
    """Ejecuta todas las pruebas"""
    print("🧪 INICIANDO PRUEBAS DE ENDPOINTS")
    print("=" * 50)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Base URL: {BASE_URL}")
    print()
    
    tests = [
        ("Conexión al servidor", test_server_connection),
        ("Login", test_login),
        ("Obtener perfil", test_get_profile),
        ("Actualizar perfil", test_update_profile),
        ("Buscar usuarios", test_search_users),
        ("Obtener todos los usuarios", test_get_all_users),
        ("Subir foto", test_upload_photo),
        ("Eliminar foto", test_delete_photo),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        success, message = test_func()
        print_test_result(test_name, success, message)
        if success:
            passed += 1
    
    print("=" * 50)
    print(f"RESULTADOS: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron! Los endpoints están funcionando correctamente.")
    else:
        print("⚠️  Algunas pruebas fallaron. Revisa los errores arriba.")
    
    return passed == total

if __name__ == "__main__":
    run_all_tests()

