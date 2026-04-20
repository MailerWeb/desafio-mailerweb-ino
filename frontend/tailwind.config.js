/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        app: {
          bg: '#f5f5f4',
          surface: '#fffefc',
          muted: '#f7f5f2',
          border: '#e7e1d8',
          strong: '#171717',
          text: '#57534e',
          soft: '#78716c',
        },
      },
      boxShadow: {
        soft: '0 10px 30px rgba(23, 23, 23, 0.06)',
      },
      borderRadius: {
        panel: '1.25rem',
      },
      fontFamily: {
        sans: ['IBM Plex Sans', 'Segoe UI', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
