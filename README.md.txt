Minha API de Análise de Sites
Uma API para analisar sites com base em regras de conformidade, usando FastAPI, Celery e PostgreSQL.
Como rodar localmente

Clone o repositório:git clone https://github.com/seu-usuario/minha-api.git
cd minha-api


Crie e ative um ambiente virtual:python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows


Instale as dependências:pip install -r requirements.txt


Configure as variáveis de ambiente em um arquivo .env:DATABASE_URL=postgresql://user:password@host:port/dbname
REDIS_URL=redis://host:port/0


Inicie o servidor FastAPI:uvicorn main:app --reload


Inicie o worker do Celery:python celery_worker.py



Endpoints

POST /scan: Inicia uma varredura de um site, retornando um scan_id.
