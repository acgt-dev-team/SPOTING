const AUTH_STORAGE_KEYS = [
  "token",
  "role",
  "username",
  "forcePasswordChange"
]

export function clearAuthStorage() {
  for (const key of AUTH_STORAGE_KEYS) {
    sessionStorage.removeItem(key)
    localStorage.removeItem(key)
  }
}
