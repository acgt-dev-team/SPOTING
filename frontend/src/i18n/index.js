import { ref } from "vue"

const localeModules = import.meta.glob("./*.json", {
  eager: true,
  import: "default"
})

const messages = Object.fromEntries(
  Object.entries(localeModules).map(([path, catalogue]) => {
    const locale = path.match(/([^/]+)\.json$/)?.[1]
    return [locale, catalogue]
  })
)

const defaultLocale = import.meta.env.VITE_DEFAULT_LOCALE || "mly"
const currentLocale = ref(messages[defaultLocale] ? defaultLocale : "mly")

function readPath(source, key) {
  return key
    .split(".")
    .reduce((value, part) => (
      value && Object.prototype.hasOwnProperty.call(value, part)
        ? value[part]
        : undefined
    ), source)
}

function interpolate(value, params) {
  if (!params || typeof value !== "string") return value

  return value.replace(/\{(\w+)\}/g, (_, name) => (
    Object.prototype.hasOwnProperty.call(params, name)
      ? String(params[name])
      : `{${name}}`
  ))
}

export function setLocale(locale) {
  if (messages[locale]) {
    currentLocale.value = locale
  }
}

export function getLocale() {
  return currentLocale.value
}

export function t(key, params = {}) {
  const value =
    readPath(messages[currentLocale.value], key) ??
    readPath(messages.mly, key) ??
    key

  return interpolate(value, params)
}

export default {
  install(app) {
    app.config.globalProperties.$t = t
    app.provide("i18n", {
      getLocale,
      setLocale,
      t
    })
  }
}