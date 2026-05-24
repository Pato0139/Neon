# Mini repositorio de credenciales para Constru-Trans_01

Este mini repositorio guarda las credenciales (`.env`) que necesita el proyecto
**Constru-Trans_01** para conectarse a la base de datos **Neon** y para enviar
los correos de **recuperación de contraseña** desde la cuenta
`construtrans588@gmail.com`.

## Estructura

```
Neon/
├── .env.example        # Plantilla con TODAS las variables que pide Django
├── .env                # (se genera con `create`, NUNCA se sube a git)
├── env_manager.py      # Script para gestionar el .env
└── env_repo/
    ├── backups/        # Backups automáticos con timestamp
    └── versions/       # Versiones nombradas (development, production, ...)
```

## Flujo recomendado (la primera vez)

```bash
# 1. Crear el .env real a partir de la plantilla
python env_manager.py create

# 2. (Opcional) probar que las credenciales de Gmail funcionen
python env_manager.py test-email

# 3. Copiar el .env al proyecto Constru-trans_01
python env_manager.py deploy
#   (o: python env_manager.py deploy C:/ruta/a/Constru-trans_01)

# 4. Guardar la versión como "produccion" o "construtrans"
python env_manager.py save construtrans
```

Después, dentro del proyecto Constru-trans_01:

```bash
python manage.py migrate
python manage.py runserver
```

Y en el navegador entras a `http://127.0.0.1:8000/usuarios/recuperar-password/`
y verás que llega el correo a la bandeja indicada.

## Todos los comandos

| Comando | Qué hace |
|---|---|
| `init` | Crea las carpetas `env_repo/backups` y `env_repo/versions` |
| `create` | Copia `.env.example` → `.env` |
| `backup` | Guarda un backup del `.env` actual con timestamp |
| `save <nombre>` | Guarda el `.env` como una versión nombrada |
| `restore <nombre>` | Restaura una versión nombrada (hace backup antes) |
| `list` | Lista todas las versiones y backups |
| `deploy [ruta]` | Copia el `.env` a la carpeta de **Constru-trans_01** |
| `test-email` | Envía un correo de prueba con las credenciales del `.env` |
| `guide` | Muestra una guía para obtener las credenciales |

## ¿Qué variables debe tener el `.env`?

El proyecto **Constru-trans_01** usa los nombres que pone Django por
convención. Las dos secciones críticas son:

### Base de datos Neon
```
DATABASE_URL=postgresql://USUARIO:PASSWORD@HOST.neon.tech/neondb?sslmode=require
```

### Correo (para recuperación de contraseña)
```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend   # ¡imprescindible!
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=construtrans588@gmail.com
EMAIL_HOST_PASSWORD=<App Password de 16 caracteres>
DEFAULT_FROM_EMAIL=Constru-Trans <construtrans588@gmail.com>
```

⚠️ Si **no** pones `EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend`,
Django no envía el correo y solo lo imprime en la consola — los usuarios nunca
recibirán el enlace para restablecer su contraseña.

## ¿Cómo obtengo el App Password de Gmail?

1. Entra a <https://myaccount.google.com/security> con la cuenta
   `construtrans588@gmail.com`.
2. Activa la **Verificación en dos pasos** si todavía no la tienes.
3. Ve a <https://myaccount.google.com/apppasswords>.
4. Crea una nueva contraseña de aplicación (nombre: *Constru-Trans Django*).
5. Copia los **16 caracteres** que te aparecen (sin espacios) y pégalos en
   `EMAIL_HOST_PASSWORD` dentro de `.env`.

## Notas de seguridad

* El archivo `.env` está en `.gitignore` y **nunca** se sube al repositorio.
* Antes de cada `restore` o `deploy` se crea un backup automático del `.env`
  anterior — así nunca pierdes credenciales por accidente.
* Si crees que el App Password se filtró, revócalo desde la página de
  *App Passwords* de Google y genera uno nuevo.
