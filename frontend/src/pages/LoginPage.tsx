import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { login } from '../api/auth'

export function LoginPage() {
  const [email, setEmail] = useState('agent@demo.com')
  const [password, setPassword] = useState('Password123!')
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const submit = async () => {
    try {
      const { data } = await login(email, password)
      localStorage.setItem('token', data.access_token)
      navigate('/inbox')
    } catch {
      setError('Invalid credentials')
    }
  }

  return (
    <div className="mx-auto mt-20 max-w-md rounded-lg bg-white p-6 shadow">
      <h2 className="mb-4 text-xl font-semibold">Agent Login</h2>
      <input className="mb-3 w-full rounded border p-2" value={email} onChange={(e) => setEmail(e.target.value)} />
      <input type="password" className="mb-3 w-full rounded border p-2" value={password} onChange={(e) => setPassword(e.target.value)} />
      {error && <p className="mb-2 text-sm text-red-600">{error}</p>}
      <button className="w-full rounded bg-indigo-600 py-2 text-white" onClick={submit}>Login</button>
    </div>
  )
}
