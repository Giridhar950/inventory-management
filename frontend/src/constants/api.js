export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

export const API_ENDPOINTS = {
  // Auth
  LOGIN: '/auth/login',
  REGISTER: '/auth/register',
  
  // Products
  PRODUCTS: '/products',
  PRODUCT_BY_ID: (id) => `/products/${id}`,
  PRODUCT_BY_BARCODE: (barcode) => `/products/barcode/${barcode}`,
  
  // Inventory
  INVENTORY: '/inventory',
  INVENTORY_LOW_STOCK: '/inventory/low-stock',
  INVENTORY_EXPIRY_RISK: '/inventory/expiry-risk',
  INVENTORY_ADJUST: '/inventory/adjust',
  
  // Sales
  SALES: '/sales',
  SALE_BY_ID: (id) => `/sales/${id}`,
  
  // Customers
  CUSTOMERS: '/customers',
  CUSTOMER_BY_ID: (id) => `/customers/${id}`,
  CUSTOMER_BY_PHONE: (phone) => `/customers/phone/${phone}`,
  
  // Users
  USERS: '/users',
  USER_ME: '/users/me',
  USER_BY_ID: (id) => `/users/${id}`,
  
  // Analytics
  ANALYTICS_SALES_SUMMARY: '/analytics/sales-summary',
  ANALYTICS_TOP_PRODUCTS: '/analytics/top-products',
  ANALYTICS_INVENTORY_METRICS: '/analytics/inventory-metrics',
  ANALYTICS_DAILY_SALES: '/analytics/daily-sales',
  ANALYTICS_CUSTOMER_INSIGHTS: '/analytics/customer-insights',
};

export const UserRole = {
  ADMIN: 'admin',
  MANAGER: 'manager',
  CASHIER: 'cashier',
  STOCK_KEEPER: 'stock_keeper',
};

export const PaymentMethod = {
  CASH: 'cash',
  CARD: 'card',
  UPI: 'upi',
  WALLET: 'wallet',
  CHECK: 'check',
};
