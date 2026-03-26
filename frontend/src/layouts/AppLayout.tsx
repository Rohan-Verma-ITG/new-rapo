import { Outlet, Link } from 'react-router-dom'

export function AppLayout() {
  return (
    <div className="flex min-h-screen">
      <aside className="w-64 bg-slate-900 p-4 text-white">
        <h1 className="text-lg font-bold">AI Helpdesk</h1>
        <nav className="mt-6 space-y-2">
          <Link className="block rounded bg-slate-800 px-3 py-2" to="/inbox">Inbox</Link>
        </nav>
      </aside>
      <main className="flex-1 p-4">
        <Outlet />
      </main>
    </div>
  )
}
