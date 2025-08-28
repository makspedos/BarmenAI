from openai import AsyncOpenAI, OpenAI
import os
from typing import List
from backend.models.query import CocktailList
from backend.services.tools import tools, call_function, system_prompts
import json
import dotenv
from backend.db.embedding import CocktailEmbedder

dotenv.load_dotenv()

class LLMService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.system_prompts = system_prompts
        self.tools = tools
        self.embedder = CocktailEmbedder()

    async def make_completion(self, messages:List[dict], action:str):
        if action == "create":
            completion = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools=self.tools,
            )
        else:
            completion= await self.client.chat.completions.parse(
                model="gpt-4o-mini",
                messages=messages,
                response_format=CocktailList,
            )
        return completion

    async def llm_response(self,prompt:str):
        messages = [
            self.system_prompts['init_prompt'],
            {
                "role": "user",
                "content": prompt,
            }
        ]
        completion = await self.make_completion(messages=messages, action='create')
        try:
            if completion.choices[0].message.tool_calls:
                for tool_call in completion.choices[0].message.tool_calls:
                    name = tool_call.function.name
                    args = json.loads(tool_call.function.arguments)
                    messages.append(completion.choices[0].message)
                    result = await call_function(name, self.embedder, args)
                    messages.append(
                        {
                                "role":"tool",
                                "tool_call_id":tool_call.id,
                                "content":json.dumps(result.to_dict())
                        }
                    )
                    print(json.dumps(result.to_dict()))
                    messages.append(self.system_prompts['tool_prompt'])
            else:
                messages.append(self.system_prompts['scripted_prompt'])
        except Exception as e:
            print("Wrong value in tool call:", e)
            return None
        completion_2 = await self.make_completion(messages=messages, action="parse")
        final_response = completion_2.choices[0].message.parsed
        return final_response.model_dump()



if __name__ == '__main__':
    llm_service = LLMService()
    llm_service.llm_response('Do you have orange juice ?')
