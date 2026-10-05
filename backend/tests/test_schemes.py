from app.schemes import SchemeProfile, evaluate_pm_usp

def test_pm_usp_eligible_profile():
    result=evaluate_pm_usp(SchemeProfile(class_12_percentile=85,regular_degree=True,recognized_institution=True,annual_family_income=300000,aadhaar_seeded_bank=True,other_scholarship=False))
    assert result.ok is True
    assert result.data["eligible"] is True
    assert result.sources[0].url == "https://www.myscheme.gov.in/schemes/csss-cus"

def test_pm_usp_ineligible_profile_is_explainable():
    result=evaluate_pm_usp(SchemeProfile(class_12_percentile=75,regular_degree=True,recognized_institution=True,annual_family_income=500000,aadhaar_seeded_bank=True,other_scholarship=False))
    assert result.data["eligible"] is False
    assert "class_12_percentile" in result.data["failed_or_missing_checks"]
    assert "income" in result.data["failed_or_missing_checks"]
