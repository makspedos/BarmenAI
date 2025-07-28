from openai import AsyncOpenAI
import os
import dotenv
import json
from backend.models.query import Cocktail
from backend.models.query import JsonResponse

dotenv.load_dotenv()

def search_drink(query:str):
    with open("all_cocktails.json", "r") as f:
        return json.load(f)

tools = [
    {
        "type":"function",
        "function":{
            "name":"search_drink",
            "description":"Return a single drink and it's information based by provided user query",
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
system_prompt = ("You are helpful barmen assistant that provide relative information about a drink. "
                 "If user asks about non-existed drink or unrelated details - do share with him available menu.")

async def call_function(name, args):
    if name == "search_drink":
        return search_drink(**args)


class LLMModel():
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.system_prompt = system_prompt

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
            #response_format=Cocktail,
        )
        print(completion.model_dump())

        for tool_call in completion.choices[0].message.tool_calls:
            name =tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            messages.append(completion.choices[0].message)

            result = await call_function(name, args)
            messages.append({"role":"tool", "tool_call_id":tool_call.id, "content":json.dumps(result)})

        completion_2 = await self.client.chat.completions.parse(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools,
            response_format=JsonResponse,
        )

        final_response = completion_2.choices[0].message.parsed
        return final_response



