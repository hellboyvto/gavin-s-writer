import os
import asyncio
from openai import AsyncOpenAI

class ContentProcessor:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    async def process_content(self, content, task="summarize", model="gpt-3.5-turbo", max_tokens=100, temperature=0):
        actions = {
            "summarize": f"总结以下内容的所有要点: {content}",
            "expand": f"根据你自己的认知，扩充下面的内容，以markdown格式输出。输出的内容越系统化越好，越详细越好！: {content}",
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
