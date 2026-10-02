// Backend base URL. Override with VITE_API_URL in frontend/.env (e.g. VITE_API_URL=http://192.168.1.5:8000).
export const API_BASE = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';
