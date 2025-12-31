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
    <div className="max-w-7xl mx-auto space-y-8">
      {/* Header */}
      <div className="pt-4">
        <div className="hero-kicker w-fit mb-4">📊 Signal-driven · Prophet forecasts</div>
        <h1 className="text-5xl font-bold bg-gradient-to-r from-cyan-400 to-pink-400 bg-clip-text text-transparent mb-4">Market Trends</h1>
        <p className="section-subtext max-w-3xl text-lg">Track skill momentum and visualize demand patterns with real-time intelligence.</p>
      </div>

      {/* Time Range & Controls */}
      <div className="card">
        <div className="flex gap-4 items-center flex-wrap justify-between">
          <div className="flex items-center gap-3">
            <span className="pill">⏱️ Time Range</span>
            <div className="flex gap-2">
              {['1m', '3m', '6m', '1y'].map(range => (
                <button
                  key={range}
                  onClick={() => setTimeRange(range)}
                  className={`px-4 py-2 rounded-lg font-semibold transition-all border ${
                    timeRange === range
                      ? 'bg-gradient-to-r from-cyan-500/25 to-pink-500/25 text-cyan-300 border-cyan-400/50 shadow-lg shadow-cyan-500/20'
                      : 'bg-[rgba(255,255,255,0.04)] text-slate-300 border-[rgba(255,255,255,0.1)] hover:bg-[rgba(255,255,255,0.08)] hover:border-cyan-400/30'
                  }`}
                >
                  {range.toUpperCase()}
                </button>
              ))}
            </div>
          </div>
          
          <button onClick={loadForecast} className="btn-primary flex items-center gap-2">
            🔮 Forecast 12M
          </button>
        </div>
      </div>

      {/* Trending Skills */}
      {trendingSkills && (
        <div className="space-y-6">
          <div className="flex items-center gap-3">
            <div className="w-2 h-8 bg-gradient-to-b from-cyan-400 to-pink-400 rounded-full"></div>
            <h2 className="text-3xl font-bold text-white">Top Skills</h2>
            <span className="text-sm text-slate-400 font-medium">{timeRange.toUpperCase()} • {trendingSkills.trends.length} found</span>
          </div>
          
          <div className="grid lg:grid-cols-3 gap-8">
            {/* Main Bar Chart - wider */}
            <div className="lg:col-span-2 card">
              <ResponsiveContainer width="100%" height={420}>
                <BarChart data={trendingSkills.trends} margin={{ left: -20, right: 16, bottom: 50, top: 16 }}>
                  <defs>
                    <linearGradient id="barGradient" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor="#06b6d4" />
                      <stop offset="100%" stopColor="#22d3ee" />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="4 4" stroke="rgba(255,255,255,0.06)" vertical={false} />
                  <XAxis
                    dataKey="skill"
                    angle={-35}
                    interval={0}
                    tickFormatter={(v) => trimSkill(v, 13)}
                    textAnchor="end"
                    height={100}
                    tick={{ fill: '#9fb3c8', fontSize: 13, fontWeight: 500 }}
                  />
                  <YAxis tick={{ fill: '#9fb3c8', fontSize: 12 }} />
                  <Tooltip 
                    contentStyle={{ 
                      background: 'rgba(12,18,33,0.95)', 
                      border: '1px solid rgba(34,211,238,0.3)', 
                      borderRadius: 12, 
                      color: '#e6ecf5',
                      boxShadow: '0 10px 30px rgba(34,211,238,0.2)'
                    }} 
                    cursor={{ fill: 'rgba(34,211,238,0.08)' }}
                  />
                  <Bar 
                    dataKey="count" 
                    fill="url(#barGradient)" 
                    radius={[10, 10, 4, 4]}
                    isAnimationActive={true}
                  />
                </BarChart>
              </ResponsiveContainer>
            </div>

            {/* Top 8 Skills Leaderboard */}
            <div className="card space-y-2">
              <h3 className="text-lg font-bold text-white mb-4">�� Leaderboard</h3>
              {trendingSkills.trends.slice(0, 8).map((trend, idx) => (
                <div key={trend.skill} className="p-3 rounded-lg bg-gradient-to-r from-slate-800/50 to-slate-900/30 border border-slate-700/50 hover:border-cyan-500/40 transition-all hover:bg-slate-800/60">
                  <div className="flex items-center justify-between gap-2">
                    <div className="flex items-center gap-3 min-w-0">
                      <div className="w-7 h-7 rounded-lg bg-gradient-to-br from-cyan-500/80 to-pink-500/80 text-slate-100 flex items-center justify-center font-bold text-sm flex-shrink-0">
                        {idx + 1}
                      </div>
                      <span className="font-semibold text-slate-100 truncate text-sm">{trend.skill}</span>
                    </div>
                    <div className="text-right flex-shrink-0">
                      <div className="font-bold text-cyan-300 text-sm">{trend.count}</div>
                      <div className={`text-xs font-semibold ${trend.growth_rate > 0 ? 'text-emerald-400' : 'text-slate-500'}`}>
                        {trend.growth_rate > 0 ? '📈' : '→'} {Math.abs(trend.growth_rate).toFixed(0)}%
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Forecast Section */}
      {forecast && (
        <div className="space-y-6">
          <div className="flex items-center gap-3">
            <div className="w-2 h-8 bg-gradient-to-b from-pink-400 to-cyan-400 rounded-full"></div>
            <h2 className="text-3xl font-bold text-white">12-Month Forecast</h2>
            <span className="text-sm text-slate-400 font-medium">AI-powered projections</span>
          </div>
          
          <div className="grid gap-6">
            {Object.entries(forecast.forecasts).slice(0, 5).map(([skill, data]) => (
              <div key={skill} className="card overflow-hidden border border-slate-700/50">
                <div className="flex justify-between items-start mb-6 pb-4 border-b border-slate-700/30">
                  <div>
                    <h3 className="text-2xl font-bold text-white">{skill}</h3>
                    <p className="text-slate-400 text-sm mt-1">Demand forecast over 12 months</p>
                  </div>
                  <div className="text-right px-4 py-2 rounded-lg bg-gradient-to-br from-slate-800 to-slate-900">
                    <div className="text-xs text-slate-400 font-medium">Growth</div>
                    <div className={`text-2xl font-bold ${
                      data.summary.total_growth_pct > 20 ? 'text-emerald-400' :
                      data.summary.total_growth_pct > 10 ? 'text-cyan-400' : 'text-slate-300'
                    }`}>
                      +{data.summary.total_growth_pct.toFixed(1)}%
                    </div>
                  </div>
                </div>
                
                <ResponsiveContainer width="100%" height={240}>
                  <LineChart data={data.forecasts} margin={{ top: 5, right: 16, bottom: 5, left: 0 }}>
                    <defs>
                      <linearGradient id={`lineGradient-${skill}`} x1="0" y1="0" x2="0" y2="1">
                        <stop offset="0%" stopColor="#f472b6" stopOpacity={0.3}/>
                        <stop offset="100%" stopColor="#f472b6" stopOpacity={0}/>
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="4 4" stroke="rgba(255,255,255,0.06)" vertical={false} />
                    <XAxis 
                      dataKey="date" 
                      tick={{ fill: '#9fb3c8', fontSize: 11 }}
                      interval={Math.floor(data.forecasts.length / 5)}
                    />
                    <YAxis tick={{ fill: '#9fb3c8', fontSize: 11 }} />
                    <Tooltip 
                      contentStyle={{ 
                        background: 'rgba(12,18,33,0.95)', 
                        border: '1px solid rgba(244,114,182,0.3)', 
                        borderRadius: 12, 
                        color: '#e6ecf5',
                        boxShadow: '0 10px 30px rgba(244,114,182,0.15)'
                      }}
                      cursor={{ stroke: 'rgba(244,114,182,0.3)' }}
                    />
                    <Line 
                      type="monotone" 
                      dataKey="predicted_demand" 
                      stroke="#f472b6" 
                      strokeWidth={3} 
                      dot={false}
                      isAnimationActive={true}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            ))}
          </div>
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
