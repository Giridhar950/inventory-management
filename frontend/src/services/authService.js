import api from './api';
import { API_ENDPOINTS } from '../constants/api';

export const authService = {
  login: async (username, password) => {
    const response = await api.post(API_ENDPOINTS.LOGIN, { username, password });
    if (response.data.access_token) {
      localStorage.setItem('access_token', response.data.access_token);
      localStorage.setItem('refresh_token', response.data.refresh_token);
    }
    return response.data;
  },

  register: async (userData) => {
    const response = await api.post(API_ENDPOINTS.REGISTER, userData);
    return response.data;
  },

  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  },

  getCurrentUser: async () => {
    const response = await api.get(API_ENDPOINTS.USER_ME);
    return response.data;
  },

  isAuthenticated: () => {
    return !!localStorage.getItem('access_token');
  },
};
