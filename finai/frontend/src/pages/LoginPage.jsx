import React from 'react'
import { getAuth, GoogleAuthProvider, signInWithPopup } from 'firebase/auth'

export default function LoginPage() {
	const [error, setError] = React.useState('')
	const handleGoogle = async () => {
		setError('')
		try {
			const auth = getAuth()
			const provider = new GoogleAuthProvider()
			await signInWithPopup(auth, provider)
		} catch (e) {
			setError(e.message)
		}
	}
	return (
		<div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100vh' }}>
			<div style={{ width: 360, background: 'white', padding: 24, borderRadius: 12, boxShadow: '0 10px 30px rgba(0,0,0,0.08)' }}>
				<h2 style={{ marginTop: 0 }}>FinAI</h2>
				<p>Inicia sesión para continuar</p>
				<button onClick={handleGoogle} style={{ width: '100%', padding: '10px 12px', borderRadius: 8, border: '1px solid #e5e7eb', background: '#fff', cursor: 'pointer' }}>Continuar con Google</button>
				{error && <p style={{ color: 'crimson' }}>{error}</p>}
			</div>
		</div>
	)
}