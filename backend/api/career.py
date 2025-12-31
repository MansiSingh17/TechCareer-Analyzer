from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from backend.services.career_service import CareerService
from backend.utils.logger import setup_logger

router = APIRouter()
logger = setup_logger(__name__)
career_service = CareerService()

class SkillProfile(BaseModel):
    skills: List[str]
    experience_years: float
    current_role: Optional[str] = None
    education: Optional[str] = None
    location: Optional[str] = None

class CareerPathResponse(BaseModel):
    recommended_roles: List[Dict[str, Any]]
    skill_gaps: List[Dict[str, Any]]
    salary_range: Dict[str, float]
    growth_trajectory: List[Dict[str, Any]]
    learning_path: List[str]

@router.post("/analyze", response_model=CareerPathResponse)
async def analyze_career_path(profile: SkillProfile):
    """
    Analyze career path based on current skills and experience
    """
    try:
        logger.info(f"Analyzing career path for profile with {len(profile.skills)} skills")
        
        result = await career_service.analyze_career_path(
            skills=profile.skills,
            experience_years=profile.experience_years,
            current_role=profile.current_role,
            education=profile.education,
            location=profile.location
        )
        
        return result
    
    except Exception as e:
        logger.error(f"Error analyzing career path: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/compare-roles")
async def compare_roles(profile: SkillProfile, target_roles: List[str]):
    """
    Compare current profile against target roles
    """
    try:
        comparison = await career_service.compare_roles(
            profile=profile.dict(),
            target_roles=target_roles
        )
        return comparison
    
    except Exception as e:
        logger.error(f"Error comparing roles: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/role-requirements/{role_name}")
async def get_role_requirements(role_name: str):
    """
    Get typical requirements for a specific role
    """
    try:
        requirements = await career_service.get_role_requirements(role_name)
        return requirements
    
    except Exception as e:
        logger.error(f"Error fetching role requirements: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
