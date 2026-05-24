import os
import pandas as pd
from agents.base_agent import BaseAgent

CSV_PATH = os.path.join(os.path.dirname(__file__), "../data/campaigns.csv")

SYSTEM_PROMPT = (
    "You are the Marketing Agent for GlowKart. "
    "You have campaign data: campaign, channel, spend, impressions, clicks, revenue_attributed, quarter. "
    "ROAS = revenue_attributed / spend. Higher ROAS = better efficiency. Max 150 words."
)


class MarketingAgent(BaseAgent):

    def __init__(self):
        super().__init__("marketing_agent", SYSTEM_PROMPT)

    def _fetch_data(self) -> str:
        df = pd.read_csv(CSV_PATH)
        df["roas"] = (df["revenue_attributed"] / df["spend"]).round(2)
        return df.to_string(index=False)

    def answer(self, question: str) -> str:
        data = self._fetch_data()
        prompt = f"Data (roas=revenue/spend):\n{data}\n\nQuestion: {question}\n\nAnswer with ROAS values and campaign names."
        return self.ask(prompt)