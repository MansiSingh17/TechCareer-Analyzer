

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from backend.services.skills_service import SkillsService
from backend.utils.logger import setup_logger

router = APIRouter()
logger = setup_logger(__name__)
skills_service = SkillsService()

class SkillGapRequest(BaseModel):
    current_skills: List[str]
    target_role: str
    experience_years: float

class JobDescriptionRequest(BaseModel):
    description: str

@router.post("/extract")
async def extract_skills(request: JobDescriptionRequest):
    """
    Extract skills from job description using NLP
    """
    try:
        logger.info("Extracting skills from job description")
        
        data = await skills_service.extract_skills(request.description)
        return data
    
    except Exception as e:
        logger.error(f"Error extracting skills: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/gap-analysis")
async def analyze_skill_gap(request: SkillGapRequest):
    """
    Analyze skill gaps between current skills and target role
    """
    try:
        logger.info(f"Analyzing skill gap for {request.target_role}")
        
        analysis = await skills_service.analyze_gap(
            current_skills=request.current_skills,
            target_role=request.target_role,
            experience_years=request.experience_years
        )
        return analysis
    
    except Exception as e:
        logger.error(f"Error analyzing skill gap: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/learning-path")
async def generate_learning_path(request: SkillGapRequest):
    """
    Generate a learning path to bridge skill gaps
    """
    try:
        path = await skills_service.generate_learning_path(
            current_skills=request.current_skills,
            target_role=request.target_role,
            experience_years=request.experience_years
        )
        return path
    
    except Exception as e:
        logger.error(f"Error generating learning path: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))