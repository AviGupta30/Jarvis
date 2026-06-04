import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

// StrictMode removed: it double-invokes async effects in dev mode,
// which causes the streaming reader to run twice → duplicated text.
createRoot(document.getElementById('root')).render(<App />)
