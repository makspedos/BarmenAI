# BarmenAI

### BarmenAI is an AI-powered cocktail assistant that recommends drinks, provides recipes, and suggests alternatives based on user queries. The project combines RAG (Retrieval-Augmented Generation) with OpenAI models to deliver accurate and context-aware cocktail suggestions.

## Features

- AI assistant prompted to behave as a bartender

- Cocktail search and recipe recommendations

- Uses CocktailAPI dataset for knowledge grounding

- RAG (Retrieval-Augmented Generation) implemented with Pinecone as a vector store

- Web UI built with Streamlit for quick testing and demos

## Two implemented approaches:

**LangChain** – retrieval chain with prompt templating

**OpenAI Python SDK with tools** – direct API usage with function/tool calling

## Tech Stack

- OpenAI API (GPT-4o-mini, embeddings)

- LangChain/OpenAI SDK

- Pinecone - vector database for embeddings

- CocktailAPI - dataset for cocktail recipes

- FastAPI - backend service

- Streamlit - frontend service

- uv - package/dependency manager

## Setup & Installation
### 1. Clone repository
***git clone https://github.com/makspedos/BarmenAI.git***
***cd BarmenAI***

### 2. Install dependencies with uv
***uv sync***

### 3. Prepare environment variables

Create a .env file in the root folder:

OPENAI_API_KEY=your_openai_api_key

PINECONE_API_KEY=your_pinecone_api_key

PINECONE_INDEX=your_index_name

### 4. Load CocktailAPI dataset
Use below script to download cocktail data from TheCocktailDB
and preprocess it before inserterting into your vector database:

***python scripts/load_cocktails.py***


### 5 Run the Service

Start FastAPI server:

***uv run fastapi dev app/main.py***

Start StreamLit service:

***streamlit run frontend/main.py***

The Services will be available at:

http://localhost:8000 - fastapi

http://localhost:8501 - streamlit
