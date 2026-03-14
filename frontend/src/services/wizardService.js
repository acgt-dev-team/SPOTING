import api from "./api"

export async function submitWizard(data) {

  const response = await api.post(
    "/api/wizard/setup",
    data
  )

  return response.data
}