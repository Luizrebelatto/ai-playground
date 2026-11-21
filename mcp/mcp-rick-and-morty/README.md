# Rick and Morty MCP

An MCP server that exposes the [Rick and Morty API](https://rickandmortyapi.com/documentation) as tools, so an AI assistant can look up characters, locations and episodes.
 
## Tools
<img width="1046" height="452" alt="Screenshot 2026-11-21 at 16 26 46" src="https://github.com/user-attachments/assets/d9107b8a-1ce7-419e-8ba2-c60f383b122e" />

## What happens when you ask "How many alive Ricks are there?
```mermaid
sequenceDiagram
    autonumber
    actor User
    participant App as App (MCP host)<br/>Claude Code / Desktop / Codex
    participant LLM as LLM<br/>Claude / GPT
    participant Server as MCP server<br/>my_server.py
    participant Tool as get_characters_by_filters<br/>tools/characters.py
    participant API as Rick and Morty API

    Note over App,Server: When the session starts
    App->>Server: start my_server.py (stdio)
    App->>Server: tools/list
    Server-->>App: 12 tools with names, descriptions and parameters

    Note over User,API: When you ask the question
    User->>App: "How many alive Ricks are there?"
    App->>LLM: question + list of the 12 tools
    LLM->>LLM: picks the tool whose description fits:<br/>get_characters_by_filters
    LLM-->>App: tool call: name="rick", status="alive"
    App->>Server: tools/call get_characters_by_filters
    Server->>Tool: run the tool
    Tool->>API: GET /character?name=rick&status=alive&page=1
    API-->>Tool: JSON: info.count = 29, results = first 20 Ricks
    Tool-->>Server: JSON
    Server-->>App: tool result
    App->>LLM: tool result
    LLM->>LLM: reads info.count = 29
    LLM-->>App: "There are 29 alive Ricks..."
    App-->>User: final answer
```

## Questions to test
```txt
"How many alive Ricks are there?"
"Who appears in episode S01E01?"
"Which planets are in dimension C-137?"
"List the episodes of season 2"
```

## Demo

#### Claude code terminal

https://github.com/user-attachments/assets/8439f8cf-d86e-4682-9ff9-0dcee23f55a7

#### Claude code desktop

https://github.com/user-attachments/assets/aa3a0a6e-4891-4cef-b425-cecc271c0f35

