/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/app/**/*.{ts,tsx}",
    "./src/components/**/*.{ts,tsx}",
    "./src/features/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          DEFAULT: "#FF5CA6",
          100: "#FFE0ED",
          200: "#FFBAD4",
          300: "#FF94BC",
          400: "#FF6DA3",
          500: "#FF478B",
          600: "#E03A79",
          700: "#C02E67",
        },
      },
    },
  },
  plugins: [],
};
