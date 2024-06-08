/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['**/*.html'],
  theme: {
    extend: {},
  },
  safelist: [
    '!bg-base-100'
  ],
  blocklist: [
    'modal',
    'hidden',
  ],
  plugins: [require('daisyui')],
}

