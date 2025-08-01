from pinecone import Pinecone, ServerlessSpec
import os
from openai import OpenAI
import dotenv

dotenv.load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

index_name= "cocktail-index"
if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric='dotproduct',
        spec=ServerlessSpec(
            cloud='aws',
            region='us-east-1'
        ),
    )

dense_index = pc.Index(index_name)


