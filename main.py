from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from routes import router  

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router) 
class UrlRequest(BaseModel):
    url: str

@app.post("/analisar")
async def analisar_url(payload: UrlRequest):
    url = payload.url
    return {
        "status": "ok",
        "mensagem": f"Analisando a URL: {url}"
    }

@app.get("/")
async def root():
    return {"status": "API online"}
