import { api } from './client'

export const fetchTickets = () => api.get('/tickets')
export const fetchTicket = (id: string) => api.get(`/tickets/${id}`)
export const patchTicket = (id: string, payload: Record<string, unknown>) => api.patch(`/tickets/${id}`, payload)
export const fetchMessages = (id: string) => api.get(`/tickets/${id}/messages`)
export const sendMessage = (id: string, payload: Record<string, unknown>) => api.post(`/tickets/${id}/messages`, payload)
export const suggestReply = (id: string) => api.post(`/ai/suggest-reply/${id}`)
export const fetchCustomer = (email: string) => api.get(`/customers/${encodeURIComponent(email)}/profile`)
