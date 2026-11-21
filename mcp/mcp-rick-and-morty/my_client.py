import asyncio

from anthropic import AsyncAnthropic
from anthropic.lib.tools.mcp import async_mcp_tool
from fastmcp import Client

MCP_SERVER_URL = "http://localhost:8000/mcp"
MODEL = "claude-opus-5-5"

SYSTEM_PROMPT = (
    "You answer questions about the Rick and Morty universe using the available tools. "
    "Always use the tools to look up characters, episodes and locations instead of "
    "answering from memory. Reply in the same language the user writes in."
)

mcp_client = Client(MCP_SERVER_URL)
claude = AsyncAnthropic()  # reads ANTHROPIC_API_KEY from the environment


async def ask(question: str, tools: list, history: list) -> str:
    history.append({"role": "user", "content": question})

    # The tool runner loops for us: Claude picks a tool, the SDK calls the MCP server,
    # sends the result back to Claude, and repeats until Claude writes the final answer.
    runner = claude.beta.messages.tool_runner(
        model=MODEL,
        max_tokens=16000,
        system=SYSTEM_PROMPT,
        tools=tools,
        messages=history,
        output_config={"effort": "medium"},
        # If the model declines a request, the API retries it on a fallback model
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
    )
    final_message = await runner.until_done()

    if final_message.stop_reason == "refusal":
        answer = "Sorry, I can't help with that request."
    else:
        answer = "".join(block.text for block in final_message.content if block.type == "text")

    history.append({"role": "assistant", "content": answer})
    return answer


async def main():
    async with mcp_client:
        mcp_tools = await mcp_client.list_tools()
        tools = [async_mcp_tool(tool, mcp_client.session) for tool in mcp_tools]
        print(f"Connected to {MCP_SERVER_URL} ({len(tools)} tools). Type 'exit' to quit.\n")

        history: list = []
        while True:
            question = (await asyncio.to_thread(input, "You: ")).strip()
            if question.lower() in {"exit", "quit", "sair"}:
                break
            if not question:
                continue

            answer = await ask(question, tools, history)
            print(f"\nClaude: {answer}\n")


if __name__ == "__main__":
    asyncio.run(main())
