from fastapi import APIRouter
from backend.models.query import InputQuery
from backend.services.llm_service import LLMService
from backend.services.langchain_prompt import LangchainService
router = APIRouter(
    prefix="/query",
    tags=["query"],
)
"""
    Prompting using Langchain: 
    model = LangchainService()
    response = await model.make_prompt(data.prompt)
    
    Prompting using OpenAI tools: 
    model = LLMService()
    response = await model.llm_response(data.prompt)
"""
model = LangchainService()
#model = LLMService()

@router.get("/prompt/{prompt}")
async def get_prompt(prompt:str):
    print(prompt)
    return {"message": f"I got a prompt - {prompt}"}

@router.post("/prompt/")
async def post_prompt(data:InputQuery):
    response = await model.make_prompt(data.prompt)
    #response = await model.llm_response(data.prompt)
    print(response)
    model_response = response['answer']
    if model_response is None:
        model_response = "Please, make relevant or more understandable request."
    cocktail_response = ""
    for cocktail in response['cocktails']:
        if cocktail['name']:
            cocktail_response += f"**Name**: {cocktail['name']}\n\n"
        if cocktail['ingredients']:
            cocktail_response += "**Ingredients**:\n"
            for ingredient in cocktail['ingredients']:
                cocktail_response += f"- {ingredient}\n"
        if cocktail['instructions']:
            cocktail_response += "\n**Instructions**:\n"
            for i, instruction in enumerate(cocktail['instructions'],1):
                cocktail_response += f"{i}. {instruction}\n"
        if cocktail['glass']:
            cocktail_response += f"\n**Glass**: {cocktail['glass']}\n"
        if cocktail['image']:
            cocktail_response += f"\n![image]({cocktail['image']})\n\n"

    return model_response, cocktail_response