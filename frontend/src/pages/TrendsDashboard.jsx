import { useState, useEffect } from 'react'
import axios from 'axios'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line } from 'recharts'

function TrendsDashboard() {
  const [trendingSkills, setTrendingSkills] = useState(null)
  const [forecast, setForecast] = useState(null)
  const [timeRange, setTimeRange] = useState('3m')
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    loadTrendingSkills()
  }, [timeRange])

  const loadTrendingSkills = async () => {
    setLoading(true)
    try {
      const response = await axios.get(`http://localhost:8000/api/trends/skills?time_range=${timeRange}&limit=15`)
      setTrendingSkills(response.data)
    } catch (error) {
      console.error('Error:', error)
    }
    setLoading(false)
  }

  const loadForecast = async () => {
    setLoading(true)
    try {
      const response = await axios.get('http://localhost:8000/api/trends/forecast/12')
      setForecast(response.data)
    } catch (error) {
      console.error('Error:', error)
    }
    setLoading(false)
  }

  const trimSkill = (name, max = 12) => name.length > max ? `${name.slice(0, max)}…` : name

  return (
    <div className="max-w-7xl mx-auto panel-grid">
      <div>
        <div className="hero-kicker w-fit">Signal-driven · Prophet forecasts</div>
        <h1 className="text-4xl font-bold text-slate-100 mt-3">📈 Market Trends</h1>
        <p className="section-subtext max-w-3xl">Track skill momentum across time ranges and peek 12 months ahead with a calibrated Prophet forecast.</p>
      </div>

      {/* Time Range Selector */}
      <div className="card">
        <div className="flex gap-4 items-center flex-wrap">
          <span className="pill">Time Range</span>
          <div className="flex gap-2">
            {['1m', '3m', '6m', '1y'].map(range => (
              <button
                key={range}
                onClick={() => setTimeRange(range)}
                className={`px-4 py-2 rounded-lg font-semibold transition-all border ${
                  timeRange === range
                    ? 'bg-[rgba(34,211,238,0.15)] text-white border-[rgba(34,211,238,0.5)]'
                    : 'bg-[rgba(255,255,255,0.04)] text-slate-200 border-[rgba(255,255,255,0.08)] hover:border-[rgba(34,211,238,0.3)]'
                }`}
              >
                {range.toUpperCase()}
              </button>
            ))}
          </div>
          
          <button onClick={loadForecast} className="btn-primary ml-auto">
            🔮 Load 12-Month Forecast
          </button>
        </div>
      </div>

      {/* Trending Skills */}
      {trendingSkills && (
        <div className="card">
          <div className="section-heading">
            <span className="pill">Trending</span>
            <span>Top skills ({timeRange.toUpperCase()})</span>
          </div>
          
          <div className="grid md:grid-cols-2 gap-6">
            {/* Bar Chart */}
            <div className="card bg-[rgba(255,255,255,0.02)] border-dashed border-[rgba(255,255,255,0.15)]">
              <ResponsiveContainer width="100%" height={360}>
                <BarChart data={trendingSkills.trends} margin={{ left: 0, right: 8, bottom: 40 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.08)" />
                  <XAxis
                    dataKey="skill"
                    angle={-30}
                    interval={0}
                    tickFormatter={(v) => trimSkill(v, 14)}
                    textAnchor="end"
                    height={90}
                    tick={{ fill: '#9fb3c8', fontSize: 12 }}
                  />
                  <YAxis tick={{ fill: '#9fb3c8', fontSize: 12 }} />
                  <Tooltip contentStyle={{ background: 'rgba(12,18,33,0.9)', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 12, color: '#e6ecf5' }} />
                  <Bar dataKey="count" fill="#22d3ee" radius={[8, 8, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>

            {/* Top Skills List */}
            <div className="space-y-3">
              {trendingSkills.trends.slice(0, 10).map((trend, idx) => (
                <div key={trend.skill} className="flex items-center justify-between p-3 rounded-lg bg-[rgba(255,255,255,0.05)] border border-[rgba(255,255,255,0.08)]">
                  <div className="flex items-center gap-3">
                    <div className="w-9 h-9 rounded-full bg-gradient-to-br from-[#22d3ee] to-[#f472b6] text-slate-900 flex items-center justify-center font-bold">
                      {idx + 1}
                    </div>
                    <span className="font-semibold text-slate-100">{trend.skill}</span>
                  </div>
                  <div className="text-right">
                    <div className="font-bold text-slate-100">{trend.count} jobs</div>
                    <div className={`text-sm ${trend.growth_rate > 0 ? 'text-emerald-300' : 'text-slate-400'}`}>
                      {trend.growth_rate > 0 ? '↗' : '→'} {trend.growth_rate.toFixed(1)}%
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Forecast */}
      {forecast && (
        <div className="card">
          <div className="section-heading">
            <span className="pill">Forecast</span>
            <span>12-month outlook</span>
          </div>
          
          {Object.entries(forecast.forecasts).slice(0, 5).map(([skill, data]) => (
            <div key={skill} className="mb-8 last:mb-0">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-xl font-bold text-slate-100">{skill}</h3>
                <div className="text-right">
                  <div className="text-sm text-slate-400">Projected Growth</div>
                  <div className={`text-2xl font-bold ${
                    data.summary.total_growth_pct > 20 ? 'text-emerald-300' :
                    data.summary.total_growth_pct > 10 ? 'text-cyan-300' : 'text-slate-300'
                  }`}>
                    +{data.summary.total_growth_pct.toFixed(1)}%
                  </div>
                </div>
              </div>
              
              <ResponsiveContainer width="100%" height={200}>
                <LineChart data={data.forecasts}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.08)" />
                  <XAxis dataKey="date" tick={{ fill: '#9fb3c8', fontSize: 12 }} />
                  <YAxis tick={{ fill: '#9fb3c8', fontSize: 12 }} />
                  <Tooltip contentStyle={{ background: 'rgba(12,18,33,0.9)', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 12, color: '#e6ecf5' }} />
                  <Line type="monotone" dataKey="predicted_demand" stroke="#f472b6" strokeWidth={3} dot={false} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          ))}
        </div>
      )}

      {loading && (
        <div className="text-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[rgba(34,211,238,0.8)] mx-auto"></div>
          <p className="mt-4 text-slate-400">Loading trends...</p>
        </div>
      )}
    </div>
  )
}

export default TrendsDashboard
