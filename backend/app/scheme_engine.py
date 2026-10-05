from dataclasses import dataclass


@dataclass(frozen=True)
class SchemeRule:
    name: str
    required_fields: tuple[str, ...]
    required_documents: tuple[str, ...]


@dataclass(frozen=True)
class EligibilityResult:
    eligible: bool
    missing_fields: tuple[str, ...]
    missing_documents: tuple[str, ...]


def evaluate(rule: SchemeRule, profile: dict[str, object], documents: set[str]) -> EligibilityResult:
    missing_fields = tuple(field for field in rule.required_fields if not profile.get(field))
    missing_documents = tuple(doc for doc in rule.required_documents if doc not in documents)
    return EligibilityResult(
        eligible=not missing_fields and not missing_documents,
        missing_fields=missing_fields,
        missing_documents=missing_documents,
    )
