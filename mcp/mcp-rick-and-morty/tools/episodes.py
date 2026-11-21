from fastmcp import FastMCP
from api import client

episodes_mcp = FastMCP(name="Episodes")

@episodes_mcp.tool(
    name="get_all_episodes",
    description="List the first page of Rick and Morty episodes, with pagination info.",
)
async def get_all_episodes() -> dict:
    response = await client.get("/episode")
    response.raise_for_status()
    return response.json()

@episodes_mcp.tool(
    name="get_a_single_episode",
    description="Get a single Rick and Morty episode by its numeric ID.",
)
async def get_a_single_episode(episode_id: int) -> dict:
    response = await client.get(f"/episode/{episode_id}")
    response.raise_for_status()
    return response.json()

@episodes_mcp.tool(
    name="get_multiple_episodes",
    description="Get multiple Rick and Morty episodes by a list of numeric IDs.",
)
async def get_multiple_episodes(episode_ids: list[int]) -> list[dict]:
    response = await client.get(f"/episode/{episode_ids}")
    response.raise_for_status()
    return response.json()

@episodes_mcp.tool(
    name="get_episodes_by_filters",
    description=(
        "Search Rick and Morty episodes using optional filters. "
        "Filter by name (e.g. 'Pilot') or by episode code "
        "(e.g. 'S01E01' for one episode, 'S01' for a whole season). "
        "Results are paginated (20 per page)."
    ),
)
async def get_episodes_by_filters(
    name: str | None = None,
    episode_code: str | None = None,
    page: int = 1,
) -> dict:
    filters = {
        "name": name,
        "episode": episode_code,
        "page": page,
    }
    params = {key: value for key, value in filters.items() if value is not None}

    response = await client.get("/episode", params=params)
    if response.status_code == 404:
        return {"info": {"count": 0, "pages": 0}, "results": []}
    response.raise_for_status()
    return response.json()
