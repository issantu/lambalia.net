import React, { useState, useEffect } from 'react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Lambalia Eats - Real-time Food Marketplace (Uber for Home Cooking)
const LambaliaEatsApp = () => {
  const [activeTab, setActiveTab] = useState('browse'); // 'browse', 'request', 'offer', 'orders', 'track'
  const [userLocation, setUserLocation] = useState({ lat: 40.7128, lng: -74.0060 }); // Default NYC
  const [nearbyOffers, setNearbyOffers] = useState([]);
  const [activeRequests, setActiveRequests] = useState([]);
  const [myOrders, setMyOrders] = useState([]);
  const [platformStats, setPlatformStats] = useState(null);
  const [loading, setLoading] = useState(false);
  const [wsConnection, setWsConnection] = useState(null);
  const [realTimeUpdates, setRealTimeUpdates] = useState([]);

  useEffect(() => {
    // Get user location
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setUserLocation({
            lat: position.coords.latitude,
            lng: position.coords.longitude
          });
        },
        (error) => console.log('Location access denied:', error)
      );
    }

    // Load initial data
    fetchPlatformStats();
    
    // Setup WebSocket connection for real-time updates
    setupWebSocket();

    return () => {
      if (wsConnection) {
        wsConnection.close();
      }
    };
  }, []);

  useEffect(() => {
    if (activeTab === 'browse') {
      fetchNearbyOffers();
    } else if (activeTab === 'request') {
      fetchActiveRequests();
    } else if (activeTab === 'orders') {
      fetchMyOrders();
    }
  }, [activeTab, userLocation]);

  const setupWebSocket = () => {
    const userId = `temp_user_${Math.random().toString(36).substr(2, 9)}`;
    const ws = new WebSocket(`ws://localhost:8001/api/eats/ws/${userId}`);
    
    ws.onopen = () => {
      console.log('Connected to Lambalia Eats real-time updates');
      setWsConnection(ws);
    };

    ws.onmessage = (event) => {
      const update = JSON.parse(event.data);
      setRealTimeUpdates(prev => [update, ...prev.slice(0, 9)]); // Keep last 10 updates
      
      // Handle specific update types
      if (update.type === 'new_order') {
        fetchMyOrders();
      } else if (update.type === 'order_update') {
        fetchMyOrders();
      }
    };

    ws.onclose = () => {
      console.log('WebSocket connection closed');
      // Reconnect after 3 seconds
      setTimeout(setupWebSocket, 3000);
    };
  };

  const fetchPlatformStats = async () => {
    try {
      const response = await axios.get(`${API}/eats/stats`);
      setPlatformStats(response.data.stats);
    } catch (error) {
      console.error('Failed to fetch platform stats:', error);
    }
  };

  const fetchNearbyOffers = async () => {
    setLoading(true);
    try {
      // First try real API, then fallback to demo data
      try {
        const response = await axios.get(`${API}/eats/offers/nearby`, {
          params: {
            lat: userLocation.lat,
            lng: userLocation.lng,
            radius_km: 15
          }
        });
        setNearbyOffers(response.data);
      } catch (error) {
        // Fallback to demo data
        const response = await axios.get(`${API}/eats/demo/sample-offers`);
        setNearbyOffers(response.data);
      }
    } catch (error) {
      console.error('Failed to fetch nearby offers:', error);
    }
    setLoading(false);
  };

  const fetchActiveRequests = async () => {
    setLoading(true);
    try {
      try {
        const response = await axios.get(`${API}/eats/requests/active`, {
          params: {
            lat: userLocation.lat,
            lng: userLocation.lng,
            radius_km: 20
          }
        });
        setActiveRequests(response.data);
      } catch (error) {
        // Fallback to demo data
        const response = await axios.get(`${API}/eats/demo/sample-requests`);
        setActiveRequests(response.data);
      }
    } catch (error) {
      console.error('Failed to fetch active requests:', error);
    }
    setLoading(false);
  };

  const fetchMyOrders = async () => {
    try {
      const response = await axios.get(`${API}/eats/orders/my-orders`);
      setMyOrders(response.data);
    } catch (error) {
      console.error('Failed to fetch orders:', error);
    }
  };

  const FoodOfferCard = ({ offer }) => (
    <div className="bg-white rounded-lg shadow-md p-4 mb-4 hover:shadow-lg transition-shadow">
      <div className="flex items-start justify-between mb-3">
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-gray-800">{offer.dish_name}</h3>
          <p className="text-sm text-gray-500 capitalize">{offer.cuisine_type?.replace('_', ' ')}</p>
          <p className="text-sm text-blue-600">by {offer.cook_name}</p>
        </div>
        <div className="text-right">
          <p className="text-xl font-bold text-green-600">${offer.price_per_serving}</p>
          <div className="flex items-center text-sm text-gray-500">
            <span>⭐ {offer.cook_rating}</span>
            <span className="mx-1">•</span>
            <span>{offer.distance_km}km</span>
          </div>
        </div>
      </div>

      <p className="text-gray-600 mb-3 text-sm">{offer.description}</p>

      <div className="flex items-center justify-between text-sm text-gray-500 mb-3">
        <span>🕒 Ready: {new Date(offer.ready_at).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</span>
        <span>📦 {offer.quantity_remaining} available</span>
      </div>

      <div className="flex flex-wrap gap-2 mb-3">
        {offer.available_service_types?.map((service, index) => (
          <span key={index} className="bg-blue-100 text-blue-700 text-xs px-2 py-1 rounded-full capitalize">
            {service.replace('_', ' ')}
          </span>
        ))}
      </div>

      <div className="flex items-center justify-between">
        <div className="text-sm text-gray-600">
          {offer.available_service_types?.includes('delivery') && (
            <span>🚚 Delivery: ${offer.delivery_fee}</span>
          )}
        </div>
        <div className="space-x-2">
          <button 
            onClick={() => handlePlaceOrder(offer, 'pickup')}
            className="bg-green-600 hover:bg-green-700 text-white px-3 py-1 rounded text-sm"
          >
            Order Now
          </button>
          <button className="bg-gray-200 hover:bg-gray-300 text-gray-700 px-3 py-1 rounded text-sm">
            Details
          </button>
        </div>
      </div>
    </div>
  );

  const FoodRequestCard = ({ request }) => (
    <div className="bg-white rounded-lg shadow-md p-4 mb-4 hover:shadow-lg transition-shadow">
      <div className="flex items-start justify-between mb-3">
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-gray-800">{request.dish_name}</h3>
          <p className="text-sm text-gray-500 capitalize">{request.cuisine_type?.replace('_', ' ')}</p>
          <p className="text-sm text-purple-600">by {request.eater_name || 'Hungry Eater'}</p>
        </div>
        <div className="text-right">
          <p className="text-lg font-bold text-purple-600">Up to ${request.max_price}</p>
          <p className="text-sm text-gray-500">{request.distance_km}km away</p>
        </div>
      </div>

      <p className="text-gray-600 mb-3 text-sm">{request.description}</p>

      <div className="flex items-center justify-between text-sm text-gray-500 mb-3">
        <span>⏰ Expires in {request.time_until_expires} min</span>
        <span>🍽️ Service: {request.preferred_service_types?.join(', ')}</span>
      </div>

      {request.dietary_restrictions?.length > 0 && (
        <div className="flex flex-wrap gap-1 mb-3">
          {request.dietary_restrictions.map((restriction, index) => (
            <span key={index} className="bg-orange-100 text-orange-700 text-xs px-2 py-1 rounded-full">
              {restriction}
            </span>
          ))}
        </div>
      )}

      <div className="flex items-center justify-between">
        <div className="text-sm text-gray-600">
          Max delivery fee: ${request.max_delivery_fee || 15}
        </div>
        <button 
          onClick={() => handleAcceptRequest(request)}
          className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded"
        >
          Accept Request
        </button>
      </div>
    </div>
  );

  const handlePlaceOrder = async (offer, serviceType) => {
    try {
      const orderData = {
        offer_id: offer.id,
        service_type: serviceType,
        quantity: 1,
        delivery_address: serviceType === 'delivery' ? '123 Main St' : null
      };

      const response = await axios.post(`${API}/eats/place-order`, orderData);
      
      if (response.data.success) {
        alert(`🎉 Order placed successfully! Tracking code: ${response.data.tracking_code}`);
        setActiveTab('orders');
        fetchMyOrders();
      }
    } catch (error) {
      console.error('Failed to place order:', error);
      alert('Failed to place order. Please try again.');
    }
  };

  const handleAcceptRequest = async (request) => {
    try {
      const orderData = {
        request_id: request.id,
        service_type: request.preferred_service_types[0],
        agreed_price: request.max_price,
        preparation_time: 45,
        cook_location: userLocation
      };

      const response = await axios.post(`${API}/eats/place-order`, orderData);
      
      if (response.data.success) {
        alert(`🎉 Request accepted! Start preparing ${request.dish_name}`);
        setActiveTab('orders');
        fetchMyOrders();
      }
    } catch (error) {
      console.error('Failed to accept request:', error);
      alert('Failed to accept request. Please try again.');
    }
  };

  const CreateFoodRequestForm = () => {
    const [formData, setFormData] = useState({
      dish_name: '',
      cuisine_type: 'american',
      description: '',
      dietary_restrictions: [],
      preferred_service_types: ['pickup'],
      max_price: 25,
      max_delivery_fee: 10,
      max_wait_time_minutes: 90,
      eater_address: '123 Main St, New York, NY',
      flexible_timing: true
    });

    const handleSubmit = async (e) => {
      e.preventDefault();
      setLoading(true);

      try {
        const requestData = {
          ...formData,
          eater_location: userLocation
        };

        const response = await axios.post(`${API}/eats/request-food`, requestData);
        
        if (response.data.success) {
          alert(`🎉 Food request posted! Request ID: ${response.data.request_id}`);
          setActiveTab('orders');
        }
      } catch (error) {
        console.error('Failed to create food request:', error);
        alert('Failed to post request. Please try again.');
      }
      setLoading(false);
    };

    return (
      <div className="max-w-2xl mx-auto">
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-2xl font-bold text-gray-800 mb-6">🍽️ Request Food</h3>
          <p className="text-gray-600 mb-6">Tell local cooks what you're craving!</p>
          
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">What do you want to eat? *</label>
                <input
                  type="text"
                  value={formData.dish_name}
                  onChange={(e) => setFormData({...formData, dish_name: e.target.value})}
                  placeholder="e.g., Chicken Biryani, Fresh Pasta"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Cuisine Type</label>
                <select
                  value={formData.cuisine_type}
                  onChange={(e) => setFormData({...formData, cuisine_type: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="american">American</option>
                  <option value="african">African</option>
                  <option value="caribbean">Caribbean</option>
                  <option value="mexican">Mexican</option>
                  <option value="italian">Italian</option>
                  <option value="chinese">Chinese</option>
                  <option value="indian">Indian</option>
                  <option value="japanese">Japanese</option>
                  <option value="thai">Thai</option>
                  <option value="korean">Korean</option>
                  <option value="vietnamese">Vietnamese</option>
                  <option value="mediterranean">Mediterranean</option>
                  <option value="middle_eastern">Middle Eastern</option>
                  <option value="latin_american">Latin American</option>
                  <option value="european">European</option>
                </select>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
              <textarea
                value={formData.description}
                onChange={(e) => setFormData({...formData, description: e.target.value})}
                rows="3"
                placeholder="Describe how you'd like it prepared, any special preferences..."
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Max Price ($)</label>
                <input
                  type="number"
                  value={formData.max_price}
                  onChange={(e) => setFormData({...formData, max_price: parseFloat(e.target.value)})}
                  min="5"
                  max="100"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Max Wait Time (minutes)</label>
                <input
                  type="number"
                  value={formData.max_wait_time_minutes}
                  onChange={(e) => setFormData({...formData, max_wait_time_minutes: parseInt(e.target.value)})}
                  min="15"
                  max="180"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Service Preferences</label>
              <div className="flex flex-wrap gap-3">
                {['pickup', 'delivery', 'dine_in'].map(service => (
                  <label key={service} className="flex items-center">
                    <input
                      type="checkbox"
                      checked={formData.preferred_service_types.includes(service)}
                      onChange={(e) => {
                        if (e.target.checked) {
                          setFormData({...formData, preferred_service_types: [...formData.preferred_service_types, service]});
                        } else {
                          setFormData({...formData, preferred_service_types: formData.preferred_service_types.filter(s => s !== service)});
                        }
                      }}
                      className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                    />
                    <span className="ml-2 text-sm capitalize">{service.replace('_', ' ')}</span>
                  </label>
                ))}
              </div>
            </div>

            <div className="pt-4">
              <button
                type="submit"
                disabled={loading}
                className="w-full bg-purple-600 hover:bg-purple-700 text-white font-medium py-3 px-4 rounded-lg disabled:opacity-50"
              >
                {loading ? 'Posting Request... ⏳' : 'Post Food Request 🍽️'}
              </button>
            </div>
          </form>
        </div>
      </div>
    );
  };

  const CreateFoodOfferForm = () => {
    const [formData, setFormData] = useState({
      dish_name: '',
      cuisine_type: 'american',
      description: '',
      ingredients: [],
      dietary_info: [],
      quantity_available: 2,
      price_per_serving: 15,
      available_service_types: ['pickup'],
      delivery_radius_km: 10,
      delivery_fee: 5,
      ready_at: new Date(Date.now() + 60*60*1000).toISOString().slice(0, 16), // 1 hour from now
      available_until: new Date(Date.now() + 4*60*60*1000).toISOString().slice(0, 16), // 4 hours from now
      cook_address: '123 Main St, New York, NY'
    });

    const handleSubmit = async (e) => {
      e.preventDefault();
      setLoading(true);

      try {
        const offerData = {
          ...formData,
          cook_location: userLocation
        };

        const response = await axios.post(`${API}/eats/offer-food`, offerData);
        
        if (response.data.success) {
          alert(`🎉 Food offer posted! Offer ID: ${response.data.offer_id}`);
          setActiveTab('browse');
          fetchNearbyOffers();
        }
      } catch (error) {
        console.error('Failed to create food offer:', error);
        alert('Failed to post offer. Please try again.');
      }
      setLoading(false);
    };

    return (
      <div className="max-w-2xl mx-auto">
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-2xl font-bold text-gray-800 mb-6">👩‍🍳 Offer Food</h3>
          <p className="text-gray-600 mb-6">Share your delicious homemade meal with hungry neighbors!</p>
          
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Dish Name *</label>
                <input
                  type="text"
                  value={formData.dish_name}
                  onChange={(e) => setFormData({...formData, dish_name: e.target.value})}
                  placeholder="e.g., Grandma's Chicken Curry"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Cuisine Type</label>
                <select
                  value={formData.cuisine_type}
                  onChange={(e) => setFormData({...formData, cuisine_type: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                >
                  <option value="american">American</option>
                  <option value="african">African</option>
                  <option value="caribbean">Caribbean</option>
                  <option value="mexican">Mexican</option>
                  <option value="italian">Italian</option>
                  <option value="chinese">Chinese</option>
                  <option value="indian">Indian</option>
                  <option value="japanese">Japanese</option>
                  <option value="thai">Thai</option>
                  <option value="korean">Korean</option>
                  <option value="vietnamese">Vietnamese</option>
                  <option value="mediterranean">Mediterranean</option>
                  <option value="middle_eastern">Middle Eastern</option>
                  <option value="latin_american">Latin American</option>
                  <option value="european">European</option>
                </select>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
              <textarea
                value={formData.description}
                onChange={(e) => setFormData({...formData, description: e.target.value})}
                rows="3"
                placeholder="Describe your dish, cooking method, what makes it special..."
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Quantity Available</label>
                <input
                  type="number"
                  value={formData.quantity_available}
                  onChange={(e) => setFormData({...formData, quantity_available: parseInt(e.target.value)})}
                  min="1"
                  max="20"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Price per Serving ($)</label>
                <input
                  type="number"
                  step="0.50"
                  value={formData.price_per_serving}
                  onChange={(e) => setFormData({...formData, price_per_serving: parseFloat(e.target.value)})}
                  min="3"
                  max="50"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Delivery Fee ($)</label>
                <input
                  type="number"
                  step="0.50"
                  value={formData.delivery_fee}
                  onChange={(e) => setFormData({...formData, delivery_fee: parseFloat(e.target.value)})}
                  min="0"
                  max="15"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Ready At</label>
                <input
                  type="datetime-local"
                  value={formData.ready_at}
                  onChange={(e) => setFormData({...formData, ready_at: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Available Until</label>
                <input
                  type="datetime-local"
                  value={formData.available_until}
                  onChange={(e) => setFormData({...formData, available_until: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Service Options</label>
              <div className="flex flex-wrap gap-3">
                {['pickup', 'delivery', 'dine_in'].map(service => (
                  <label key={service} className="flex items-center">
                    <input
                      type="checkbox"
                      checked={formData.available_service_types.includes(service)}
                      onChange={(e) => {
                        if (e.target.checked) {
                          setFormData({...formData, available_service_types: [...formData.available_service_types, service]});
                        } else {
                          setFormData({...formData, available_service_types: formData.available_service_types.filter(s => s !== service)});
                        }
                      }}
                      className="rounded border-gray-300 text-green-600 focus:ring-green-500"
                    />
                    <span className="ml-2 text-sm capitalize">{service.replace('_', ' ')}</span>
                  </label>
                ))}
              </div>
            </div>

            <div className="pt-4">
              <button
                type="submit"
                disabled={loading}
                className="w-full bg-green-600 hover:bg-green-700 text-white font-medium py-3 px-4 rounded-lg disabled:opacity-50"
              >
                {loading ? 'Posting Offer... ⏳' : 'Post Food Offer 👩‍🍳'}
              </button>
            </div>
          </form>
        </div>
      </div>
    );
  };

  const RealTimeUpdatesPanel = () => (
    <div className="bg-white rounded-lg shadow-md p-4 mb-4">
      <h4 className="font-semibold text-gray-800 mb-3">📡 Live Updates</h4>
      <div className="max-h-32 overflow-y-auto space-y-2">
        {realTimeUpdates.length === 0 ? (
          <p className="text-sm text-gray-500">No recent updates</p>
        ) : (
          realTimeUpdates.map((update, index) => (
            <div key={index} className="text-xs bg-gray-50 p-2 rounded">
              <span className="font-medium">{update.type}:</span> {update.message}
              {update.timestamp && (
                <span className="text-gray-400 ml-2">
                  {new Date(update.timestamp).toLocaleTimeString()}
                </span>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-4">
              <h1 className="text-2xl font-bold text-green-600">🍽️ Lambalia Eats</h1>
              <span className="text-sm text-gray-500">Real-time Food Marketplace</span>
            </div>
            <div className="flex items-center space-x-4 text-sm">
              {platformStats && (
                <>
                  <span className="text-green-600">🔴 {platformStats.orders_in_progress} live orders</span>
                  <span className="text-blue-600">👨‍🍳 {platformStats.available_cooks} cooks online</span>
                </>
              )}
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {/* Tab Navigation */}
        <div className="mb-6">
          <div className="flex space-x-1 bg-gray-100 p-1 rounded-lg max-w-3xl mx-auto">
            <button
              onClick={() => setActiveTab('browse')}
              className={`flex-1 px-4 py-2 text-sm font-medium rounded-md transition-all ${
                activeTab === 'browse'
                  ? 'bg-white text-green-600 shadow-sm'
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              🛒 Browse Food
            </button>
            <button
              onClick={() => setActiveTab('request')}
              className={`flex-1 px-4 py-2 text-sm font-medium rounded-md transition-all ${
                activeTab === 'request'
                  ? 'bg-white text-purple-600 shadow-sm'
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              🍽️ Request Food
            </button>
            <button
              onClick={() => setActiveTab('offer')}
              className={`flex-1 px-4 py-2 text-sm font-medium rounded-md transition-all ${
                activeTab === 'offer'
                  ? 'bg-white text-green-600 shadow-sm'
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              👩‍🍳 Offer Food
            </button>
            <button
              onClick={() => setActiveTab('orders')}
              className={`flex-1 px-4 py-2 text-sm font-medium rounded-md transition-all ${
                activeTab === 'orders'
                  ? 'bg-white text-blue-600 shadow-sm'
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              📋 My Orders
            </button>
            <button
              onClick={() => setActiveTab('requests')}
              className={`flex-1 px-4 py-2 text-sm font-medium rounded-md transition-all ${
                activeTab === 'requests'
                  ? 'bg-white text-orange-600 shadow-sm'
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              📤 Active Requests
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Main Content */}
          <div className="lg:col-span-3">
            {activeTab === 'browse' && (
              <div>
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-2xl font-bold text-gray-800">🍳 Available Food Near You</h2>
                  <button
                    onClick={fetchNearbyOffers}
                    disabled={loading}
                    className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg disabled:opacity-50"
                  >
                    {loading ? 'Loading...' : 'Refresh'}
                  </button>
                </div>
                
                {loading ? (
                  <div className="text-center py-8">
                    <div className="text-4xl mb-4">⏳</div>
                    <p>Finding delicious food near you...</p>
                  </div>
                ) : nearbyOffers.length === 0 ? (
                  <div className="text-center py-12 bg-white rounded-lg">
                    <div className="text-6xl mb-4">🍽️</div>
                    <h3 className="text-xl font-semibold text-gray-800 mb-2">No food offers nearby</h3>
                    <p className="text-gray-600">Be the first to post a delicious meal!</p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {nearbyOffers.map((offer, index) => (
                      <FoodOfferCard key={offer.id || index} offer={offer} />
                    ))}
                  </div>
                )}
              </div>
            )}

            {activeTab === 'request' && <CreateFoodRequestForm />}
            {activeTab === 'offer' && <CreateFoodOfferForm />}

            {activeTab === 'requests' && (
              <div>
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-2xl font-bold text-gray-800">📤 Active Food Requests</h2>
                  <button
                    onClick={fetchActiveRequests}
                    disabled={loading}
                    className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg disabled:opacity-50"
                  >
                    {loading ? 'Loading...' : 'Refresh'}
                  </button>
                </div>
                
                {loading ? (
                  <div className="text-center py-8">
                    <div className="text-4xl mb-4">⏳</div>
                    <p>Finding hungry eaters...</p>
                  </div>
                ) : activeRequests.length === 0 ? (
                  <div className="text-center py-12 bg-white rounded-lg">
                    <div className="text-6xl mb-4">🍽️</div>
                    <h3 className="text-xl font-semibold text-gray-800 mb-2">No active requests</h3>
                    <p className="text-gray-600">Check back later for hungry eaters!</p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {activeRequests.map((request, index) => (
                      <FoodRequestCard key={request.id || index} request={request} />
                    ))}
                  </div>
                )}
              </div>
            )}

            {activeTab === 'orders' && (
              <div>
                <h2 className="text-2xl font-bold text-gray-800 mb-6">📋 My Orders</h2>
                {myOrders.length === 0 ? (
                  <div className="text-center py-12 bg-white rounded-lg">
                    <div className="text-6xl mb-4">📋</div>
                    <h3 className="text-xl font-semibold text-gray-800 mb-2">No orders yet</h3>
                    <p className="text-gray-600">Start by browsing available food or posting a request!</p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {myOrders.map((order, index) => (
                      <div key={order.id || index} className="bg-white rounded-lg shadow-md p-4">
                        <div className="flex items-center justify-between mb-2">
                          <h4 className="font-semibold">{order.dish_name}</h4>
                          <span className={`px-2 py-1 rounded-full text-xs ${
                            order.current_status === 'completed' ? 'bg-green-100 text-green-800' :
                            order.current_status === 'cancelled' ? 'bg-red-100 text-red-800' :
                            'bg-yellow-100 text-yellow-800'
                          }`}>
                            {order.current_status}
                          </span>
                        </div>
                        <p className="text-sm text-gray-600">
                          Role: {order.user_role} | Service: {order.service_type} | 
                          Total: ${order.total_amount}
                        </p>
                        <p className="text-xs text-gray-500">
                          Tracking: {order.tracking_code} | 
                          Ordered: {new Date(order.ordered_at).toLocaleString()}
                        </p>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Sidebar */}
          <div className="lg:col-span-1 space-y-4">
            <RealTimeUpdatesPanel />
            
            {/* Platform Stats */}
            {platformStats && (
              <div className="bg-white rounded-lg shadow-md p-4">
                <h4 className="font-semibold text-gray-800 mb-3">📊 Platform Stats</h4>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span>Active Offers:</span>
                    <span className="font-medium">{platformStats.active_offers}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Active Requests:</span>
                    <span className="font-medium">{platformStats.active_requests}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Orders in Progress:</span>
                    <span className="font-medium text-red-600">{platformStats.orders_in_progress}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Available Cooks:</span>
                    <span className="font-medium text-green-600">{platformStats.available_cooks}</span>
                  </div>
                </div>
              </div>
            )}

            {/* Service Types Info */}
            <div className="bg-white rounded-lg shadow-md p-4">
              <h4 className="font-semibold text-gray-800 mb-3">🚚 Service Options</h4>
              <div className="space-y-2 text-sm">
                <div className="flex items-start space-x-2">
                  <span>🚶</span>
                  <div>
                    <span className="font-medium">Pickup:</span>
                    <p className="text-gray-600">You pick up, pay meal only</p>
                  </div>
                </div>
                <div className="flex items-start space-x-2">
                  <span>🚚</span>
                  <div>
                    <span className="font-medium">Delivery:</span>
                    <p className="text-gray-600">Delivered to you, pay meal + delivery</p>
                  </div>
                </div>
                <div className="flex items-start space-x-2">
                  <span>🏠</span>
                  <div>
                    <span className="font-medium">Dine-in:</span>
                    <p className="text-gray-600">Eat at cook's place</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LambaliaEatsApp;