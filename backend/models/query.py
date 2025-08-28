from pydantic import BaseModel, Field
from typing import List, Optional

class InputQuery(BaseModel):
    prompt:str = Field(description='User prompt')

class Cocktail(BaseModel):
    name: Optional[str] = Field(None,description="Name of the cocktail")
    ingredients: Optional[List[str]] = Field(None,description="List of names of ingredients that was mentioned by a user")
    instructions: Optional[List[str]] = Field(None,description="Details and steps how to cook the cocktail. Provide them strictly only if user requests instructions")
    glass:Optional[str] = Field(None, description="Cocktail glass")
    image:Optional[str] = Field(None, description="Cocktail image URL")

class JsonResponse(BaseModel):
    response: str = Field(description="Provide a response based on user info and conformity with cocktails from the menu.")

class CocktailList(BaseModel):
    answer: str = Field(description="Provide a quick text response based on the results. ")
    cocktails: Optional[List[Cocktail]] = Field(None, description="List of cocktails")