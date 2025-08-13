import React from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { initializeApp } from 'firebase/app'
import { getAuth, onAuthStateChanged } from 'firebase/auth'
import LoginPage from './pages/LoginPage'
import Dashboard from './pages/Dashboard'
import './styles.css'

const firebaseConfig = {
	apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
	authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
	projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
	appId: import.meta.env.VITE_FIREBASE_APP_ID,
	messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
	storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
}

initializeApp(firebaseConfig)

function App() {
	const [user, setUser] = React.useState(null)
	React.useEffect(() => {
		const auth = getAuth()
		return onAuthStateChanged(auth, (u) => setUser(u))
	}, [])
	return (
		<BrowserRouter>
			<Routes>
				<Route path="/login" element={<LoginPage />} />
				<Route path="/" element={user ? <Dashboard /> : <Navigate to="/login" replace />} />
			</Routes>
		</BrowserRouter>
	)
}

createRoot(document.getElementById('root')).render(<App />)