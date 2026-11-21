from typing import Literal
from fastmcp import FastMCP
from api import client

characters_mcp = FastMCP(name="Characters")

@characters_mcp.tool(
    name="get_all_characters",
    description="List the first page of Rick and Morty characters, with pagination info.",
)
async def get_all_characters() -> dict:
    response = await client.get("/character")
    response.raise_for_status()
    return response.json()

@characters_mcp.tool(
    name="get_a_single_character",
    description="Get a single Rick and Morty character by its numeric ID.",
)
async def get_a_single_character(character_id: int) -> dict:
    response = await client.get(f"/character/{character_id}")
    response.raise_for_status()
    return response.json()


@characters_mcp.tool(
    name="get_multiple_characters",
    description="Get multiple Rick and Morty characters by a list of numeric IDs.",
)
async def get_multiple_characters(character_ids: list[int]) -> list[dict]:
    response = await client.get(f"/character/{character_ids}")
    response.raise_for_status()
    return response.json()

@characters_mcp.tool(
    name="get_characters_by_filters",
    description=(
        "Search Rick and Morty characters using optional filters. "
        "All filters can be combined, e.g. name='rick' and status='alive'. "
        "Results are paginated (20 per page)."
    ),
)
async def get_characters_by_filters(
    name: str | None = None,
    status: Literal["alive", "dead", "unknown"] | None = None,
    species: str | None = None,
    character_type: str | None = None,
    gender: Literal["female", "male", "genderless", "unknown"] | None = None,
    page: int = 1,
) -> dict:
    filters = {
        "name": name,
        "status": status,
        "species": species,
        "type": character_type,
        "gender": gender,
        "page": page,
    }
    params = {key: value for key, value in filters.items() if value is not None}

    response = await client.get("/character", params=params)
    if response.status_code == 404:
        return {"info": {"count": 0, "pages": 0}, "results": []}
    response.raise_for_status()
    return response.json()
