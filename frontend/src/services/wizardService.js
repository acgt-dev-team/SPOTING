import api from "./api"

export async function submitWizard(data) {

  const response = await api.post(
    "/wizard/setup",
    data
  )

  return response.data
}