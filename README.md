# RavexClient

**RavexClient** es un cliente HTTP base diseñado para facilitar la creación de clientes API reutilizables en Python. Proporciona una base sólida con soporte integrado para proxies, manejo de cookies, autenticación y gestión de errores.

## 🚀 Características

- ✅ **Cliente HTTP Asíncrono**: Basado en `httpx` para alto rendimiento
- ✅ **Soporte de Proxies**: Configuración fácil de proxies HTTP/HTTPS
- ✅ **Gestión de Cookies**: Soporte para Cloudflare clearance y cookies personalizadas
- ✅ **Manejo de Errores**: Excepciones personalizadas para mejor control de errores
- ✅ **Type Hints**: Totalmente tipado para mejor autocompletado en IDEs
- ✅ **Logging**: Sistema de logging integrado para debugging
- ✅ **Context Manager**: Soporte para uso con `async with`
- ✅ **Extensible**: Diseño ABC para fácil herencia y personalización

## 📦 Instalación

```bash
pip install ravexclient
```

O con uv:

```bash
uv add ravexclient
```

## 🔧 Uso Básico

### Crear tu propio cliente API

```python
from ravexclient import BaseClient

class MiAPIClient(BaseClient):
    BASE_URL = "https://api.ejemplo.com"
    
    async def obtener_usuario(self, user_id: int):
        """Obtener información de un usuario."""
        return await self._get(f"/usuarios/{user_id}")
    
    async def crear_usuario(self, nombre: str, email: str):
        """Crear un nuevo usuario."""
        payload = {"nombre": nombre, "email": email}
        return await self._post("/usuarios", payload=payload)
    
    async def actualizar_usuario(self, user_id: int, datos: dict):
        """Actualizar información de usuario."""
        return await self._put(f"/usuarios/{user_id}", payload=datos)
    
    async def eliminar_usuario(self, user_id: int):
        """Eliminar un usuario."""
        return await self._delete(f"/usuarios/{user_id}")
```

### Usar el cliente con Context Manager (Recomendado)

```python
async def main():
    async with MiAPIClient() as cliente:
        # Hacer requests
        usuario = await cliente.obtener_usuario(123)
        print(usuario)
    # El cliente se cierra automáticamente

# Ejecutar
import asyncio
asyncio.run(main())
```

### Usar el cliente manualmente

```python
async def main():
    cliente = MiAPIClient()
    try:
        usuario = await cliente.obtener_usuario(123)
        print(usuario)
    finally:
        await cliente.close()  # Importante: cerrar el cliente

asyncio.run(main())
```

## 🔐 Configuración Avanzada

### Uso con Proxy

```python
cliente = MiAPIClient(
    proxy="proxy.ejemplo.com:8080"
    # o con formato completo:
    # proxy="http://proxy.ejemplo.com:8080"
)
```

### Cloudflare Clearance

```python
cliente = MiAPIClient(
    cf_clearance="tu_token_de_cloudflare_aqui"
)
```

### URL Base Personalizada

```python
# Sobrescribir la URL base por instancia
cliente = MiAPIClient(
    base_url="https://api-staging.ejemplo.com"
)
```

### Timeout Personalizado

```python
cliente = MiAPIClient(
    timeout=60.0  # 60 segundos
)
```

### Headers Personalizados

```python
cliente = MiAPIClient(
    headers={
        "Authorization": "Bearer tu_token",
        "X-Custom-Header": "valor"
    }
)
```

### Configuración Completa

```python
cliente = MiAPIClient(
    base_url="https://api.ejemplo.com",
    proxy="proxy.ejemplo.com:8080",
    cf_clearance="tu_cf_clearance",
    timeout=30.0,
    headers={"Authorization": "Bearer token123"},
    verify=True,  # Verificación SSL
    follow_redirects=True,
)
```

## 🛠️ Métodos Disponibles

### Métodos Principales

- **`_fetch(method, endpoint, params, payload, headers, **kwargs)`**: Método principal para requests HTTP
- **`_get(endpoint, params, **kwargs)`**: Método de conveniencia para GET
- **`_post(endpoint, payload, **kwargs)`**: Método de conveniencia para POST
- **`_put(endpoint, payload, **kwargs)`**: Método de conveniencia para PUT
- **`_delete(endpoint, **kwargs)`**: Método de conveniencia para DELETE

### Métodos de Utilidad

- **`_check_ip()`**: Verifica la IP actual (útil para verificar proxies)
- **`close()`**: Cierra el cliente y libera recursos

## ⚠️ Manejo de Errores

RavexClient proporciona excepciones personalizadas para mejor control:

```python
from ravexclient import (
    HTTPError,
    ProxyError,
    AuthenticationError,
    ConfigurationError,
    TimeoutError,
)

async def ejemplo_manejo_errores():
    cliente = MiAPIClient()
    
    try:
        resultado = await cliente.obtener_usuario(999)
    except HTTPError as e:
        print(f"Error HTTP: {e.message}")
        print(f"Status Code: {e.status_code}")
        print(f"Response: {e.response_body}")
    except ProxyError as e:
        print(f"Error de proxy: {e}")
    except TimeoutError as e:
        print(f"Timeout: {e}")
    except ConfigurationError as e:
        print(f"Error de configuración: {e}")
    finally:
        await cliente.close()
```

## 📝 Ejemplo Completo

```python
from ravexclient import BaseClient, HTTPError
import asyncio

class GitHubClient(BaseClient):
    BASE_URL = "https://api.github.com"
    
    def __init__(self, token: str | None = None, **kwargs):
        super().__init__(**kwargs)
        if token:
            self.client.headers["Authorization"] = f"token {token}"
    
    async def get_user(self, username: str):
        """Obtener información de usuario de GitHub."""
        return await self._get(f"/users/{username}")
    
    async def get_repos(self, username: str):
        """Obtener repositorios de un usuario."""
        return await self._get(f"/users/{username}/repos")

async def main():
    async with GitHubClient() as client:
        try:
            # Obtener información de usuario
            user = await client.get_user("octocat")
            print(f"Usuario: {user['login']}")
            print(f"Nombre: {user['name']}")
            
            # Obtener repositorios
            repos = await client.get_repos("octocat")
            print(f"\nRepositorios ({len(repos)}):")
            for repo in repos[:5]:
                print(f"  - {repo['name']}: {repo['description']}")
                
        except HTTPError as e:
            print(f"Error: {e.message}")

if __name__ == "__main__":
    asyncio.run(main())
```

## 🧪 Testing

Para verificar la configuración del proxy:

```python
async def verificar_proxy():
    async with MiAPIClient(proxy="tu_proxy:puerto") as cliente:
        ip_info = await cliente._check_ip()
        print(f"IP actual: {ip_info['ip']}")

asyncio.run(verificar_proxy())
```

## 📚 Logging

RavexClient usa el módulo `logging` de Python. Para habilitar logs:

```python
import logging

# Configurar logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Ahora verás logs detallados de las requests
async with MiAPIClient() as cliente:
    await cliente.obtener_usuario(123)
```

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-feature`)
3. Commit tus cambios (`git commit -am 'Agrega nueva feature'`)
4. Push a la rama (`git push origin feature/nueva-feature`)
5. Crea un Pull Request

## 📄 Licencia
MIT License

## 👤 Autor

**Christian Flores**
- Email: christianmfm10@gmail.com

## 🔗 Links

- Repositorio: [GitHub](https://github.com/christifm10/ravexclient)
- Issues: [GitHub Issues](https://github.com/christianfm10/ravexclient/issues)
- PyPI: [ravexclient](https://pypi.org/project/ravexclient/)

---

**Nota**: Este es un cliente base diseñado para ser heredado. No está pensado para ser usado directamente, sino como base para construir tus propios clientes API específicos.
