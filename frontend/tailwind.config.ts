import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        base: '#080C12',
        surface: '#0F1520',
        elevated: '#162030',
        accent: {
          red: '#FF3B3B',
          amber: '#F59E0B',
          green: '#10B981',
          blue: '#3B82F6',
          cyan: '#06B6D4',
        },
        text: {
          primary: '#F1F5F9',
          muted: '#64748B',
        },
        border: '#1E293B',
      },
      fontFamily: {
        display: ['Space Grotesk', 'sans-serif'],
        body: ['Inter', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      backgroundImage: {
        'grid-pattern': `radial-gradient(circle at 1px 1px, rgba(30, 41, 59, 0.5) 1px, transparent 0)`,
      },
      backgroundSize: {
        'grid': '24px 24px',
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'fade-in-up': 'fadeInUp 0.6s ease-out',
        'count-up': 'countUp 0.5s ease-out',
      },
      keyframes: {
        fadeInUp: {
          '0%': {
            opacity: '0',
            transform: 'translateY(10px)',
          },
          '100%': {
            opacity: '1',
            transform: 'translateY(0)',
          },
        },
        countUp: {
          '0%': {
            opacity: '0',
            transform: 'scale(0.8)',
          },
          '100%': {
            opacity: '1',
            transform: 'scale(1)',
          },
        },
      },
    },
  },
  plugins: [],
}
export default config
