import { useState } from 'react'
import axios from 'axios'

function SkillExtractor() {
  const [jobDescription, setJobDescription] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleExtract = async (e) => {
    e.preventDefault()
    setLoading(true)
    
    try {
      const response = await axios.post('http://localhost:8000/api/skills/extract', {
        description: jobDescription
      })
      
      setResult(response.data)
    } catch (error) {
      console.error('Error:', error)
      alert('Error extracting skills')
    }
    
    setLoading(false)
  }

  const sampleDescription = `We are seeking a Senior Full Stack Developer with 5+ years of experience.

Required Skills:
- Strong proficiency in Python and JavaScript
- Experience with React, Node.js, and Express
- Database knowledge (PostgreSQL, MongoDB)
- Cloud platforms (AWS, Docker, Kubernetes)
- RESTful API design and implementation

Nice to have:
- Machine Learning experience
- TypeScript
- GraphQL
- CI/CD pipelines`

  const loadSample = () => {
    setJobDescription(sampleDescription)
  }

  return (
    <div className="max-w-6xl mx-auto panel-grid">
      <div className="flex flex-col gap-2">
        <div className="hero-kicker w-fit">NLP extraction · Zero-shot ready</div>
        <h1 className="text-4xl font-bold text-slate-100">🧠 Skill Extractor</h1>
        <p className="section-subtext max-w-3xl">Paste any JD; we parse core technical signals with a transformer-backed extractor and surface them as crisp, animated chips.</p>
      </div>

      <div className="grid md:grid-cols-[6px,1fr,1fr] gap-6 items-start">
        <div className="accent-rail" aria-hidden="true"></div>

        {/* Input */}
        <div className="card">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-2xl font-bold text-slate-100">Job Description</h2>
            <button onClick={loadSample} className="text-sm font-semibold text-cyan-300 hover:text-white">
              Load Sample
            </button>
          </div>
          
          <form onSubmit={handleExtract} className="space-y-4">
            <div>
              <label className="label">Paste Job Description</label>
              <textarea
                className="textarea-glass"
                placeholder="Paste a job description here..."
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
                required
              />
            </div>

            <button type="submit" className="btn-primary w-full" disabled={loading}>
              {loading ? '🔍 Extracting...' : '🚀 Extract Skills'}
            </button>
          </form>
        </div>

        {/* Results */}
        <div className="card">
          <div className="section-heading">
            <span className="pill">Extracted</span>
            <span>Structured skills</span>
          </div>
          
          {result ? (
            <div className="space-y-6">
              <div className="text-center">
                <div className="text-6xl font-bold text-cyan-300 mb-2">
                  {result.counts?.total ?? 0}
                </div>
                <div className="text-slate-400">Skills identified</div>
                <div className="text-sm text-slate-500 mt-1">
                  {result.counts?.technical ?? 0} technical · {result.counts?.soft ?? 0} soft
                </div>
              </div>

              <div className="bg-[rgba(255,255,255,0.03)] border border-[rgba(255,255,255,0.08)] rounded-lg p-6 space-y-4">
                <div>
                  <h3 className="font-bold mb-2 text-lg text-slate-100">Technical Skills</h3>
                  <div className="flex flex-wrap gap-3">
                    {(result.technical_skills || []).map((skill) => (
                      <div key={skill} className="chip">
                        {skill}
                      </div>
                    ))}
                  </div>
                </div>

                <div className="divider-line"></div>

                <div>
                  <h3 className="font-bold mb-2 text-lg text-slate-100">Soft Skills</h3>
                  <div className="flex flex-wrap gap-3">
                    {(result.soft_skills || []).map((skill) => (
                      <div key={skill} className="chip">
                        {skill}
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              <div className="bg-[rgba(255,255,255,0.04)] border border-[rgba(255,255,255,0.08)] p-4 rounded">
                <h3 className="font-bold text-slate-100 mb-2">💡 How it works</h3>
                <p className="text-sm text-slate-300">
                  We parse the description, normalize entities, and rank signals. Technical skills use pattern matching; soft skills are keyword-based to surface collaboration and communication signals.
                </p>
              </div>
            </div>
          ) : (
            <div className="text-center text-slate-500 py-12">
              <AcademicCapIcon className="w-16 h-16 mx-auto mb-4 opacity-50" />
              <p>Paste a job description and extract skills</p>
              <p className="text-sm mt-2">Powered by BERT NLP model</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

function AcademicCapIcon({ className }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 14l9-5-9-5-9 5 9 5z" />
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z" />
    </svg>
  )
}

export default SkillExtractor
