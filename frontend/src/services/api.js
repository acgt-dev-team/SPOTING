import axios from "axios"

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token")

  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }

  return config
})

// =========================
// RESPONSE INTERCEPTOR
// =========================
api.interceptors.response.use(
  (response) => response,
  (error) => {
    const status = error.response?.status

    // 🔐 Auto logout on 401
    if (status === 401) {
      console.warn("Unauthorized - logging out")

      localStorage.removeItem("token")
      localStorage.removeItem("role")

      // redirect manually
      window.location.href = "/login"
    }

    return Promise.reject(error)
  }
)

export default api