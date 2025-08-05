from openai import AsyncOpenAI
import os
from backend.models.query import JsonResponse
from .tools import tools, call_function
import json
import dotenv
from backend.db.embedding import CocktailEmbedder

dotenv.load_dotenv()

class LLMService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.system_prompt = ("You are helpful barmen assistant that provide relative information about a drink."
                              "You have to provide only matching cocktails based on query."
                 "If user asks about non-existed drink or unrelated details - do share with him available menu and ask again.")

    async def llm_response(self,prompt:str):
        messages = [
                {
                    "role":"system",
                    "content":self.system_prompt,
                },
                {
                    "role":"user",
                    "content":prompt,
                }
            ]
        completion = await self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages= messages,
            tools = tools,
        )
        embedder = CocktailEmbedder()
        for tool_call in completion.choices[0].message.tool_calls:
            name =tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            messages.append(completion.choices[0].message)

            result = call_function(name, embedder, args)
            print(result)
            messages.append({"role":"tool", "tool_call_id":tool_call.id, "content":json.dumps(result.to_dict())})

        completion_2 = await self.client.chat.completions.parse(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools,
            response_format=JsonResponse,
        )

        final_response = completion_2.choices[0].message.parsed
        print(final_response)
        return final_response



