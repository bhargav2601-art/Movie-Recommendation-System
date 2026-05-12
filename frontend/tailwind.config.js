/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        ink: 'rgb(var(--background-deep-rgb) / <alpha-value>)',
        night: 'rgb(var(--background-soft-rgb) / <alpha-value>)',
        slate: 'rgb(var(--subtle-rgb) / <alpha-value>)',
        mist: 'rgb(var(--foreground-rgb) / <alpha-value>)',
        gold: 'rgb(var(--gold-rgb) / <alpha-value>)',
        neon: 'rgb(var(--accent-rgb) / <alpha-value>)',
        danger: '#fb7185',
        background: 'rgb(var(--background-rgb) / <alpha-value>)',
        'background-soft': 'rgb(var(--background-soft-rgb) / <alpha-value>)',
        'background-elevated': 'rgb(var(--background-elevated-rgb) / <alpha-value>)',
        foreground: 'rgb(var(--foreground-rgb) / <alpha-value>)',
        muted: 'rgb(var(--muted-rgb) / <alpha-value>)',
        subtle: 'rgb(var(--subtle-rgb) / <alpha-value>)',
        border: 'rgb(var(--border-rgb) / <alpha-value>)',
        card: 'rgb(var(--card-rgb) / <alpha-value>)',
        'card-strong': 'rgb(var(--card-strong-rgb) / <alpha-value>)',
        overlay: 'rgb(var(--overlay-rgb) / <alpha-value>)',
      },
      boxShadow: {
        glow: 'var(--shadow-glow)',
        card: 'var(--shadow-card)',
      },
      backgroundImage: {
        'hero-gradient':
          'radial-gradient(circle at top, rgba(105,230,255,0.16), transparent 28%), linear-gradient(135deg, rgba(10,15,28,0.96), rgba(6,8,18,0.86))',
        'panel-gradient':
          'linear-gradient(180deg, rgba(20,30,52,0.78), rgba(11,17,31,0.74))',
      },
      fontFamily: {
        display: ['"Plus Jakarta Sans"', 'sans-serif'],
        body: ['"Inter"', 'sans-serif'],
      },
      animation: {
        shimmer: 'shimmer 1.6s linear infinite',
        float: 'float 7s ease-in-out infinite',
      },
      keyframes: {
        shimmer: {
          '0%': { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-12px)' },
        },
      },
    },
  },
  plugins: [],
}
