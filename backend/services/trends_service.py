

import numpy as np
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from collections import Counter
from backend.models.job import Job
from backend.utils.db import get_db_session
from ml.inference.forecaster import SkillForecaster
from sqlalchemy import func, and_

class TrendsService:
    def __init__(self):
        self.forecaster = SkillForecaster()
    
    async def get_trending_skills(
        self,
        time_range: str,
        role: Optional[str] = None,
        location: Optional[str] = None,
        limit: int = 20
    ) -> Dict:
        """
        Get trending skills in the job market
        """
        db = get_db_session()
        
        try:
            # Calculate date range
            days = self._get_days_from_range(time_range)
            start_date = datetime.now() - timedelta(days=days)
            
            # Query jobs
            query = db.query(Job).filter(Job.posted_date >= start_date)
            
            if role:
                query = query.filter(Job.title.ilike(f"%{role}%"))
            
            if location:
                query = query.filter(Job.location.ilike(f"%{location}%"))
            
            jobs = query.all()
            
            # Count skill occurrences
            skill_counts = Counter()
            for job in jobs:
                skill_counts.update(job.required_skills)
            
            # Calculate growth rates
            trends = []
            for skill, count in skill_counts.most_common(limit):
                growth_rate = await self._calculate_skill_growth(
                    skill, days, role, location
                )
                
                trends.append({
                    "skill": skill,
                    "count": count,
                    "growth_rate": growth_rate,
                    "trend": "rising" if growth_rate > 10 else "stable"
                })
            
            return {
                "time_range": time_range,
                "role": role,
                "location": location,
                "trends": trends
            }
        
        finally:
            db.close()
    
    def _get_days_from_range(self, time_range: str) -> int:
        """
        Convert time range string to days
        """
        ranges = {
            "1m": 30,
            "3m": 90,
            "6m": 180,
            "1y": 365
        }
        return ranges.get(time_range, 90)
    
    async def _calculate_skill_growth(
        self,
        skill: str,
        days: int,
        role: Optional[str],
        location: Optional[str]
    ) -> float:
        """
        Calculate growth rate for a skill
        """
        db = get_db_session()
        
        try:
            now = datetime.now()
            mid_point = now - timedelta(days=days//2)
            start_date = now - timedelta(days=days)
            
            base_query = db.query(Job).filter(
                Job.required_skills.contains([skill])
            )
            
            if role:
                base_query = base_query.filter(Job.title.ilike(f"%{role}%"))
            if location:
                base_query = base_query.filter(Job.location.ilike(f"%{location}%"))
            
            recent_count = base_query.filter(
                Job.posted_date >= mid_point
            ).count()
            
            older_count = base_query.filter(
                and_(Job.posted_date >= start_date, Job.posted_date < mid_point)
            ).count()
            
            if older_count == 0:
                return 100.0 if recent_count > 0 else 0.0
            
            growth_rate = ((recent_count - older_count) / older_count) * 100
            return round(growth_rate, 2)
        
        finally:
            db.close()
    
    async def forecast_demand(self, months: int, skills: Optional[List[str]] = None) -> Dict:
        """
        Forecast skill demand using time-series model
        """
        if skills:
            forecasts = {}
            for skill in skills:
                forecast = await self.forecaster.predict(skill, months)
                forecasts[skill] = forecast
        else:
            # Forecast top 20 skills
            trending = await self.get_trending_skills("6m", limit=20)
            forecasts = {}
            for trend in trending["trends"]:
                skill = trend["skill"]
                forecast = await self.forecaster.predict(skill, months)
                forecasts[skill] = forecast
        
        return {
            "forecast_months": months,
            "forecasts": forecasts,
            "generated_at": datetime.now().isoformat()
        }
    
    async def get_salary_trends(
        self,
        role: str,
        time_range: str,
        location: Optional[str] = None
    ) -> Dict:
        """
        Get salary trends over time for a role
        """
        db = get_db_session()
        
        try:
            days = self._get_days_from_range(time_range)
            start_date = datetime.now() - timedelta(days=days)
            
            query = db.query(Job).filter(
                Job.title.ilike(f"%{role}%"),
                Job.posted_date >= start_date,
                Job.salary.isnot(None)
            )
            
            if location:
                query = query.filter(Job.location.ilike(f"%{location}%"))
            
            jobs = query.order_by(Job.posted_date).all()
            
            if not jobs:
                return {"error": "No data found"}
            
            # Group by month
            monthly_data = {}
            for job in jobs:
                month_key = job.posted_date.strftime("%Y-%m")
                if month_key not in monthly_data:
                    monthly_data[month_key] = []
                monthly_data[month_key].append(job.salary)
            
            # Calculate statistics
            trends = []
            for month, salaries in sorted(monthly_data.items()):
                trends.append({
                    "month": month,
                    "avg_salary": np.mean(salaries),
                    "median_salary": np.median(salaries),
                    "sample_size": len(salaries)
                })
            
            # Calculate overall trend
            if len(trends) >= 2:
                first_avg = trends[0]["avg_salary"]
                last_avg = trends[-1]["avg_salary"]
                overall_change = ((last_avg - first_avg) / first_avg) * 100
            else:
                overall_change = 0
            
            return {
                "role": role,
                "location": location,
                "time_range": time_range,
                "trends": trends,
                "overall_change_pct": round(overall_change, 2)
            }
        
        finally:
            db.close()