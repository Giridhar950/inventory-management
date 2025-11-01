import api from './api';
import { API_ENDPOINTS } from '../constants/api';

export const productService = {
  getProducts: async (params = {}) => {
    const response = await api.get(API_ENDPOINTS.PRODUCTS, { params });
    return response.data;
  },

  getProductById: async (id) => {
    const response = await api.get(API_ENDPOINTS.PRODUCT_BY_ID(id));
    return response.data;
  },

  getProductByBarcode: async (barcode) => {
    const response = await api.get(API_ENDPOINTS.PRODUCT_BY_BARCODE(barcode));
    return response.data;
  },

  createProduct: async (productData) => {
    const response = await api.post(API_ENDPOINTS.PRODUCTS, productData);
    return response.data;
  },

  updateProduct: async (id, productData) => {
    const response = await api.put(API_ENDPOINTS.PRODUCT_BY_ID(id), productData);
    return response.data;
  },

  deleteProduct: async (id) => {
    const response = await api.delete(API_ENDPOINTS.PRODUCT_BY_ID(id));
    return response.data;
  },

  searchProducts: async (query) => {
    const response = await api.get(API_ENDPOINTS.PRODUCTS, { params: { search: query } });
    return response.data;
  },
};
