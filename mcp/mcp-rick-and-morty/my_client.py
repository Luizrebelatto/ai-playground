import asyncio
from fastmcp import Client

client = Client("http://localhost:8000/mcp")

async def get_all_characters():
    async with client:
        result = await client.call_tool("get_all_characters")
        data = result.data
        print(f"Total de personagens: {data['info']['count']}")
        for character in data["results"]:
            print(f"{character['id']:>3} - {character['name']} ({character['species']}, {character['status']})")

asyncio.run(get_all_characters())
