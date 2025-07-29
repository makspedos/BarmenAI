import json

def search_drink(query:str):
    with open("test_cocktails.json", "r") as f:
        return json.load(f)

tools = [
    {
        "type":"function",
        "function":{
            "name":"search_drink",
            "description":"Return a single drink and it's information based by provided user query. "
                          "The drink ingredients must accord to the query.",
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


async def call_function(name, args):
    if name == "search_drink":
        return search_drink(**args)