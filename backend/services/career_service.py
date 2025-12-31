import numpy as np
from typing import List, Dict, Optional
from ml.inference.skill_extractor import SkillExtractor
from ml.inference.salary_predictor import SalaryPredictor
from backend.models.job import Job
from backend.utils.db import get_db_session
from sqlalchemy import func

class CareerService:
    def __init__(self):
        self.skill_extractor = SkillExtractor()
        self.salary_predictor = SalaryPredictor()
    
    async def analyze_career_path(
        self,
        skills: List[str],
        experience_years: float,
        current_role: Optional[str] = None,
        education: Optional[str] = None,
        location: Optional[str] = None
    ) -> Dict:
        """Analyze career path and provide recommendations"""
        
        # Find matching roles based on skills
        recommended_roles = await self._find_matching_roles(skills, experience_years)
        
        # Analyze skill gaps for top roles
        skill_gaps = await self._analyze_skill_gaps(skills, recommended_roles[:5])
        
        # Predict salary range
        salary_range = await self._predict_salary_range(skills, experience_years, location)
        
        # Generate growth trajectory
        growth_trajectory = await self._generate_growth_trajectory(
            skills, experience_years, recommended_roles
        )
        
        # Create learning path
        learning_path = await self._create_learning_path(skill_gaps)
        
        return {
            "recommended_roles": recommended_roles,
            "skill_gaps": skill_gaps,
            "salary_range": salary_range,
            "growth_trajectory": growth_trajectory,
            "learning_path": learning_path
        }
    
    async def _find_matching_roles(self, skills: List[str], experience_years: float) -> List[Dict]:
        """Find roles that match the skill set"""
        db = get_db_session()
        
        try:
            # Get all jobs
            jobs = db.query(Job).all()
            
            # Calculate match scores
            role_scores = {}
            for job in jobs:
                # Calculate skill match
                job_skills = set(job.required_skills) if job.required_skills else set()
                user_skills = set(skills)
                
                if not job_skills:
                    continue
                
                matching_skills = job_skills & user_skills
                match_score = len(matching_skills) / len(job_skills) if job_skills else 0
                
                # Calculate experience match
                exp_match = 1.0 - abs(job.experience_required - experience_years) / 10.0
                exp_match = max(0, exp_match)
                
                total_score = (match_score * 0.7) + (exp_match * 0.3)
                
                if job.title not in role_scores:
                    role_scores[job.title] = {
                        "role": job.title,
                        "match_score": total_score,
                        "avg_salary": 0,
                        "required_skills": list(job_skills),
                        "count": 0
                    }
                
                if job.salary:
                    role_scores[job.title]["avg_salary"] += job.salary
                role_scores[job.title]["count"] += 1
            
            # Calculate averages
            recommended_roles = []
            for role_data in role_scores.values():
                if role_data["count"] > 0 and role_data["avg_salary"] > 0:
                    role_data["avg_salary"] /= role_data["count"]
                recommended_roles.append(role_data)
            
            # Sort by match score
            recommended_roles.sort(key=lambda x: x["match_score"], reverse=True)
            
            return recommended_roles[:10]
        
        finally:
            db.close()
    
    async def _analyze_skill_gaps(self, current_skills: List[str], target_roles: List[Dict]) -> List[Dict]:
        """Analyze skill gaps for target roles"""
        gaps = []
        
        for role in target_roles:
            required_skills = set(role["required_skills"])
            current_skills_set = set(current_skills)
            
            missing_skills = required_skills - current_skills_set
            
            if missing_skills:
                gaps.append({
                    "role": role["role"],
                    "missing_skills": list(missing_skills),
                    "gap_count": len(missing_skills),
                    "priority": self._calculate_skill_priority(missing_skills)
                })
        
        return gaps
    
    def _calculate_skill_priority(self, skills: set) -> str:
        """Calculate priority level for skill gaps"""
        gap_count = len(skills)
        if gap_count <= 2:
            return "low"
        elif gap_count <= 5:
            return "medium"
        else:
            return "high"
    
    async def _predict_salary_range(self, skills: List[str], experience_years: float, location: Optional[str]) -> Dict:
        """Predict salary range"""
        predicted_salary = await self.salary_predictor.predict(
            skills=skills,
            experience_years=experience_years,
            location=location or "Remote",
            role="Software Engineer"
        )
        
        return {
            "predicted": predicted_salary,
            "min": predicted_salary * 0.85,
            "max": predicted_salary * 1.15
        }
    
    async def _generate_growth_trajectory(self, skills: List[str], experience_years: float, recommended_roles: List[Dict]) -> List[Dict]:
        """Generate career growth trajectory"""
        trajectory = []
        
        current_salary = await self._predict_salary_range(skills, experience_years, None)
        trajectory.append({
            "year": 0,
            "role": "Current",
            "skills_count": len(skills),
            "estimated_salary": current_salary
        })
        
        for year in [1, 2, 3]:
            projected_skills = len(skills) + (year * 2)
            projected_exp = experience_years + year
            projected_salary = await self._predict_salary_range(skills, projected_exp, None)
            
            trajectory.append({
                "year": year,
                "role": recommended_roles[min(year-1, len(recommended_roles)-1)]["role"] if recommended_roles else "Projected",
                "skills_count": projected_skills,
                "estimated_salary": projected_salary
            })
        
        return trajectory
    
    async def _create_learning_path(self, skill_gaps: List[Dict]) -> List[str]:
        """Create prioritized learning path"""
        all_missing_skills = set()
        for gap in skill_gaps:
            all_missing_skills.update(gap["missing_skills"])
        
        skill_frequency = {}
        for gap in skill_gaps:
            for skill in gap["missing_skills"]:
                skill_frequency[skill] = skill_frequency.get(skill, 0) + 1
        
        sorted_skills = sorted(skill_frequency.items(), key=lambda x: x[1], reverse=True)
        return [skill for skill, _ in sorted_skills[:10]]
    
    async def compare_roles(self, profile: Dict, target_roles: List[str]) -> Dict:
        """Compare profile against multiple target roles"""
        comparisons = []
        
        for role in target_roles:
            requirements = await self.get_role_requirements(role)
            
            if "error" not in requirements:
                profile_skills = set(profile.get("skills", []))
                req_skills = set(requirements.get("skills", []))
                
                skill_match = len(profile_skills & req_skills) / max(len(req_skills), 1)
                
                comparisons.append({
                    "role": role,
                    "match_percentage": skill_match * 100,
                    "requirements": requirements,
                    "skill_gap": list(req_skills - profile_skills)
                })
        
        return {"comparisons": comparisons}
    
    async def get_role_requirements(self, role_name: str) -> Dict:
        """Get typical requirements for a role"""
        db = get_db_session()
        
        try:
            jobs = db.query(Job).filter(
                func.lower(Job.title).like(f"%{role_name.lower()}%")
            ).all()
            
            if not jobs:
                return {"error": "Role not found"}
            
            from collections import Counter
            all_skills = []
            salaries = []
            experience_levels = []
            
            for job in jobs:
                if job.required_skills:
                    all_skills.extend(job.required_skills)
                if job.salary:
                    salaries.append(job.salary)
                experience_levels.append(job.experience_required)
            
            skill_counts = Counter(all_skills)
            top_skills = [skill for skill, _ in skill_counts.most_common(15)]
            
            return {
                "role": role_name,
                "skills": top_skills,
                "avg_salary": np.mean(salaries) if salaries else 0,
                "avg_experience": np.mean(experience_levels),
                "sample_size": len(jobs)
            }
        
        finally:
            db.close()
