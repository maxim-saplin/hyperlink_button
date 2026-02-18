import { defineConfig } from "vite"

export default defineConfig({
  // Streamlit serves component assets under a nested route like:
  // /component/<component_name>/index.html
  // We need relative asset paths.
  base: "./",
  build: {
    outDir: "dist",
    emptyOutDir: true,
  },
})
