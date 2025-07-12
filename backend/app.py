from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.core.config import settings
from backend.routers.query import router

import dotenv

dotenv.load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)
#uvicorn backend.app:app --host localhost --port 8000 --reload


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app:app", host="localhost", port=8000, reload=True)