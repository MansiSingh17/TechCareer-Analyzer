#!/usr/bin/env python3
"""
Collect job data from Adzuna API
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
import time
import pandas as pd
from typing import List, Dict, Optional
from datetime import datetime
from dotenv import load_dotenv
from backend.models.job import Job
from backend.utils.db import get_db
from ml.inference.skill_extractor import SkillExtractor

load_dotenv()

class JobCollector:
    def __init__(self):
        self.skill_extractor = SkillExtractor()
        self.collected_jobs = []
    
    def collect_from_adzuna(
        self,
        keywords: str,
        location: str,
        pages: int = 5,
        remote: bool = False,
    ) -> List[Dict]:
        """
        Collect jobs from Adzuna API
        """
        app_id = os.getenv("ADZUNA_APP_ID")
        api_key = os.getenv("ADZUNA_API_KEY")
        
        if not app_id or not api_key:
            print("=" * 70)
            print("⚠️  ADZUNA API CREDENTIALS NOT FOUND")
            print("=" * 70)
            print("\nTo collect real job data:")
            print("1. Get FREE API key at: https://developer.adzuna.com/")
            print("2. Add to .env file:")
            print("   ADZUNA_APP_ID=your_app_id")
            print("   ADZUNA_API_KEY=your_api_key")
            print("=" * 70)
            return []
        
        # Adzuna expects the page number in the path: /search/{page}
        base_url = "https://api.adzuna.com/v1/api/jobs/us/search"
        jobs = []
        
        print(f"\n🔍 Searching Adzuna: '{keywords}' in {location}")
        print("=" * 70)

        # Adzuna doesn't have a dedicated remote filter; add "remote" to the keywords if requested
        if remote:
            keywords = f"{keywords} remote"
            if location.lower() == "remote":
                location = ""  # blank location for broader remote search
        
        for page in range(1, pages + 1):
            try:
                params = {
                    "app_id": app_id,
                    "app_key": api_key,
                    "results_per_page": 50,
                    "what": keywords,
                    "where": location,
                }
                
                # Page number must be in the path for Adzuna API
                response = requests.get(f"{base_url}/{page}", params=params)
                
                try:
                    response.raise_for_status()
                except requests.HTTPError as http_err:
                    # Show server-provided error body to help diagnose issues (bad creds, params, etc.)
                    print(f"❌ Error fetching page {page}: {http_err}")
                    print(f"   Response body: {response.text[:500]}")
                    continue
                
                data = response.json()
                results = data.get("results", [])
                
                print(f"📄 Page {page}/{pages}: Found {len(results)} jobs")
                
                for job in results:
                    jobs.append({
                        "job_id": f"adzuna_{job.get('id', '')}",
                        "title": job.get("title", ""),
                        "company": job.get("company", {}).get("display_name", ""),
                        "location": job.get("location", {}).get("display_name", location),
                        "description": job.get("description", ""),
                        "salary": self._parse_salary(job.get("salary_min"), job.get("salary_max")),
                        "salary_min": job.get("salary_min"),
                        "salary_max": job.get("salary_max"),
                        "posted_date": datetime.now(),
                        "url": job.get("redirect_url", ""),
                        "source": "adzuna"
                    })
                
                time.sleep(1)  # Rate limiting
                
            except Exception as e:
                print(f"❌ Error fetching page {page}: {e}")
                continue
        
        print("=" * 70)
        print(f"✅ Collected {len(jobs)} jobs from Adzuna")
        return jobs
    
    def _parse_salary(self, salary_min: Optional[float], salary_max: Optional[float]) -> Optional[float]:
        """Parse salary from min/max values"""
        if salary_min and salary_max:
            return (salary_min + salary_max) / 2
        elif salary_min:
            return salary_min
        elif salary_max:
            return salary_max
        return None
    
    async def extract_skills_for_jobs(self, jobs: List[Dict]) -> List[Dict]:
        """Extract skills from job descriptions"""
        print("\n" + "=" * 70)
        print("🧠 EXTRACTING SKILLS FROM JOB DESCRIPTIONS")
        print("=" * 70)
        
        for i, job in enumerate(jobs, 1):
            if i % 10 == 0:
                print(f"📊 Processed {i}/{len(jobs)} jobs")
            
            try:
                skills = await self.skill_extractor.extract(job["description"])
                job["required_skills"] = skills
                job["preferred_skills"] = []
                
                # Estimate experience from description
                job["experience_required"] = self._estimate_experience(job["description"])
                
            except Exception as e:
                print(f"⚠️  Error extracting skills for job {job.get('title')}: {e}")
                job["required_skills"] = []
                job["preferred_skills"] = []
                job["experience_required"] = 0.0
        
        print(f"✅ Skills extracted for all {len(jobs)} jobs")
        return jobs
    
    def _estimate_experience(self, description: str) -> float:
        """Estimate required experience from description"""
        import re
        
        patterns = [
            r'(\d+)\+?\s*(?:to|-)\s*(\d+)\s*years?',
            r'(\d+)\+\s*years?',
            r'(\d+)\s*years?'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, description.lower())
            if matches:
                if isinstance(matches[0], tuple):
                    return float(matches[0][0])
                else:
                    return float(matches[0])
        
        # Default based on role level
        if any(word in description.lower() for word in ['senior', 'lead', 'staff']):
            return 5.0
        elif any(word in description.lower() for word in ['junior', 'entry']):
            return 0.0
        else:
            return 2.0
    
    def save_to_database(self, jobs: List[Dict]):
        """Save jobs to database"""
        print("\n" + "=" * 70)
        print("💾 SAVING TO DATABASE")
        print("=" * 70)
        
        saved = 0
        skipped = 0
        
        with get_db() as db:
            for job in jobs:
                try:
                    # Check if job already exists
                    existing = db.query(Job).filter(
                        Job.job_id == str(job["job_id"])
                    ).first()
                    
                    if existing:
                        skipped += 1
                        continue
                    
                    # Create new job record
                    new_job = Job(
                        job_id=str(job["job_id"]),
                        title=job["title"],
                        company=job["company"],
                        location=job["location"],
                        description=job["description"],
                        required_skills=job.get("required_skills", []),
                        preferred_skills=job.get("preferred_skills", []),
                        experience_required=job.get("experience_required", 0.0),
                        salary=job.get("salary"),
                        salary_min=job.get("salary_min"),
                        salary_max=job.get("salary_max"),
                        employment_type="full-time",
                        remote_allowed="unknown",
                        posted_date=job["posted_date"],
                        source=job["source"],
                        url=job["url"]
                    )
                    
                    db.add(new_job)
                    saved += 1
                    
                except Exception as e:
                    print(f"⚠️  Error saving job: {e}")
                    continue
        
        print(f"✅ Saved: {saved} new jobs")
        print(f"⏭️  Skipped: {skipped} duplicates")
        print("=" * 70)
    
    def save_to_csv(self, jobs: List[Dict], output_path: str):
        """Save jobs to CSV file"""
        df = pd.DataFrame(jobs)
        
        # Convert lists to strings for CSV
        if 'required_skills' in df.columns:
            df['required_skills'] = df['required_skills'].apply(
                lambda x: ','.join(x) if isinstance(x, list) else ''
            )
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
        
        print(f"\n✅ Data saved to: {output_path}")
    
    def print_summary(self, jobs: List[Dict]):
        """Print collection summary"""
        from collections import Counter
        
        print("\n" + "=" * 70)
        print("📊 COLLECTION SUMMARY")
        print("=" * 70)
        print(f"Total jobs collected: {len(jobs)}")
        print(f"Jobs with salaries: {sum(1 for j in jobs if j.get('salary'))}")
        print(f"Unique companies: {len(set(j['company'] for j in jobs if j.get('company')))}")
        
        # Most common skills
        all_skills = []
        for job in jobs:
            all_skills.extend(job.get('required_skills', []))
        
        if all_skills:
            skill_counts = Counter(all_skills)
            print("\n🔥 Top 10 Skills Found:")
            for i, (skill, count) in enumerate(skill_counts.most_common(10), 1):
                print(f"   {i}. {skill:20} ({count} jobs)")
        
        # Salary stats
        salaries = [j['salary'] for j in jobs if j.get('salary')]
        if salaries:
            import numpy as np
            print(f"\n💰 Salary Statistics:")
            print(f"   Min:    ${min(salaries):,.0f}")
            print(f"   Max:    ${max(salaries):,.0f}")
            print(f"   Mean:   ${np.mean(salaries):,.0f}")
            print(f"   Median: ${np.median(salaries):,.0f}")
        
        print("=" * 70)

async def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Collect job postings from Adzuna")
    parser.add_argument("--keywords", default="software engineer", help="Job search keywords")
    parser.add_argument("--location", default="Seattle", help="Job location")
    parser.add_argument("--pages", type=int, default=5, help="Number of pages to collect")
    parser.add_argument("--remote", action="store_true", help="Filter for remote jobs")
    parser.add_argument("--save-db", action="store_true", help="Save to database")
    parser.add_argument("--save-csv", type=str, help="Save to CSV file")
    
    args = parser.parse_args()
    
    print("\n" + "=" * 70)
    print("🚀 TECHCAREER ANALYZER - JOB DATA COLLECTION")
    print("=" * 70)
    print(f"Keywords: {args.keywords}")
    print(f"Location: {args.location}")
    print(f"Pages: {args.pages}")
    print("=" * 70)
    
    collector = JobCollector()
    
    # Collect jobs
    jobs = collector.collect_from_adzuna(
        keywords=args.keywords,
        location=args.location,
        pages=args.pages,
        remote=args.remote,
    )
    
    if not jobs:
        print("\n❌ No jobs collected! Check your API credentials.")
        return
    
    # Extract skills
    jobs = await collector.extract_skills_for_jobs(jobs)
    
    # Save data
    if args.save_db:
        collector.save_to_database(jobs)
    
    if args.save_csv:
        collector.save_to_csv(jobs, args.save_csv)
    
    # Print summary
    collector.print_summary(jobs)
    
    print("\n✅ DATA COLLECTION COMPLETE!")
    print("\nNext steps:")
    print("  1. Check data: python scripts/view_data.py")
    print("  2. Train models: python ml/training/train_salary_predictor.py")
    print("  3. Create visualizations: python scripts/visualize_trends.py")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
