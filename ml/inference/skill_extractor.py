

import re
from typing import List, Dict

class SkillExtractor:
    def __init__(self):
        self.skill_patterns = self._load_skill_patterns()
        self.soft_skill_keywords = self._load_soft_skills()
    
    def _load_skill_patterns(self) -> dict:
        return {
            "languages": r'\b(Python|Java|JavaScript|TypeScript|Go|Rust|C\+\+|C#|Ruby|PHP|Swift|Kotlin)\b',
            "frameworks": r'\b(React|Angular|Vue|Django|Flask|FastAPI|Spring|Express|Rails)\b',
            "databases": r'\b(PostgreSQL|MySQL|MongoDB|Redis|Elasticsearch)\b',
            "cloud": r'\b(AWS|Azure|GCP|Docker|Kubernetes)\b',
            "ml": r'\b(Machine Learning|Deep Learning|TensorFlow|PyTorch)\b',
        }

    def _load_soft_skills(self) -> List[str]:
        return [
            "communication", "leadership", "teamwork", "collaboration", "problem solving",
            "critical thinking", "adaptability", "creativity", "time management", "mentoring",
            "stakeholder management", "presentation", "writing", "negotiation", "conflict resolution",
            "ownership", "self-starter", "attention to detail", "decision making"
        ]
    
    async def load_model(self):
        print("Skill extractor initialized (rule-based)")
    
    async def extract(self, text: str) -> Dict[str, List[str]]:
        text = self._preprocess_text(text)
        technical = sorted(set(self._extract_with_rules(text)))
        soft = sorted(set(self._extract_soft_skills(text)))
        return {"technical": technical, "soft": soft}
    
    def _preprocess_text(self, text: str) -> str:
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def _extract_with_rules(self, text: str) -> List[str]:
        skills = []
        for category, pattern in self.skill_patterns.items():
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                skills.append(match.group(0))
        return skills

    def _extract_soft_skills(self, text: str) -> List[str]:
        found = []
        lower_text = text.lower()
        for keyword in self.soft_skill_keywords:
            if keyword in lower_text:
                # Keep original casing for readability
                found.append(keyword.title())
        return found