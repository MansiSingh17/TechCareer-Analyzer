#!/usr/bin/env python3
"""
Demo script to test all features
"""

import sys
import os
import asyncio

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.services.career_service import CareerService
from backend.services.salary_service import SalaryService
from backend.services.skills_service import SkillsService

async def demo_skill_extraction():
    print("\n" + "="*70)
    print("DEMO: SKILL EXTRACTION")
    print("="*70)
    
    skills_service = SkillsService()
    
    job_desc = """
    Looking for Senior Python Developer with 5+ years experience.
    Required: Python, React, AWS, Docker, PostgreSQL
    Nice to have: Kubernetes, Machine Learning
    """
    
    print("\nJob Description:")
    print(job_desc)
    
    skills = await skills_service.extract_skills(job_desc)
    print(f"\n✅ Extracted {len(skills)} skills:")
    for skill in skills:
        print(f"  • {skill}")

async def demo_salary_prediction():
    print("\n" + "="*70)
    print("DEMO: SALARY PREDICTION")
    print("="*70)
    
    salary_service = SalaryService()
    
    prediction = await salary_service.predict_salary(
        skills=["Python", "React", "AWS", "Docker"],
        experience_years=3,
        role="Software Engineer",
        location="Seattle"
    )
    
    print(f"\n💰 Predicted Salary: ${prediction['predicted_salary']:,.0f}")
    print(f"📈 Range: ${prediction['salary_range']['min']:,.0f} - ${prediction['salary_range']['max']:,.0f}")
    print(f"🎯 Confidence: {prediction['confidence_score']*100:.0f}%")

async def main():
    print("\n" + "="*70)
    print("TECHCAREER ANALYZER - DEMO")
    print("="*70)
    
    try:
        await demo_skill_extraction()
        await demo_salary_prediction()
    except Exception as e:
        print(f"\n⚠️  Error: {e}")
    
    print("\n" + "="*70)
    print("DEMO COMPLETE!")
    print("="*70)

if __name__ == "__main__":
    asyncio.run(main())
