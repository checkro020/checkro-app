from fastapi import FastAPI
from routes import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Adicionando o middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou ["https://premioverde.com"] para mais segurança
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API de Análise de Sites"}

