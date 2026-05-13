#!/usr/bin/env python3
import os
import shutil
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_FILE = os.path.join(BASE_DIR, '.env')
REPO_DIR = os.path.join(BASE_DIR, 'env_repo')
BACKUPS_DIR = os.path.join(REPO_DIR, 'backups')
VERSIONS_DIR = os.path.join(REPO_DIR, 'versions')


def init():
    """Inicializa el repositorio si no existe"""
    for dir_path in [REPO_DIR, BACKUPS_DIR, VERSIONS_DIR]:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(f"Creado directorio: {dir_path}")


def backup():
    """Crea un backup del .env actual con timestamp"""
    if not os.path.exists(ENV_FILE):
        print("Error: No existe el archivo .env en el directorio principal")
        return

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_name = f'.env.backup_{timestamp}'
    backup_path = os.path.join(BACKUPS_DIR, backup_name)
    shutil.copy2(ENV_FILE, backup_path)
    print(f"Backup creado: {backup_path}")


def save_version(name):
    """Guarda una versión nombrada del .env"""
    if not os.path.exists(ENV_FILE):
        print("Error: No existe el archivo .env en el directorio principal")
        return

    version_path = os.path.join(VERSIONS_DIR, f'.env.{name}')
    shutil.copy2(ENV_FILE, version_path)
    print(f"Versión guardada: {version_path}")


def restore_version(name):
    """Restaura una versión nombrada"""
    version_path = os.path.join(VERSIONS_DIR, f'.env.{name}')
    if not os.path.exists(version_path):
        print(f"Error: No existe la versión {name}")
        return

    backup()
    shutil.copy2(version_path, ENV_FILE)
    print(f"Versión {name} restaurada")


def list_versions():
    """Lista todas las versiones disponibles"""
    print("\n=== VERSIONES GUARDADAS ===")
    if os.path.exists(VERSIONS_DIR):
        for filename in sorted(os.listdir(VERSIONS_DIR)):
            if filename.startswith('.env.'):
                print(f"- {filename.replace('.env.', '')}")
    else:
        print("No hay versiones guardadas")

    print("\n=== BACKUPS ===")
    if os.path.exists(BACKUPS_DIR):
        for filename in sorted(os.listdir(BACKUPS_DIR), reverse=True):
            if filename.startswith('.env.backup_'):
                print(f"- {filename}")
    else:
        print("No hay backups")


def main():
    import sys
    if len(sys.argv) < 2:
        print("""
Uso: python env_manager.py [comando] [opciones]

Comandos:
  init                - Inicializa el repositorio
  backup              - Crea un backup del .env actual
  save <nombre>       - Guarda una versión con nombre (ej: save development)
  restore <nombre>    - Restaura una versión (ej: restore production)
  list                - Lista todas las versiones y backups
        """)
        return

    command = sys.argv[1]

    init()

    if command == 'init':
        print("Repositorio inicializado")
    elif command == 'backup':
        backup()
    elif command == 'save' and len(sys.argv) == 3:
        save_version(sys.argv[2])
    elif command == 'restore' and len(sys.argv) == 3:
        restore_version(sys.argv[2])
    elif command == 'list':
        list_versions()
    else:
        print("Comando inválido. Usa 'python env_manager.py' para ver ayuda")


if __name__ == '__main__':
    main()
