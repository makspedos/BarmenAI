from backend.db.connection import dense_index
from backend.models.query import CocktailList

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_pinecone import PineconeVectorStore
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

import os
import dotenv

dotenv.load_dotenv()

class LangchainService:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.vector_store = PineconeVectorStore(index=dense_index, embedding=self.embeddings)
        self.llm = ChatOpenAI(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"), temperature=0)
        self.parser = PydanticOutputParser(pydantic_object=CocktailList)

    def get_prompt_instructions(self):
        prompt = (
            "You are a bartender assistant. Use the context results to map the Cocktail schema "
            "(extracting name, ingredients, instructions, glass, image from fields in metadata and page_content) "
            "and respond strictly in that format and dont forget about image URLs in field image. "
            "If the user requests only specific fields (like just names), "
            "return only those fields in the schema, leaving other fields null."
            "If user asked irrelevant question, provide a list of cocktails from the menu or ask him to make more understandable request"
            "{format_instructions}\n\n"
            "Context:\n{context}\n\n"
            "Question:\n{input}"
        )
        template = PromptTemplate(
            template=prompt,
            input_variables=["context", "input"],
            partial_variables={"format_instructions":self.parser.get_format_instructions()},
        )

        return template

    async def make_prompt(self, query):
        prompt_template = self.get_prompt_instructions()
        question_answer_chain = create_stuff_documents_chain(llm=self.llm, prompt=prompt_template)
        retriever = self.vector_store.as_retriever(search_type="similarity")
        retriever_chain = create_retrieval_chain(retriever, question_answer_chain)

        result_cocktails =  await retriever_chain.ainvoke({"input": query})
        print(result_cocktails)

        try:
            cocktails_parsed = self.parser.parse(result_cocktails['answer']).model_dump()
            print(cocktails_parsed)
            cocktails_names = {cocktail.metadata.get('name'): cocktail.metadata.get('image') for cocktail in result_cocktails['context']}
            print(cocktails_names)
            for cocktail in cocktails_parsed['cocktails']:
                name = cocktail['name']
                if name in cocktails_names:
                    cocktail['image'] = cocktails_names[name]

        except Exception as e:
            print("Parsing error:", e)
            cocktails_parsed = None
        return cocktails_parsed



if __name__ == '__main__':
    langchain_service = LangchainService()
    print(langchain_service.make_prompt('What cocktails do you have with milk? '))



