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
    """
    Service for interacting with OpenAI LLM using chat-based prompting.

    Features:
    - Handles both tool-augmented queries and direct schema-based responses.
    - Uses CocktailEmbedder for semantic search.
    - Supports async workflow with AsyncOpenAI client.

    Attributes:
        client (AsyncOpenAI): OpenAI client for async requests.
        system_prompts (dict): Predefined system messages for different cases.
        tools (list): List of tool specifications for LLM.
        embedder (CocktailEmbedder): Helper for semantic search embeddings.
    """
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.system_prompts = system_prompts
        self.tools = tools
        self.embedder = CocktailEmbedder()

    async def make_completion(self, messages: List[dict], action: str):
        if action == "create":
            completion = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools=self.tools,
            )
        else:
            completion = await self.client.chat.completions.parse(
                model="gpt-4o-mini",
                messages=messages,
                response_format=CocktailList,
            )
        return completion

    async def llm_response(self, prompt: str):

        """
           Main entrypoint for user queries.

           - Sends initial prompt to the model.
           - If tools are invoked, executes them and appends results back to messages. (tools description in file tools.py)
           - If no tools are used, applies scripted fallback prompt.
           - Returns structured CocktailList response.

           Args:
               prompt (str): User query.

           Returns:
               dict: Parsed CocktailList model as Python dict.
           """

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
                messages.append(completion.choices[0].message)

                for tool_call in completion.choices[0].message.tool_calls:
                    name = tool_call.function.name
                    args = json.loads(tool_call.function.arguments)

                    result = await call_function(name, self.embedder, args)
                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": json.dumps(result.to_dict())
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


"""
    For testing locally don`t forget to change OpenAI async client to sync.
    
    if __name__ == '__main__':
        llm_service = LLMService()
        llm_service.llm_response('Do you have orange juice ?')
"""
