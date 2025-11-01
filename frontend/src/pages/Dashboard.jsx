import { useState, useEffect } from 'react';
import {
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
} from '@mui/material';
import {
  TrendingUp,
  Inventory,
  ShoppingCart,
  Warning,
} from '@mui/icons-material';
import { analyticsService } from '../services/analyticsService';
import { inventoryService } from '../services/inventoryService';

const StatCard = ({ title, value, icon, color }) => (
  <Card>
    <CardContent>
      <Box display="flex" justifyContent="space-between" alignItems="center">
        <Box>
          <Typography color="textSecondary" gutterBottom variant="body2">
            {title}
          </Typography>
          <Typography variant="h4">{value}</Typography>
        </Box>
        <Box
          sx={{
            backgroundColor: color,
            borderRadius: '50%',
            width: 60,
            height: 60,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          {icon}
        </Box>
      </Box>
    </CardContent>
  </Card>
);

const Dashboard = () => {
  const [salesSummary, setSalesSummary] = useState(null);
  const [inventoryMetrics, setInventoryMetrics] = useState(null);
  const [lowStockItems, setLowStockItems] = useState([]);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      const [sales, inventory, lowStock] = await Promise.all([
        analyticsService.getSalesSummary(),
        analyticsService.getInventoryMetrics(),
        inventoryService.getLowStockItems(),
      ]);
      setSalesSummary(sales);
      setInventoryMetrics(inventory);
      setLowStockItems(lowStock);
    } catch (error) {
      console.error('Error loading dashboard data:', error);
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>
      
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Total Sales"
            value={`$${salesSummary?.total_sales?.toFixed(2) || '0.00'}`}
            icon={<TrendingUp style={{ color: 'white', fontSize: 30 }} />}
            color="#4caf50"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Transactions"
            value={salesSummary?.total_transactions || 0}
            icon={<ShoppingCart style={{ color: 'white', fontSize: 30 }} />}
            color="#2196f3"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Total Items"
            value={inventoryMetrics?.total_items || 0}
            icon={<Inventory style={{ color: 'white', fontSize: 30 }} />}
            color="#ff9800"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Low Stock Items"
            value={inventoryMetrics?.low_stock_items || 0}
            icon={<Warning style={{ color: 'white', fontSize: 30 }} />}
            color="#f44336"
          />
        </Grid>
      </Grid>

      {lowStockItems.length > 0 && (
        <Paper sx={{ p: 2, mt: 2 }}>
          <Typography variant="h6" gutterBottom>
            Low Stock Alerts
          </Typography>
          <Box>
            {lowStockItems.slice(0, 5).map((item) => (
              <Box
                key={item.inventory_id}
                sx={{
                  p: 1,
                  borderBottom: '1px solid #eee',
                  display: 'flex',
                  justifyContent: 'space-between',
                }}
              >
                <Typography>{item.product_name}</Typography>
                <Typography color="error">
                  Stock: {item.quantity} (Reorder: {item.reorder_level})
                </Typography>
              </Box>
            ))}
          </Box>
        </Paper>
      )}
    </Box>
  );
};

export default Dashboard;
