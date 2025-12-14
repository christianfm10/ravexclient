"""
Ejemplo básico de uso de RavexClient.

Este ejemplo muestra cómo crear un cliente simple para la API de GitHub.
"""

import asyncio
from ravexclient import BaseClient, HTTPError


class GitHubClient(BaseClient):
    """Cliente simple para la API pública de GitHub."""

    BASE_URL = "https://api.github.com"

    def __init__(self, token: str | None = None, **kwargs):
        """
        Inicializar cliente de GitHub.

        Args:
            token: Token de autenticación de GitHub (opcional).
            **kwargs: Argumentos adicionales para BaseClient.
        """
        super().__init__(**kwargs)
        if token:
            self.client.headers["Authorization"] = f"token {token}"

    async def get_user(self, username: str) -> dict:
        """Obtener información de un usuario."""
        return await self._get(f"/users/{username}")

    async def get_repos(self, username: str) -> dict:
        """Obtener repositorios de un usuario."""
        return await self._get(f"/users/{username}/repos")

    async def search_repos(self, query: str, per_page: int = 10) -> dict:
        """Buscar repositorios."""
        params = {"q": query, "per_page": per_page}
        return await self._get("/search/repositories", params=params)


async def main():
    """Función principal de ejemplo."""
    # Crear cliente usando context manager (recomendado)
    async with GitHubClient() as client:
        try:
            # Obtener información de usuario
            print("Obteniendo información de usuario...")
            user = await client.get_user("octocat")
            print(f"\n👤 Usuario: {user['login']}")
            print(f"📛 Nombre: {user['name']}")
            print(f"📍 Ubicación: {user.get('location', 'No especificada')}")
            print(f"👥 Seguidores: {user['followers']}")

            # Obtener repositorios
            print("\n📦 Obteniendo repositorios...")
            repos = await client.get_repos("octocat")
            print(f"\nTotal de repositorios: {len(repos)}")
            print("\nPrimeros 5 repositorios:")
            for i, repo in enumerate(repos[:5], 1):
                print(f"  {i}. {repo['name']}")
                if repo.get("description"):
                    print(f"     {repo['description']}")
                print(f"     ⭐ {repo['stargazers_count']} stars")

            # Buscar repositorios
            print("\n🔍 Buscando repositorios de Python...")
            search_results = await client.search_repos("language:python", per_page=5)
            print(f"\nTotal encontrados: {search_results['total_count']}")
            print("\nTop 5 repositorios de Python:")
            for i, repo in enumerate(search_results["items"], 1):
                print(f"  {i}. {repo['full_name']}")
                print(f"     ⭐ {repo['stargazers_count']} stars")

        except HTTPError as e:
            print(f"\n❌ Error HTTP: {e.message}")
            if e.status_code:
                print(f"   Status code: {e.status_code}")
        except Exception as e:
            print(f"\n❌ Error inesperado: {e}")


if __name__ == "__main__":
    asyncio.run(main())
