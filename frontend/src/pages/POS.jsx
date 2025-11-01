import { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import {
  Grid,
  Paper,
  Typography,
  Box,
  TextField,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  IconButton,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Alert,
} from '@mui/material';
import {
  Delete,
  Add,
  Remove,
  QrCodeScanner,
} from '@mui/icons-material';
import { addToCart, removeFromCart, updateQuantity, clearCart, setDiscount } from '../store/cartSlice';
import { productService } from '../services/productService';
import { saleService } from '../services/saleService';
import { PaymentMethod } from '../constants/api';

const POS = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [paymentMethod, setPaymentMethod] = useState(PaymentMethod.CASH);
  const [showCheckout, setShowCheckout] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  
  const dispatch = useDispatch();
  const cart = useSelector((state) => state.cart);

  const handleSearch = async () => {
    if (!searchQuery.trim()) return;
    
    try {
      const results = await productService.searchProducts(searchQuery);
      setSearchResults(results);
    } catch (error) {
      console.error('Search error:', error);
    }
  };

  const handleAddToCart = (product) => {
    dispatch(addToCart(product));
    setSearchQuery('');
    setSearchResults([]);
  };

  const handleQuantityChange = (productId, delta) => {
    const item = cart.items.find((i) => i.product_id === productId);
    if (item) {
      const newQuantity = item.quantity + delta;
      if (newQuantity > 0) {
        dispatch(updateQuantity({ product_id: productId, quantity: newQuantity }));
      } else {
        dispatch(removeFromCart(productId));
      }
    }
  };

  const calculateTotal = () => {
    const subtotal = cart.items.reduce((sum, item) => sum + item.price * item.quantity, 0);
    const discount = cart.discount || 0;
    const tax = (subtotal - discount) * 0.1; // 10% tax
    return {
      subtotal: subtotal.toFixed(2),
      discount: discount.toFixed(2),
      tax: tax.toFixed(2),
      total: (subtotal - discount + tax).toFixed(2),
    };
  };

  const handleCheckout = async () => {
    const totals = calculateTotal();
    
    const saleData = {
      payment_method: paymentMethod,
      line_items: cart.items.map((item) => ({
        product_id: item.product_id,
        quantity: item.quantity,
        unit_price: item.price,
        discount: 0,
      })),
      discount_amount: parseFloat(cart.discount || 0),
      tax_rate: 10,
    };

    try {
      const result = await saleService.createSale(saleData);
      setSuccessMessage(`Sale completed! Receipt: ${result.receipt_number}`);
      dispatch(clearCart());
      setShowCheckout(false);
      
      setTimeout(() => setSuccessMessage(''), 5000);
    } catch (error) {
      setErrorMessage(error.response?.data?.detail || 'Checkout failed');
      setTimeout(() => setErrorMessage(''), 5000);
    }
  };

  const totals = calculateTotal();

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Point of Sale (POS)
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

      <Grid container spacing={3}>
        <Grid item xs={12} md={7}>
          <Paper sx={{ p: 2 }}>
            <Box sx={{ mb: 2, display: 'flex', gap: 1 }}>
              <TextField
                fullWidth
                label="Search Products (Name, SKU, Barcode)"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
              />
              <Button variant="contained" onClick={handleSearch}>
                Search
              </Button>
            </Box>

            {searchResults.length > 0 && (
              <Box sx={{ mb: 2 }}>
                <Typography variant="h6">Search Results</Typography>
                {searchResults.map((product) => (
                  <Paper
                    key={product.product_id}
                    sx={{
                      p: 1,
                      mb: 1,
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      cursor: 'pointer',
                    }}
                    onClick={() => handleAddToCart(product)}
                  >
                    <Box>
                      <Typography variant="body1">{product.name}</Typography>
                      <Typography variant="body2" color="textSecondary">
                        SKU: {product.sku} | ${product.price}
                      </Typography>
                    </Box>
                    <Button size="small" variant="outlined">
                      Add
                    </Button>
                  </Paper>
                ))}
              </Box>
            )}

            <Typography variant="h6" gutterBottom>
              Cart Items
            </Typography>
            <TableContainer>
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>Product</TableCell>
                    <TableCell align="center">Quantity</TableCell>
                    <TableCell align="right">Price</TableCell>
                    <TableCell align="right">Total</TableCell>
                    <TableCell align="center">Actions</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {cart.items.map((item) => (
                    <TableRow key={item.product_id}>
                      <TableCell>{item.name}</TableCell>
                      <TableCell align="center">
                        <IconButton
                          size="small"
                          onClick={() => handleQuantityChange(item.product_id, -1)}
                        >
                          <Remove fontSize="small" />
                        </IconButton>
                        {item.quantity}
                        <IconButton
                          size="small"
                          onClick={() => handleQuantityChange(item.product_id, 1)}
                        >
                          <Add fontSize="small" />
                        </IconButton>
                      </TableCell>
                      <TableCell align="right">${item.price}</TableCell>
                      <TableCell align="right">
                        ${(item.price * item.quantity).toFixed(2)}
                      </TableCell>
                      <TableCell align="center">
                        <IconButton
                          size="small"
                          color="error"
                          onClick={() => dispatch(removeFromCart(item.product_id))}
                        >
                          <Delete fontSize="small" />
                        </IconButton>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Paper>
        </Grid>

        <Grid item xs={12} md={5}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Order Summary
            </Typography>
            
            <Box sx={{ mb: 2 }}>
              <Box display="flex" justifyContent="space-between" mb={1}>
                <Typography>Subtotal:</Typography>
                <Typography>${totals.subtotal}</Typography>
              </Box>
              <Box display="flex" justifyContent="space-between" mb={1}>
                <Typography>Discount:</Typography>
                <TextField
                  size="small"
                  type="number"
                  value={cart.discount}
                  onChange={(e) => dispatch(setDiscount(parseFloat(e.target.value) || 0))}
                  sx={{ width: 100 }}
                />
              </Box>
              <Box display="flex" justifyContent="space-between" mb={1}>
                <Typography>Tax (10%):</Typography>
                <Typography>${totals.tax}</Typography>
              </Box>
              <Box display="flex" justifyContent="space-between" mb={2}>
                <Typography variant="h6">Total:</Typography>
                <Typography variant="h6">${totals.total}</Typography>
              </Box>
            </Box>

            <FormControl fullWidth sx={{ mb: 2 }}>
              <InputLabel>Payment Method</InputLabel>
              <Select
                value={paymentMethod}
                label="Payment Method"
                onChange={(e) => setPaymentMethod(e.target.value)}
              >
                <MenuItem value={PaymentMethod.CASH}>Cash</MenuItem>
                <MenuItem value={PaymentMethod.CARD}>Card</MenuItem>
                <MenuItem value={PaymentMethod.UPI}>UPI</MenuItem>
                <MenuItem value={PaymentMethod.WALLET}>Wallet</MenuItem>
              </Select>
            </FormControl>

            <Button
              fullWidth
              variant="contained"
              size="large"
              disabled={cart.items.length === 0}
              onClick={() => setShowCheckout(true)}
            >
              Checkout (${totals.total})
            </Button>
            
            <Button
              fullWidth
              variant="outlined"
              color="error"
              sx={{ mt: 1 }}
              onClick={() => dispatch(clearCart())}
              disabled={cart.items.length === 0}
            >
              Clear Cart
            </Button>
          </Paper>
        </Grid>
      </Grid>

      <Dialog open={showCheckout} onClose={() => setShowCheckout(false)}>
        <DialogTitle>Confirm Checkout</DialogTitle>
        <DialogContent>
          <Typography>Total Amount: ${totals.total}</Typography>
          <Typography>Payment Method: {paymentMethod.toUpperCase()}</Typography>
          <Typography>Items: {cart.items.length}</Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowCheckout(false)}>Cancel</Button>
          <Button onClick={handleCheckout} variant="contained">
            Confirm Payment
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default POS;
