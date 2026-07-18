export const USER_ID_PATTERN = /^[a-z0-9.]{10,24}$/

export function isValidUserId(userId) {
  return USER_ID_PATTERN.test(userId)
}

export function getPasswordRuleChecks(password, labels) {
  return [
    { label: labels.length, passed: password.length >= 8 },
    { label: labels.upper, passed: /[A-Z]/.test(password) },
    { label: labels.lower, passed: /[a-z]/.test(password) },
    { label: labels.number, passed: /[0-9]/.test(password) },
    { label: labels.special, passed: /[^A-Za-z0-9]/.test(password) }
  ]
}

export function isValidPassword(password) {
  return getPasswordRuleChecks(password, {
    length: "length",
    upper: "upper",
    lower: "lower",
    number: "number",
    special: "special"
  }).every((rule) => rule.passed)
}
