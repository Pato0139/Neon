#!/usr/bin/env python3
import os
import shutil
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_FILE = os.path.join(BASE_DIR, '.env')
ENV_EXAMPLE = os.path.join(BASE_DIR, '.env.example')
REPO_DIR = os.path.join(BASE_DIR, 'env_repo')
BACKUPS_DIR = os.path.join(REPO_DIR, 'backups')
VERSIONS_DIR = os.path.join(REPO_DIR, 'versions')


def init():
    """Inicializa el repositorio si no existe"""
    for dir_path in [REPO_DIR, BACKUPS_DIR, VERSIONS_DIR]:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(f"Creado directorio: {dir_path}")


def create_from_example():
    """Crea el archivo .env desde .env.example"""
    if not os.path.exists(ENV_EXAMPLE):
        print("Error: No existe el archivo .env.example")
        return
    
    if os.path.exists(ENV_FILE):
        print("Error: El archivo .env ya existe. Usa backup primero si necesitas guardarlo.")
        return
    
    shutil.copy2(ENV_EXAMPLE, ENV_FILE)
    print("Archivo .env creado desde .env.example")
    print("IMPORTANTE: Edita el archivo .env y agrega tus credenciales reales!")


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


def deploy(destino=None):
    """Copia el .env al proyecto Constru-trans_01 (o ruta indicada)."""
    if not os.path.exists(ENV_FILE):
        print("Error: No existe .env. Ejecuta primero: python env_manager.py create")
        return

    # Rutas candidatas si no se pasa una explícita
    if destino is None:
        candidatos = [
            os.path.expanduser('~/Constru-trans_01'),
            os.path.expanduser('~/Documents/Constru-trans_01'),
            os.path.expanduser('~/Desktop/Constru-trans_01'),
            os.path.join(os.path.dirname(BASE_DIR), 'Constru-trans_01'),
        ]
        destino = next((c for c in candidatos if os.path.isdir(c)), None)
        if destino is None:
            print("No encontré Constru-trans_01 automáticamente.")
            print("Usa: python env_manager.py deploy <ruta-al-proyecto>")
            return

    if not os.path.isdir(destino):
        print(f"Error: la carpeta {destino} no existe")
        return

    # Verificar que sea el proyecto correcto (debe tener manage.py)
    if not os.path.isfile(os.path.join(destino, 'manage.py')):
        print(f"Aviso: en {destino} no se encontró manage.py.")
        print("¿Seguro que es la raíz del proyecto Constru-trans_01? (s/N)")
        respuesta = input().strip().lower()
        if respuesta != 's':
            print("Cancelado")
            return

    destino_env = os.path.join(destino, '.env')
    if os.path.exists(destino_env):
        # Backup del .env existente en el destino
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_destino = os.path.join(destino, f'.env.backup_{timestamp}')
        shutil.copy2(destino_env, backup_destino)
        print(f"Backup del .env anterior: {backup_destino}")

    shutil.copy2(ENV_FILE, destino_env)
    print(f"✅ .env copiado a: {destino_env}")
    print("Ya puedes iniciar Django y probar la recuperación de contraseña.")


def test_email():
    """Envía un correo de prueba con las credenciales del .env actual."""
    import smtplib
    from email.mime.text import MIMEText

    if not os.path.exists(ENV_FILE):
        print("Error: No existe .env. Ejecuta primero: python env_manager.py create")
        return

    # Leer variables del .env
    env = {}
    with open(ENV_FILE, encoding='utf-8') as f:
        for linea in f:
            linea = linea.strip()
            if not linea or linea.startswith('#') or '=' not in linea:
                continue
            clave, _, valor = linea.partition('=')
            env[clave.strip()] = valor.strip()

    host = env.get('EMAIL_HOST', 'smtp.gmail.com')
    port = int(env.get('EMAIL_PORT', 587))
    user = env.get('EMAIL_HOST_USER')
    password = env.get('EMAIL_HOST_PASSWORD')

    if not user or not password:
        print("Error: faltan EMAIL_HOST_USER o EMAIL_HOST_PASSWORD en el .env")
        return

    destinatario = input(f"Correo destinatario para la prueba [{user}]: ").strip() or user

    mensaje = MIMEText(
        "Este es un correo de prueba de Constru-Trans.\n"
        "Si lo recibes, la recuperación de contraseña ya está lista.",
        'plain', 'utf-8'
    )
    mensaje['Subject'] = '[Constru-Trans] Prueba de configuración de correo'
    mensaje['From'] = env.get('DEFAULT_FROM_EMAIL', user)
    mensaje['To'] = destinatario

    print(f"Conectando a {host}:{port} como {user}...")
    try:
        with smtplib.SMTP(host, port, timeout=30) as smtp:
            smtp.starttls()
            smtp.login(user, password)
            smtp.send_message(mensaje)
        print(f"✅ Correo enviado a {destinatario}. Revisa la bandeja (y spam).")
    except smtplib.SMTPAuthenticationError:
        print("❌ Error de autenticación. Revisa EMAIL_HOST_PASSWORD (App Password de 16 caracteres).")
    except Exception as exc:
        print(f"❌ Error al enviar: {exc}")


def show_credentials_guide():
    """Muestra una guía para obtener las credenciales"""
    print("""
=== GUÍA PARA OBTENER CREDENCIALES ===

1. CREDENCIALES DE NEON:
   - Ve a https://console.neon.tech
   - Selecciona tu proyecto
   - Ve a la sección "Connection String" o "Connect"
   - Copia las credenciales: host, port, database, user, password
   - Puedes usar la URL completa en NEON_DATABASE_URL

2. CREDENCIALES DE GMAIL:
   - Ve a https://myaccount.google.com/security
   - Habilita la "Verificación en dos pasos" si no la tienes
   - Luego ve a "Contraseñas de aplicaciones"
   - Crea una nueva contraseña de aplicación
   - Usa tu correo normal en GMAIL_USER
   - Usa la contraseña de aplicación en GMAIL_APP_PASSWORD
""")


def main():
    import sys
    if len(sys.argv) < 2:
        print("""
Uso: python env_manager.py [comando] [opciones]

Comandos:
  init                - Inicializa el repositorio
  create              - Crea .env desde .env.example
  backup              - Crea un backup del .env actual
  save <nombre>       - Guarda una versión con nombre (ej: save development)
  restore <nombre>    - Restaura una versión (ej: restore production)
  list                - Lista todas las versiones y backups
  deploy [ruta]       - Copia el .env a Constru-trans_01 (autodetecta si no
                        se pasa ruta). Hace backup del .env anterior.
  test-email          - Envía un correo de prueba con las credenciales
                        del .env (verifica que la recuperación de contraseña
                        funcione antes de subirla al proyecto).
  guide               - Muestra guía para obtener credenciales
        """)
        return

    command = sys.argv[1]

    init()

    if command == 'init':
        print("Repositorio inicializado")
    elif command == 'create':
        create_from_example()
    elif command == 'backup':
        backup()
    elif command == 'save' and len(sys.argv) == 3:
        save_version(sys.argv[2])
    elif command == 'restore' and len(sys.argv) == 3:
        restore_version(sys.argv[2])
    elif command == 'list':
        list_versions()
    elif command == 'deploy':
        deploy(sys.argv[2] if len(sys.argv) == 3 else None)
    elif command == 'test-email':
        test_email()
    elif command == 'guide':
        show_credentials_guide()
    else:
        print("Comando inválido. Usa 'python env_manager.py' para ver ayuda")


if __name__ == '__main__':
    main()
