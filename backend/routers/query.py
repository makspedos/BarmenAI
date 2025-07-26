from fastapi import APIRouter
from backend.models.query import Cocktail, InputQuery
from backend.agent.config import LLMModel

router = APIRouter(
    prefix="/query",
    tags=["query"],
)
model = LLMModel()


@router.get("/prompt/{prompt}")
async def get_prompt(prompt:str):
    print(prompt)
    return {"message": f"I got a prompt - {prompt}"}

@router.post("/prompt/")
async def post_prompt(data:InputQuery):
    print(data.prompt)
    response = await model.llm_response(data.prompt)
    return Cocktail(ingredients=response.ingredients, description=response.description, amount=response.amount)