#!/usr/bin/env python3
"""
Initialize the database with tables and sample data
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.utils.db import init_db, drop_db, get_db
from backend.models.job import Job, SkillTrend, SalaryData
from datetime import datetime, timedelta
import random

def seed_sample_data():
    """
    Seed database with sample data
    """
    print("Seeding database with sample data...")
    
    sample_skills = [
        "Python", "JavaScript", "React", "Node.js", "AWS",
        "Docker", "Kubernetes", "PostgreSQL", "MongoDB", "Machine Learning"
    ]
    
    sample_roles = [
        "Software Engineer",
        "Senior Software Engineer",
        "Frontend Developer",
        "Backend Developer",
        "Full Stack Developer",
        "Data Scientist",
        "DevOps Engineer"
    ]
    
    sample_companies = [
        "Tech Corp", "Innovation Labs", "Cloud Solutions", "Data Systems"
    ]
    
    sample_locations = [
        "Seattle, WA", "San Francisco, CA", "New York, NY", "Remote"
    ]
    
    with get_db() as db:
        # Create sample jobs
        for i in range(50):
            role = random.choice(sample_roles)
            num_skills = random.randint(5, 10)
            skills = random.sample(sample_skills, num_skills)
            
            job = Job(
                job_id=f"sample_{i}",
                title=role,
                company=random.choice(sample_companies),
                location=random.choice(sample_locations),
                description=f"Sample job for {role}",
                required_skills=skills,
                preferred_skills=random.sample(sample_skills, 2),
                experience_required=random.uniform(0, 10),
                salary=random.uniform(80000, 180000),
                salary_min=random.uniform(70000, 150000),
                salary_max=random.uniform(100000, 200000),
                employment_type="full-time",
                remote_allowed="hybrid",
                posted_date=datetime.now() - timedelta(days=random.randint(0, 90)),
                source="sample_data",
                url=f"https://example.com/jobs/{i}"
            )
            db.add(job)
        
        print("Sample data created!")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Initialize database")
    parser.add_argument("--drop", action="store_true", help="Drop existing tables")
    parser.add_argument("--seed", action="store_true", help="Seed with sample data")
    
    args = parser.parse_args()
    
    if args.drop:
        print("Dropping existing tables...")
        drop_db()
    
    print("Initializing database...")
    init_db()
    print("Database initialized successfully!")
    
    if args.seed:
        seed_sample_data()
        print("Database seeded successfully!")
    
    print("✓ All operations completed successfully!")

if __name__ == "__main__":
    main()
