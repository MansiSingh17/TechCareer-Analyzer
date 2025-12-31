# Location: /techcareer-analyzer/backend/services/salary_service.py

import numpy as np
from typing import List, Dict, Optional
from ml.inference.salary_predictor import SalaryPredictor
from backend.models.job import Job
from backend.utils.db import get_db_session
from sqlalchemy import func

class SalaryService:
    def __init__(self):
        self.predictor = SalaryPredictor()
        self.location_multipliers = {
            "San Francisco": 1.35,
            "New York": 1.30,
            "Seattle": 1.25,
            "Austin": 1.10,
            "Remote": 1.00,
            "Denver": 1.05,
            "Chicago": 1.08
        }
    
    async def predict_salary(
        self,
        skills: List[str],
        experience_years: float,
        role: str,
        location: str,
        company_size: Optional[str] = None,
        education: Optional[str] = None
    ) -> Dict:
        """
        Predict salary using ML model
        """
        # Get base prediction from model
        base_salary = await self.predictor.predict(
            skills=skills,
            experience_years=experience_years,
            role=role,
            location=location
        )
        
        # Apply location adjustment
        location_multiplier = self.location_multipliers.get(location, 1.0)
        adjusted_salary = base_salary * location_multiplier
        
        # Apply company size adjustment
        if company_size:
            size_adjustment = self._get_company_size_adjustment(company_size)
            adjusted_salary *= size_adjustment
        
        # Apply education adjustment
        if education:
            edu_adjustment = self._get_education_adjustment(education)
            adjusted_salary *= edu_adjustment
        
        # Calculate confidence and percentile
        confidence = await self._calculate_confidence(
            skills, experience_years, role, location
        )
        
        percentile = await self._calculate_market_percentile(
            adjusted_salary, role, location
        )
        
        # Analyze contributing factors
        factors = self._analyze_salary_factors(
            skills, experience_years, location, company_size, education
        )
        
        return {
            "predicted_salary": round(adjusted_salary, 2),
            "salary_range": {
                "min": round(adjusted_salary * 0.85, 2),
                "max": round(adjusted_salary * 1.15, 2),
                "median": round(adjusted_salary, 2)
            },
            "confidence_score": confidence,
            "market_percentile": percentile,
            "factors": factors
        }
    
    def _get_company_size_adjustment(self, company_size: str) -> float:
        """
        Get salary adjustment based on company size
        """
        size_multipliers = {
            "startup": 0.90,
            "small": 0.95,
            "medium": 1.00,
            "large": 1.10,
            "enterprise": 1.15
        }
        return size_multipliers.get(company_size.lower(), 1.0)
    
    def _get_education_adjustment(self, education: str) -> float:
        """
        Get salary adjustment based on education
        """
        edu_multipliers = {
            "bachelor": 1.00,
            "master": 1.10,
            "phd": 1.20,
            "bootcamp": 0.95
        }
        education_lower = education.lower()
        for key, multiplier in edu_multipliers.items():
            if key in education_lower:
                return multiplier
        return 1.0
    
    async def _calculate_confidence(
        self,
        skills: List[str],
        experience_years: float,
        role: str,
        location: str
    ) -> float:
        """
        Calculate confidence score for prediction
        """
        db = get_db_session()
        
        try:
            similar_jobs = db.query(func.count(Job.id)).filter(
                Job.title.ilike(f"%{role}%"),
                Job.experience_required.between(experience_years - 2, experience_years + 2)
            ).scalar()
            
            # Confidence based on sample size
            if similar_jobs > 100:
                return 0.95
            elif similar_jobs > 50:
                return 0.85
            elif similar_jobs > 20:
                return 0.75
            else:
                return 0.65
        
        finally:
            db.close()
    
    async def _calculate_market_percentile(
        self,
        salary: float,
        role: str,
        location: str
    ) -> float:
        """
        Calculate what percentile this salary represents
        """
        db = get_db_session()
        
        try:
            salaries = db.query(Job.salary).filter(
                Job.title.ilike(f"%{role}%"),
                Job.salary.isnot(None)
            ).all()
            
            if not salaries:
                return 50.0
            
            salary_values = [s[0] for s in salaries]
            percentile = (sum(s < salary for s in salary_values) / len(salary_values)) * 100
            
            return round(percentile, 1)
        
        finally:
            db.close()
    
    def _analyze_salary_factors(
        self,
        skills: List[str],
        experience_years: float,
        location: str,
        company_size: Optional[str],
        education: Optional[str]
    ) -> Dict[str, float]:
        """
        Analyze which factors contribute most to salary
        """
        factors = {
            "experience": min(experience_years / 15.0, 1.0) * 0.35,
            "skills": min(len(skills) / 20.0, 1.0) * 0.30,
            "location": (self.location_multipliers.get(location, 1.0) - 0.9) * 0.20,
            "company_size": 0.10 if company_size else 0.05,
            "education": 0.05 if education else 0.00
        }
        
        # Normalize to 100%
        total = sum(factors.values())
        return {k: round(v / total * 100, 1) for k, v in factors.items()}
    
    async def get_salary_range(self, role: str, location: Optional[str] = None) -> Dict:
        """
        Get salary range from market data
        """
        db = get_db_session()
        
        try:
            query = db.query(Job.salary).filter(
                Job.title.ilike(f"%{role}%"),
                Job.salary.isnot(None)
            )
            
            if location:
                query = query.filter(Job.location.ilike(f"%{location}%"))
            
            salaries = [s[0] for s in query.all()]
            
            if not salaries:
                return {"error": "No data found for this role"}
            
            return {
                "role": role,
                "location": location or "All locations",
                "min": min(salaries),
                "max": max(salaries),
                "median": np.median(salaries),
                "mean": np.mean(salaries),
                "p25": np.percentile(salaries, 25),
                "p75": np.percentile(salaries, 75),
                "sample_size": len(salaries)
            }
        
        finally:
            db.close()
    
    async def compare_locations(
        self,
        role: str,
        locations: List[str],
        experience_years: float
    ) -> Dict:
        """
        Compare salaries across locations
        """
        comparisons = []
        
        for location in locations:
            salary_range = await self.get_salary_range(role, location)
            
            if "error" not in salary_range:
                col_adjustment = self.location_multipliers.get(location, 1.0)
                
                comparisons.append({
                    "location": location,
                    "median_salary": salary_range["median"],
                    "col_adjusted": salary_range["median"] / col_adjustment,
                    "range": {
                        "min": salary_range["min"],
                        "max": salary_range["max"]
                    }
                })
        
        return {"role": role, "comparisons": comparisons}
    
    async def get_negotiation_insights(
        self,
        skills: List[str],
        experience_years: float,
        role: str,
        location: str
    ) -> Dict:
        """
        Get insights for salary negotiation
        """
        # Get prediction
        prediction = await self.predict_salary(
            skills=skills,
            experience_years=experience_years,
            role=role,
            location=location
        )
        
        # Get market data
        market_range = await self.get_salary_range(role, location)
        
        if "error" in market_range:
            market_range = {
                "median": prediction["predicted_salary"],
                "p75": prediction["predicted_salary"] * 1.15
            }
        
        # Generate insights
        insights = {
            "your_position": "strong" if prediction["market_percentile"] > 60 else "moderate",
            "target_range": {
                "conservative": round(market_range["median"] * 1.05, 2),
                "moderate": round(market_range["median"] * 1.10, 2),
                "aggressive": round(market_range.get("p75", market_range["median"] * 1.15), 2)
            },
            "leverage_points": self._get_leverage_points(
                skills, experience_years, prediction["market_percentile"]
            ),
            "market_data": market_range
        }
        
        return insights
    
    def _get_leverage_points(
        self,
        skills: List[str],
        experience_years: float,
        percentile: float
    ) -> List[str]:
        """
        Get negotiation leverage points
        """
        points = []
        
        if experience_years > 5:
            points.append(f"Strong experience: {experience_years} years")
        
        if len(skills) > 10:
            points.append(f"Diverse skill set: {len(skills)} skills")
        
        if percentile > 70:
            points.append(f"Above market average (top {100-percentile:.0f}%)")
        
        # Add high-value skills
        high_value_skills = ["AWS", "Kubernetes", "Machine Learning", "React", "Python"]
        matching_high_value = [s for s in skills if s in high_value_skills]
        
        if matching_high_value:
            points.append(f"High-demand skills: {', '.join(matching_high_value)}")
        
        return points