import { Link } from 'react-router-dom'
import { ChartBarIcon, CurrencyDollarIcon, AcademicCapIcon, ArrowTrendingUpIcon } from '@heroicons/react/24/outline'

function Home() {
  return (
    <div className="space-y-12">
      {/* Hero Section */}
      <div className="text-center py-20 grid-fade">
        <div className="hero-kicker mx-auto mb-6 w-fit">
          ✨ Precision forecasts · Human-grade UX
        </div>
        <h1 className="hero-title mx-auto mb-6">
          TechCareer Analyzer
        </h1>
        <p className="hero-description mx-auto mb-3 max-w-2xl">
          Market-native, ML-powered career intelligence using BERT, PyTorch, TensorFlow, and Prophet.
        </p>
        <p className="hero-subtext">
          Analyzing <span className="font-bold">1,469+</span> real roles from live market signals
        </p>
      </div>

      {/* Feature Cards Grid */}
      <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
        <FeatureCard
          icon={<CurrencyDollarIcon className="w-8 h-8" />}
          title="Salary Predictor"
          description="Neural network predicts your salary based on skills & experience"
          link="/salary"
          color="blue"
        />
        
        <FeatureCard
          icon={<ChartBarIcon className="w-8 h-8" />}
          title="Career Path"
          description="Analyze career trajectory and get role recommendations"
          link="/career"
          color="purple"
        />
        
        <FeatureCard
          icon={<AcademicCapIcon className="w-8 h-8" />}
          title="Skill Extractor"
          description="BERT-powered NLP extracts skills from job descriptions"
          link="/skills"
          color="green"
        />
        
        <FeatureCard
          icon={<ArrowTrendingUpIcon className="w-8 h-8" />}
          title="Market Trends"
          description="Prophet forecasts which skills will be hot in 6-12 months"
          link="/trends"
          color="orange"
        />
      </div>

      {/* Stats Section */}
      <div className="card mt-4 bg-[rgba(255,255,255,0.02)] border border-[rgba(255,255,255,0.08)] grid md:grid-cols-4 gap-6 text-center">
        <StatCard number="1,469" label="Real Jobs Analyzed" />
        <StatCard number="3" label="ML Models" />
        <StatCard number="14" label="API Endpoints" />
        <StatCard number="87%" label="Model Accuracy" />
      </div>

      {/* Tech Stack removed per request */}
    </div>
  )
}

function FeatureCard({ icon, title, description, link, color }) {
  return (
    <Link to={link} className="feature-card group">
      <div className="feature-card-inner">
        <div className={`feature-icon ${color}`}>
          {icon}
        </div>
        <h3 className="feature-title">{title}</h3>
        <p className="feature-description">{description}</p>
        <div className="mt-4 pt-4 border-t border-[rgba(255,255,255,0.08)] text-xs font-semibold text-cyan-400 group-hover:text-cyan-300 transition-colors">
          Explore →
        </div>
      </div>
    </Link>
  )
}

function StatCard({ number, label }) {
  return (
    <div className="stat-card">
      <div className="stat-number">{number}</div>
      <div className="stat-label">{label}</div>
    </div>
  )
}

export default Home
