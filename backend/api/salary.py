

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from backend.services.salary_service import SalaryService
from backend.utils.logger import setup_logger

router = APIRouter()
logger = setup_logger(__name__)
salary_service = SalaryService()

class SalaryPredictionRequest(BaseModel):
    skills: List[str]
    experience_years: float
    role: str
    location: str
    company_size: Optional[str] = None
    education: Optional[str] = None

class SalaryPredictionResponse(BaseModel):
    predicted_salary: float
    salary_range: Dict[str, float]
    confidence_score: float
    market_percentile: float
    factors: Dict[str, float]

@router.post("/predict", response_model=SalaryPredictionResponse)
async def predict_salary(request: SalaryPredictionRequest):
    """
    Predict salary based on skills, experience, and location
    """
    try:
        logger.info(f"Predicting salary for {request.role} with {request.experience_years} years")
        
        prediction = await salary_service.predict_salary(
            skills=request.skills,
            experience_years=request.experience_years,
            role=request.role,
            location=request.location,
            company_size=request.company_size,
            education=request.education
        )
        
        return prediction
    
    except Exception as e:
        logger.error(f"Error predicting salary: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/range/{role}")
async def get_salary_range(role: str, location: Optional[str] = None):
    """
    Get salary range for a specific role
    """
    try:
        salary_range = await salary_service.get_salary_range(
            role=role,
            location=location
        )
        return salary_range
    
    except Exception as e:
        logger.error(f"Error fetching salary range: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/compare-locations")
async def compare_salary_by_location(
    role: str,
    locations: List[str],
    experience_years: float
):
    """
    Compare salaries across different locations
    """
    try:
        comparison = await salary_service.compare_locations(
            role=role,
            locations=locations,
            experience_years=experience_years
        )
        return comparison
    
    except Exception as e:
        logger.error(f"Error comparing salaries: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/negotiation-insights")
async def get_negotiation_insights(request: SalaryPredictionRequest):
    """
    Get insights for salary negotiation
    """
    try:
        insights = await salary_service.get_negotiation_insights(
            skills=request.skills,
            experience_years=request.experience_years,
            role=request.role,
            location=request.location
        )
        return insights
    
    except Exception as e:
        logger.error(f"Error generating negotiation insights: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))