import OpenAI from "openai";

// O "input" de sistema: define a persona do modelo.
export const SYSTEM_PROMPT =
  "Você é um sabe-tudo de frutas. Responda sempre em português, com entusiasmo e precisão, " +
  "sobre origem, sabor, nutrientes, época de colheita, curiosidades e receitas com frutas. " +
  "Se a pergunta não for sobre frutas, traga a conversa de volta para as frutas com bom humor.";

export const MODEL = process.env.OPENAI_MODEL || "gpt-4o-mini";

if (!process.env.OPENAI_API_KEY) {
  console.error("Falta OPENAI_API_KEY. Copie .env.example para .env e coloque sua chave.");
  process.exit(1);
}

const client = new OpenAI(); // lê OPENAI_API_KEY do ambiente

/**
 * Faz uma pergunta ao "sabe-tudo de frutas" com a temperatura escolhida.
 * temperature: 0 (determinístico) até 2 (bem criativo/caótico).
 */
export async function askFruitExpert(question, { temperature = 1, maxTokens = 300 } = {}) {
  const start = Date.now();
  const completion = await client.chat.completions.create({
    model: MODEL,
    temperature,
    max_tokens: maxTokens,
    messages: [
      { role: "system", content: SYSTEM_PROMPT },
      { role: "user", content: question },
    ],
  });

  return {
    temperature,
    model: completion.model,
    answer: completion.choices[0].message.content,
    finishReason: completion.choices[0].finish_reason,
    usage: completion.usage,
    ms: Date.now() - start,
  };
}

export function parseTemperature(value) {
  const t = Number(value);
  if (!Number.isFinite(t) || t < 0 || t > 2) {
    throw new Error(`temperature inválida: ${value} (use um número entre 0 e 2)`);
  }
  return t;
}
