from fastmcp import FastMCP
from api import client

locations_mcp = FastMCP(name="Locations")

@locations_mcp.tool(
    name="get_all_locations",
    description="List the first page of Rick and Morty locations, with pagination info."
)
async def get_all_locations() -> dict:
    response = await client.get("/location")
    response.raise_for_status()
    return response.json()

@locations_mcp.tool(
    name="get_a_single_location",
    description="Get a single Rick and Morty location by its numeric ID.",
)
async def get_a_single_location(location_id: int) -> dict:
    response = await client.get(f"/location/{location_id}")
    response.raise_for_status()
    return response.json()

@locations_mcp.tool(
    name="get_multiple_locations",
    description="Get multiple Rick and Morty locations by a list of numeric IDs.",
)
async def get_multiple_locations(location_ids: list[int]) -> list[dict]:
    response = await client.get(f"/location/{location_ids}")
    response.raise_for_status()
    return response.json()

@locations_mcp.tool(
    name="get_locations_by_filters",
    description=(
        "Search Rick and Morty locations using optional filters. "
        "All filters can be combined, e.g. type='planet' and dimension='C-137'. "
        "Results are paginated (20 per page)."
    ),
)
async def get_locations_by_filters(
    name: str | None = None,
    location_type: str | None = None,
    dimension: str | None = None,
    page: int = 1,
) -> dict:
    filters = {
        "name": name,
        "type": location_type,
        "dimension": dimension,
        "page": page,
    }
    params = {key: value for key, value in filters.items() if value is not None}

    response = await client.get("/location", params=params)
    if response.status_code == 404:
        return {"info": {"count": 0, "pages": 0}, "results": []}
    response.raise_for_status()
    return response.json()
