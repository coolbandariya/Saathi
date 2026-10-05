from pydantic import BaseModel, Field
from .domain import SourceRef, ToolResult

class SchemeProfile(BaseModel):
    class_12_percentile: float | None = Field(default=None, ge=0, le=100)
    regular_degree: bool | None = None
    recognized_institution: bool | None = None
    annual_family_income: int | None = Field(default=None, ge=0)
    aadhaar_seeded_bank: bool | None = None
    other_scholarship: bool | None = None

class Scheme(BaseModel):
    id: str
    name: str
    source: SourceRef
    eligibility: dict
    application_url: str | None = None

PM_USP = Scheme(
    id="pm-usp-csss-cus",
    name="Pradhan Mantri Uchchatar Shiksha Protsahan (PM-USP) Central Sector Scheme of Scholarship for College and University Students",
    source=SourceRef(name="myScheme", url="https://www.myscheme.gov.in/schemes/csss-cus"),
    eligibility={
        "class_12_percentile_min": 80,
        "regular_degree_required": True,
        "recognized_institution_required": True,
        "annual_family_income_max": 450000,
        "aadhaar_seeded_bank_required": True,
        "other_scholarship_allowed": False,
    },
    application_url="https://scholarships.gov.in/",
)

def evaluate_pm_usp(profile: SchemeProfile) -> ToolResult:
    checks = {
        "class_12_percentile": profile.class_12_percentile is not None and profile.class_12_percentile >= 80,
        "regular_degree": profile.regular_degree is True,
        "recognized_institution": profile.recognized_institution is True,
        "income": profile.annual_family_income is not None and profile.annual_family_income <= 450000,
        "aadhaar_seeded_bank": profile.aadhaar_seeded_bank is True,
        "no_other_scholarship": profile.other_scholarship is False,
    }
    missing = [name for name, passed in checks.items() if not passed]
    return ToolResult(
        ok=True,
        data={"scheme_id": PM_USP.id, "eligible": not missing, "failed_or_missing_checks": missing, "application_url": PM_USP.application_url},
        sources=[PM_USP.source],
    )
