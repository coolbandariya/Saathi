from pathlib import Path
from pydantic import BaseModel, Field
ALLOWED_TYPES={"application/pdf","image/jpeg","image/png"}; MAX_BYTES=10*1024*1024
class DocumentExtraction(BaseModel):
    text: str; confidence: float=Field(ge=0,le=1); fields: dict={}; needs_human_review: bool=False
def validate_upload(content_type: str,size_bytes: int,filename: str)->None:
    if content_type not in ALLOWED_TYPES: raise ValueError("unsupported document type")
    if size_bytes<=0 or size_bytes>MAX_BYTES: raise ValueError("document size must be between 1 byte and 10 MB")
    if Path(filename).name!=filename: raise ValueError("invalid filename")
def review_gate(extraction: DocumentExtraction,threshold: float=.85)->DocumentExtraction:
    return extraction.model_copy(update={"needs_human_review":extraction.confidence<threshold})
