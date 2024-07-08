/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["*.py"],
  corePlugins: {
    preflight: false,
  },
  plugins: [require("@tailwindcss/typography"), require("@tailwindcss/forms")],
};
