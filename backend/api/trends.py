from fastapi import APIRouter, HTTPException, Query, Path
from typing import List, Optional
from backend.services.trends_service import TrendsService
from backend.utils.logger import setup_logger

router = APIRouter()
logger = setup_logger(__name__)
trends_service = TrendsService()

@router.get("/skills")
async def get_trending_skills(
    time_range: str = Query("3m", regex="^(1m|3m|6m|1y)$"),
    role: Optional[str] = None,
    location: Optional[str] = None,
    limit: int = 20
):
    """
    Get trending skills in the job market
    """
    try:
        trends = await trends_service.get_trending_skills(
            time_range=time_range,
            role=role,
            location=location,
            limit=limit
        )
        return trends
    
    except Exception as e:
        logger.error(f"Error fetching trending skills: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/forecast/{months}")
async def forecast_skill_demand(
    months: int = Path(..., ge=1, le=24),
    skills: Optional[List[str]] = Query(None)
):
    """
    Forecast skill demand for the next N months
    """
    try:
        logger.info(f"Forecasting skill demand for {months} months")
        
        forecast = await trends_service.forecast_demand(
            months=months,
            skills=skills
        )
        return forecast
    
    except Exception as e:
        logger.error(f"Error forecasting demand: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/salary-trends/{role}")
async def get_salary_trends(
    role: str = Path(...),
    time_range: str = Query("1y"),
    location: Optional[str] = None
):
    """
    Get salary trends over time for a role
    """
    try:
        trends = await trends_service.get_salary_trends(
            role=role,
            time_range=time_range,
            location=location
        )
        return trends
    
    except Exception as e:
        logger.error(f"Error fetching salary trends: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/emerging-roles")
async def get_emerging_roles(limit: int = Query(10, ge=1, le=50)):
    """
    Get emerging job roles
    """
    try:
        return {
            "emerging_roles": [],
            "message": "Feature coming soon - collect more data first"
        }
    except Exception as e:
        logger.error(f"Error fetching emerging roles: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
