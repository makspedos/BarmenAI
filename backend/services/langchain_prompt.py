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
    """
        LangchainService provides a structured workflow to query a Pinecone vector store
        with cocktail information, retrieve relevant results, and map them into a strict
        Cocktail schema using a language model.

        The service supports:
        - Embedding user queries and retrieving similar cocktail documents.
        - Using a ChatOpenAI LLM to format retrieved results into a structured schema.
        - Preserving additional metadata like image URLs even if they are not part of the text embeddings.
        - Asynchronous retrieval and processing for efficient integration in web applications.
    """

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
            "return only those fields in the schema, leaving other fields null. "
            "If user asked irrelevant question, get a 3 random cocktails from the menu and ask him to make more understandable request"
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

    @staticmethod
    def insert_image_back(retrieved_cocktails, cocktails_parsed):
        cocktails_metadata = {cocktail.metadata.get('name'): cocktail.metadata.get('image') for cocktail in retrieved_cocktails['context']}
        for cocktail in cocktails_parsed.get('cocktails', []):
            name = cocktail['name']
            if name in cocktails_metadata:
                cocktail['image'] = cocktails_metadata[name]
        return cocktails_parsed


    def parse_cocktails(self, retrieved_cocktails):
        try:
            cocktails_parsed = self.parser.parse(retrieved_cocktails['answer']).model_dump()
            cocktails_parsed_img = self.insert_image_back(retrieved_cocktails,cocktails_parsed)
        except Exception as e:
            print("Parsing error:", e)
            cocktails_parsed_img = None
        return cocktails_parsed_img

    async def make_prompt(self, query):
        prompt_template = self.get_prompt_instructions()
        question_answer_chain = create_stuff_documents_chain(llm=self.llm, prompt=prompt_template)
        retriever = self.vector_store.as_retriever(search_type="similarity")
        retriever_chain = create_retrieval_chain(retriever, question_answer_chain)
        retrieved_cocktails =  await retriever_chain.ainvoke({"input": query})

        cocktails_parsed = self.parse_cocktails(retrieved_cocktails)
        return cocktails_parsed



# if __name__ == '__main__':
#     langchain_service = LangchainService()
#     print(langchain_service.make_prompt('What cocktails do you have with milk? '))

