from fastapi import FastAPI
from routes import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configuração correta e segura de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://checkro.com"],  # Somente aceita requisições do domínio oficial
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui as rotas da aplicação
app.include_router(router)

# Rota raiz (opcional, só para teste)
@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API de Análise de Sites"}
