import os, yaml, json, re
from agents.base_agent import BaseAgent

REGISTRY_DIR = os.path.join(os.path.dirname(__file__), "../registry")

SYSTEM_PROMPT = (
    "You are a Schema Registry Agent for CXO Copilot. "
    "Your ONLY job: decide which agents can answer the question. "
    "Respond with ONLY a JSON array like: ['orders_agent'] "
    "Available: orders_agent, pipeline_agent, marketing_agent. "
    "NEVER explain. ONLY the JSON array."
)


class RegistryAgent(BaseAgent):

    def __init__(self):
        super().__init__("registry_agent", SYSTEM_PROMPT)
        self.schemas = self._load_all_schemas()

    def _load_all_schemas(self) -> str:
        combined = []
        for fname in sorted(os.listdir(REGISTRY_DIR)):
            if fname.endswith(".yaml"):
                path = os.path.join(REGISTRY_DIR, fname)
                with open(path) as f:
                    data = yaml.safe_load(f)
                    combined.append(f"Agent: {data['name']}\nDescription: {data['description']}")
        return "\n\n".join(combined)

    def get_relevant_agents(self, question: str) -> list:
        prompt = f"Available sources:\n{self.schemas}\n\nQuestion: {question}\n\nReturn ONLY the JSON array."
        response = self.ask(prompt)
        try:
            match = re.search(r'\[.*?\]', response, re.DOTALL)
            if match:
                return json.loads(match.group())
        except Exception:
            pass
        return ["orders_agent", "pipeline_agent", "marketing_agent"]  # fallback