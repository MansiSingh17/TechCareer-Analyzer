// Color themes for TechCareer Analyzer
export const themes = {
  // Default: Cyan & Pink (current)
  cyberpunk: {
    name: 'Cyberpunk',
    bg: '#070910',
    bg2: '#0c1221',
    accent: '#22d3ee',
    accent2: '#f472b6',
    gradientStart: '#fbbf24',
    gradientMid1: '#f97316',
    gradientMid2: '#22d3ee',
    gradientEnd: '#f472b6',
  },
  
  // Purple & Violet
  nebula: {
    name: 'Nebula',
    bg: '#0a0415',
    bg2: '#15082a',
    accent: '#a78bfa',
    accent2: '#c084fc',
    gradientStart: '#a78bfa',
    gradientMid1: '#d8b4fe',
    gradientMid2: '#c084fc',
    gradientEnd: '#a78bfa',
  },
  
  // Blue & Teal
  ocean: {
    name: 'Ocean',
    bg: '#051a30',
    bg2: '#0a2d4d',
    accent: '#06b6d4',
    accent2: '#0891b2',
    gradientStart: '#06b6d4',
    gradientMid1: '#0ea5e9',
    gradientMid2: '#0891b2',
    gradientEnd: '#06b6d4',
  },
  
  // Green & Emerald
  forest: {
    name: 'Forest',
    bg: '#050f0a',
    bg2: '#0d1d17',
    accent: '#10b981',
    accent2: '#059669',
    gradientStart: '#34d399',
    gradientMid1: '#10b981',
    gradientMid2: '#059669',
    gradientEnd: '#047857',
  },
  
  // Orange & Amber
  sunset: {
    name: 'Sunset',
    bg: '#1a0f05',
    bg2: '#2d1810',
    accent: '#f97316',
    accent2: '#fb923c',
    gradientStart: '#fbbf24',
    gradientMid1: '#f97316',
    gradientMid2: '#fb923c',
    gradientEnd: '#f59e0b',
  },
  
  // Red & Rose
  passion: {
    name: 'Passion',
    bg: '#1a0a0a',
    bg2: '#2d1414',
    accent: '#ef4444',
    accent2: '#f43f5e',
    gradientStart: '#f43f5e',
    gradientMid1: '#ef4444',
    gradientMid2: '#f87171',
    gradientEnd: '#fca5a5',
  },
}

export const getTheme = (themeName = 'cyberpunk') => {
  return themes[themeName] || themes.cyberpunk
}

export const applyTheme = (themeName) => {
  const theme = getTheme(themeName)
  const root = document.documentElement
  
  root.style.setProperty('--bg', theme.bg)
  root.style.setProperty('--bg-2', theme.bg2)
  root.style.setProperty('--accent', theme.accent)
  root.style.setProperty('--accent-2', theme.accent2)
  
  // Update body background
  root.style.setProperty(
    '--theme-gradient-colors',
    `rgba(${hexToRgb(theme.accent).join(',')},0.10), ${theme.accent2}`
  )
  
  localStorage.setItem('app-theme', themeName)
}

export const hexToRgb = (hex) => {
  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex)
  return result ? [
    parseInt(result[1], 16),
    parseInt(result[2], 16),
    parseInt(result[3], 16)
  ] : [34, 211, 238]
}

export const getStoredTheme = () => {
  return localStorage.getItem('app-theme') || 'cyberpunk'
}
