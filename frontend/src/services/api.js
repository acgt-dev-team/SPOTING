import axios from "axios"
import { clearAuthStorage } from "./authSession"

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL
})

api.interceptors.request.use((config) => {
  const token = sessionStorage.getItem("token")

  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }

  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    const status = error.response?.status

    if (status === 401) {
      console.warn("Unauthorized - logging out")
      clearAuthStorage()
      window.location.hash = "#/login"
    }

    if (status === 428) {
      sessionStorage.setItem("forcePasswordChange", "true")
      window.location.hash = "#/change-password"
    }

    return Promise.reject(error)
  }
)

export default api
