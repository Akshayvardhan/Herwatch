// Centralized API configuration for production and local environments
export const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001';
export const WS_BASE_URL = process.env.REACT_APP_WS_URL || API_BASE_URL.replace(/^http/, 'ws');
