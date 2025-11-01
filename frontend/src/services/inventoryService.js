import api from './api';
import { API_ENDPOINTS } from '../constants/api';

export const inventoryService = {
  getInventory: async (storeId = null) => {
    const params = storeId ? { store_id: storeId } : {};
    const response = await api.get(API_ENDPOINTS.INVENTORY, { params });
    return response.data;
  },

  getLowStockItems: async (storeId = null) => {
    const params = storeId ? { store_id: storeId } : {};
    const response = await api.get(API_ENDPOINTS.INVENTORY_LOW_STOCK, { params });
    return response.data;
  },

  getExpiryRiskItems: async (days = 30) => {
    const response = await api.get(API_ENDPOINTS.INVENTORY_EXPIRY_RISK, { params: { days } });
    return response.data;
  },

  adjustInventory: async (adjustmentData) => {
    const response = await api.post(API_ENDPOINTS.INVENTORY_ADJUST, adjustmentData);
    return response.data;
  },
};
