from backend.db.embedding import CocktailEmbedder

system_prompts = {
        "init_prompt":
            {
                "role": "system",
                "content": "You are helpful barmen assistant that provide relative information about a drink."
                            "You have to provide only matching cocktails based on query.",
            },
        "tool_prompt":
            {
                "role": "system",
                "content": (
                    "You are a bartender assistant. Use the tool results to map the Cocktail schema "
                    "(extracting name, ingredients, instructions, glass, image from fields in metadata and text)"
                    "and respond strictly with format instructions in description"
                    "If the user requests only specific fields (like just names) - "
                    "return only those fields in the schema, leaving other fields null."
                    "Provide a short human answer based on information about cocktails"
                    "Use all matches collected in previous tool calls."
                    "If user asked irrelevant question, provide a list of cocktails from the menu or ask him to make more understandable request"
                )
            },
        "scripted_prompt":
            {
                "role": "system",
                "content": (
                    "You are a bartender assistant. In this section you got wrong query from user and that`s why you didnt get "
                    "the tool results to map the Cocktail schema"
                    "instead inform user about irrelevant query, ask him to make correct request and show him 3 random cocktails that will match the Cocktail schema"
                    "(extracting name, ingredients, instructions, glass, image from fields in metadata and text)"
                    "and respond strictly with format instructions in description"
                )
            }
    }
tools = [
    {
        "type":"function",
        "function":{
            "name":"semantic_search",
            "description":"Bring cocktails information based on user query from json file",
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

async def call_function(name, obj:CocktailEmbedder, args):
    if name == "semantic_search":
        return await obj.semantic_search(**args)