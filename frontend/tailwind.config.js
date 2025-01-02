import daisyui from "daisyui"
/** @type {import('tailwindcss').Config} */

export default {
  content: ["./src/**/*.{js,jsx,ts,tsx}"], // Dodaj ścieżki, które mają być przeszukiwane
  theme: {
    extend: {},
  },
  plugins: [
    daisyui,
  ],
}
