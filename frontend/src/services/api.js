import axios from "axios"

const api = axios.create({
  baseURL: "https://seahorse-app-6x2kt.ondigitalocean.app"
})

export default api