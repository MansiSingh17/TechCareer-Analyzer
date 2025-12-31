

from typing import List, Optional

class SalaryPredictor:
    def __init__(self):
        self.baseline_salaries = {
            "software engineer": 110000,
            "senior software engineer": 150000,
            "data scientist": 130000,
            "machine learning engineer": 140000,
            "frontend developer": 105000,
            "backend developer": 115000,
            "full stack developer": 120000,
        }
    
    async def load_model(self):
        print("Salary predictor initialized (baseline model)")
    
    async def predict(
        self,
        skills: List[str],
        experience_years: float,
        role: str,
        location: Optional[str] = None
    ) -> float:
        # Get base salary
        role_lower = role.lower()
        base_salary = 100000
        
        for known_role, salary in self.baseline_salaries.items():
            if known_role in role_lower:
                base_salary = salary
                break
        
        # Adjust for experience (5% per year)
        experience_multiplier = 1 + (experience_years * 0.05)
        experience_multiplier = min(experience_multiplier, 2.0)
        
        adjusted_salary = base_salary * experience_multiplier
        
        # Add skill bonus
        high_value_skills = {
            "Machine Learning": 15000,
            "AWS": 10000,
            "Kubernetes": 12000,
            "React": 8000,
            "Python": 5000
        }
        
        skill_bonus = sum(high_value_skills.get(skill, 0) for skill in skills)
        adjusted_salary += skill_bonus
        
        # Location multiplier
        location_multipliers = {
            "san francisco": 1.35,
            "new york": 1.30,
            "seattle": 1.25,
            "remote": 1.00
        }
        
        if location:
            location_lower = location.lower()
            for loc, multiplier in location_multipliers.items():
                if loc in location_lower:
                    adjusted_salary *= multiplier
                    break
        
        return round(adjusted_salary, 2)