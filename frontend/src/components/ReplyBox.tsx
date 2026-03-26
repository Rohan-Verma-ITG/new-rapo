import { useState } from 'react'

type Props = {
  onSend: (body: string) => Promise<void>
  onAIAutofill: () => Promise<void>
  aiReply: string
}

export function ReplyBox({ onSend, onAIAutofill, aiReply }: Props) {
  const [text, setText] = useState('')

  return (
    <div className="space-y-2 rounded-lg bg-white p-3">
      <div className="flex gap-2">
        <button className="rounded bg-indigo-600 px-3 py-2 text-sm text-white" onClick={onAIAutofill}>AI Suggest</button>
      </div>
      {aiReply && <div className="rounded border border-indigo-200 bg-indigo-50 p-2 text-sm">{aiReply}</div>}
      <textarea
        className="h-28 w-full rounded border p-2"
        value={text || aiReply}
        onChange={(e) => setText(e.target.value)}
        placeholder="Write your reply..."
      />
      <button className="rounded bg-emerald-600 px-3 py-2 text-sm text-white" onClick={() => onSend(text || aiReply)}>
        Send
      </button>
    </div>
  )
}
