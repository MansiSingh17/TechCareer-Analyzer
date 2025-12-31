import { useState } from 'react'
import axios from 'axios'

function CareerAnalyzer() {
  const [skills, setSkills] = useState('')
  const [experience, setExperience] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleAnalyze = async (e) => {
    e.preventDefault()
    setLoading(true)
    
    try {
      const response = await axios.post('http://localhost:8000/api/career/analyze', {
        skills: skills.split(',').map(s => s.trim()),
        experience_years: parseFloat(experience)
      })
      
      setResult(response.data)
    } catch (error) {
      console.error('Error:', error)
      alert('Error analyzing career path')
    }
    
    setLoading(false)
  }

  return (
    <div className="max-w-6xl mx-auto panel-grid">
      <div>
        <div className="hero-kicker w-fit">Paths, gaps, trajectories</div>
        <h1 className="text-4xl font-bold text-slate-100 mt-3">📊 Career Path Analyzer</h1>
        <p className="section-subtext max-w-3xl">Map your current skills to target roles, reveal gaps, and see a three-year growth trajectory with salary expectations.</p>
      </div>

      {/* Input Form */}
      <div className="card">
        <form onSubmit={handleAnalyze} className="grid md:grid-cols-[2fr,1fr,auto] gap-4 items-end">
          <div className="flex-1">
            <label className="label">Your Skills (comma separated)</label>
            <input
              type="text"
              className="input-field"
              placeholder="Python, JavaScript, React, PostgreSQL"
              value={skills}
              onChange={(e) => setSkills(e.target.value)}
              required
            />
          </div>
          
          <div className="w-full">
            <label className="label">Years of Experience</label>
            <input
              type="number"
              step="0.5"
              className="input-field"
              placeholder="3"
              value={experience}
              onChange={(e) => setExperience(e.target.value)}
              required
            />
          </div>
          
          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? 'Analyzing...' : 'Analyze Career'}
          </button>
        </form>
      </div>

      {/* Results */}
      {result && (
        <div className="panel-grid">
          {/* Recommended Roles */}
          <div className="card">
            <div className="section-heading">
              <span className="pill">Recommendations</span>
              <span>Top matches</span>
            </div>
            <div className="space-y-3">
              {result.recommended_roles.slice(0, 5).map((role, idx) => (
                <div key={idx} className="flex justify-between items-start p-4 rounded-lg bg-[rgba(255,255,255,0.05)] border border-[rgba(255,255,255,0.08)]">
                  <div>
                    <div className="text-sm text-slate-400">#{idx + 1}</div>
                    <h3 className="font-bold text-lg text-slate-100">{role.role}</h3>
                    <p className="text-sm text-slate-400">
                      Top Skills: {role.required_skills.slice(0, 5).join(', ')}
                    </p>
                  </div>
                  <div className="text-right">
                    <div className="text-2xl font-bold text-orange-300">{(role.match_score * 100).toFixed(0)}%</div>
                    <div className="text-sm text-slate-400">Match</div>
                    <div className="text-sm font-semibold mt-1 text-slate-200">${role.avg_salary.toLocaleString()}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Skill Gaps */}
          <div className="card">
            <div className="section-heading">
              <span className="pill">Gaps</span>
              <span>Close these</span>
            </div>
            <div className="grid md:grid-cols-2 gap-3">
              {result.skill_gaps.slice(0, 4).map((gap, idx) => (
                <div key={idx} className="p-4 rounded-lg bg-[rgba(255,255,255,0.04)] border border-[rgba(255,255,255,0.08)]">
                  <h3 className="font-bold mb-1 text-slate-100">{gap.role}</h3>
                  <div className="flex flex-wrap gap-2 mb-2">
                    {gap.missing_skills.map(skill => (
                      <span key={skill} className="px-3 py-1 pill text-slate-200 border-[rgba(255,255,255,0.2)] bg-[rgba(255,255,255,0.06)]">
                        {skill}
                      </span>
                    ))}
                  </div>
                  <div className="text-sm font-semibold text-orange-300">
                    {gap.priority.toUpperCase()} Priority
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Learning Path */}
          <div className="card">
            <div className="section-heading">
              <span className="pill">Path</span>
              <span>Actionable sequence</span>
            </div>
            <div className="flex flex-wrap gap-3">
              {result.learning_path.map((skill, idx) => (
                <div key={skill} className="px-4 py-2 bg-gradient-to-r from-orange-400 to-cyan-400 text-slate-900 rounded-lg font-semibold shadow-md">
                  {idx + 1}. {skill}
                </div>
              ))}
            </div>
          </div>

          {/* Growth Trajectory */}
          <div className="card">
            <div className="section-heading">
              <span className="pill">Trajectory</span>
              <span>3-year projection</span>
            </div>
            <div className="space-y-3">
              {result.growth_trajectory.map((milestone, idx) => (
                <div key={idx} className="flex items-center gap-4 p-4 bg-[rgba(255,255,255,0.04)] border border-[rgba(255,255,255,0.08)] rounded-lg">
                  <div className="w-16 h-16 rounded-full bg-gradient-to-br from-orange-400 to-cyan-400 text-slate-900 flex items-center justify-center font-bold text-xl">
                    {milestone.year === 0 ? 'Now' : `+${milestone.year}y`}
                  </div>
                  <div className="flex-1">
                    <div className="font-bold text-lg text-slate-100">{milestone.role}</div>
                    <div className="text-sm text-slate-400">{milestone.skills_count} skills</div>
                  </div>
                  <div className="text-right">
                    <div className="text-2xl font-bold text-orange-200">
                      ${milestone.estimated_salary.predicted.toLocaleString()}
                    </div>
                    <div className="text-xs text-slate-400">
                      ${milestone.estimated_salary.min.toLocaleString()} - ${milestone.estimated_salary.max.toLocaleString()}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default CareerAnalyzer
