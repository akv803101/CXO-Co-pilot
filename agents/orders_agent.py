import os, sqlite3, json
from agents.base_agent import BaseAgent

DB_PATH = os.path.join(os.path.dirname(__file__), "../data/glowkart.db")

SYSTEM_PROMPT = (
    "You are the Orders Agent for GlowKart, a D2C beauty brand. "
    "You have two tables: orders and forecast. "
    "Give clear answers with specific numbers and percentages. Max 150 words."
)


class OrdersAgent(BaseAgent):

    def __init__(self):
        super().__init__("orders_agent", SYSTEM_PROMPT)

    def _fetch_data(self) -> dict:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cur  = conn.cursor()
        cur.execute("SELECT * FROM orders")
        orders = [dict(row) for row in cur.fetchall()]
        cur.execute("SELECT * FROM forecast")
        forecast = [dict(row) for row in cur.fetchall()]
        conn.close()
        return {"orders": orders, "forecast": forecast}

    def answer(self, question: str) -> str:
        data = self._fetch_data()
        prompt = f"Data: {json.dumps(data, indent=2)}\n\nQuestion: {question}\n\nAnswer with numbers. Show variances as %."
        return self.ask(prompt)