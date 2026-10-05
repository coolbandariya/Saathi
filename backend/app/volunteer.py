from datetime import datetime, timezone
from typing import Literal
from pydantic import BaseModel
class SupportCase(BaseModel):
    id:str; household_id:str; reason:str; transcript:list[dict]; status:Literal["open","assigned","resolved"]="open"; volunteer_id:str|None=None; created_at:datetime=datetime.now(timezone.utc)
def assign_case(case:SupportCase,volunteer_id:str)->SupportCase:
    if case.status!="open": raise ValueError("only open cases can be assigned")
    if not volunteer_id.strip(): raise ValueError("volunteer_id is required")
    return case.model_copy(update={"status":"assigned","volunteer_id":volunteer_id})
def resolve_case(case:SupportCase)->SupportCase:
    if case.status!="assigned": raise ValueError("only assigned cases can be resolved")
    return case.model_copy(update={"status":"resolved"})
