import api from './api';
import { API_ENDPOINTS } from '../constants/api';

export const analyticsService = {
  getSalesSummary: async (startDate = null, endDate = null) => {
    const params = {};
    if (startDate) params.start_date = startDate;
    if (endDate) params.end_date = endDate;
    const response = await api.get(API_ENDPOINTS.ANALYTICS_SALES_SUMMARY, { params });
    return response.data;
  },

  getTopProducts: async (limit = 10, startDate = null, endDate = null) => {
    const params = { limit };
    if (startDate) params.start_date = startDate;
    if (endDate) params.end_date = endDate;
    const response = await api.get(API_ENDPOINTS.ANALYTICS_TOP_PRODUCTS, { params });
    return response.data;
  },

  getInventoryMetrics: async () => {
    const response = await api.get(API_ENDPOINTS.ANALYTICS_INVENTORY_METRICS);
    return response.data;
  },

  getDailySales: async (days = 30) => {
    const response = await api.get(API_ENDPOINTS.ANALYTICS_DAILY_SALES, { params: { days } });
    return response.data;
  },

  getCustomerInsights: async (limit = 10) => {
    const response = await api.get(API_ENDPOINTS.ANALYTICS_CUSTOMER_INSIGHTS, { params: { limit } });
    return response.data;
  },
};
