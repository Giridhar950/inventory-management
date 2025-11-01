import api from './api';
import { API_ENDPOINTS } from '../constants/api';

export const saleService = {
  createSale: async (saleData) => {
    const response = await api.post(API_ENDPOINTS.SALES, saleData);
    return response.data;
  },

  getSales: async (params = {}) => {
    const response = await api.get(API_ENDPOINTS.SALES, { params });
    return response.data;
  },

  getSaleById: async (id) => {
    const response = await api.get(API_ENDPOINTS.SALE_BY_ID(id));
    return response.data;
  },
};
