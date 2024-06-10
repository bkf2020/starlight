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
  darkMode: 'selector',
  plugins: [require('daisyui')]
}

