import { useEffect, useState } from 'react'
import { fetchCustomer, fetchMessages, fetchTickets, sendMessage, suggestReply } from '../api/tickets'
import { CustomerPanel } from '../components/CustomerPanel'
import { MessageThread } from '../components/MessageThread'
import { ReplyBox } from '../components/ReplyBox'
import { TicketList } from '../components/TicketList'
import { Message, Ticket } from '../types'

export function InboxPage() {
  const [tickets, setTickets] = useState<Ticket[]>([])
  const [selectedId, setSelectedId] = useState<string>()
  const [messages, setMessages] = useState<Message[]>([])
  const [aiReply, setAiReply] = useState('')
  const [profile, setProfile] = useState<any>(null)

  useEffect(() => {
    fetchTickets().then(({ data }) => {
      setTickets(data)
      if (data.length && !selectedId) setSelectedId(data[0]._id)
    })
  }, [selectedId])

  useEffect(() => {
    if (!selectedId) return
    fetchMessages(selectedId).then(({ data }) => setMessages(data))
    const ticket = tickets.find((t) => t._id === selectedId)
    if (ticket) fetchCustomer(ticket.customer_email).then(({ data }) => setProfile(data))
  }, [selectedId, tickets])

  const onSend = async (body: string) => {
    if (!selectedId || !body.trim()) return
    await sendMessage(selectedId, {
      body,
      sender_type: 'agent',
      sender_email: 'agent@demo.com',
      is_internal: false
    })
    const { data } = await fetchMessages(selectedId)
    setMessages(data)
    setAiReply('')
  }

  const onAIAutofill = async () => {
    if (!selectedId) return
    const { data } = await suggestReply(selectedId)
    setAiReply(data.suggested_reply)
  }

  return (
    <div className="grid grid-cols-12 gap-4">
      <section className="col-span-3"><TicketList tickets={tickets} selectedId={selectedId} onSelect={setSelectedId} /></section>
      <section className="col-span-6 space-y-3">
        <MessageThread messages={messages} />
        <ReplyBox onSend={onSend} onAIAutofill={onAIAutofill} aiReply={aiReply} />
      </section>
      <section className="col-span-3"><CustomerPanel profile={profile} /></section>
    </div>
  )
}
