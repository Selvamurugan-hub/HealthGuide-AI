import re
from typing import List, Optional
from pydantic import BaseModel
from .rules import EMERGENCY_RULES, EmergencyRule


class WarningSignMatch(BaseModel):
    category: str
    rule_name_en: str
    rule_name_ta: str
    description_en: str
    description_ta: str
    matched_snippet: str


def normalize_input_text(text: str) -> str:
    """Normalize text by collapsing whitespace and standardizing quotes/apostrophes."""
    if not text:
        return ""
    # Standardize apostrophes
    normalized = text.replace("’", "'").replace("`", "'")
    # Collapse multiple whitespaces
    normalized = re.sub(r"\s+", " ", normalized)
    return normalized.strip()


class EmergencyDetector:
    """Deterministic, auditable emergency warning signs scanner."""

    def __init__(self, rules: Optional[List[EmergencyRule]] = None):
        self.rules = rules or EMERGENCY_RULES

    def scan(self, text: str, context: Optional[str] = None) -> List[WarningSignMatch]:
        combined_text = normalize_input_text(f"{text} {context or ''}")
        matches: List[WarningSignMatch] = []
        seen_categories = set()

        for rule in self.rules:
            for pattern in rule.compiled_patterns:
                m = pattern.search(combined_text)
                if m:
                    # Avoid duplicate reporting of the same category
                    if rule.category not in seen_categories:
                        seen_categories.add(rule.category)
                        matches.append(
                            WarningSignMatch(
                                category=rule.category,
                                rule_name_en=rule.name_en,
                                rule_name_ta=rule.name_ta,
                                description_en=rule.description_en,
                                description_ta=rule.description_ta,
                                matched_snippet=m.group(0),
                            )
                        )
                    break

        return matches
