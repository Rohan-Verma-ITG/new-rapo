import { Ticket } from '../types'

type Props = {
  tickets: Ticket[]
  selectedId?: string
  onSelect: (id: string) => void
}

export function TicketList({ tickets, selectedId, onSelect }: Props) {
  return (
    <div className="space-y-2">
      {tickets.map((ticket) => (
        <button
          key={ticket._id}
          className={`w-full rounded-lg border p-3 text-left ${selectedId === ticket._id ? 'border-indigo-500 bg-indigo-50' : 'bg-white'}`}
          onClick={() => onSelect(ticket._id)}
        >
          <div className="text-sm font-semibold">{ticket.subject}</div>
          <div className="text-xs text-gray-500">{ticket.customer_email}</div>
          <div className="mt-2 flex gap-2 text-xs">
            <span className="rounded bg-slate-200 px-2 py-1">{ticket.status}</span>
            <span className="rounded bg-amber-200 px-2 py-1">{ticket.priority}</span>
          </div>
        </button>
      ))}
    </div>
  )
}
