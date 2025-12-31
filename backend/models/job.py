

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, unique=True, index=True)
    title = Column(String, index=True)
    company = Column(String, index=True)
    location = Column(String, index=True)
    description = Column(Text)
    required_skills = Column(JSON)  # store list of skills as JSON for SQLite compatibility
    preferred_skills = Column(JSON, nullable=True)
    experience_required = Column(Float)
    salary = Column(Float, nullable=True)
    salary_min = Column(Float, nullable=True)
    salary_max = Column(Float, nullable=True)
    employment_type = Column(String)
    remote_allowed = Column(String)
    posted_date = Column(DateTime, default=datetime.utcnow)
    source = Column(String)
    url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Job(title='{self.title}', company='{self.company}')>"

class UserProfile(Base):
    __tablename__ = "user_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    current_role = Column(String)
    experience_years = Column(Float)
    skills = Column(JSON)
    education = Column(String)
    location = Column(String)
    target_roles = Column(JSON)
    salary_expectation = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class SkillTrend(Base):
    __tablename__ = "skill_trends"
    
    id = Column(Integer, primary_key=True, index=True)
    skill = Column(String, index=True)
    count = Column(Integer)
    growth_rate = Column(Float)
    date = Column(DateTime, default=datetime.utcnow)
    role = Column(String, nullable=True)
    location = Column(String, nullable=True)

class SalaryData(Base):
    __tablename__ = "salary_data"
    
    id = Column(Integer, primary_key=True, index=True)
    role = Column(String, index=True)
    location = Column(String, index=True)
    experience_years = Column(Float)
    skills = Column(JSON)
    salary = Column(Float)
    company_size = Column(String, nullable=True)
    education = Column(String, nullable=True)
    date_reported = Column(DateTime, default=datetime.utcnow)