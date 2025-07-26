from pydantic import BaseModel, Field

class InputQuery(BaseModel):
    prompt:str = Field(description='User prompt')

class Cocktail(BaseModel):
    ingredients: list[str] = Field(description="List of names of ingredients that was mentioned by a user")
    description:str = Field(description="Details in a query")
    amount:int = Field(description="Amount of ordered drinks if it was set")



