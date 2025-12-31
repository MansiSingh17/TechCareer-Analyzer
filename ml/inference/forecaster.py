

import numpy as np
from typing import Dict
from datetime import datetime, timedelta

class SkillForecaster:
    def __init__(self):
        self.skill_growth_patterns = {
            "Machine Learning": {"base": 100, "growth_rate": 0.15},
            "Kubernetes": {"base": 80, "growth_rate": 0.20},
            "React": {"base": 120, "growth_rate": 0.10},
            "Python": {"base": 150, "growth_rate": 0.08},
        }
    
    async def load_models(self):
        print("Forecaster initialized")
    
    async def predict(self, skill: str, months: int) -> Dict:
        pattern = self.skill_growth_patterns.get(
            skill,
            {"base": 100, "growth_rate": 0.10}
        )
        
        forecasts = []
        current_date = datetime.now()
        
        for month in range(1, months + 1):
            trend = pattern["base"] * ((1 + pattern["growth_rate"]) ** (month / 12))
            predicted_demand = trend
            
            forecast_date = current_date + timedelta(days=30 * month)
            
            forecasts.append({
                "date": forecast_date.strftime("%Y-%m"),
                "month": month,
                "predicted_demand": round(predicted_demand, 2),
                "growth_rate_pct": round(pattern["growth_rate"] * 100, 1)
            })
        
        total_growth = ((forecasts[-1]["predicted_demand"] - pattern["base"]) / pattern["base"]) * 100
        
        return {
            "skill": skill,
            "forecast_horizon_months": months,
            "forecasts": forecasts,
            "summary": {
                "total_growth_pct": round(total_growth, 2),
                "trend": "growing" if pattern["growth_rate"] > 0.10 else "stable"
            }
        }