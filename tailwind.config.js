/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",        // base.html e páginas globais
    "./**/templates/**/*.html",     // templates dentro dos apps (automation/…)
    "./**/*.py"                     // opcional: classes em strings no Python
  ],
  theme: {
    extend: {
      colors: { brand: "#499E9D", ink: "#383838" },
      fontFamily: {
        sans: ["Lato","ui-sans-serif","system-ui","-apple-system","Segoe UI","Roboto","Helvetica Neue","Arial","Noto Sans","sans-serif"]
      }
    }
  },
  plugins: [
    require("@tailwindcss/forms"),
    require("@tailwindcss/typography"),
    require("@tailwindcss/line-clamp"),
  ],
  // TEMPORÁRIO: assegura que a estrutura básica exista mesmo se o scanner falhar
  safelist: [
    "flex","min-h-screen","grid","items-center","gap-3","md:flex-row",
    "fixed","inset-y-0","left-0","w-72","-translate-x-full","md:translate-x-0","md:static",
    "bg-white","border","border-b","border-r","shadow-sm",
    "sticky","top-0","backdrop-blur","max-w-7xl","mx-auto","px-4","py-3",
    "rounded","rounded-lg","rounded-xl","rounded-2xl",
    "bg-gradient-to-r","from-ink","to-brand","text-white","text-ink"
  ]
};
