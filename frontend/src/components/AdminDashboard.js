// Comprehensive Admin Dashboard Component
import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';

const AdminDashboard = () => {
  const { t } = useTranslation();
  const [dashboardData, setDashboardData] = useState(null);
  const [realTimeStats, setRealTimeStats] = useState(null);
  const [chartData, setChartData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedPeriod, setSelectedPeriod] = useState('daily');
  const [selectedMetric, setSelectedMetric] = useState('transactions');
  const [isAdmin, setIsAdmin] = useState(false);

  const API_BASE = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';

  // Check if user is admin
  useEffect(() => {
    const checkAdminStatus = async () => {
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          setError('Please login to access admin dashboard');
          setLoading(false);
          return;
        }

        // Try to access admin endpoint to verify admin status
        const response = await fetch(`${API_BASE}/api/admin/dashboard/real-time`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        if (response.status === 403) {
          setError('Admin access required. You do not have admin privileges.');
          setLoading(false);
          return;
        }

        if (response.ok) {
          setIsAdmin(true);
          loadDashboardData();
          loadRealTimeStats();
          loadChartData();
        } else {
          setError('Failed to verify admin access');
          setLoading(false);
        }
      } catch (err) {
        setError('Failed to connect to admin dashboard');
        setLoading(false);
      }
    };

    checkAdminStatus();
  }, []);

  // Load main dashboard data
  const loadDashboardData = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(
        `${API_BASE}/api/admin/dashboard/overview?period=${selectedPeriod}`,
        {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }
      );

      if (response.ok) {
        const data = await response.json();
        setDashboardData(data.data);
      } else {
        throw new Error('Failed to load dashboard data');
      }
    } catch (err) {
      console.error('Dashboard data error:', err);
      setError('Failed to load dashboard data');
    }
  };

  // Load real-time statistics
  const loadRealTimeStats = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_BASE}/api/admin/dashboard/real-time`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        setRealTimeStats(data.data);
      }
    } catch (err) {
      console.error('Real-time stats error:', err);
    }
  };

  // Load chart data
  const loadChartData = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(
        `${API_BASE}/api/admin/dashboard/charts/${selectedMetric}?period=${selectedPeriod}&days_back=30`,
        {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }
      );

      if (response.ok) {
        const data = await response.json();
        setChartData(data.data);
      }
    } catch (err) {
      console.error('Chart data error:', err);
    }
  };

  // Refresh all data
  const refreshData = async () => {
    setLoading(true);
    setError(null);
    
    await Promise.all([
      loadDashboardData(),
      loadRealTimeStats(),
      loadChartData()
    ]);
    
    setLoading(false);
  };

  // Handle period change
  const handlePeriodChange = async (newPeriod) => {
    setSelectedPeriod(newPeriod);
    setLoading(true);
    
    await Promise.all([
      loadDashboardData(),
      loadChartData()
    ]);
    
    setLoading(false);
  };

  // Handle metric change
  const handleMetricChange = async (newMetric) => {
    setSelectedMetric(newMetric);
    await loadChartData();
  };

  // Auto-refresh real-time stats every 30 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      if (isAdmin) {
        loadRealTimeStats();
      }
    }, 30000);

    return () => clearInterval(interval);
  }, [isAdmin]);

  // Update data when period changes
  useEffect(() => {
    if (isAdmin && dashboardData) {
      loadDashboardData();
      loadChartData();
    }
  }, [selectedPeriod]);

  // Update chart when metric changes
  useEffect(() => {
    if (isAdmin && chartData) {
      loadChartData();
    }
  }, [selectedMetric]);

  // Format currency
  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  };

  // Format percentage
  const formatPercentage = (value) => {
    return `${value >= 0 ? '+' : ''}${value.toFixed(2)}%`;
  };

  if (!isAdmin && error) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="bg-white p-8 rounded-lg shadow-md max-w-md w-full text-center">
          <div className="text-red-600 text-6xl mb-4">🚫</div>
          <h2 className="text-2xl font-bold text-gray-800 mb-4">Access Denied</h2>
          <p className="text-gray-600 mb-6">{error}</p>
          <button
            onClick={() => window.location.href = '/'}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Return to Homepage
          </button>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="text-2xl text-gray-600">
          <div className="animate-spin h-8 w-8 border-4 border-blue-600 border-t-transparent rounded-full mx-auto mb-4"></div>
          Loading Admin Dashboard...
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                🏢 Lambalia Admin Dashboard
              </h1>
              <p className="text-gray-600 mt-1">
                Monitor platform performance and transactions
              </p>
            </div>
            
            <div className="flex space-x-4">
              {/* Period Selector */}
              <select
                value={selectedPeriod}
                onChange={(e) => handlePeriodChange(e.target.value)}
                className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="daily">Daily</option>
                <option value="weekly">Weekly</option>
                <option value="monthly">Monthly</option>
                <option value="yearly">Yearly</option>
              </select>
              
              {/* Refresh Button */}
              <button
                onClick={refreshData}
                className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors flex items-center space-x-2"
              >
                <span>🔄</span>
                <span>Refresh</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Real-time Stats */}
        {realTimeStats && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <div className="bg-white p-6 rounded-lg shadow-sm">
              <div className="flex items-center">
                <div className="text-3xl text-blue-600 mr-4">📊</div>
                <div>
                  <p className="text-sm text-gray-600">Today's Transactions</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {realTimeStats.today_transactions.toLocaleString()}
                  </p>
                </div>
              </div>
            </div>
            
            <div className="bg-white p-6 rounded-lg shadow-sm">
              <div className="flex items-center">
                <div className="text-3xl text-green-600 mr-4">💰</div>
                <div>
                  <p className="text-sm text-gray-600">Today's Revenue</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {formatCurrency(realTimeStats.today_revenue_usd)}
                  </p>
                </div>
              </div>
            </div>
            
            <div className="bg-white p-6 rounded-lg shadow-sm">
              <div className="flex items-center">
                <div className="text-3xl text-purple-600 mr-4">👥</div>
                <div>
                  <p className="text-sm text-gray-600">Active Users (24h)</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {realTimeStats.active_users_24h.toLocaleString()}
                  </p>
                </div>
              </div>
            </div>
            
            <div className="bg-white p-6 rounded-lg shadow-sm">
              <div className="flex items-center">
                <div className="text-3xl text-orange-600 mr-4">⏳</div>
                <div>
                  <p className="text-sm text-gray-600">Pending Transactions</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {realTimeStats.pending_transactions.toLocaleString()}
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Main Dashboard Data */}
        {dashboardData && (
          <>
            {/* Key Metrics */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
              <div className="bg-white p-6 rounded-lg shadow-sm">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">
                  📈 Transaction Overview
                </h3>
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Total Transactions</span>
                    <span className="font-semibold">
                      {dashboardData.total_transactions.toLocaleString()}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Transaction Volume</span>
                    <span className="font-semibold">
                      {formatCurrency(dashboardData.transaction_volume_usd)}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Commission Earned</span>
                    <span className="font-semibold text-green-600">
                      {formatCurrency(dashboardData.commission_earned_usd)}
                    </span>
                  </div>
                </div>
              </div>

              <div className="bg-white p-6 rounded-lg shadow-sm">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">
                  👥 User Metrics
                </h3>
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Total Users</span>
                    <span className="font-semibold">
                      {dashboardData.total_users.toLocaleString()}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">New Users</span>
                    <span className="font-semibold text-blue-600">
                      {dashboardData.new_users.toLocaleString()}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Active Users</span>
                    <span className="font-semibold text-purple-600">
                      {dashboardData.active_users.toLocaleString()}
                    </span>
                  </div>
                </div>
              </div>

              <div className="bg-white p-6 rounded-lg shadow-sm">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">
                  🚀 Platform Performance
                </h3>
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Total Orders</span>
                    <span className="font-semibold">
                      {dashboardData.total_orders.toLocaleString()}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">LOD Offers</span>
                    <span className="font-semibold">
                      {dashboardData.total_offers.toLocaleString()}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Completion Rate</span>
                    <span className="font-semibold text-green-600">
                      {dashboardData.completion_rate.toFixed(1)}%
                    </span>
                  </div>
                </div>
              </div>
            </div>

            {/* Growth Metrics */}
            <div className="bg-white p-6 rounded-lg shadow-sm mb-8">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                📊 Growth Analysis
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <p className="text-sm text-gray-600 mb-2">Growth Rate vs Previous Period</p>
                  <p className={`text-2xl font-bold ${
                    dashboardData.growth_rate >= 0 ? 'text-green-600' : 'text-red-600'
                  }`}>
                    {formatPercentage(dashboardData.growth_rate)}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-600 mb-2">Previous Period Volume</p>
                  <p className="text-xl font-semibold text-gray-900">
                    {formatCurrency(dashboardData.previous_period_volume)}
                  </p>
                </div>
              </div>
            </div>

            {/* Revenue Breakdown */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
              {/* By Service */}
              <div className="bg-white p-6 rounded-lg shadow-sm">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">
                  💼 Revenue by Service
                </h3>
                <div className="space-y-2">
                  {Object.entries(dashboardData.revenue_by_service).map(([service, revenue]) => (
                    <div key={service} className="flex justify-between">
                      <span className="text-gray-600 capitalize">{service}</span>
                      <span className="font-semibold">{formatCurrency(revenue)}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* By Currency */}
              <div className="bg-white p-6 rounded-lg shadow-sm">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">
                  💱 Revenue by Currency
                </h3>
                <div className="space-y-2">
                  {Object.entries(dashboardData.revenue_by_currency).slice(0, 5).map(([currency, revenue]) => (
                    <div key={currency} className="flex justify-between">
                      <span className="text-gray-600">{currency}</span>
                      <span className="font-semibold">{formatCurrency(revenue)}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* By Country */}
              <div className="bg-white p-6 rounded-lg shadow-sm">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">
                  🌍 Revenue by Country
                </h3>
                <div className="space-y-2">
                  {Object.entries(dashboardData.revenue_by_country).slice(0, 5).map(([country, revenue]) => (
                    <div key={country} className="flex justify-between">
                      <span className="text-gray-600">{country}</span>
                      <span className="font-semibold">{formatCurrency(revenue)}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Top Performers */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
              {/* Top Earners */}
              <div className="bg-white p-6 rounded-lg shadow-sm">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">
                  🏆 Top Earners
                </h3>
                <div className="space-y-3">
                  {dashboardData.top_earners.slice(0, 5).map((earner, index) => (
                    <div key={earner.user_id} className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        <span className="text-sm font-medium text-gray-500">#{index + 1}</span>
                        <span className="text-sm text-gray-900 truncate max-w-20">
                          {earner.user_id}
                        </span>
                      </div>
                      <span className="text-sm font-semibold text-green-600">
                        {formatCurrency(earner.total_earned_usd)}
                      </span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Top Services */}
              <div className="bg-white p-6 rounded-lg shadow-sm">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">
                  🎯 Top Services
                </h3>
                <div className="space-y-3">
                  {dashboardData.top_services.slice(0, 5).map((service, index) => (
                    <div key={service.service} className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        <span className="text-sm font-medium text-gray-500">#{index + 1}</span>
                        <span className="text-sm text-gray-900 capitalize">
                          {service.service}
                        </span>
                      </div>
                      <span className="text-sm font-semibold text-blue-600">
                        {service.transaction_count}
                      </span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Top Countries */}
              <div className="bg-white p-6 rounded-lg shadow-sm">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">
                  🌟 Top Countries
                </h3>
                <div className="space-y-3">
                  {dashboardData.top_countries.slice(0, 5).map((country, index) => (
                    <div key={country.country} className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        <span className="text-sm font-medium text-gray-500">#{index + 1}</span>
                        <span className="text-sm text-gray-900">
                          {country.country}
                        </span>
                      </div>
                      <span className="text-sm font-semibold text-purple-600">
                        {country.unique_users} users
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Chart Visualization */}
            <div className="bg-white p-6 rounded-lg shadow-sm">
              <div className="flex justify-between items-center mb-6">
                <h3 className="text-lg font-semibold text-gray-900">
                  📈 Trends Analysis
                </h3>
                <select
                  value={selectedMetric}
                  onChange={(e) => handleMetricChange(e.target.value)}
                  className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="transactions">Transactions</option>
                  <option value="volume">Volume (USD)</option>
                  <option value="commission">Commission (USD)</option>
                </select>
              </div>
              
              {chartData && chartData.labels && chartData.labels.length > 0 ? (
                <div className="h-64 flex items-center justify-center">
                  <div className="text-center">
                    <p className="text-gray-600 mb-2">Chart Data Available</p>
                    <p className="text-sm text-gray-500">
                      {chartData.labels.length} data points for {selectedMetric}
                    </p>
                    <p className="text-xs text-gray-400 mt-2">
                      Chart visualization would be rendered here with a library like Chart.js
                    </p>
                  </div>
                </div>
              ) : (
                <div className="h-64 flex items-center justify-center">
                  <p className="text-gray-500">No chart data available for this period</p>
                </div>
              )}
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default AdminDashboard;