import React from 'react'
import axios from 'axios'
import { getAuth, signOut } from 'firebase/auth'

function useIdToken() {
	const [token, setToken] = React.useState('')
	React.useEffect(() => {
		const auth = getAuth()
		const unsub = auth.onIdTokenChanged(async (u) => {
			setToken(u ? await u.getIdToken() : '')
		})
		return () => unsub()
	}, [])
	return token
}

export default function Dashboard() {
	const token = useIdToken()
	const [data, setData] = React.useState({ buy_opportunities: [], sell_risks: [] })
	const [loading, setLoading] = React.useState(true)
	const [error, setError] = React.useState('')

	React.useEffect(() => {
		const run = async () => {
			if (!token) return
			setLoading(true)
			setError('')
			try {
				const api = import.meta.env.VITE_API_BASE_URL
				const res = await axios.get(`${api}/api/colcap/scan`, { headers: { Authorization: `Bearer ${token}` } })
				setData(res.data)
			} catch (e) {
				setError(e.message)
			} finally {
				setLoading(false)
			}
		}
		run()
	}, [token])

	const auth = getAuth()

	return (
		<div style={{ padding: 24 }}>
			<div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
				<h2 style={{ margin: 0 }}>Oportunidades de Mercado (COLCAP)</h2>
				<button onClick={() => signOut(auth)}>Salir</button>
			</div>
			{loading && <p>Cargando...</p>}
			{error && <p style={{ color: 'crimson' }}>{error}</p>}
			<div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 24, marginTop: 24 }}>
				<section>
					<h3>Oportunidades de compra</h3>
					<div style={{ display: 'grid', gap: 12 }}>
						{data.buy_opportunities.map((x) => (
							<div key={x.symbol} style={{ border: '1px solid #e5e7eb', borderRadius: 10, padding: 12 }}>
								<strong>{x.symbol}</strong> - {x.name}
								<div>Score: {x.score}</div>
								<div>RSI: {Math.round(x.indicators.rsi)}</div>
							</div>
						))}
					</div>
				</section>
				<section>
					<h3>Potencial caída</h3>
					<div style={{ display: 'grid', gap: 12 }}>
						{data.sell_risks.map((x) => (
							<div key={x.symbol} style={{ border: '1px solid #e5e7eb', borderRadius: 10, padding: 12 }}>
								<strong>{x.symbol}</strong> - {x.name}
								<div>Score: {x.score}</div>
								<div>RSI: {Math.round(x.indicators.rsi)}</div>
							</div>
						))}
					</div>
				</section>
			</div>
		</div>
	)
}