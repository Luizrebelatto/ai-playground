import express from "express";
import { askFruitExpert, parseTemperature, SYSTEM_PROMPT, MODEL } from "./openai.js";

const app = express();
app.use(express.json());

// Mostra a configuração atual (persona + modelo)
app.get("/", (_req, res) => {
  res.json({ model: MODEL, systemPrompt: SYSTEM_PROMPT });
});

// Uma pergunta, uma temperatura
// POST /ask { "question": "...", "temperature": 0.7 }
app.post("/ask", async (req, res) => {
  try {
    const { question, temperature = 1, maxTokens } = req.body ?? {};
    if (!question) return res.status(400).json({ error: "Envie 'question' no body." });
    res.json(await askFruitExpert(question, { temperature: parseTemperature(temperature), maxTokens }));
  } catch (err) {
    res.status(err.status ?? 400).json({ error: err.message });
  }
});

// Mesma pergunta em várias temperaturas, lado a lado
// POST /compare { "question": "...", "temperatures": [0, 0.7, 1.5] }
app.post("/compare", async (req, res) => {
  try {
    const { question, temperatures = [0, 0.7, 1.5], maxTokens } = req.body ?? {};
    if (!question) return res.status(400).json({ error: "Envie 'question' no body." });
    const temps = temperatures.map(parseTemperature);
    const results = await Promise.all(temps.map((t) => askFruitExpert(question, { temperature: t, maxTokens })));
    res.json({ question, results });
  } catch (err) {
    res.status(err.status ?? 400).json({ error: err.message });
  }
});

const port = process.env.PORT || 3000;
app.listen(port, () => console.log(`🍍 Sabe-tudo de frutas rodando em http://localhost:${port} (modelo: ${MODEL})`));
