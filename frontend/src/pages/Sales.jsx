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
  Chip,
} from '@mui/material';
import { saleService } from '../services/saleService';
import { format } from 'date-fns';

const Sales = () => {
  const [sales, setSales] = useState([]);

  useEffect(() => {
    loadSales();
  }, []);

  const loadSales = async () => {
    try {
      const data = await saleService.getSales();
      setSales(data);
    } catch (error) {
      console.error('Error loading sales:', error);
    }
  };

  const getPaymentMethodColor = (method) => {
    const colors = {
      cash: 'success',
      card: 'primary',
      upi: 'info',
      wallet: 'secondary',
    };
    return colors[method] || 'default';
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Sales History
      </Typography>

      <Paper sx={{ p: 2 }}>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Receipt Number</TableCell>
                <TableCell>Date</TableCell>
                <TableCell align="right">Total Amount</TableCell>
                <TableCell align="right">Discount</TableCell>
                <TableCell align="right">Final Amount</TableCell>
                <TableCell>Payment Method</TableCell>
                <TableCell align="right">Items</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {sales.map((sale) => (
                <TableRow key={sale.sale_id}>
                  <TableCell>{sale.receipt_number}</TableCell>
                  <TableCell>
                    {format(new Date(sale.date), 'MMM dd, yyyy HH:mm')}
                  </TableCell>
                  <TableCell align="right">${sale.total_amount.toFixed(2)}</TableCell>
                  <TableCell align="right">${sale.discount_amount.toFixed(2)}</TableCell>
                  <TableCell align="right">
                    <strong>${sale.final_amount.toFixed(2)}</strong>
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={sale.payment_method.toUpperCase()}
                      color={getPaymentMethodColor(sale.payment_method)}
                      size="small"
                    />
                  </TableCell>
                  <TableCell align="right">{sale.line_items?.length || 0}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>
    </Box>
  );
};

export default Sales;
