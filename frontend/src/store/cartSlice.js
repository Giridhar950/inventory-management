import { createSlice } from '@reduxjs/toolkit';

const cartSlice = createSlice({
  name: 'cart',
  initialState: {
    items: [],
    customer: null,
    discount: 0,
    taxRate: 0,
  },
  reducers: {
    addToCart: (state, action) => {
      const product = action.payload;
      const existingItem = state.items.find(item => item.product_id === product.product_id);
      
      if (existingItem) {
        existingItem.quantity += 1;
      } else {
        state.items.push({
          ...product,
          quantity: 1,
        });
      }
    },
    removeFromCart: (state, action) => {
      state.items = state.items.filter(item => item.product_id !== action.payload);
    },
    updateQuantity: (state, action) => {
      const { product_id, quantity } = action.payload;
      const item = state.items.find(item => item.product_id === product_id);
      if (item && quantity > 0) {
        item.quantity = quantity;
      }
    },
    clearCart: (state) => {
      state.items = [];
      state.customer = null;
      state.discount = 0;
    },
    setCustomer: (state, action) => {
      state.customer = action.payload;
    },
    setDiscount: (state, action) => {
      state.discount = action.payload;
    },
    setTaxRate: (state, action) => {
      state.taxRate = action.payload;
    },
  },
});

export const {
  addToCart,
  removeFromCart,
  updateQuantity,
  clearCart,
  setCustomer,
  setDiscount,
  setTaxRate,
} = cartSlice.actions;

export default cartSlice.reducer;
