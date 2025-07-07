from fastapi import FastAPI
from routes import router
from fastapi.middleware.cors import CORSMiddleware  # <— corrija aqui

app = FastAPI()

# Adicionando o middleware correto
app.add_middleware(
    CORSMiddleware,           # <— use CORSMiddleware
    allow_origins=["*"],      # ou ["https://seusite.com"] para restringir
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API de Análise de Sites"}
