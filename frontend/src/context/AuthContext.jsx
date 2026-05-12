import { createContext, useContext, useEffect, useMemo, useState } from 'react'

import {
  loginAdmin as loginAdminRequest,
  loginUser as loginUserRequest,
  logout as logoutRequest,
  signup as signupRequest,
} from '../api/auth'


const AuthContext = createContext(null)
const USER_KEY = 'cineverse-user'
const TOKEN_KEY = 'cineverse-token'
const SESSION_KEY = 'cineverse-session'
const SESSION_TTL_MS = 1000 * 60 * 60 * 8


function readStoredUser() {
  const storedUser = window.localStorage.getItem(USER_KEY)
  const storedSession = window.localStorage.getItem(SESSION_KEY)
  if (!storedUser || !storedSession) return null

  try {
    const user = JSON.parse(storedUser)
    const session = JSON.parse(storedSession)
    if (!session?.expiresAt || Date.now() > session.expiresAt) {
      window.localStorage.removeItem(USER_KEY)
      window.localStorage.removeItem(TOKEN_KEY)
      window.localStorage.removeItem(SESSION_KEY)
      return null
    }
    return user
  } catch {
    window.localStorage.removeItem(USER_KEY)
    window.localStorage.removeItem(TOKEN_KEY)
    window.localStorage.removeItem(SESSION_KEY)
    return null
  }
}


export function AuthProvider({ children }) {
  const [user, setUser] = useState(readStoredUser)

  useEffect(() => {
    if (user) {
      window.localStorage.setItem(USER_KEY, JSON.stringify(user))
      window.localStorage.setItem(
        SESSION_KEY,
        JSON.stringify({
          role: user.role,
          expiresAt: Date.now() + SESSION_TTL_MS,
        }),
      )
    } else {
      window.localStorage.removeItem(USER_KEY)
      window.localStorage.removeItem(TOKEN_KEY)
      window.localStorage.removeItem(SESSION_KEY)
    }
  }, [user])

  useEffect(() => {
    const timer = window.setInterval(() => {
      const session = window.localStorage.getItem(SESSION_KEY)
      if (!session) return
      try {
        const parsed = JSON.parse(session)
        if (Date.now() > parsed.expiresAt) {
          setUser(null)
        }
      } catch {
        setUser(null)
      }
    }, 60_000)

    return () => window.clearInterval(timer)
  }, [])

  const storeSession = (payload) => {
    window.localStorage.setItem(TOKEN_KEY, payload.token)
    setUser(payload.user)
    return payload.user
  }

  const value = useMemo(
    () => ({
      user,
      isAuthenticated: Boolean(user),
      loginUser: async (payload) => storeSession(await loginUserRequest(payload)),
      loginAdmin: async (payload) => storeSession(await loginAdminRequest(payload)),
      signup: async (payload) => {
        const userPayload = await signupRequest(payload)
        if (userPayload.user.role !== 'user') {
          throw new Error('Unexpected role returned during signup.')
        }
        return storeSession(userPayload)
      },
      logout: async () => {
        await logoutRequest()
        setUser(null)
      },
    }),
    [user],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}
