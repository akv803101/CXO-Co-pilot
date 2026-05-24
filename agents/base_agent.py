import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()  # reads your .env file


class BaseAgent:
    """Parent class. All sub-agents inherit from this."""

    def __init__(self, name: str, system_prompt: str):
        self.name          = name
        self.system_prompt = system_prompt  # the agent job description
        self.model         = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        self.client        = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def ask(self, user_message: str) -> str:
        """Send a message to Groq and return the reply as a string."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system",  "content": self.system_prompt},
                {"role": "user",    "content": user_message},
            ],
            temperature=0.1,   # low = consistent factual answers
            max_tokens=1024,
        )
        return response.choices[0].message.content.strip()