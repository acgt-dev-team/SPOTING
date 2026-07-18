import { describe, expect, it } from "vitest"

import {
  isValidPassword,
  isValidUserId
} from "../src/utils/validation"


describe("authentication validation", () => {
  it.each([
    "user.name1",
    "abcdefghij",
    "abc.def.1234567890123456"
  ])("accepts valid User ID %s", (userId) => {
    expect(isValidUserId(userId)).toBe(true)
  })

  it.each([
    "short.id",
    "abcdefghijklmnopqrstuvwxy",
    "User.name1",
    "user name1",
    "user_name1",
    "user-name1",
    "user@name1"
  ])("rejects invalid User ID %s", (userId) => {
    expect(isValidUserId(userId)).toBe(false)
  })

  it("accepts a password satisfying every rule", () => {
    expect(isValidPassword("Secure1!")).toBe(true)
  })

  it.each([
    "Short1!",
    "lowercase1!",
    "UPPERCASE1!",
    "NoNumber!",
    "NoSpecial1"
  ])("rejects password missing a requirement: %s", (password) => {
    expect(isValidPassword(password)).toBe(false)
  })
})
