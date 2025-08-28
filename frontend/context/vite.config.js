import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
    plugins: [react()],
    server: {
        proxy: {
            "/login": { target: "http://127.0.0.1:8000", changeOrigin: true },
            "/logout": { target: "http://127.0.0.1:8000", changeOrigin: true },
            "/signup": { target: "http://127.0.0.1:8000", changeOrigin: true },
            "/me": { target: "http://127.0.0.1:8000", changeOrigin: true },
            "/requests": { target: "http://127.0.0.1:8000", changeOrigin: true },
            "/firebase-login": { target: "http://127.0.0.1:8000", changeOrigin: true },
        },
    },
});
