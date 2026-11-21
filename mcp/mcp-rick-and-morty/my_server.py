from fastmcp import FastMCP

from tools.characters import characters_mcp
from tools.episodes import episodes_mcp
from tools.locations import locations_mcp

mcp = FastMCP(
    name="RickAndMortyMCP",
    instructions="""
        Provides information about Rick and Morty characters,
        episodes, and locations using the Rick and Morty API.
    """,
)

# Mounted without a namespace, so tool names stay the same (e.g. get_all_characters)
mcp.mount(characters_mcp)
mcp.mount(episodes_mcp)
mcp.mount(locations_mcp)

if __name__ == "__main__":
    mcp.run()
