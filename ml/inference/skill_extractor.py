

import re
from typing import List, Dict

class SkillExtractor:
    def __init__(self):
        self.skill_patterns = self._load_skill_patterns()
        self.soft_skill_keywords = self._load_soft_skills()
    
    def _load_skill_patterns(self) -> dict:
        return {
            "languages": r'\b(Python|Java|JavaScript|TypeScript|Go|Rust|C\+\+|C#|Ruby|PHP|Swift|Kotlin|Scala|Elixir|Haskell|R|MATLAB|Perl|Lua|Clojure|Groovy|VB\.NET|Objective-C)\b',
            "frameworks": r'\b(React|Angular|Vue|Django|Flask|FastAPI|Spring|Express|Rails|Nest\.?js|Next\.?js|Svelte|Ember|Backbone|Tornado|Pyramid|Bottle|Falcon|Quart|Starlette|ASP\.NET|Blazor|Xamarin|Flutter|SwiftUI)\b',
            "databases": r'\b(PostgreSQL|MySQL|MongoDB|Redis|Elasticsearch|SQLite|MariaDB|Oracle|SQLServer|Cassandra|HBase|DynamoDB|Firestore|CosmosDB|Neo4j|ArangoDB|CouchDB|Memcached|RethinkDB)\b',
            "cloud": r'\b(AWS|Azure|GCP|Google Cloud|DigitalOcean|Heroku|Firebase|Netlify|Vercel|IBM Cloud|Oracle Cloud|Alibaba Cloud|Docker|Kubernetes|OpenShift|ECS|Lambda|CloudFunctions|Serverless)\b',
            "ml": r'\b(Machine Learning|Deep Learning|TensorFlow|PyTorch|Keras|scikit-learn|XGBoost|LightGBM|CatBoost|OpenCV|NLP|Natural Language Processing|Computer Vision|BERT|GPT|Transformers|Hugging Face|Jupyter|Pandas|NumPy|SciPy|Matplotlib|Seaborn|Plotly)\b',
            "devops": r'\b(CI\/CD|Jenkins|GitLab CI|GitHub Actions|Travis CI|CircleCI|Terraform|Ansible|Puppet|Chef|Vagrant|Prometheus|Grafana|ELK|Splunk|DataDog|New Relic|Git|SVN)\b',
            "testing": r'\b(pytest|unittest|Jest|Mocha|Jasmine|RSpec|Selenium|Cypress|Playwright|LoadRunner|JMeter|Test|Automation|QA|BDD|TDD|Coverage|Mock)\b',
            "other_tech": r'\b(REST|GraphQL|gRPC|Microservices|API|WebSocket|OAuth|JWT|SSL|TLS|CORS|JSON|XML|Protocol Buffers|WebAssembly|Linux|Unix|Windows|macOS|Git|GitHub|GitLab|Bitbucket|Jira|Confluence|Slack|Agile|Scrum|Kanban)\b',
        }

    def _load_soft_skills(self) -> List[str]:
        return [
            # Communication & Interpersonal
            "communication", "active listening", "presentation", "public speaking", "writing",
            "storytelling", "clarity", "articulation", "negotiation", "persuasion",
            
            # Leadership & Management
            "leadership", "mentoring", "coaching", "delegation", "motivation",
            "team building", "performance management", "strategic planning", "vision",
            "decision making", "executive presence", "influence",
            
            # Teamwork & Collaboration
            "teamwork", "collaboration", "cooperation", "partnership", "cross-functional",
            "stakeholder management", "interpersonal skills", "empathy", "social skills",
            
            # Problem Solving & Critical Thinking
            "problem solving", "critical thinking", "analytical thinking", "analytical skills",
            "logical thinking", "reasoning", "debugging", "troubleshooting", "root cause analysis",
            "systems thinking", "strategic thinking", "creativity", "innovation",
            
            # Work Ethic & Attitude
            "reliability", "accountability", "ownership", "self-starter", "initiative",
            "proactive", "adaptability", "flexibility", "agility", "resilience",
            "persistence", "determination", "work ethic", "professionalism", "integrity",
            
            # Organization & Planning
            "time management", "organization", "planning", "prioritization", "multitasking",
            "project management", "attention to detail", "follow-through", "execution",
            
            # Learning & Development
            "learning", "continuous learning", "growth mindset", "curiosity", "intellectual ability",
            "adaptability", "quick learner", "self-directed learning", "knowledge sharing",
            
            # Conflict & Interpersonal Resolution
            "conflict resolution", "diplomatic", "mediation", "consensus building",
            "patience", "emotional intelligence", "self-awareness", "humility",
            
            # Additional Professional Skills
            "customer focus", "customer service", "customer empathy", "user-centric",
            "business acumen", "financial literacy", "data-driven", "quality focus",
            "customer satisfaction", "vendor management", "relationship building"
        ]
    
    async def load_model(self):
        print("Skill extractor initialized (rule-based with expanded skill detection)")
    
    async def extract(self, text: str) -> Dict[str, List[str]]:
        text = self._preprocess_text(text)
        technical = sorted(set(self._extract_with_rules(text)))
        soft = sorted(set(self._extract_soft_skills(text)))
        return {"technical": technical, "soft": soft}
    
    def _preprocess_text(self, text: str) -> str:
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def _extract_with_rules(self, text: str) -> List[str]:
        """Extract technical skills using regex patterns"""
        skills = []
        for category, pattern in self.skill_patterns.items():
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                skill = match.group(0)
                # Normalize variations (e.g., "Nest.js" → "NestJS")
                skill = self._normalize_skill_name(skill)
                skills.append(skill)
        return skills

    def _normalize_skill_name(self, skill: str) -> str:
        """Normalize skill names for consistency"""
        normalizations = {
            r'Nest\.?js': 'NestJS',
            r'Next\.?js': 'NextJS',
            r'Node\.?js': 'NodeJS',
            r'C\+\+': 'C++',
            r'\.NET': '.NET',
            r'ASP\.NET': 'ASP.NET',
            r'VB\.NET': 'VB.NET',
            r'CI\/?CD': 'CI/CD',
            r'REST API': 'REST API',
        }
        for pattern, replacement in normalizations.items():
            skill = re.sub(pattern, replacement, skill, flags=re.IGNORECASE)
        return skill.strip()

    def _extract_soft_skills(self, text: str) -> List[str]:
        """Extract soft skills with word boundary checking"""
        found = []
        lower_text = text.lower()
        
        for keyword in self.soft_skill_keywords:
            # Use word boundaries to match whole phrases, not partial matches
            pattern = r'\b' + re.escape(keyword) + r'\b'
            if re.search(pattern, lower_text, re.IGNORECASE):
                # Preserve original casing format
                found.append(keyword.replace(' ', ' ').title())
        
        return found