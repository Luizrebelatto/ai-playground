import httpx2

client = httpx2.AsyncClient(
    base_url="https://rickandmortyapi.com/api",
    timeout=30.0,
)
