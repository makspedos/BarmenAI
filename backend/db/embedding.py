import json
from backend.db.connection import client, dense_index
from paths import BASE_PATH

class CocktailEmbedder:
    def __init__(self):
        self.client =  client
        self.dense_index = dense_index

    @staticmethod
    def load_cocktails_json(file_name):
        """ Loads cocktails from json file """
        with open(file_name, 'r') as f:
            return json.load(f)

    @staticmethod
    def check_insertion(response, cocktail):
        """ Check whether operation was successful or not """
        if response and response.get('upserted_count') == 1:
            print(f"Успішно додано до Pinecone.")
        else:
            print(f"Помилка при додаванні {cocktail['strDrink']}. Відповідь: {response}")

    def create_embeddings(self, input_text):
        """ Retrieves embeddings based on text, uses openai model for embeddings """
        embedding = self.client.embeddings.create(
            input=input_text,
            model="text-embedding-3-small",
        )
        return embedding.data[0].embedding


    def insert_embeddings(self, embedding, cocktail, input_text):
        """Inserts embedding into Pinecone vector store with metadata"""
        response = dense_index.upsert(
            [
                {
                    "id": cocktail['idDrink'],
                    "values": embedding,
                    "metadata": {
                        "text":input_text,
                        "name":cocktail['strDrink'],
                        "image": cocktail['strDrinkThumb'],
                    }
                }
            ]
        )
        self.check_insertion(response, cocktail=cocktail)


    def process_all_cocktails(self):
        """
        Loads cocktail json data, prepares data, calls create_embeddings() and insert_embeddings()

        Steps:
        1. Load cocktail data from JSON file.
        2. Format relevant fields (name, ingredients, etc.).
        3. Create embedding via OpenAI model.
        4. Insert into Pinecone vector store with metadata.
        """

        file_path = BASE_PATH / "all_cocktails.json"

        cocktails = self.load_cocktails_json(file_path)

        for cocktail in cocktails:
            ingredients = ', '.join(
                [cocktail.get(f"strIngredient{i}")
                 for i in range(1,16)
                 if cocktail.get(f"strIngredient{i}")]
            )
            input_text = f"""
                Name: {cocktail['strDrink']}
                Ingredients: {ingredients}
                Instruction: {cocktail['strInstructions']}
                Alcohol: {cocktail['strAlcoholic']}
                Category: {cocktail['strCategory']}
                Glass: {cocktail['strGlass']}
            """
            embedding = self.create_embeddings(input_text=input_text)
            self.insert_embeddings(embedding, cocktail, input_text)

    async def semantic_search(self, query):
        embedding = await self.client.embeddings.create(
            input=query,
            model="text-embedding-3-small",
        )
        vector = embedding.data[0].embedding
        results = self.dense_index.query(
            vector=vector,
            top_k=2,
            include_metadata=True,
        )
        return results

#
# if __name__ == '__main__':
#     embedding = CocktailEmbedder()
#     embedding.process_all_cocktails()
