import { createSlice } from '@reduxjs/toolkit';

// Load cart from localStorage
const loadCartFromStorage = () => {
  try {
    const serializedCart = localStorage.getItem('shopping_cart');
    if (serializedCart === null) {
      return { items: [], customer: null, discount: 0, taxRate: 0 };
    }
    return JSON.parse(serializedCart);
  } catch (err) {
    console.error('Error loading cart from storage:', err);
    return { items: [], customer: null, discount: 0, taxRate: 0 };
  }
};

// Save cart to localStorage
const saveCartToStorage = (state) => {
  try {
    const serializedCart = JSON.stringify(state);
    localStorage.setItem('shopping_cart', serializedCart);
  } catch (err) {
    console.error('Error saving cart to storage:', err);
  }
};

const cartSlice = createSlice({
  name: 'cart',
  initialState: loadCartFromStorage(),
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
      saveCartToStorage(state);
    },
    removeFromCart: (state, action) => {
      state.items = state.items.filter(item => item.product_id !== action.payload);
      saveCartToStorage(state);
    },
    updateQuantity: (state, action) => {
      const { product_id, quantity } = action.payload;
      const item = state.items.find(item => item.product_id === product_id);
      if (item && quantity > 0) {
        item.quantity = quantity;
      }
      saveCartToStorage(state);
    },
    clearCart: (state) => {
      state.items = [];
      state.customer = null;
      state.discount = 0;
      saveCartToStorage(state);
    },
    setCustomer: (state, action) => {
      state.customer = action.payload;
      saveCartToStorage(state);
    },
    setDiscount: (state, action) => {
      state.discount = action.payload;
      saveCartToStorage(state);
    },
    setTaxRate: (state, action) => {
      state.taxRate = action.payload;
      saveCartToStorage(state);
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
