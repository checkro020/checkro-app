from fastapi import APIRouter, HTTPException, Request
import requests

router = APIRouter()

@router.post("/scan")
async def scan_url(request: Request):
    body = await request.json()
    url = body.get("url")

    if not url:
        raise HTTPException(status_code=400, detail="URL não fornecida")

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return {"status": "ok", "code": response.status_code}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Erro ao acessar a URL: {str(e)}")

