import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import Home from './pages/Home'
import SalaryPredictor from './pages/SalaryPredictor'
import CareerAnalyzer from './pages/CareerAnalyzer'
import SkillExtractor from './pages/SkillExtractor'
import TrendsDashboard from './pages/TrendsDashboard'

function App() {
  return (
    <Router>
      <div className="app-shell">
        {/* Navigation */}
        <nav className="nav-surface sticky top-0 z-30">
          <div className="max-w-7xl mx-auto px-6 py-3 flex items-center justify-between gap-6">
            <Link to="/" className="brand-mark">
              <span className="text-sm uppercase tracking-[0.2em] text-slate-100">TechCareer</span>
              <span className="text-lg">Analyzer</span>
            </Link>

            <div className="flex items-center gap-2">
              <Link to="/" className="nav-link">Home</Link>
              <Link to="/salary" className="nav-link">Salary Predictor</Link>
              <Link to="/career" className="nav-link">Career Path</Link>
              <Link to="/skills" className="nav-link">Skill Extractor</Link>
              <Link to="/trends" className="nav-link">Trends</Link>
            </div>

            <div className="flex items-center gap-3" />
          </div>
        </nav>

        {/* Main Content */}
        <main className="max-w-7xl mx-auto px-6 lg:px-8 py-10">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/salary" element={<SalaryPredictor />} />
            <Route path="/career" element={<CareerAnalyzer />} />
            <Route path="/skills" element={<SkillExtractor />} />
            <Route path="/trends" element={<TrendsDashboard />} />
          </Routes>
        </main>

        {/* Footer */}
        <footer className="px-6 pb-10 pt-6">
          <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between text-sm text-gray-400 gap-3">
            <div>TechCareer Analyzer — ML-powered market intelligence</div>
            <div className="pill">Built with React · FastAPI · PyTorch · TensorFlow · Prophet</div>
          </div>
        </footer>
      </div>
    </Router>
  )
}

export default App
