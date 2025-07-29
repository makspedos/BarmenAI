from pinecone import Pinecone, ServerlessSpec
import os


pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

index_name= "cocktail-index"
if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric='dotproduct',
        spec3=ServerlessSpec(
            cloud='aws',
            region='us-east-1'
        ),
    )

dense_index = pc.Index(index_name)
