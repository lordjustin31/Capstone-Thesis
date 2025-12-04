// src/utils/config.ts

let API_URL = "";

// Use environment variable if set (for Vercel/production)
const envApiUrl = import.meta.env.VITE_API_BASE_URL;
if (envApiUrl) {
  API_URL = `${envApiUrl.replace(/\/$/, '')}/api`;
} else if (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1") {
  // Dev desktop
  API_URL = "http://localhost:8000/api";
} else if (window.location.hostname.startsWith("192.168.")) {
  // LAN access from phone
  API_URL = `http://${window.location.hostname}:8000/api`;
} else {
  // Production - use new Render backend URL
  API_URL = "https://capstone-thesis-w018.onrender.com/api";
}

export default API_URL;
