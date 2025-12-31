import { useState, useEffect } from 'react'
import { themes, applyTheme, getStoredTheme } from '../themes'

function ThemeSwitcher() {
  const [currentTheme, setCurrentTheme] = useState(getStoredTheme())
  const [showThemes, setShowThemes] = useState(false)

  useEffect(() => {
    applyTheme(currentTheme)
  }, [currentTheme])

  const themeList = Object.entries(themes)

  return (
    <div className="fixed bottom-6 right-6 z-50">
      <div className="flex flex-col gap-2 items-end">
        {/* Theme Picker Button */}
        <button
          onClick={() => setShowThemes(!showThemes)}
          className="p-3 rounded-full bg-gradient-to-r from-cyan-500/20 to-pink-500/20 border border-cyan-400/40 hover:border-cyan-300/60 transition-all hover:shadow-lg hover:shadow-cyan-500/30"
          title="Change theme"
        >
          🎨
        </button>

        {/* Theme Menu */}
        {showThemes && (
          <div className="bg-slate-900/95 backdrop-blur border border-slate-700/50 rounded-lg shadow-2xl p-3 space-y-2 min-w-[140px]">
            {themeList.map(([key, theme]) => (
              <button
                key={key}
                onClick={() => {
                  setCurrentTheme(key)
                  setShowThemes(false)
                }}
                className={`w-full px-3 py-2 rounded-lg transition-all text-sm font-semibold flex items-center gap-2 ${
                  currentTheme === key
                    ? 'bg-cyan-500/30 text-cyan-300 border border-cyan-400/50'
                    : 'bg-slate-800/50 text-slate-300 border border-slate-700/30 hover:bg-slate-700/50'
                }`}
              >
                <div
                  className="w-3 h-3 rounded-full border border-current"
                  style={{ backgroundColor: theme.accent }}
                />
                {theme.name}
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default ThemeSwitcher
