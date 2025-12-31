import { Link } from 'react-router-dom'
import { ChartBarIcon, CurrencyDollarIcon, AcademicCapIcon, ArrowTrendingUpIcon } from '@heroicons/react/24/outline'

function Home() {
  return (
    <div className="space-y-12">
      {/* Hero Section */}
      <div className="text-center py-14 grid-fade">
        <div className="hero-kicker mx-auto mb-6 w-fit">
          Precision forecasts · Human-grade UX
        </div>
        <h1 className="text-5xl font-bold bg-gradient-to-r from-orange-400 via-amber-300 to-cyan-300 bg-clip-text text-transparent mb-4">
          TechCareer Analyzer
        </h1>
        <p className="text-xl text-slate-200 max-w-3xl mx-auto leading-relaxed">
          Market-native, ML-powered career intelligence using BERT, PyTorch, TensorFlow, and Prophet.
        </p>
        <p className="text-lg text-slate-400 mt-3 tracking-wide">
          Analyzing {1469} real roles from live market signals.
        </p>
      </div>

      {/* Feature Cards */}
      <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
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
  const colorClasses = {
    blue: 'from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700',
    purple: 'from-purple-500 to-purple-600 hover:from-purple-600 hover:to-purple-700',
    green: 'from-green-500 to-green-600 hover:from-green-600 hover:to-green-700',
    orange: 'from-orange-500 to-orange-600 hover:from-orange-600 hover:to-orange-700'
  }
  
  return (
    <Link to={link} className="group">
      <div className="card group-hover:scale-105 transition-transform">
        <div className={`w-16 h-16 rounded-lg bg-gradient-to-r ${colorClasses[color]} flex items-center justify-center text-white mb-4`}>
          {icon}
        </div>
        <h3 className="text-xl font-bold mb-2">{title}</h3>
        <p className="text-gray-600">{description}</p>
      </div>
    </Link>
  )
}

function StatCard({ number, label }) {
  return (
    <div>
      <div className="text-4xl font-bold text-blue-600">{number}</div>
      <div className="text-gray-600 mt-1">{label}</div>
    </div>
  )
}

export default Home
