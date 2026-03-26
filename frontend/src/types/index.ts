export type Ticket = {
  _id: string
  subject: string
  customer_email: string
  status: 'open' | 'pending' | 'resolved' | 'closed'
  priority: 'low' | 'medium' | 'high' | 'urgent'
  assignee_id?: string
  tags: string[]
  source: string
  created_at: string
  updated_at: string
}

export type Message = {
  _id: string
  ticket_id: string
  body: string
  sender_type: string
  sender_email: string
  is_internal: boolean
  created_at: string
}
