# Contributing to RavexClient

¡Gracias por considerar contribuir a RavexClient! 🎉

## Cómo Contribuir

### Reportar Bugs

Si encuentras un bug, por favor abre un issue con:
- Descripción clara del problema
- Pasos para reproducir
- Comportamiento esperado vs actual
- Versión de Python y RavexClient
- Código de ejemplo si es posible

### Proponer Features

Para proponer nuevas características:
1. Abre un issue describiendo la feature
2. Explica el caso de uso
3. Discute la implementación propuesta

### Pull Requests

1. Fork el repositorio
2. Crea una rama desde `main`: `git checkout -b feature/mi-feature`
3. Realiza tus cambios
4. Asegúrate de que el código siga el estilo del proyecto
5. Agrega tests si es aplicable
6. Actualiza la documentación si es necesario
7. Commit tus cambios: `git commit -am 'Agrega nueva feature'`
8. Push a la rama: `git push origin feature/mi-feature`
9. Abre un Pull Request

## Estilo de Código

- Sigue PEP 8
- Usa type hints
- Documenta funciones públicas con docstrings
- Máximo 88 caracteres por línea (compatible con Black)

## Desarrollo Local

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/ravexclient.git
cd ravexclient

# Instalar dependencias de desarrollo
uv sync --dev

# Ejecutar tests
pytest

# Ejecutar linter
ruff check .

# Formatear código
black .
```

## Licencia

Al contribuir, aceptas que tus contribuciones serán licenciadas bajo la misma licencia del proyecto.
