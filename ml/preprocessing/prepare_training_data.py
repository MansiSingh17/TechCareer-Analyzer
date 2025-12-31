#!/usr/bin/env python3
"""
Prepare training data from collected jobs
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pandas as pd
import numpy as np
from backend.utils.db import get_db
from backend.models.job import Job
from collections import Counter

def prepare_salary_training_data(output_path: str = "./data/processed/salary_data.csv"):
    """
    Prepare data for salary prediction model training
    """
    print("\n" + "="*70)
    print("📊 PREPARING SALARY TRAINING DATA")
    print("="*70)
    
    with get_db() as db:
        jobs = db.query(Job).filter(Job.salary.isnot(None)).all()
        
        if len(jobs) < 50:
            print(f"\n⚠️  Only {len(jobs)} jobs with salary data found!")
            print("Recommendation: Collect at least 200 jobs for good training")
            print("Run: python scripts/collect_jobs.py --save-db --pages 10")
            return
        
        print(f"✅ Found {len(jobs)} jobs with salary data")
        
        # Create training dataframe
        data = []
        for job in jobs:
            if not job.required_skills or len(job.required_skills) == 0:
                continue
            
            data.append({
                'role': job.title,
                'location': job.location,
                'experience_years': job.experience_required,
                'skills': ','.join(job.required_skills),  # Store as comma-separated
                'salary': job.salary,
                'company': job.company,
                'source': job.source
            })
        
        df = pd.DataFrame(data)
        
        # Data cleaning
        print("\n🧹 Cleaning data...")
        
        # Remove outliers (salaries outside 10th-90th percentile)
        lower = df['salary'].quantile(0.10)
        upper = df['salary'].quantile(0.90)
        df = df[(df['salary'] >= lower) & (df['salary'] <= upper)]
        
        print(f"   Removed outliers, kept {len(df)} jobs")
        
        # Remove rows with missing critical data
        df = df.dropna(subset=['role', 'experience_years', 'skills', 'salary'])
        
        print(f"   After removing nulls: {len(df)} jobs")
        
        # Save to CSV
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
        
        print(f"\n✅ Training data saved to: {output_path}")
        print(f"   Total samples: {len(df)}")
        print(f"   Salary range: ${df['salary'].min():,.0f} - ${df['salary'].max():,.0f}")
        print(f"   Avg salary: ${df['salary'].mean():,.0f}")
        print(f"   Unique roles: {df['role'].nunique()}")
        print(f"   Unique skills: {len(set(','.join(df['skills']).split(',')))} ")
        
        # Show sample
        print("\n📋 Sample Data (first 3 rows):")
        print(df[['role', 'experience_years', 'salary', 'location']].head(3).to_string())
        
        print("\n" + "="*70)
        
        return df

def prepare_skill_extraction_data(output_path: str = "./data/processed/skill_extraction_data.csv"):
    """
    Prepare data for skill extraction model (requires manual labeling)
    """
    print("\n" + "="*70)
    print("📊 PREPARING SKILL EXTRACTION DATA")
    print("="*70)
    
    with get_db() as db:
        jobs = db.query(Job).limit(100).all()
        
        data = []
        for job in jobs:
            if job.description and job.required_skills:
                # Create training example
                # In production, you'd manually label this
                data.append({
                    'text': job.description[:500],  # Truncate long descriptions
                    'skills': ','.join(job.required_skills)
                })
        
        df = pd.DataFrame(data)
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
        
        print(f"✅ Saved {len(df)} examples to: {output_path}")
        print("⚠️  Note: For BERT training, you need token-level labels")
        print("   This is a simplified version for demonstration")
        print("="*70)

def prepare_time_series_data(output_path: str = "./data/processed/skill_time_series.csv"):
    """
    Prepare time-series data for forecasting
    """
    print("\n" + "="*70)
    print("📊 PREPARING TIME-SERIES DATA")
    print("="*70)
    
    with get_db() as db:
        jobs = db.query(Job).all()
        
        # Group by date and skill
        data = []
        
        # Get all unique skills
        all_skills = set()
        for job in jobs:
            if job.required_skills:
                all_skills.update(job.required_skills)
        
        print(f"Found {len(all_skills)} unique skills")
        
        # For each skill, count occurrences by month
        from datetime import datetime, timedelta
        
        # Create monthly buckets for the last 12 months
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        
        current = start_date
        while current <= end_date:
            month_key = current.strftime("%Y-%m-01")
            month_end = current + timedelta(days=30)
            
            for skill in all_skills:
                # Count jobs with this skill in this month
                count = sum(1 for job in jobs 
                          if job.required_skills and skill in job.required_skills
                          and start_date <= job.posted_date <= month_end)
                
                if count > 0:
                    data.append({
                        'date': month_key,
                        'skill': skill,
                        'count': count
                    })
            
            current = month_end
        
        df = pd.DataFrame(data)
        
        if len(df) > 0:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            df.to_csv(output_path, index=False)
            print(f"✅ Saved time-series data to: {output_path}")
            print(f"   Total records: {len(df)}")
            print(f"   Skills tracked: {df['skill'].nunique()}")
            print(f"   Date range: {df['date'].min()} to {df['date'].max()}")
        else:
            print("⚠️  Not enough historical data for time-series")
        
        print("="*70)

def main():
    """Prepare all training datasets"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Prepare training data")
    parser.add_argument("--all", action="store_true", help="Prepare all datasets")
    parser.add_argument("--salary", action="store_true", help="Prepare salary data")
    parser.add_argument("--skills", action="store_true", help="Prepare skill extraction data")
    parser.add_argument("--timeseries", action="store_true", help="Prepare time-series data")
    
    args = parser.parse_args()
    
    if args.all or args.salary:
        prepare_salary_training_data()
    
    if args.all or args.skills:
        prepare_skill_extraction_data()
    
    if args.all or args.timeseries:
        prepare_time_series_data()
    
    if not any([args.all, args.salary, args.skills, args.timeseries]):
        print("Run with --all to prepare all datasets")
        print("Or use --salary, --skills, or --timeseries individually")

if __name__ == "__main__":
    main()
