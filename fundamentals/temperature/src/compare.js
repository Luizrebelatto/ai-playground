// CLI: npm run compare -- "Qual a fruta mais doce?" 0 0.7 1.5
import { askFruitExpert, parseTemperature } from "./openai.js";

const [question = "Me conte uma curiosidade sobre a manga.", ...rawTemps] = process.argv.slice(2);
const temps = (rawTemps.length ? rawTemps : ["0", "0.7", "1.5"]).map(parseTemperature);

console.log(`\n❓ ${question}\n`);

// Sequencial para a saída ficar na ordem das temperaturas
for (const t of temps) {
  const r = await askFruitExpert(question, { temperature: t });
  console.log(`━━━━━━━━ temperature = ${t}  (${r.ms} ms, ${r.usage.total_tokens} tokens) ━━━━━━━━`);
  console.log(r.answer, "\n");
}
