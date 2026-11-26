# Fruit Know-It-All — temperature lab

A Node.js service that talks to the OpenAI API with a fixed persona
(**"Você é um sabe-tudo de frutas"**, i.e. *"You are a fruit know-it-all"*) and lets you change the `temperature` to compare responses.

## Getting started

```bash
cp .env.example .env     # add your OPENAI_API_KEY
npm install
npm start                # http://localhost:3000
```

Environment variables:

| Variable | Default | Description |
|---|---|---|
| `OPENAI_API_KEY` | — (required) | Your OpenAI API key |
| `OPENAI_MODEL` | `gpt-4o-mini` | Chat model (must accept `temperature`) |
| `PORT` | `3000` | HTTP server port |

## Architecture

```mermaid
flowchart TD
    C["Client<br/>(curl / Postman / frontend)"] -->|HTTP JSON| S
    T["Terminal"] -->|argv| CLI

    subgraph Entry["Entry layer"]
        S["src/server.js (Express)<br/>GET / · POST /ask · POST /compare"]
        CLI["src/compare.js (CLI)<br/>sequential loop"]
    end

    subgraph Service["Service layer — src/openai.js"]
        P["SYSTEM_PROMPT<br/>fruit persona"]
        V["parseTemperature()<br/>validates 0..2"]
        A["askFruitExpert()<br/>builds messages and calls the SDK"]
    end

    S --> V
    CLI --> V
    V --> A
    P -.-> A
    A -->|"openai SDK (HTTPS + API key)"| O[("OpenAI<br/>POST /v1/chat/completions")]
```

| Layer | File | Responsibility |
|---|---|---|
| Entry | `src/server.js`, `src/compare.js` | Read input, validate it, format the output |
| Service | `src/openai.js` | Persona, model, temperature and the SDK call |
| External | OpenAI | Generate the text |

All the logic lives in `openai.js`, so the HTTP server and the CLI share the same function. To switch providers, you only change that file.

## Request flow (`POST /ask`)

```mermaid
sequenceDiagram
    autonumber
    actor U as Client
    participant S as server.js
    participant SV as openai.js
    participant O as OpenAI API

    U->>S: POST /ask { question, temperature }
    S->>SV: parseTemperature(temperature)
    alt outside 0..2
        SV-->>S: Error
        S-->>U: 400 { error }
    else valid
        S->>SV: askFruitExpert(question, { temperature })
        SV->>O: chat.completions.create<br/>[system: persona, user: question]
        alt OpenAI error (401, 429...)
            O-->>SV: error + status
            SV-->>S: throw err
            S-->>U: err.status { error }
        else success
            O-->>SV: choices[0].message, usage
            SV-->>S: { answer, usage, ms, ... }
            S-->>U: 200 JSON
        end
    end
```

## `/compare` (parallel) vs CLI (sequential)

```mermaid
flowchart LR
    subgraph HTTP["POST /compare — Promise.all"]
        Q1[question] --> T0[t = 0] & T1[t = 0.7] & T2[t = 1.5]
        T0 & T1 & T2 --> R1[results in parallel]
    end

    subgraph CLI["npm run compare — for...of"]
        Q2[question] --> C0[t = 0] --> C1[t = 0.7] --> C2[t = 1.5] --> R2[ordered output]
    end
```

- **`/compare`**: sends every temperature at once. It's faster, but uses your quota all at once.
- **CLI**: one temperature at a time, so the terminal output comes out in order.

## Endpoints

### `GET /`
Shows the model and system prompt in use.

### `POST /ask`
```bash
curl -X POST localhost:3000/ask -H 'content-type: application/json' \
  -d '{"question":"What is the sweetest fruit?","temperature":0.2}'
```
```json
{
  "temperature": 0.2,
  "model": "gpt-4o-mini-...",
  "answer": "...",
  "finishReason": "stop",
  "usage": { "prompt_tokens": 80, "completion_tokens": 120, "total_tokens": 200 },
  "ms": 1350
}
```

### `POST /compare`
```bash
curl -X POST localhost:3000/compare -H 'content-type: application/json' \
  -d '{"question":"Invent a fruit juice","temperatures":[0,0.8,1.6]}'
```
Returns `{ question, results: [ ...one /ask-style object per temperature ] }`.

### CLI
```bash
npm run compare -- "Tell me about cashew fruit" 0 1 1.8
```

## What to look for when changing temperature

```mermaid
flowchart LR
    A["0<br/>deterministic<br/>nearly identical answers"] --> B["0.7 – 1<br/>natural<br/>healthy variation"] --> C["1.5 – 2<br/>creative → chaotic<br/>may lose coherence"]
```

- Ask the same question several times at `0`, then at `1.5`, and compare.
- Reasoning models (o-series, GPT-5) **do not accept** `temperature`. Use a regular chat model.
- The service is **stateless**: each call sends only `system` + `user`. For conversation memory, you'd need to store and resend the `messages[]` history.
- The system prompt tells the model to answer in Portuguese. Edit `SYSTEM_PROMPT` in `src/openai.js` to change that.
