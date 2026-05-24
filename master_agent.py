import os
from groq import Groq
from dotenv import load_dotenv
from agents.registry_agent  import RegistryAgent
from agents.orders_agent    import OrdersAgent
from agents.pipeline_agent  import PipelineAgent
from agents.marketing_agent import MarketingAgent

load_dotenv()

SYNTHESIS_PROMPT = (
    "You are the Master Agent for CXO Copilot. "
    "Combine specialist agent answers into ONE clear executive response. "
    "Lead with the direct answer and the most important number. "
    "Max 200 words. Never mention sub-agents or internal architecture. "
    "Write like a Chief of Staff briefing the CEO."
)


class MasterAgent:

    def __init__(self):
        self.registry = RegistryAgent()
        self.agents   = {
            "orders_agent":    OrdersAgent(),
            "pipeline_agent":  PipelineAgent(),
            "marketing_agent": MarketingAgent(),
        }
        self.model   = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        self.client  = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.history = []

    def ask(self, question: str) -> dict:
        # Step 1: which agents do we need?
        agents_needed = self.registry.get_relevant_agents(question)

        # Step 2: call each one
        raw_responses = {}
        for name in agents_needed:
            if name in self.agents:
                raw_responses[name] = self.agents[name].answer(question)

        if not raw_responses:
            return {"answer": "I couldn't find relevant data.", "agents_used": [], "raw_responses": {}}

        # Step 3: combine answers
        combined = "\n\n".join([f"[{n}]:\n{r}" for n, r in raw_responses.items()])

        # Step 4: inject history for follow-up questions
        history_text = ""
        if self.history:
            recent = self.history[-3:]
            history_text = "Recent conversation:\n" + "\n".join(
                [f"Q: {h['q']}\nA: {h['a']}" for h in recent])

        synthesis = (
            f"{history_text}\n\nData responses:\n{combined}"
            f"\n\nCurrent question: {question}\n\nSynthesise into one executive answer."
        )

        # Step 5: final synthesis call
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system",  "content": SYNTHESIS_PROMPT},
                {"role": "user",    "content": synthesis},
            ],
            temperature=0.2, max_tokens=1024,
        )
        answer = response.choices[0].message.content.strip()
        self.history.append({"q": question, "a": answer})

        return {"answer": answer, "agents_used": agents_needed, "raw_responses": raw_responses}