import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{js,ts,jsx,tsx}", "./components/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      boxShadow: { glow: "0 0 40px rgba(59, 130, 246, 0.25)" }
    }
  },
  plugins: []
};
export default config;
