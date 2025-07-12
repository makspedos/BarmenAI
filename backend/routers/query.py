from fastapi import APIRouter
from backend.models.query import Query

router = APIRouter(
    prefix="/query",
    tags=["query"],
)


@router.get("/prompt/{prompt}")
async def get_prompt(prompt:str):
    return {"message": f"I got a prompt - {prompt}"}

@router.post("/prompt/")
async def post_prompt(data:Query):
    return {"message": f"Your prompt is - {data.prompt}"}