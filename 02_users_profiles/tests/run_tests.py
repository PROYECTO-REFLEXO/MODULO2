#!/usr/bin/env python
"""
Script optimizado para ejecutar tests del módulo 02_users_profiles
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_settings_simple')

# Agregar el directorio actual al path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

import django
django.setup()


def run_command(command, description):
    """Ejecuta un comando y muestra el resultado"""
    print(f"\n{'='*60}")
    print(f"🔍 {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=current_dir
        )
        
        if result.stdout:
            print(result.stdout)
        
        if result.stderr:
            print(f"⚠️ Errores:\n{result.stderr}")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Error ejecutando comando: {e}")
        return False


def run_optimized_tests():
    """Ejecuta los tests optimizados"""
    print("🚀 EJECUTANDO TESTS OPTIMIZADOS")
    print("="*60)
    
    # Lista de archivos de tests optimizados
    test_files = [
        'tests/test_models.py',
        'tests/test_views.py',
        'tests/test_integration.py'
    ]
    
    # Verificar que los archivos existen
    missing_files = []
    for test_file in test_files:
        if not Path(test_file).exists():
            missing_files.append(test_file)
    
    if missing_files:
        print(f"❌ Archivos de tests faltantes: {missing_files}")
        return False
    
    # Ejecutar tests optimizados
    test_files_str = ' '.join(test_files)
    command = f"python -m pytest {test_files_str} -v --tb=short"
    
    return run_command(command, "Ejecutando tests optimizados")


def run_all_tests():
    """Ejecuta todos los tests"""
    print("🚀 EJECUTANDO TODOS LOS TESTS")
    print("="*60)
    
    command = "python -m pytest tests/ -v --tb=short"
    return run_command(command, "Ejecutando todos los tests")


def run_tests_by_type(test_type):
    """Ejecuta tests por tipo"""
    print(f"🚀 EJECUTANDO TESTS DE TIPO: {test_type.upper()}")
    print("="*60)
    
    if test_type == 'models':
        command = "python -m pytest tests/test_models.py -v --tb=short"
    elif test_type == 'views':
        command = "python -m pytest tests/test_views.py -v --tb=short"
    elif test_type == 'integration':
        command = "python -m pytest tests/test_integration.py -v --tb=short"
    elif test_type == 'unit':
        command = "python -m pytest tests/ -m unit -v --tb=short"
    else:
        print(f"❌ Tipo de test no válido: {test_type}")
        return False
    
    return run_command(command, f"Ejecutando tests de {test_type}")


def run_tests_with_coverage():
    """Ejecuta tests con cobertura"""
    print("🚀 EJECUTANDO TESTS CON COBERTURA")
    print("="*60)
    
    command = "python -m pytest tests/test_models.py tests/test_views.py tests/test_integration.py --cov=. --cov-report=html --cov-report=term-missing -v"
    return run_command(command, "Ejecutando tests con cobertura")


def run_fast_tests():
    """Ejecuta solo tests rápidos (sin integración)"""
    print("🚀 EJECUTANDO TESTS RÁPIDOS")
    print("="*60)
    
    command = "python -m pytest tests/test_models.py tests/test_views.py -v --tb=short"
    return run_command(command, "Ejecutando tests rápidos")


def show_test_summary():
    """Muestra un resumen de los tests disponibles"""
    print("📊 RESUMEN DE TESTS DISPONIBLES")
    print("="*60)
    
    test_files = [
        'test_models.py',
        'test_views.py', 
        'test_integration.py'
    ]
    
    print(f"\nTests disponibles:")
    for file in test_files:
        file_path = Path(f"tests/{file}")
        if file_path.exists():
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} (no encontrado)")
    
    print(f"\n📈 Estadísticas:")
    existing_count = sum(1 for f in test_files if Path(f"tests/{f}").exists())
    print(f"  - Tests disponibles: {existing_count}/{len(test_files)}")
    
    if existing_count == len(test_files):
        print("  - ✅ Todos los tests están disponibles")
    else:
        print("  - ⚠️ Algunos tests faltan")


def main():
    """Función principal"""
    parser = argparse.ArgumentParser(description='Script optimizado para ejecutar tests')
    parser.add_argument(
        '--mode',
        choices=['optimized', 'all', 'fast', 'coverage'],
        default='optimized',
        help='Modo de ejecución de tests'
    )
    parser.add_argument(
        '--type',
        choices=['models', 'views', 'integration', 'unit'],
        help='Tipo específico de tests a ejecutar'
    )
    parser.add_argument(
        '--summary',
        action='store_true',
        help='Mostrar resumen de tests disponibles'
    )
    
    args = parser.parse_args()
    
    print("🧪 SISTEMA DE TESTS OPTIMIZADO - MÓDULO 02_USERS_PROFILES")
    print("="*60)
    
    if args.summary:
        show_test_summary()
        return
    
    success = False
    
    if args.type:
        success = run_tests_by_type(args.type)
    elif args.mode == 'optimized':
        success = run_optimized_tests()
    elif args.mode == 'all':
        success = run_all_tests()
    elif args.mode == 'fast':
        success = run_fast_tests()
    elif args.mode == 'coverage':
        success = run_tests_with_coverage()
    
    print(f"\n{'='*60}")
    if success:
        print("🎉 ¡TESTS EJECUTADOS EXITOSAMENTE!")
    else:
        print("❌ HUBO ERRORES EN LA EJECUCIÓN DE TESTS")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
