# Mini Repositorio para Archivos .env

Este mini repositorio te ayuda a gestionar tus archivos .env con backups y versiones nombradas.

## Estructura

```
neon/
├── .env                  # Tu archivo .env principal
├── env_manager.py        # Script de gestión
└── env_repo/
    ├── backups/          # Backups automáticos con timestamp
    └── versions/         # Versiones nombradas (dev, prod, etc.)
```

## Uso

### Inicializar el repositorio
```bash
python env_manager.py init
```

### Crear un backup del .env actual
```bash
python env_manager.py backup
```

### Guardar una versión con nombre
```bash
python env_manager.py save development
python env_manager.py save production
```

### Restaurar una versión
```bash
python env_manager.py restore development
```

### Listar todas las versiones y backups
```bash
python env_manager.py list
```

## Notas
- Siempre se hace un backup automático antes de restaurar una versión
- Los backups tienen un timestamp para identificar cuándo se crearon
