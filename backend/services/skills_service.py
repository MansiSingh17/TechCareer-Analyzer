
from typing import List, Dict, Optional
import numpy as np
from collections import Counter
from ml.inference.skill_extractor import SkillExtractor
from backend.models.job import Job
from backend.utils.db import get_db_session
from sqlalchemy import func

class SkillsService:
    def __init__(self):
        self.extractor = SkillExtractor()
        
        # Skill categories
        self.skill_categories = {
            "Programming Languages": [
                "Python", "JavaScript", "Java", "TypeScript", "Go", "Rust", "C++", "C#"
            ],
            "Frontend": [
                "React", "Vue", "Angular", "HTML", "CSS", "Next.js"
            ],
            "Backend": [
                "Node.js", "Express", "Django", "Flask", "Spring"
            ],
            "Database": [
                "PostgreSQL", "MySQL", "MongoDB", "Redis"
            ],
            "Cloud & DevOps": [
                "AWS", "Azure", "GCP", "Docker", "Kubernetes"
            ],
            "Data Science & ML": [
                "Machine Learning", "TensorFlow", "PyTorch", "Pandas"
            ]
        }
    
    async def extract_skills(self, job_description: str) -> Dict:
        """
        Extract skills (technical + soft) from job description
        """
        extracted = await self.extractor.extract(job_description)
        validated_tech = await self.validate_skills(extracted["technical"])
        soft_skills = extracted.get("soft", [])
        return {
            "technical_skills": validated_tech["valid_skills"],
            "soft_skills": soft_skills,
            "counts": {
                "technical": len(validated_tech["valid_skills"]),
                "soft": len(soft_skills),
                "total": len(validated_tech["valid_skills"]) + len(soft_skills)
            }
        }
    
    async def analyze_gap(
        self,
        current_skills: List[str],
        target_role: str,
        experience_years: float
    ) -> Dict:
        """
        Analyze skill gaps for target role
        """
        # Get typical skills for target role
        role_skills = await self._get_role_skills(target_role)
        
        current_set = set(current_skills)
        required_set = set(role_skills["required"])
        
        # Calculate gaps
        critical_gaps = list(required_set - current_set)
        matching_skills = list(current_set & required_set)
        
        # Calculate match percentage
        match_percentage = len(matching_skills) / len(required_set) * 100 if required_set else 0
        
        # Prioritize gaps
        prioritized_gaps = await self._prioritize_gaps(critical_gaps, target_role)
        
        return {
            "target_role": target_role,
            "match_percentage": round(match_percentage, 1),
            "matching_skills": matching_skills,
            "critical_gaps": critical_gaps,
            "prioritized_learning_path": prioritized_gaps,
            "estimated_time_to_ready": self._estimate_learning_time(len(critical_gaps))
        }
    
    async def _get_role_skills(self, role: str) -> Dict:
        """
        Get typical skills for a role
        """
        db = get_db_session()
        
        try:
            jobs = db.query(Job).filter(
                Job.title.ilike(f"%{role}%")
            ).limit(100).all()
            
            if not jobs:
                return {"required": []}
            
            # Count skill frequencies
            skill_counts = Counter()
            for job in jobs:
                skill_counts.update(job.required_skills)
            
            # Skills appearing in >60% of jobs are required
            threshold = len(jobs) * 0.6
            required = [skill for skill, count in skill_counts.items() if count >= threshold]
            
            return {
                "required": required,
                "total_jobs_analyzed": len(jobs)
            }
        
        finally:
            db.close()
    
    async def _prioritize_gaps(self, gaps: List[str], role: str) -> List[Dict]:
        """
        Prioritize skill gaps
        """
        prioritized = []
        
        for skill in gaps:
            demand = await self._get_skill_demand(skill, role)
            difficulty = self._estimate_difficulty(skill)
            
            prioritized.append({
                "skill": skill,
                "priority": "critical",
                "demand_score": demand,
                "difficulty": difficulty,
                "estimated_learning_weeks": difficulty * 2
            })
        
        prioritized.sort(key=lambda x: x["demand_score"], reverse=True)
        return prioritized
    
    async def _get_skill_demand(self, skill: str, role: str) -> float:
        """
        Calculate demand score for a skill
        """
        db = get_db_session()
        
        try:
            total_jobs = db.query(func.count(Job.id)).filter(
                Job.title.ilike(f"%{role}%")
            ).scalar()
            
            jobs_with_skill = db.query(func.count(Job.id)).filter(
                Job.title.ilike(f"%{role}%"),
                Job.required_skills.contains([skill])
            ).scalar()
            
            if total_jobs == 0:
                return 50.0
            
            demand = (jobs_with_skill / total_jobs) * 100
            return min(demand, 100)
        
        finally:
            db.close()
    
    def _estimate_difficulty(self, skill: str) -> int:
        """
        Estimate learning difficulty (1-5)
        """
        difficulty_map = {
            "HTML": 1, "CSS": 1, "Git": 1,
            "JavaScript": 2, "Python": 2, "React": 2,
            "TypeScript": 3, "AWS": 3, "Docker": 3,
            "Machine Learning": 4, "Kubernetes": 4,
            "Deep Learning": 5
        }
        return difficulty_map.get(skill, 3)
    
    def _estimate_learning_time(self, gap_count: int) -> str:
        """
        Estimate time to learn all gaps
        """
        weeks = gap_count * 3
        if weeks <= 4:
            return "1 month"
        elif weeks <= 12:
            return f"{weeks // 4} months"
        else:
            return f"{weeks // 4} months"
    
    async def generate_learning_path(
        self,
        current_skills: List[str],
        target_role: str,
        experience_years: float
    ) -> Dict:
        """
        Generate a structured learning path
        """
        gap_analysis = await self.analyze_gap(
            current_skills, target_role, experience_years
        )
        
        prioritized = gap_analysis["prioritized_learning_path"]
        
        # Group by difficulty
        phase1 = [s for s in prioritized if s["difficulty"] <= 2][:3]
        phase2 = [s for s in prioritized if s["difficulty"] == 3][:3]
        phase3 = [s for s in prioritized if s["difficulty"] >= 4][:2]
        
        return {
            "target_role": target_role,
            "current_match": gap_analysis["match_percentage"],
            "phases": [
                {
                    "phase": 1,
                    "duration": "1-2 months",
                    "focus": "Foundation Skills",
                    "skills": phase1
                },
                {
                    "phase": 2,
                    "duration": "2-3 months",
                    "focus": "Core Competencies",
                    "skills": phase2
                },
                {
                    "phase": 3,
                    "duration": "3-4 months",
                    "focus": "Advanced Skills",
                    "skills": phase3
                }
            ],
            "total_estimated_time": gap_analysis["estimated_time_to_ready"]
        }
    
    async def validate_skills(self, skills: List[str]) -> Dict:
        """
        Validate and normalize skill names
        """
        known_skills = set()
        for category_skills in self.skill_categories.values():
            known_skills.update([s.lower() for s in category_skills])
        
        valid_skills = []
        invalid_skills = []
        
        for skill in skills:
            skill_lower = skill.lower()
            
            if skill_lower in known_skills:
                for cat_skills in self.skill_categories.values():
                    for known_skill in cat_skills:
                        if known_skill.lower() == skill_lower:
                            valid_skills.append(known_skill)
                            break
            else:
                valid_skills.append(skill)  # Keep unknown skills
        
        return {
            "valid_skills": valid_skills,
            "invalid_skills": invalid_skills
        }