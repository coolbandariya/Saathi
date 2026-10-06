from pathlib import Path


def test_dashboard_contains_memory_reminder_and_task_continuation_controls():
    source = Path(__file__).parents[2].joinpath("frontend/app/dashboard/page.tsx").read_text(encoding="utf-8")
    assert "memoryConsent" in source
    assert "reminderConsent" in source
    assert "followUpStatus" in source
    assert "simulateThreeDaysLater" in source
    assert "Consent" in source
