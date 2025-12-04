// Centralized API configuration
// Use this utility to get the correct API base URL for all API calls

const getApiBaseUrl = (): string => {
  // Check for environment variable first (for production/Vercel)
  if (import.meta.env.VITE_API_BASE_URL) {
    return import.meta.env.VITE_API_BASE_URL.replace(/\/$/, '');
  }
  
  // Development defaults
  if (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1") {
    return "http://localhost:8000";
  } else if (window.location.hostname.startsWith("192.168.")) {
    return `http://${window.location.hostname}:8000`;
  } else {
    // Production - use new Render backend URL
    return "https://capstone-thesis-w018.onrender.com";
  }
};

export const API_BASE_URL = getApiBaseUrl();
export const API_URL = `${API_BASE_URL}/api`;

// Helper function to build full API endpoint URLs
export const buildApiUrl = (endpoint: string): string => {
  const cleanEndpoint = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
  return `${API_URL}${cleanEndpoint}`;
};

// Helper function to build media/image URLs
export const buildMediaUrl = (path: string): string => {
  if (!path) return '';
  if (path.startsWith('http')) return path;
  const cleanPath = path.startsWith('/') ? path : `/${path}`;
  return `${API_BASE_URL}${cleanPath}`;
};

