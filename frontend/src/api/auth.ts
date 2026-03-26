import { api } from './client'

export const login = (email: string, password: string) =>
  api.post('/auth/login', { email, password })

export const me = () => api.get('/auth/me')
