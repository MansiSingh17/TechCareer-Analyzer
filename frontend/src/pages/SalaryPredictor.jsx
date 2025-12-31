import { useState } from 'react'
import axios from 'axios'

function SalaryPredictor() {
  const [formData, setFormData] = useState({
    skills: '',
    experience_years: '',
    role: 'Software Engineer',
    location: 'Seattle'
  })
  
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    
    try {
      const response = await axios.post('http://localhost:8000/api/salary/predict', {
        skills: formData.skills.split(',').map(s => s.trim()),
        experience_years: parseFloat(formData.experience_years),
        role: formData.role,
        location: formData.location
      })
      
      setResult(response.data)
    } catch (error) {
      console.error('Error:', error)
      alert('Error predicting salary. Check console.')
    }
    
    setLoading(false)
  }

  return (
    <div className="max-w-5xl mx-auto panel-grid">
      <div>
        <div className="hero-kicker w-fit">Comp intelligence · Live market</div>
        <h1 className="text-4xl font-bold text-slate-100 mt-3">💰 Salary Predictor</h1>
        <p className="section-subtext max-w-3xl">Signal-driven predictions with calibrated confidence. Tune role, location, and skill mix to see market-aligned pay bands.</p>
      </div>

      <div className="grid md:grid-cols-2 gap-8 items-start">
        {/* Input Form */}
        <div className="card">
          <div className="section-heading">
            <span className="pill">Profile</span>
            <span>Your inputs</span>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="label">Skills (comma separated)</label>
              <input
                type="text"
                className="input-field"
                placeholder="Python, React, AWS, Docker"
                value={formData.skills}
                onChange={(e) => setFormData({...formData, skills: e.target.value})}
                required
              />
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="label">Years of Experience</label>
                <input
                  type="number"
                  step="0.5"
                  className="input-field"
                  placeholder="3"
                  value={formData.experience_years}
                  onChange={(e) => setFormData({...formData, experience_years: e.target.value})}
                  required
                />
              </div>

              <div>
                <label className="label">Location</label>
                <select
                  className="input-field"
                  value={formData.location}
                  onChange={(e) => setFormData({...formData, location: e.target.value})}
                >
                  <option>Seattle</option>
                  <option>San Francisco</option>
                  <option>New York</option>
                  <option>Austin</option>
                  <option>Remote</option>
                  <option>Boston</option>
                  <option>Denver</option>
                </select>
              </div>
            </div>

            <div>
              <label className="label">Target Role</label>
              <select
                className="input-field"
                value={formData.role}
                onChange={(e) => setFormData({...formData, role: e.target.value})}
              >
                <option>Software Engineer</option>
                <option>Senior Software Engineer</option>
                <option>Frontend Developer</option>
                <option>Backend Developer</option>
                <option>Full Stack Developer</option>
                <option>Data Scientist</option>
                <option>Machine Learning Engineer</option>
                <option>DevOps Engineer</option>
              </select>
            </div>

            <button type="submit" className="btn-primary w-full" disabled={loading}>
              {loading ? '🔮 Predicting...' : '🚀 Predict Salary'}
            </button>
          </form>
        </div>

        {/* Results */}
        <div className="card">
          <div className="section-heading">
            <span className="pill">Forecast</span>
            <span>Market-calibrated</span>
          </div>
          
          {result ? (
            <div className="space-y-6">
              <div className="flex items-start justify-between gap-4">
                <div>
                  <div className="text-sm uppercase tracking-[0.2em] text-slate-400">Predicted</div>
                  <div className="text-5xl font-bold text-orange-300">
                    ${result.predicted_salary.toLocaleString()}
                  </div>
                  <div className="text-slate-400 mt-1">Annual salary</div>
                </div>
                <div className="metric-badge">Confidence {(result.confidence_score * 100).toFixed(0)}%</div>
              </div>

              <div className="divider-line"></div>

              <div className="grid grid-cols-2 gap-4">
                <div className="card bg-transparent border-dashed border-[rgba(255,255,255,0.2)]">
                  <div className="text-slate-400 text-sm">Range</div>
                  <div className="text-xl font-semibold text-slate-100">${result.salary_range.min.toLocaleString()} - ${result.salary_range.max.toLocaleString()}</div>
                </div>
                <div className="card bg-transparent border-dashed border-[rgba(255,255,255,0.2)]">
                  <div className="text-slate-400 text-sm">Market Percentile</div>
                  <div className="text-xl font-semibold text-slate-100">{result.market_percentile.toFixed(0)}th</div>
                </div>
              </div>

              <div>
                <h3 className="text-slate-100 font-semibold mb-3">Salary Factors</h3>
                <div className="space-y-3">
                  {Object.entries(result.factors).map(([factor, value]) => (
                    <div key={factor} className="flex items-center gap-3">
                      <div className="w-40 capitalize text-sm text-slate-300">{factor.replace('_', ' ')}</div>
                      <div className="flex-1 bg-[rgba(255,255,255,0.07)] rounded-full h-3">
                        <div 
                          className="bg-gradient-to-r from-orange-400 to-cyan-400 h-3 rounded-full"
                          style={{ width: `${value}%` }}
                        ></div>
                      </div>
                      <div className="w-12 text-right text-sm font-semibold text-slate-200">{value.toFixed(0)}%</div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ) : (
            <div className="text-center text-slate-500 py-12">
              <CurrencyDollarIcon className="w-16 h-16 mx-auto mb-4 opacity-50" />
              <p>Enter your profile details and click predict</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

function CurrencyDollarIcon({ className }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
  )
}

export default SalaryPredictor
