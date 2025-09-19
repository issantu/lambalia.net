import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useTranslation } from 'react-i18next';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const LocalOffersAndDemands = () => {
  const { t } = useTranslation();
  const [activeTab, setActiveTab] = useState('offers');
  const [offers, setOffers] = useState([]);
  const [requests, setRequests] = useState([]);
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState({});

  useEffect(() => {
    fetchData();
  }, [activeTab]);

  const fetchData = async () => {
    setLoading(true);
    try {
      if (activeTab === 'offers') {
        const response = await axios.get(`${API}/daily-marketplace/cooking-offers`);
        setOffers(response.data.offers || []);
      } else {
        const response = await axios.get(`${API}/daily-marketplace/eating-requests`);
        setRequests(response.data.requests || []);
      }
      
      // Get stats
      const statsResponse = await axios.get(`${API}/daily-marketplace/stats`);
      setStats(statsResponse.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
    setLoading(false);
  };

  const formatPrice = (price) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(price);
  };

  const formatTime = (timeString) => {
    return new Date(timeString).toLocaleString();
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            🍽️ {t('offers.title', 'Local Offers & Demands')}
          </h1>
          <p className="text-xl text-gray-600 mb-6">
            {t('offers.subtitle', 'Discover delicious meals from local cooks or request what you\'re craving')}
          </p>
          
          {/* Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            <div className="bg-white rounded-lg p-4 shadow-sm">
              <div className="text-2xl font-bold text-green-600">{stats.active_offers || 0}</div>
              <div className="text-sm text-gray-600">{t('offers.stats.activeOffers', 'Active Offers')}</div>
            </div>
            <div className="bg-white rounded-lg p-4 shadow-sm">
              <div className="text-2xl font-bold text-blue-600">{stats.active_requests || 0}</div>
              <div className="text-sm text-gray-600">{t('offers.stats.activeRequests', 'Active Requests')}</div>
            </div>
            <div className="bg-white rounded-lg p-4 shadow-sm">
              <div className="text-2xl font-bold text-orange-600">{stats.orders_in_progress || 0}</div>
              <div className="text-sm text-gray-600">{t('offers.stats.ordersProgress', 'Orders in Progress')}</div>
            </div>
            <div className="bg-white rounded-lg p-4 shadow-sm">
              <div className="text-2xl font-bold text-purple-600">{stats.available_cooks || 0}</div>
              <div className="text-sm text-gray-600">{t('offers.stats.availableCooks', 'Available Cooks')}</div>
            </div>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="flex justify-center mb-8">
          <div className="bg-white rounded-lg p-1 flex shadow-sm">
            <button
              onClick={() => setActiveTab('offers')}
              className={`px-6 py-3 rounded-md font-medium transition-colors ${
                activeTab === 'offers'
                  ? 'bg-green-500 text-white'
                  : 'text-gray-600 hover:text-green-600'
              }`}
            >
              🍳 {t('offers.tabs.offers', 'Available Offers')}
            </button>
            <button
              onClick={() => setActiveTab('requests')}
              className={`px-6 py-3 rounded-md font-medium transition-colors ${
                activeTab === 'requests'
                  ? 'bg-blue-500 text-white'
                  : 'text-gray-600 hover:text-blue-600'
              }`}
            >
              🍽️ {t('offers.tabs.requests', 'Food Requests')}
            </button>
          </div>
        </div>

        {/* Content */}
        {loading ? (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-500 mx-auto"></div>
            <p className="mt-4 text-gray-600">{t('common.loading', 'Loading...')}</p>
          </div>
        ) : (
          <div>
            {activeTab === 'offers' ? (
              <div>
                <h2 className="text-2xl font-semibold mb-6">🍳 {t('offers.availableOffers', 'Available Food Offers Near You')}</h2>
                {offers.length === 0 ? (
                  <div className="text-center py-12 bg-white rounded-lg shadow-sm">
                    <div className="text-6xl mb-4">🍽️</div>
                    <h3 className="text-xl font-medium text-gray-600 mb-2">
                      {t('offers.noOffers', 'No food offers available nearby')}
                    </h3>
                    <p className="text-gray-500">
                      {t('offers.noOffersMessage', 'Be the first to share a delicious meal with your community!')}
                    </p>
                  </div>
                ) : (
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {offers.map((offer, index) => (
                      <div key={index} className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
                        <div className="p-6">
                          <div className="flex justify-between items-start mb-4">
                            <h3 className="text-lg font-semibold text-gray-900">{offer.dish_name}</h3>
                            <span className="text-lg font-bold text-green-600">{formatPrice(offer.price_per_serving)}</span>
                          </div>
                          
                          <p className="text-gray-600 mb-4">{offer.description}</p>
                          
                          <div className="space-y-2 text-sm text-gray-500 mb-4">
                            <div>📍 {offer.location?.address || 'Local Area'}</div>
                            <div>👨‍🍳 {offer.cook_name}</div>
                            <div>⏰ Ready: {formatTime(offer.ready_at)}</div>
                            <div>📦 Available: {offer.servings_available} servings</div>
                          </div>
                          
                          <div className="flex flex-wrap gap-2 mb-4">
                            {offer.service_options?.map((service, idx) => (
                              <span key={idx} className="px-2 py-1 bg-gray-100 text-gray-700 rounded-full text-xs">
                                {service}
                              </span>
                            ))}
                          </div>
                          
                          <button className="w-full bg-green-500 text-white py-2 px-4 rounded-md hover:bg-green-600 transition-colors">
                            {t('offers.orderNow', 'Order Now')}
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ) : (
              <div>
                <h2 className="text-2xl font-semibold mb-6">🍽️ {t('offers.foodRequests', 'Food Requests from Your Community')}</h2>
                {requests.length === 0 ? (
                  <div className="text-center py-12 bg-white rounded-lg shadow-sm">
                    <div className="text-6xl mb-4">🥘</div>
                    <h3 className="text-xl font-medium text-gray-600 mb-2">
                      {t('offers.noRequests', 'No food requests in your area')}
                    </h3>
                    <p className="text-gray-500">
                      {t('offers.noRequestsMessage', 'Check back later or be the first to request something delicious!')}
                    </p>
                  </div>
                ) : (
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {requests.map((request, index) => (
                      <div key={index} className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
                        <div className="p-6">
                          <div className="flex justify-between items-start mb-4">
                            <h3 className="text-lg font-semibold text-gray-900">{request.dish_name}</h3>
                            <span className="text-lg font-bold text-blue-600">Up to {formatPrice(request.max_price)}</span>
                          </div>
                          
                          <p className="text-gray-600 mb-4">{request.description}</p>
                          
                          <div className="space-y-2 text-sm text-gray-500 mb-4">
                            <div>📍 {request.location?.address || 'Local Area'}</div>
                            <div>🍽️ {request.requester_name}</div>
                            <div>⏰ Needed by: {formatTime(request.needed_by)}</div>
                            <div>📦 Servings: {request.servings_requested}</div>
                          </div>
                          
                          <div className="flex flex-wrap gap-2 mb-4">
                            {request.service_preferences?.map((service, idx) => (
                              <span key={idx} className="px-2 py-1 bg-gray-100 text-gray-700 rounded-full text-xs">
                                {service}
                              </span>
                            ))}
                          </div>
                          
                          <button className="w-full bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600 transition-colors">
                            {t('offers.acceptRequest', 'Accept Request')}
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default LocalOffersAndDemands;
