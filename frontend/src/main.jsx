import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { AuthProvider } from './context/AuthContext'  // Add this import
import './index.css'
import App from './App.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <AuthProvider>  {/* Wrap App with AuthProvider */}
      <App />
    </AuthProvider>
  </StrictMode>
)