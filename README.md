# Location: /techcareer-analyzer/README.md

# TechCareer Analyzer - ML Career Path Predictor

An intelligent career path analyzer that uses machine learning to predict optimal career trajectories, identify skill gaps, and forecast tech stack trends based on real-time job market data.

## Features

- **Job Data Collection**: Scrapes job postings from LinkedIn, Indeed, and Adzuna
- **Skill Extraction**: Uses BERT/transformer models to extract technical skills from job descriptions
- **Salary Prediction**: TensorFlow/PyTorch models predict salary ranges based on skills and experience
- **Trend Analysis**: Interactive visualizations showing tech stack trends and salary distributions
- **Skill Forecasting**: Time-series models predict which skills will be in demand 6-12 months ahead
- **Gap Analysis**: Identifies skill gaps between your profile and target roles

## Tech Stack

- **ML/DL**: PyTorch, TensorFlow, Transformers, Prophet
- **Data Processing**: pandas, NumPy, scikit-learn
- **NLP**: BERT, spaCy, NLTK
- **Visualization**: Matplotlib, Seaborn, Plotly
- **Backend**: FastAPI, SQLAlchemy, Redis
- **Database**: PostgreSQL

## Quick Start
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/techcareer-analyzer.git
cd techcareer-analyzer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your API keys

# Initialize database
python scripts/init_db.py --seed

# Start API server
uvicorn backend.main:app --reload
```

Visit http://localhost:8000/docs for API documentation.

## Project Structure
```
techcareer-analyzer/
├── backend/           # FastAPI backend
│   ├── api/          # API endpoints
│   ├── models/       # Database models
│   ├── services/     # Business logic
│   └── utils/        # Helper functions
├── ml/               # Machine learning
│   ├── training/     # Model training
│   ├── inference/    # Model inference
│   └── preprocessing/# Data preprocessing
├── data/             # Data storage
├── scripts/          # Utility scripts
└── tests/           # Unit tests
```

