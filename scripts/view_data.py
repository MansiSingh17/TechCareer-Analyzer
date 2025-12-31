#!/usr/bin/env python3
"""
View collected job data
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.utils.db import get_db
from backend.models.job import Job
from collections import Counter
import numpy as np

def view_database_stats():
    """View database statistics"""
    with get_db() as db:
        total_jobs = db.query(Job).count()
        
        print("\n" + "=" * 70)
        print("📊 DATABASE STATISTICS")
        print("=" * 70)
        print(f"Total Jobs: {total_jobs}")
        
        if total_jobs == 0:
            print("\n⚠️  No jobs in database yet!")
            print("Run: python scripts/collect_jobs.py --save-db")
            return
        
        # Get all jobs
        jobs = db.query(Job).all()
        
        # Count by source
        sources = Counter([j.source for j in jobs])
        print("\n📈 By Source:")
        for source, count in sources.items():
            print(f"   {source:15} {count} jobs")
        
        # Top companies
        companies = Counter([j.company for j in jobs if j.company])
        print("\n🏢 Top Companies:")
        for company, count in companies.most_common(10):
            print(f"   {company:30} {count} jobs")
        
        # Top skills
        all_skills = []
        for job in jobs:
            if job.required_skills:
                all_skills.extend(job.required_skills)
        
        if all_skills:
            skill_counts = Counter(all_skills)
            print("\n🎯 Top 15 Skills:")
            for i, (skill, count) in enumerate(skill_counts.most_common(15), 1):
                pct = (count / total_jobs) * 100
                print(f"   {i:2}. {skill:20} {count:3} jobs ({pct:.1f}%)")
        
        # Salary statistics
        salaries = [j.salary for j in jobs if j.salary]
        if salaries:
            print(f"\n💰 Salary Statistics ({len(salaries)} jobs with salary data):")
            print(f"   Min:    ${min(salaries):>12,.0f}")
            print(f"   25th:   ${np.percentile(salaries, 25):>12,.0f}")
            print(f"   Median: ${np.median(salaries):>12,.0f}")
            print(f"   Mean:   ${np.mean(salaries):>12,.0f}")
            print(f"   75th:   ${np.percentile(salaries, 75):>12,.0f}")
            print(f"   Max:    ${max(salaries):>12,.0f}")
        
        # Experience distribution
        exp_levels = [j.experience_required for j in jobs]
        print(f"\n📚 Experience Required:")
        print(f"   Min:    {min(exp_levels):.1f} years")
        print(f"   Mean:   {np.mean(exp_levels):.1f} years")
        print(f"   Median: {np.median(exp_levels):.1f} years")
        print(f"   Max:    {max(exp_levels):.1f} years")
        
        # Top locations
        locations = Counter([j.location for j in jobs if j.location])
        print("\n📍 Top Locations:")
        for location, count in locations.most_common(10):
            print(f"   {location:30} {count} jobs")
        
        print("\n" + "=" * 70)

if __name__ == "__main__":
    view_database_stats()
