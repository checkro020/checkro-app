from pydantic import BaseModel

class ScanRequest(BaseModel):
    url: str

class IssueResponse(BaseModel):
    id: int
    page_url: str
    rule_code: str
    description: str
    term_detected: str | None
    suggestion: str
