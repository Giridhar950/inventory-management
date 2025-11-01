import { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Button,
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Chip,
  Alert,
} from '@mui/material';
import { Warning, CheckCircle } from '@mui/icons-material';
import { inventoryService } from '../services/inventoryService';
import { format } from 'date-fns';

const Inventory = () => {
  const [inventory, setInventory] = useState([]);
  const [openAdjustDialog, setOpenAdjustDialog] = useState(false);
  const [selectedItem, setSelectedItem] = useState(null);
  const [adjustmentQty, setAdjustmentQty] = useState(0);
  const [adjustmentReason, setAdjustmentReason] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  useEffect(() => {
    loadInventory();
  }, []);

  const loadInventory = async () => {
    try {
      const data = await inventoryService.getInventory();
      setInventory(data);
    } catch (error) {
      console.error('Error loading inventory:', error);
    }
  };

  const handleOpenAdjust = (item) => {
    setSelectedItem(item);
    setOpenAdjustDialog(true);
  };

  const handleAdjust = async () => {
    if (!selectedItem || !adjustmentReason) return;

    try {
      await inventoryService.adjustInventory({
        product_id: selectedItem.product_id,
        store_id: selectedItem.store_id,
        quantity_change: parseFloat(adjustmentQty),
        reason: adjustmentReason,
      });
      
      setSuccessMessage('Inventory adjusted successfully');
      setOpenAdjustDialog(false);
      setAdjustmentQty(0);
      setAdjustmentReason('');
      loadInventory();
      
      setTimeout(() => setSuccessMessage(''), 3000);
    } catch (error) {
      setErrorMessage(error.response?.data?.detail || 'Failed to adjust inventory');
      setTimeout(() => setErrorMessage(''), 3000);
    }
  };

  const getStockStatus = (quantity, reorderLevel) => {
    if (quantity === 0) {
      return <Chip label="Out of Stock" color="error" size="small" />;
    } else if (quantity <= reorderLevel) {
      return <Chip label="Low Stock" color="warning" size="small" />;
    } else {
      return <Chip label="In Stock" color="success" size="small" />;
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Inventory Management
      </Typography>

      {successMessage && (
        <Alert severity="success" sx={{ mb: 2 }}>
          {successMessage}
        </Alert>
      )}
      
      {errorMessage && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {errorMessage}
        </Alert>
      )}

      <Paper sx={{ p: 2 }}>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Product</TableCell>
                <TableCell>SKU</TableCell>
                <TableCell align="right">Quantity</TableCell>
                <TableCell align="right">Reorder Level</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>Expiry Date</TableCell>
                <TableCell align="center">Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {inventory.map((item) => (
                <TableRow key={item.inventory_id}>
                  <TableCell>{item.product_name}</TableCell>
                  <TableCell>{item.product_sku}</TableCell>
                  <TableCell align="right">{item.quantity}</TableCell>
                  <TableCell align="right">{item.reorder_level}</TableCell>
                  <TableCell>
                    {getStockStatus(item.quantity, item.reorder_level)}
                  </TableCell>
                  <TableCell>
                    {item.expiry_date
                      ? format(new Date(item.expiry_date), 'MMM dd, yyyy')
                      : 'N/A'}
                  </TableCell>
                  <TableCell align="center">
                    <Button
                      size="small"
                      variant="outlined"
                      onClick={() => handleOpenAdjust(item)}
                    >
                      Adjust
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>

      <Dialog open={openAdjustDialog} onClose={() => setOpenAdjustDialog(false)}>
        <DialogTitle>Adjust Inventory</DialogTitle>
        <DialogContent>
          {selectedItem && (
            <Box sx={{ pt: 1 }}>
              <Typography variant="body1" gutterBottom>
                Product: {selectedItem.product_name}
              </Typography>
              <Typography variant="body2" gutterBottom>
                Current Quantity: {selectedItem.quantity}
              </Typography>
              
              <TextField
                fullWidth
                label="Adjustment Quantity"
                type="number"
                value={adjustmentQty}
                onChange={(e) => setAdjustmentQty(e.target.value)}
                helperText="Use negative numbers to decrease stock"
                sx={{ mt: 2, mb: 2 }}
              />
              
              <TextField
                fullWidth
                label="Reason"
                value={adjustmentReason}
                onChange={(e) => setAdjustmentReason(e.target.value)}
                multiline
                rows={3}
                required
              />
              
              <Typography variant="body2" color="textSecondary" sx={{ mt: 2 }}>
                New Quantity: {selectedItem.quantity + parseFloat(adjustmentQty || 0)}
              </Typography>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenAdjustDialog(false)}>Cancel</Button>
          <Button onClick={handleAdjust} variant="contained">
            Adjust
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Inventory;
