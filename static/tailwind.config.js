module.exports = {
  purge: [],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      height: {
        splash: '32rem',
        majority: '100rem'
      },
      margin: {
        splash: '30rem'
      },
      gridTemplateColumns: {
        'main': 'auto 30rem'
      },
      colors: {
        primary: {
          100: '#cd0033',
          200: '#b3002d',
          300: '#9a0026',
          400: '#800020',
          500: '#67001a',
          600: '#4d0013',
          700: '#34000d'
        },
        charcoal: {
          100: '#A1A1A1',
          200: '#5A5A5A',
          500: '#2B2B2B',
          700: '#151515',
          900: '#121212'
        }
      },
      animation: {
        spin: 'spin 6s linear infinite',
        wiggle: 'wiggle 1s ease-in-out infinite'
      },
      keyframes: {
        wiggle: {
          '0% 100%': { transform: 'rotate(-3deg)'},
          '50%': { transform: 'rotate(3deg)'}
        }
      },
      fontFamily: {
        body: ['Nunito'],
        lobster: ['Lobster', 'cursive']
      },
      backgroundImage: {
        splash: 'url(\'/static/bin/splash.jpeg\')'
      }
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
