import { defineConfig } from "vite"
import react from "@vitejs/plugin-react"
import { resolve } from "path"

export default defineConfig({
  base: "./",
  plugins: [react()],
  build: {
    outDir: resolve(__dirname, "build"),
    emptyOutDir: true,
    rollupOptions: {
      input: resolve(__dirname, "index.html")
    }
  }
})
