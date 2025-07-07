from fastapi import APIRouter, Depends, HTTPException
from models import Scan
from database import get_db
from apptasks import scan_site

import uuid
import time
from sqlalchemy.orm import Session

router = APIRouter()

# Rota POST original para iniciar análise
@router.post("/scan")
def start_scan(url: str, db: Session = Depends(get_db)):
    scan_id = str(uuid.uuid4())
    scan = Scan(id=scan_id, url=url, status="pending", created_at=int(time.time()))
    db.add(scan)
    db.commit()
    scan_site.delay(scan_id, url)
    return {"scan_id": scan_id, "status": "pending"}

# NOVA rota GET para funcionar com a URL ?url=...
@router.get("/analisar")
def analisar_get(url: str, db: Session = Depends(get_db)):
    scan_id = str(uuid.uuid4())
    scan = Scan(id=scan_id, url=url, status="pending", created_at=int(time.time()))
    db.add(scan)
    db.commit()
    scan_site.delay(scan_id, url)
    return {"scan_id": scan_id, "status": "pending"}
