import os
import asyncio
from openai import AsyncOpenAI

class ContentProcessor:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    async def process_content(self, content, task="summarize", model="gpt-3.5-turbo", max_tokens=100, temperature=0):
        actions = {
            "summarize": f"Summarize this: {content}",
            "expand": f"Expand on this content in detail: {content}",
        }
        
        prompt = actions.get(task, content)  # Fallback to original content if task is not recognized

        chat_completion = await self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
        )

        if not chat_completion.choices or len(chat_completion.choices) == 0:
            return None
        
        # Assuming the response text will be stored in the first choice's "message" "content"
        result_text = chat_completion.choices[0].message.content.strip()
        return result_text
