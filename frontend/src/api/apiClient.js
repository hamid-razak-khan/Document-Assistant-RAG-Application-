import axios from "axios";

const api = axios.create({
  baseURL: process.env.REACT_APP_API_BASE_URL,
  timeout: 30000, // 30 second timeout
});

// Add response interceptor to handle network errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.code === 'ECONNABORTED') {
      console.error('Request timeout');
      throw new Error('Request timed out. Please try again.');
    }
    if (!error.response) {
      console.error('Network error');
      throw new Error('Network error. Please check your connection and try again.');
    }
    return Promise.reject(error);
  }
);

export default api;