from openai import OpenAI
import os
from rich.markdown import Markdown
from rich.live import Live


class TAClient:
    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_KEY")
        self.base_url = "https://api.deepseek.com"
        self.model = "deepseek-chat"
        if not self.api_key:
            raise ValueError("API_KEY is not set")
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def chat(self, question: str, live: Live = None) -> str:
        response_text = ""
        try:
            for chunk in self.client.chat.completions.create(
                messages=[{"role": "user", "content": question}],
                model=self.model,
                stream=True,
                temperature=0.7,
                top_p=0.95,
            ):
                if chunk.choices[0].delta.content is not None:
                    response_text += chunk.choices[0].delta.content
                    if live:
                        live.update(Markdown(response_text))
            return response_text
        except Exception as e:
            raise Exception(f"Error during chat: {e}")
