import os, json
from agents.base_agent import BaseAgent

JSON_PATH = os.path.join(os.path.dirname(__file__), "../data/pipeline.json")

SYSTEM_PROMPT = (
    "You are the Pipeline Agent for GlowKart. "
    "You have CRM pipeline data with deals (name, rep, stage, value, close_date, risk) "
    "and summary stats. Stages: Discovery > Proposal > Negotiation > Closed Won. "
    "Risk: High = likely to slip. Max 150 words."
)


class PipelineAgent(BaseAgent):

    def __init__(self):
        super().__init__("pipeline_agent", SYSTEM_PROMPT)

    def _fetch_data(self) -> dict:
        with open(JSON_PATH) as f:
            return json.load(f)

    def answer(self, question: str) -> str:
        data = self._fetch_data()
        prompt = f"Data: {json.dumps(data, indent=2)}\n\nQuestion: {question}\n\nAnswer with deal names and rupee values."
        return self.ask(prompt)