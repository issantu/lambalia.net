import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import axios from 'axios';
import { Icon } from './components/ProfessionalIcons';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const LambaliaMarket = () => {
  const { t } = useTranslation();
  const [userLocation, setUserLocation] = useState('');
  const [offers, setOffers] = useState([]);
  const [demands, setDemands] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('offers');
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [modalType, setModalType] = useState('offer'); // 'offer' or 'demand'
  
  // Form data for creating offers/demands
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    dish_name: '',
    cuisine_type: '',
    quantity_people: 1,
    price_per_person: 0,
    postal_code: '',
    pickup_available: true,
    delivery_available: false,
    preparation_time_hours: 1,
    dietary_restrictions: [],
    spice_level: 'mild',
    expires_at: ''
  });

  useEffect(() => {
    getUserLocation();
    fetchMarketData();
  }, [userLocation]);

  const getUserLocation = () => {
    // Try to get user's location from localStorage or geolocation
    const savedLocation = localStorage.getItem('userPostalCode');
    if (savedLocation) {
      setUserLocation(savedLocation);
    } else if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(async (position) => {
        // In production, you'd use a reverse geocoding service
        const mockPostalCode = '90210'; // Default for demo
        setUserLocation(mockPostalCode);
        localStorage.setItem('userPostalCode', mockPostalCode);
      });
    }
  };

  const fetchMarketData = async () => {
    try {
      setLoading(true);
      const [offersResponse, demandsResponse] = await Promise.all([
        axios.get(`${API}/lambalia-market/offers${userLocation ? `?postal_code=${userLocation}` : ''}`),
        axios.get(`${API}/lambalia-market/demands${userLocation ? `?postal_code=${userLocation}` : ''}`)
      ]);
      
      setOffers(offersResponse.data);
      setDemands(demandsResponse.data);
    } catch (error) {
      console.error('Failed to fetch market data:', error);
      // Mock data for demo
      setOffers([
        {
          id: '1',
          title: 'Jollof Rice with Chicken & Plantain',
          dish_name: 'Jollof Rice Combo',
          description: 'Authentic Nigerian Jollof rice with grilled chicken and sweet plantains',
          cuisine_type: 'Nigerian',
          quantity_people: 4,
          price_per_person: 12.99,
          postal_code: userLocation || '90210',
          pickup_available: true,
          delivery_available: true,
          preparation_time_hours: 0.5,
          spice_level: 'medium',
          user_name: 'Chef Amina',
          user_rating: 4.8,
          distance_miles: 1.2,
          created_at: new Date().toISOString(),
          expires_at: new Date(Date.now() + 4 * 60 * 60 * 1000).toISOString(), // 4 hours
          is_locked: false
        },
        {
          id: '2', 
          title: 'Homemade Thai Green Curry',
          dish_name: 'Thai Green Curry',
          description: 'Creamy coconut curry with vegetables and jasmine rice',
          cuisine_type: 'Thai',
          quantity_people: 2,
          price_per_person: 15.50,
          postal_code: userLocation || '90210',
          pickup_available: true,
          delivery_available: false,
          preparation_time_hours: 1,
          spice_level: 'hot',
          user_name: 'Chef Siriporn',
          user_rating: 4.9,
          distance_miles: 0.8,
          created_at: new Date().toISOString(),
          expires_at: new Date(Date.now() + 6 * 60 * 60 * 1000).toISOString(),
          is_locked: false
        }
      ]);
      
      setDemands([
        {
          id: '1',
          title: 'Looking for Authentic Poulet Mayo',
          dish_name: 'Poulet Mayo',
          description: 'Craving traditional French chicken with mayo sauce like my grandmother made',
          cuisine_type: 'French',
          quantity_people: 2,
          price_per_person: 18.00,
          postal_code: userLocation || '90210',
          pickup_available: true,
          delivery_available: true,
          preparation_time_hours: 2,
          user_name: 'Marie',
          distance_miles: 2.1,
          created_at: new Date().toISOString(),
          expires_at: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString(),
          is_locked: false
        },
        {
          id: '2',
          title: 'Need Johnson Spaghetti Recipe Made',
          dish_name: 'Johnson Spaghetti',
          description: 'Family recipe my Italian neighbor used to make - very specific preparation needed',
          cuisine_type: 'Italian',
          quantity_people: 4,
          price_per_person: 14.00,
          postal_code: userLocation || '90210',
          pickup_available: false,
          delivery_available: true,
          preparation_time_hours: 1.5,
          user_name: 'Robert J.',
          distance_miles: 3.2,
          created_at: new Date().toISOString(),
          expires_at: new Date(Date.now() + 48 * 60 * 60 * 1000).toISOString(),
          is_locked: false
        }
      ]);
    }
    setLoading(false);
  };

  const handleCreateItem = async (e) => {
    e.preventDefault();
    try {
      const endpoint = modalType === 'offer' ? 'offers' : 'demands';
      const submitData = {
        ...formData,
        quantity_people: parseInt(formData.quantity_people),
        price_per_person: parseFloat(formData.price_per_person),
        preparation_time_hours: parseFloat(formData.preparation_time_hours),
        postal_code: formData.postal_code || userLocation
      };

      await axios.post(`${API}/lambalia-market/${endpoint}`, submitData);
      
      setShowCreateModal(false);
      setFormData({
        title: '',
        description: '',
        dish_name: '',
        cuisine_type: '',
        quantity_people: 1,
        price_per_person: 0,
        postal_code: '',
        pickup_available: true,
        delivery_available: false,
        preparation_time_hours: 1,
        dietary_restrictions: [],
        spice_level: 'mild',
        expires_at: ''
      });
      
      fetchMarketData();
      alert(`${modalType === 'offer' ? 'Offer' : 'Demand'} created successfully!`);
    } catch (error) {
      console.error('Failed to create item:', error);
      alert('Failed to create item. Please try again.');
    }
  };

  const handleSubscribe = async (item, type) => {
    try {
      const endpoint = type === 'offer' ? 'subscribe-to-offer' : 'subscribe-to-demand';
      await axios.post(`${API}/lambalia-market/${endpoint}`, {
        item_id: item.id,
        subscription_type: item.pickup_available ? 'pickup' : 'delivery'
      });
      
      alert(`Successfully subscribed to ${item.dish_name}! You will be contacted with pickup/delivery details.`);
      fetchMarketData();
    } catch (error) {
      console.error('Subscription failed:', error);
      alert('Subscription failed. Please try again.');
    }
  };

  const formatTimeRemaining = (expiresAt) => {
    const now = new Date();
    const expires = new Date(expiresAt);
    const diffMs = expires - now;
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
    const diffMins = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60));
    
    if (diffHours > 0) {
      return `${diffHours}h ${diffMins}m left`;
    } else if (diffMins > 0) {
      return `${diffMins}m left`;
    } else {
      return 'Expired';
    }
  };

  const MarketItemCard = ({ item, type, onSubscribe }) => (
    <div className="recipe-card mb-4">
      <div className="p-6">
        <div className="flex items-start justify-between mb-3">
          <div className="flex-1">
            <h3 className="text-lg font-semibold text-gray-800">{item.title}</h3>
            <p className="text-sm text-gray-500">
              by {item.user_name} • {item.distance_miles} miles away
            </p>
          </div>
          <div className="flex flex-col items-end">
            <span className={`text-xs px-2 py-1 rounded-full ${
              type === 'offer' 
                ? 'bg-green-100 text-green-800' 
                : 'bg-blue-100 text-blue-800'
            }`}>
              {type === 'offer' ? '🍽️ Available' : '🥺 Wanted'}
            </span>
            {item.is_locked && (
              <span className="text-xs px-2 py-1 rounded-full bg-red-100 text-red-800 mt-1">
                🔒 Locked
              </span>
            )}
          </div>
        </div>
        
        <div className="mb-3">
          <h4 className="font-medium text-gray-700">{item.dish_name}</h4>
          <p className="text-sm text-gray-600 line-clamp-2">{item.description}</p>
        </div>

        <div className="grid grid-cols-2 gap-4 mb-3 text-sm">
          <div className="space-y-1">
            <div className="flex items-center text-gray-600">
              <Icon name="Users" size={12} className="mr-1" />
              <span>{item.quantity_people} people</span>
            </div>
            <div className="flex items-center text-gray-600">
              <Icon name="Clock" size={12} className="mr-1" />
              <span>{item.preparation_time_hours}h prep</span>
            </div>
            <div className="flex items-center text-gray-600">
              <Icon name="MapPin" size={12} className="mr-1" />
              <span>{item.postal_code}</span>
            </div>
          </div>
          <div className="space-y-1">
            <div className="flex items-center text-gray-600">
              <span className="text-lg mr-1">💰</span>
              <span className="font-semibold text-green-600">
                ${item.price_per_person}/person
              </span>
            </div>
            <div className="flex items-center text-gray-600">
              <span className="text-lg mr-1">🌶️</span>
              <span className="capitalize">{item.spice_level || 'mild'}</span>
            </div>
            <div className="flex items-center text-gray-600">
              <span className="text-lg mr-1">🏷️</span>
              <span>{item.cuisine_type}</span>
            </div>
          </div>
        </div>

        <div className="flex items-center justify-between mb-3 pb-3 border-b">
          <div className="flex space-x-2 text-xs">
            {item.pickup_available && (
              <span className="bg-blue-100 text-blue-700 px-2 py-1 rounded">
                🏃 Pickup
              </span>
            )}
            {item.delivery_available && (
              <span className="bg-purple-100 text-purple-700 px-2 py-1 rounded">
                🚚 Delivery
              </span>
            )}
          </div>
          <div className="text-xs text-orange-600 font-medium">
            ⏰ {formatTimeRemaining(item.expires_at)}
          </div>
        </div>

        <div className="flex items-center justify-between">
          {item.user_rating && (
            <div className="flex items-center text-sm text-gray-500">
              <span className="text-yellow-500 mr-1">⭐</span>
              <span>{item.user_rating}</span>
            </div>
          )}
          
          <button
            onClick={() => onSubscribe(item, type)}
            disabled={item.is_locked}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
              item.is_locked
                ? 'bg-gray-200 text-gray-500 cursor-not-allowed'
                : type === 'offer'
                ? 'btn-primary'
                : 'bg-blue-500 hover:bg-blue-600 text-white'
            }`}
          >
            {item.is_locked 
              ? '🔒 Locked' 
              : type === 'offer' 
              ? '🛒 Subscribe & Buy' 
              : '👨‍🍳 I Can Make This'
            }
          </button>
        </div>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-4xl font-bold mb-4">🌍 {t('lod.title')}</h1>
            <p className="text-xl mb-2">{t('lod.subtitle')}</p>
            <p className="text-blue-100">
              {t('lod.description')}
            </p>
            {userLocation && (
              <div className="mt-4 inline-block bg-white bg-opacity-20 px-4 py-2 rounded-lg">
                <Icon name="MapPin" size={16} className="inline mr-2" />
                {t('lod.showingResults')} {userLocation}
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Controls */}
        <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-8">
          <div className="flex space-x-1 mb-4 md:mb-0">
            <button
              onClick={() => setActiveTab('offers')}
              className={`px-4 py-2 rounded-lg font-medium transition-all ${
                activeTab === 'offers'
                  ? 'bg-green-500 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              🍽️ {t('lod.availableOffers')} ({offers.length})
            </button>
            <button
              onClick={() => setActiveTab('demands')}
              className={`px-4 py-2 rounded-lg font-medium transition-all ${
                activeTab === 'demands'
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              🥺 {t('lod.foodDemands')} ({demands.length})
            </button>
          </div>

          <div className="flex space-x-2">
            <button
              onClick={() => {
                setModalType('offer');
                setShowCreateModal(true);
              }}
              className="btn-primary px-4 py-2 rounded-lg flex items-center space-x-2"
            >
              <Icon name="Plus" size={16} />
              <span>{t('common.postOffer')}</span>
            </button>
            <button
              onClick={() => {
                setModalType('demand');
                setShowCreateModal(true);
              }}
              className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg flex items-center space-x-2"
            >
              <Icon name="Plus" size={16} />
              <span>{t('common.postDemand')}</span>
            </button>
          </div>
        </div>

        {/* Location Input */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Filter by Location:
          </label>
          <div className="flex space-x-2">
            <input
              type="text"
              value={userLocation}
              onChange={(e) => setUserLocation(e.target.value)}
              placeholder="Enter zip code or postal code"
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button
              onClick={fetchMarketData}
              className="btn-primary px-4 py-2 rounded-lg"
            >
              🔍 Update
            </button>
          </div>
        </div>

        {/* Market Items */}
        {loading ? (
          <div className="text-center py-12">
            <div className="text-lg text-gray-600">Loading market data...</div>
          </div>
        ) : (
          <div className="grid lg:grid-cols-2 gap-6">
            {activeTab === 'offers' ? (
              <div className="space-y-4">
                <h2 className="text-xl font-semibold text-gray-800 mb-4">
                  🍽️ Available Food Offers Near You
                </h2>
                {offers.length > 0 ? (
                  offers.map(offer => (
                    <MarketItemCard
                      key={offer.id}
                      item={offer}
                      type="offer"
                      onSubscribe={handleSubscribe}
                    />
                  ))
                ) : (
                  <div className="text-center py-8 text-gray-500">
                    No offers available in your area. Be the first to post one!
                  </div>
                )}
              </div>
            ) : (
              <div className="space-y-4">
                <h2 className="text-xl font-semibold text-gray-800 mb-4">
                  🥺 Food Demands in Your Area
                </h2>
                {demands.length > 0 ? (
                  demands.map(demand => (
                    <MarketItemCard
                      key={demand.id}
                      item={demand}
                      type="demand"
                      onSubscribe={handleSubscribe}
                    />
                  ))
                ) : (
                  <div className="text-center py-8 text-gray-500">
                    No demands in your area. Check back later!
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </div>

      {/* Create Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-2xl font-bold">
                  {modalType === 'offer' ? '🍽️ Post Food Offer' : '🥺 Post Food Demand'}
                </h3>
                <button
                  onClick={() => setShowCreateModal(false)}
                  className="text-gray-500 hover:text-gray-700"
                >
                  <Icon name="X" size={24} />
                </button>
              </div>

              <form onSubmit={handleCreateItem} className="space-y-4">
                <div className="grid md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Title *
                    </label>
                    <input
                      type="text"
                      value={formData.title}
                      onChange={(e) => setFormData({...formData, title: e.target.value})}
                      placeholder={modalType === 'offer' ? 'e.g., Fresh Jollof Rice Available' : 'e.g., Looking for Authentic Poulet Mayo'}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Dish Name *
                    </label>
                    <input
                      type="text"
                      value={formData.dish_name}
                      onChange={(e) => setFormData({...formData, dish_name: e.target.value})}
                      placeholder="e.g., Jollof Rice with Chicken"
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      required
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Description *
                  </label>
                  <textarea
                    value={formData.description}
                    onChange={(e) => setFormData({...formData, description: e.target.value})}
                    placeholder="Describe the dish, ingredients, preparation style..."
                    rows="3"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  />
                </div>

                <div className="grid md:grid-cols-3 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Cuisine Type *
                    </label>
                    <input
                      type="text"
                      value={formData.cuisine_type}
                      onChange={(e) => setFormData({...formData, cuisine_type: e.target.value})}
                      placeholder="e.g., Nigerian, Thai, French"
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Quantity (People) *
                    </label>
                    <input
                      type="number"
                      min="1"
                      max="20"
                      value={formData.quantity_people}
                      onChange={(e) => setFormData({...formData, quantity_people: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Price per Person ($) *
                    </label>
                    <input
                      type="number"
                      min="0"
                      step="0.01"
                      value={formData.price_per_person}
                      onChange={(e) => setFormData({...formData, price_per_person: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      required
                    />
                  </div>
                </div>

                <div className="grid md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Your Postal Code *
                    </label>
                    <input
                      type="text"
                      value={formData.postal_code || userLocation}
                      onChange={(e) => setFormData({...formData, postal_code: e.target.value})}
                      placeholder="e.g., 90210 or SW1A 1AA"
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Preparation Time (hours)
                    </label>
                    <input
                      type="number"
                      min="0.5"
                      step="0.5"
                      value={formData.preparation_time_hours}
                      onChange={(e) => setFormData({...formData, preparation_time_hours: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                </div>

                <div className="grid md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <label className="block text-sm font-medium text-gray-700">
                      Fulfillment Options
                    </label>
                    <label className="flex items-center">
                      <input
                        type="checkbox"
                        checked={formData.pickup_available}
                        onChange={(e) => setFormData({...formData, pickup_available: e.target.checked})}
                        className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                      />
                      <span className="ml-2 text-sm text-gray-700">🏃 Pickup Available</span>
                    </label>
                    <label className="flex items-center">
                      <input
                        type="checkbox"
                        checked={formData.delivery_available}
                        onChange={(e) => setFormData({...formData, delivery_available: e.target.checked})}
                        className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                      />
                      <span className="ml-2 text-sm text-gray-700">🚚 Delivery Available</span>
                    </label>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Spice Level
                    </label>
                    <select
                      value={formData.spice_level}
                      onChange={(e) => setFormData({...formData, spice_level: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="mild">🌶️ Mild</option>
                      <option value="medium">🌶️🌶️ Medium</option>
                      <option value="hot">🌶️🌶️🌶️ Hot</option>
                      <option value="very_hot">🌶️🌶️🌶️🌶️ Very Hot</option>
                    </select>
                  </div>
                </div>

                <div className="bg-yellow-50 p-4 rounded-lg">
                  <h4 className="font-medium text-yellow-800 mb-2">💰 Commission Info</h4>
                  <p className="text-sm text-yellow-700">
                    Lambalia charges a 15% commission on all transactions. 
                    You'll receive ${((formData.price_per_person * formData.quantity_people * 0.85) || 0).toFixed(2)} 
                    from a ${((formData.price_per_person * formData.quantity_people) || 0).toFixed(2)} transaction.
                  </p>
                </div>

                <div className="flex space-x-3 pt-4">
                  <button
                    type="submit"
                    className={`flex-1 py-3 px-4 rounded-lg font-medium ${
                      modalType === 'offer'
                        ? 'btn-primary'
                        : 'bg-blue-500 hover:bg-blue-600 text-white'
                    }`}
                  >
                    {modalType === 'offer' ? '🍽️ Post Offer' : '🥺 Post Demand'}
                  </button>
                  <button
                    type="button"
                    onClick={() => setShowCreateModal(false)}
                    className="flex-1 bg-gray-200 hover:bg-gray-300 py-3 px-4 rounded-lg font-medium"
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default LambaliaMarket;