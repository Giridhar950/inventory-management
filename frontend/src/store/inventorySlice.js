import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { inventoryService } from '../services/inventoryService';

export const fetchInventory = createAsyncThunk(
  'inventory/fetchInventory',
  async (storeId, { rejectWithValue }) => {
    try {
      const data = await inventoryService.getInventory(storeId);
      return data;
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Failed to fetch inventory');
    }
  }
);

export const fetchLowStock = createAsyncThunk(
  'inventory/fetchLowStock',
  async (storeId, { rejectWithValue }) => {
    try {
      const data = await inventoryService.getLowStockItems(storeId);
      return data;
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Failed to fetch low stock items');
    }
  }
);

const inventorySlice = createSlice({
  name: 'inventory',
  initialState: {
    items: [],
    lowStockItems: [],
    loading: false,
    error: null,
  },
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchInventory.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchInventory.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload;
      })
      .addCase(fetchInventory.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(fetchLowStock.fulfilled, (state, action) => {
        state.lowStockItems = action.payload;
      });
  },
});

export const { clearError } = inventorySlice.actions;
export default inventorySlice.reducer;
