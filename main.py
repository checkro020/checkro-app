from fastapi import FastAPI
from routes import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configuração correta de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://checkro.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui as rotas
app.include_router(router)

# Rota raiz para teste
@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API de Análise de Sites"}
