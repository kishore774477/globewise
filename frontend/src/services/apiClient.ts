import axios from "axios";

// Defaults to the Vite dev proxy (/api -> http://127.0.0.1:8000).
// Override with VITE_API_BASE_URL, e.g. https://my-backend.example.com/api/v1
export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "/api/v1",
  timeout: 30000,
  headers: {
    "Content-Type": "application/json",
  },
});
