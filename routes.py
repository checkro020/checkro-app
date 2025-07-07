from database import get_db
from tasks import scan_site
  

import uuid
import time
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from models import Scan

router = APIRouter()

@router.post("/scan")
def start_scan(url: str, db: Session = Depends(get_db)):
    scan_id = str(uuid.uuid4())
    scan = Scan(id=scan_id, url=url, status="pending", created_at=int(time.time()))
    db.add(scan)
    db.commit()
    scan_site.delay(scan_id, url)
    return {"scan_id": scan_id, "status": "pending"}

@router.get("/analisar")
def analisar_get(url: str, db: Session = Depends(get_db)):
    scan_id = str(uuid.uuid4())
    scan = Scan(id=scan_id, url=url, status="pending", created_at=int(time.time()))
    db.add(scan)
    db.commit()
    scan_site.delay(scan_id, url)
    return {"scan_id": scan_id, "status": "pending"}
