from openai import AsyncOpenAI
import os
import dotenv
import json
from backend.models.query import Cocktail
dotenv.load_dotenv()

def search_drink(details:str):
    with open("drinks.json", "r") as f:
        return json.load(f)

tools = [
    {
        "type":"function",
        "function":{
            "name":"search_drink",
            "description":"Return drink recipe based on provided query",
            "parameters":{
                "type":"object",
                "properties":{
                    "query":{"type":"string"},
                },
                "required":["query"],
                "additionalProperties":False,
            },
            "strict":True,
        }
    }
]


class LLMModel():
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.system_prompt = "Extract information about user query"

    async def llm_response(self,prompt:str):
        completion = await self.client.chat.completions.parse(         #self.client.chat.completions.create
            model="gpt-4o-mini",
            messages=[
                {
                    "role":"system",
                    "content":self.system_prompt,
                },
                {
                    "role":"user",
                    "content":prompt,
                }
            ],
            #tools = tools,
            response_format=Cocktail,
        )
        return completion.choices[0].message.parsed

#system_prompt = ("You are helpful barmen assistant that provide relative information about a drink. "
#                 "If user asks about non-existed drink or unrelated details - do share with him available menu.")