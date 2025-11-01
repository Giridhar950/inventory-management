import { configureStore } from '@reduxjs/toolkit';
import authReducer from './authSlice';
import cartReducer from './cartSlice';
import inventoryReducer from './inventorySlice';

const store = configureStore({
  reducer: {
    auth: authReducer,
    cart: cartReducer,
    inventory: inventoryReducer,
  },
});

export default store;
