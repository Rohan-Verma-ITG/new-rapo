export function CustomerPanel({ profile }: { profile: any }) {
  if (!profile) return <div className="rounded-lg bg-white p-3 text-sm">No customer data</div>

  return (
    <div className="space-y-2 rounded-lg bg-white p-3 text-sm">
      <h3 className="font-semibold">Customer</h3>
      <p>{profile.customer_snapshot?.first_name} {profile.customer_snapshot?.last_name}</p>
      <p>{profile.email}</p>
      <h4 className="pt-2 font-semibold">Last Orders</h4>
      <div className="space-y-1">
        {(profile.orders_snapshot || []).slice(0, 10).map((order: any) => (
          <div key={order.id} className="rounded border p-2">
            #{order.order_number || order.id} · {order.financial_status || 'unknown'}
          </div>
        ))}
      </div>
    </div>
  )
}
