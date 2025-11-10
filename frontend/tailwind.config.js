export default {
  darkMode: 'class',
  content: ["./index.html", "./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Poppins', 'ui-sans-serif', 'system-ui']
      },
      colors: {
        neon: {
          50: '#e8f0ff',
          100: '#cfe0ff',
          300: '#4fd1ff',
          500: '#00e5ff'
        }
      }
    }
  },
  plugins: [],
}
