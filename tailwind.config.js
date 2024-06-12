/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['**/*.html'],
  theme: {
    extend: {},
  },
  safelist: [
    '!bg-base-100',
    'text-green-700',
    'dark:text-green-300',
    'text-orange-700',
    'dark:text-orange-300',
    'bg-inherit',
    'border-black',
    'focus:border-black',
    'focus:outline-black'
  ],
  blocklist: [
    'modal',
    'hidden',
  ],
  darkMode: ['class', '[data-theme="dark"]'],
  plugins: [require('daisyui')],
  daisyui: {
    themes: [
      {
      light: {
        ...require("daisyui/src/theming/themes")["light"],
	primary: "#1d4ed8",
	secondary: "#0369a1",
        accent: "#047857",
	info: "#0e7490",
	warning: "#eab308",
	success: "#15803d",
	error: "#be123c"
      },
      dark: {
        ...require("daisyui/src/theming/themes")["dark"],
	primary: "#60a5fa",
	secondary: "#38bdf8",
        accent: "#34d399",
	info: "#06b6d4",
	warning: "#facc15",
	success: "#22c55e",
	error: "#fb7185",
	"base-100": "#222222",
	"base-200": "#404040",
	"base-300": "#525252",
	"color": "#e5e5e5",
	"neutral": "#404040",
	"base-content": "#d4d4d4"
      },
      }
    ],
     darkTheme: 'light'
  },
}

