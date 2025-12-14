"""
Ejemplo avanzado de uso de RavexClient.

Este ejemplo muestra características avanzadas como:
- Autenticación personalizada
- Manejo de rate limiting
- Reintentos automáticos
- Logging detallado
"""

import asyncio
import httpx
import logging
from typing import Any
from ravexclient import BaseClient, HTTPError, TimeoutError


# Configurar logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class AdvancedAPIClient(BaseClient):
    """Cliente API con características avanzadas."""

    BASE_URL = "https://api.example.com"

    def __init__(self, api_key: str, max_retries: int = 3, **kwargs):
        """
        Inicializar cliente avanzado.

        Args:
            api_key: Clave de API para autenticación.
            max_retries: Número máximo de reintentos en caso de error.
            **kwargs: Argumentos adicionales para BaseClient.
        """
        super().__init__(**kwargs)
        self.api_key = api_key
        self.max_retries = max_retries

        # Agregar header de autenticación
        self.client.headers["X-API-Key"] = api_key

    async def _fetch_with_retry(
        self,
        method: str,
        endpoint: str,
        max_retries: int | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Realizar request con reintentos automáticos.

        Args:
            method: Método HTTP.
            endpoint: Endpoint de la API.
            max_retries: Número de reintentos (usa self.max_retries si es None).
            **kwargs: Argumentos adicionales para _fetch.

        Returns:
            Respuesta JSON.

        Raises:
            HTTPError: Si todos los reintentos fallan.
        """
        retries = max_retries if max_retries is not None else self.max_retries
        last_error = None

        for attempt in range(retries + 1):
            try:
                logger.info(
                    f"Intento {attempt + 1}/{retries + 1} para {method} {endpoint}"
                )
                return await self._fetch(method, endpoint, **kwargs)

            except HTTPError as e:
                last_error = e

                # No reintentar en ciertos códigos de error
                if e.status_code in [400, 401, 403, 404]:
                    logger.error(f"Error no recuperable: {e.status_code}")
                    raise

                # Reintentar en errores 5xx o rate limiting
                if e.status_code in [429, 500, 502, 503, 504]:
                    if attempt < retries:
                        wait_time = 2**attempt  # Backoff exponencial
                        logger.warning(
                            f"Error {e.status_code}, reintentando en {wait_time}s..."
                        )
                        await asyncio.sleep(wait_time)
                        continue

                raise

            except TimeoutError as e:
                last_error = e
                if attempt < retries:
                    wait_time = 2**attempt
                    logger.warning(f"Timeout, reintentando en {wait_time}s...")
                    await asyncio.sleep(wait_time)
                    continue
                raise

        # Si llegamos aquí, todos los reintentos fallaron
        if last_error:
            raise last_error

    async def get_data(self, resource_id: int) -> dict:
        """Obtener datos con reintentos automáticos."""
        return await self._fetch_with_retry("GET", f"/data/{resource_id}")

    async def create_data(self, data: dict) -> dict:
        """Crear datos con reintentos automáticos."""
        return await self._fetch_with_retry("POST", "/data", payload=data)

    async def batch_get(self, resource_ids: list[int]) -> list[dict]:
        """
        Obtener múltiples recursos en paralelo.

        Args:
            resource_ids: Lista de IDs a obtener.

        Returns:
            Lista de respuestas.
        """
        tasks = [self.get_data(rid) for rid in resource_ids]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Filtrar errores
        successful_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Error obteniendo recurso {resource_ids[i]}: {result}")
            else:
                successful_results.append(result)

        return successful_results


class ProxyRotatingClient(BaseClient):
    """Cliente que rota entre múltiples proxies."""

    BASE_URL = "https://api.example.com"

    def __init__(self, proxies: list[str], **kwargs):
        """
        Inicializar cliente con rotación de proxies.

        Args:
            proxies: Lista de proxies en formato "host:port".
            **kwargs: Argumentos adicionales para BaseClient.
        """
        self.proxies = proxies
        self.current_proxy_index = 0
        super().__init__(proxy=self._get_next_proxy(), **kwargs)

    def _get_next_proxy(self) -> str:
        """Obtener el siguiente proxy en la rotación."""
        proxy = self.proxies[self.current_proxy_index]
        self.current_proxy_index = (self.current_proxy_index + 1) % len(self.proxies)
        return proxy

    async def rotate_proxy(self):
        """Cambiar al siguiente proxy."""
        next_proxy = self._get_next_proxy()
        logger.info(f"Rotando a proxy: {next_proxy}")

        # Cerrar cliente actual
        await self.client.aclose()

        # Crear nuevo cliente con nuevo proxy
        self.proxy = next_proxy
        proxy_url = (
            next_proxy if next_proxy.startswith("http") else f"http://{next_proxy}"
        )
        self.client = httpx.AsyncClient(
            cookies=self.cookies,
            proxy=proxy_url,
        )
        self.client.headers.update(
            {
                "Accept": "application/json",
                "User-Agent": "RavexClient/0.1.0",
            }
        )


async def example_advanced_features():
    """Ejemplo de características avanzadas."""

    # Ejemplo 1: Cliente con reintentos
    logger.info("=== Ejemplo 1: Cliente con reintentos ===")
    async with AdvancedAPIClient(
        api_key="your-api-key-here", timeout=10.0, max_retries=3
    ) as client:
        try:
            # Este endpoint podría fallar y se reintentará automáticamente
            data = await client.get_data(123)
            logger.info(f"Datos obtenidos: {data}")
        except HTTPError as e:
            logger.error(f"Error después de reintentos: {e}")

    # Ejemplo 2: Requests en batch
    logger.info("\n=== Ejemplo 2: Requests en paralelo ===")
    async with AdvancedAPIClient(api_key="your-api-key-here") as client:
        resource_ids = [1, 2, 3, 4, 5]
        results = await client.batch_get(resource_ids)
        logger.info(f"Obtenidos {len(results)} recursos exitosamente")

    # Ejemplo 3: Rotación de proxies
    logger.info("\n=== Ejemplo 3: Rotación de proxies ===")
    proxies = [
        "proxy1.example.com:8080",
        "proxy2.example.com:8080",
        "proxy3.example.com:8080",
    ]

    async with ProxyRotatingClient(proxies=proxies) as client:
        # Verificar IP inicial
        ip_info = await client._check_ip()
        logger.info(f"IP actual: {ip_info['ip']}")

        # Rotar proxy
        await client.rotate_proxy()

        # Verificar nueva IP
        ip_info = await client._check_ip()
        logger.info(f"Nueva IP: {ip_info['ip']}")


async def example_with_authentication():
    """Ejemplo con diferentes tipos de autenticación."""

    class BearerAuthClient(BaseClient):
        """Cliente con autenticación Bearer."""

        BASE_URL = "https://api.example.com"

        def __init__(self, token: str, **kwargs):
            super().__init__(**kwargs)
            self.client.headers["Authorization"] = f"Bearer {token}"

    class BasicAuthClient(BaseClient):
        """Cliente con autenticación básica."""

        BASE_URL = "https://api.example.com"

        def __init__(self, username: str, password: str, **kwargs):
            super().__init__(**kwargs)
            import base64

            credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
            self.client.headers["Authorization"] = f"Basic {credentials}"

    # Usar cliente con Bearer token
    async with BearerAuthClient(token="your-token-here") as client:
        logger.info("Cliente Bearer Auth inicializado")

    # Usar cliente con autenticación básica
    async with BasicAuthClient(username="user", password="pass") as client:
        logger.info("Cliente Basic Auth inicializado")


if __name__ == "__main__":
    asyncio.run(example_advanced_features())
