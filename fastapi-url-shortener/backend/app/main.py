from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core import settings
from app.api.router import router


app = FastAPI(
    title="URL Shortener",
    description="My URL shortener",
    version="0.1.0",
    docs_url=f"{settings.BASE_PATH}/api/docs"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix=f"{settings.BASE_PATH}/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0", 
        port = settings.PORT,
        reload = settings.DEBUG
    )
