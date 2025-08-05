from backend.db.embedding import CocktailEmbedder

tools = [
    {
        "type":"function",
        "function":{
            "name":"semantic_search",
            "description":"Brings cocktails information based on user query. ",
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

def call_function(name, obj:CocktailEmbedder, args):
    if name == "semantic_search":
        return obj.semantic_search(**args)