import { Message } from '../types'

export function MessageThread({ messages }: { messages: Message[] }) {
  return (
    <div className="space-y-3">
      {messages.map((m) => (
        <div key={m._id} className="rounded-lg bg-white p-3 shadow-sm">
          <div className="text-xs text-gray-500">{m.sender_email} · {new Date(m.created_at).toLocaleString()}</div>
          <p className="mt-1 text-sm text-slate-900 whitespace-pre-wrap">{m.body}</p>
        </div>
      ))}
    </div>
  )
}
