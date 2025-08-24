import React, { useState, useEffect, createContext, useContext } from 'react';
import { BrowserRouter, Routes, Route, Navigate, Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useTranslation } from 'react-i18next';
import './i18n'; // Initialize i18n
import LanguageSwitcher from './LanguageSwitcher';
import './App.css';
import LocalMarketplacePage from './LocalMarketplace';
import CharityProgramPage from './CharityProgram';
import LambaliaEatsApp from './LambaliaEats';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Context for authentication
const AuthContext = createContext();

const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};

// Auth Provider Component
const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      fetchCurrentUser();
    } else {
      setLoading(false);
    }
  }, []);

  const fetchCurrentUser = async () => {
    try {
      const response = await axios.get(`${API}/users/me`);
      setUser(response.data);
    } catch (error) {
      console.error('Failed to fetch current user:', error);
      localStorage.removeItem('token');
      delete axios.defaults.headers.common['Authorization'];
    }
    setLoading(false);
  };

  const login = async (email, password) => {
    try {
      const response = await axios.post(`${API}/auth/login`, { email, password });
      const { access_token, user } = response.data;
      
      localStorage.setItem('token', access_token);
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
      setUser(user);
      
      return { success: true };
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Login failed' 
      };
    }
  };

  const register = async (userData) => {
    try {
      const response = await axios.post(`${API}/auth/register`, userData);
      const { access_token, user } = response.data;
      
      localStorage.setItem('token', access_token);
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
      setUser(user);
      
      return { success: true };
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Registration failed' 
      };
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    delete axios.defaults.headers.common['Authorization'];
    setUser(null);
  };

  const value = {
    user,
    login,
    register,
    logout,
    loading
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

// Enhanced Login Component with Dynamic Background
const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    full_name: '',
    postal_code: '',
    preferred_language: 'en'
  });
  const { login, register } = useAuth();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    
    const result = await login(email, password);
    if (result.success) {
      window.location.href = '/';
    } else {
      setError(result.error);
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setError('');
    
    const result = await register(formData);
    if (result.success) {
      window.location.href = '/';
    } else {
      setError(result.error);
    }
  };

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div className="landing-page flex items-center justify-center px-4">
      {/* Animated Background Elements */}
      <div className="fume-container">
        <div className="fume"></div>
        <div className="fume"></div>
        <div className="fume"></div>
        <div className="fume"></div>
      </div>

      <div className="max-w-md w-full auth-form rounded-xl shadow-2xl p-8 z-10 relative">
        <div className="text-center mb-8">
          <div className="logo-shine">
            <img 
              src="https://customer-assets.emergentagent.com/job_lambalia-recipes/artifacts/qzs71f09_2.png" 
              alt="Lambalia - Global Heritage Recipes" 
              className="w-40 h-40 mx-auto mb-4 drop-shadow-lg"
            />
          </div>
          <h1 className="text-4xl font-bold heading-gradient">Lambalia</h1>
          <p className="text-gray-600 mt-2 font-medium">Transform Your Kitchen Into a Global Culinary Experience</p>
          <div className="mt-4 text-sm text-gray-500">
            <p>🌍 198+ Traditional Recipes • 💰 Monetize Your Cooking • 🏠 Home Restaurant Platform</p>
          </div>
        </div>

        <div className="flex mb-6">
          <button
            className={`flex-1 py-3 px-4 rounded-l-lg font-medium transition-all ${
              isLogin ? 'btn-primary' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
            onClick={() => setIsLogin(true)}
          >
            Login
          </button>
          <button
            className={`flex-1 py-3 px-4 rounded-r-lg font-medium transition-all ${
              !isLogin ? 'btn-primary' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
            onClick={() => setIsLogin(false)}
          >
            Join Lambalia
          </button>
        </div>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4 success-message">
            {error}
          </div>
        )}

        {isLogin ? (
          <form onSubmit={handleLogin} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 transition-all"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 transition-all"
                required
              />
            </div>
            <button
              type="submit"
              className="w-full btn-primary py-3 px-4 rounded-lg font-medium text-lg"
            >
              Enter Your Kitchen 👩‍🍳
            </button>
          </form>
        ) : (
          <form onSubmit={handleRegister} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Username</label>
              <input
                type="text"
                name="username"
                value={formData.username}
                onChange={handleInputChange}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 transition-all"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Full Name</label>
              <input
                type="text"
                name="full_name"
                value={formData.full_name}
                onChange={handleInputChange}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 transition-all"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleInputChange}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 transition-all"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Postal Code</label>
              <input
                type="text"
                name="postal_code"
                value={formData.postal_code}
                onChange={handleInputChange}
                placeholder="For local grocery & delivery services"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 transition-all"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
              <input
                type="password"
                name="password"
                value={formData.password}
                onChange={handleInputChange}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 transition-all"
                required
              />
            </div>
            <button
              type="submit"
              className="w-full btn-primary py-3 px-4 rounded-lg font-medium text-lg"
            >
              Start Your Culinary Journey 🌟
            </button>
          </form>
        )}

        <div className="text-center mt-6">
          <p className="text-sm text-gray-600 mb-4">
            Join our community of home chefs sharing authentic recipes from around the world!
          </p>
          
          {/* Monetization Preview */}
          <div className="bg-gradient-to-r from-green-50 to-blue-50 p-4 rounded-lg">
            <h4 className="font-semibold text-gray-800 mb-2">💰 Monetize Your Cooking Skills</h4>
            <div className="grid grid-cols-2 gap-2 text-xs">
              <div className="bg-white p-2 rounded">📱 Paid Consultations</div>
              <div className="bg-white p-2 rounded">🏠 Home Restaurant</div>
              <div className="bg-white p-2 rounded">🛒 Grocery Partnership</div>
              <div className="bg-white p-2 rounded">📺 Recipe Ads</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Enhanced Navigation Header
const Header = () => {
  const { user, logout } = useAuth();
  const { t } = useTranslation();

  return (
    <header className="nav-header shadow-lg border-b">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo and Navigation */}
          <div className="flex items-center space-x-8">
            <Link to="/" className="flex items-center space-x-3 group">
              <img 
                src="https://customer-assets.emergentagent.com/job_lambalia-recipes/artifacts/qzs71f09_2.png" 
                alt="Lambalia - Global Heritage Recipes" 
                className="w-12 h-12 transition-transform group-hover:scale-110 drop-shadow-md"
              />
              <h1 className="text-2xl font-bold heading-gradient">Lambalia</h1>
            </Link>
            <nav className="hidden md:flex space-x-1">
              <Link to="/templates" className="nav-link text-gray-700 hover:text-green-600 px-3 py-2 rounded-md font-medium">
                {t('nav.browse')}
              </Link>
              <Link to="/create-snippet" className="nav-link text-gray-700 hover:text-green-600 px-3 py-2 rounded-md font-medium">
                {t('nav.create')}
              </Link>
              <Link to="/grocery" className="nav-link text-gray-700 hover:text-green-600 px-3 py-2 rounded-md font-medium">
                {t('nav.ingredients')}
              </Link>
              <Link to="/home-restaurant" className="nav-link text-gray-700 hover:text-green-600 px-3 py-2 rounded-md font-medium">
                {t('nav.restaurant')}
              </Link>
              <Link to="/local-marketplace" className="nav-link text-gray-700 hover:text-green-600 px-3 py-2 rounded-md font-medium">
                {t('nav.marketplace')}
              </Link>
              <Link to="/charity-program" className="nav-link text-gray-700 hover:text-green-600 px-3 py-2 rounded-md font-medium">
                {t('nav.charity')}
              </Link>
              <Link to="/lambalia-eats" className="nav-link text-gray-700 hover:text-orange-600 px-3 py-2 rounded-md font-medium">
                {t('nav.eats')}
              </Link>
              <Link to="/profile" className="nav-link text-gray-700 hover:text-green-600 px-3 py-2 rounded-md font-medium">
                {t('nav.profile')}
              </Link>
            </nav>
          </div>

          {/* User actions and Language Switcher */}
          <div className="flex items-center space-x-4">
            <LanguageSwitcher />
            
            {user ? (
              <div className="flex items-center space-x-4">
                <span className="text-sm text-gray-700">
                  {t('common.welcome', { name: user.username || user.full_name })}
                </span>
                <button 
                  onClick={logout}
                  className="text-sm text-gray-500 hover:text-gray-700"
                >
                  {t('auth.logout')}
                </button>
              </div>
            ) : (
              <div className="flex items-center space-x-4">
                <Link to="/login" className="text-sm text-gray-700 hover:text-green-600">
                  {t('auth.login')}
                </Link>
                <Link to="/register" className="btn-primary px-4 py-2 rounded-md text-sm">
                  {t('auth.joinLambalia')}
                </Link>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};

// Communication Tools Component
const CommunicationTools = ({ recipientId, recipientName }) => {
  const [showPayment, setShowPayment] = useState(null);

  const communicationOptions = [
    {
      type: 'message',
      icon: '💬',
      name: 'WhatsApp Message',
      price: 2.99,
      description: 'Real-time text chat about the recipe'
    },
    {
      type: 'audio',
      icon: '📞',
      name: 'Voice Call',
      price: 7.99,
      description: 'Live voice consultation (15 min)'
    },
    {
      type: 'video',
      icon: '📹',
      name: 'Video Call',
      price: 12.99,
      description: 'Live cooking session (20 min)'
    }
  ];

  const handleCommunication = async (option) => {
    setShowPayment(option);
  };

  const processCommunication = async (option) => {
    try {
      // Mock payment processing
      console.log(`Processing ${option.type} communication for $${option.price}`);
      
      // Here would be the actual API integration
      if (option.type === 'message') {
        // WhatsApp API integration
        window.open(`https://wa.me/1234567890?text=Hi! I'm interested in your ${recipientName} recipe from Lambalia!`);
      } else if (option.type === 'audio') {
        // Voice call API (Twilio, etc.)
        alert('Voice call feature coming soon! You\'ll be connected via phone call.');
      } else if (option.type === 'video') {
        // Video call API (Zoom, Jitsi, etc.)
        alert('Video call feature coming soon! You\'ll join a live cooking session.');
      }
      
      setShowPayment(null);
    } catch (error) {
      console.error('Communication failed:', error);
    }
  };

  return (
    <div className="communication-tools">
      {communicationOptions.map((option) => (
        <div key={option.type} className="tooltip">
          <div
            className={`comm-tool ${option.type}`}
            onClick={() => handleCommunication(option)}
          >
            <span className="text-xl">{option.icon}</span>
            <div className="price-badge">${option.price}</div>
          </div>
          <span className="tooltiptext">{option.description}</span>
        </div>
      ))}

      {/* Payment Modal */}
      {showPayment && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white p-6 rounded-xl max-w-md w-full mx-4">
            <h3 className="text-xl font-bold mb-4">Connect with {recipientName}</h3>
            <div className="mb-4">
              <p className="text-lg">{showPayment.name}</p>
              <p className="text-sm text-gray-600">{showPayment.description}</p>
              <p className="text-2xl font-bold text-green-600 mt-2">${showPayment.price}</p>
            </div>
            <div className="flex gap-3">
              <button
                onClick={() => processCommunication(showPayment)}
                className="flex-1 btn-primary py-3 rounded-lg"
              >
                Pay & Connect
              </button>
              <button
                onClick={() => setShowPayment(null)}
                className="flex-1 bg-gray-200 hover:bg-gray-300 py-3 rounded-lg"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

// Ad Component
const AdComponent = ({ placement = "feed" }) => {
  const [adContent, setAdContent] = useState(null);

  useEffect(() => {
    // Mock ad loading - in production, integrate with Google AdSense or similar
    const mockAds = [
      {
        title: "Premium Kitchen Tools",
        description: "Upgrade your cooking with professional-grade equipment",
        image: "🔪",
        sponsor: "CookingPro"
      },
      {
        title: "Organic Ingredients Delivered",
        description: "Fresh, organic ingredients delivered to your door",
        image: "🥕",
        sponsor: "FreshDirect"
      },
      {
        title: "Cooking Classes Online",
        description: "Learn from master chefs around the world",
        image: "👨‍🍳",
        sponsor: "MasterClass"
      }
    ];

    const randomAd = mockAds[Math.floor(Math.random() * mockAds.length)];
    setAdContent(randomAd);
  }, []);

  if (!adContent) return null;

  return (
    <div className="ad-container">
      <div className="flex items-center space-x-4">
        <div className="text-4xl">{adContent.image}</div>
        <div className="flex-1">
          <h4 className="font-semibold text-gray-800">{adContent.title}</h4>
          <p className="text-sm text-gray-600">{adContent.description}</p>
          <p className="text-xs text-gray-500">Sponsored by {adContent.sponsor}</p>
        </div>
        <button className="btn-secondary text-sm px-4 py-2">
          Learn More
        </button>
      </div>
    </div>
  );
};

// Home Restaurant Feature Component
// Home Restaurant Card Component
const HomeRestaurantCard = ({ restaurant }) => (
  <div className="recipe-card">
    <div className="p-6">
      <div className="flex items-start justify-between mb-3">
        <div>
          <h3 className="text-lg font-semibold text-gray-800">{restaurant.restaurant_name}</h3>
          <p className="text-sm text-gray-500">by Host • {restaurant.address}</p>
        </div>
        <span className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded-full">
          Home Kitchen
        </span>
      </div>
      
      <p className="text-gray-600 mb-3 line-clamp-2">{restaurant.description}</p>
      
      <div className="flex items-center text-sm text-gray-500 mb-3">
        <span>👥 {restaurant.dining_capacity} guests max</span>
        <span className="mx-2">•</span>
        <span>💰 ${restaurant.base_price_per_person}/person</span>
        <span className="mx-2">•</span>
        <span>⭐ {restaurant.average_rating || 'New'}</span>
      </div>

      <div className="mb-3">
        <div className="flex flex-wrap gap-1">
          {restaurant.cuisine_type.slice(0, 3).map((cuisine, index) => (
            <span key={index} className="bg-blue-100 text-blue-700 text-xs px-2 py-1 rounded">
              {cuisine}
            </span>
          ))}
        </div>
      </div>
      
      <div className="flex items-center justify-between">
        <div className="text-sm text-gray-500">
          {restaurant.is_accepting_bookings ? (
            <span className="text-green-600">✅ Accepting bookings</span>
          ) : (
            <span className="text-red-600">❌ Fully booked</span>
          )}
        </div>
        <button className="btn-primary px-4 py-2 rounded-lg text-sm">
          Book Now
        </button>
      </div>
    </div>
  </div>
);

// Special Order Card Component
const SpecialOrderCard = ({ order }) => (
  <div className="recipe-card">
    <div className="p-6">
      <div className="flex items-start justify-between mb-3">
        <div>
          <h3 className="text-lg font-semibold text-gray-800">{order.title}</h3>
          <p className="text-sm text-gray-500">by {order.restaurant_name}</p>
        </div>
        <span className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full">
          Special Order
        </span>
      </div>
      
      <p className="text-gray-600 mb-3 line-clamp-2">{order.description}</p>
      
      <div className="flex items-center text-sm text-gray-500 mb-3">
        <span>👥 {order.minimum_people}-{order.maximum_people} people</span>
        <span className="mx-2">•</span>
        <span>💰 ${order.price_per_person}/person</span>
      </div>

      <div className="mb-3">
        <div className="flex flex-wrap gap-1">
          <span className="bg-purple-100 text-purple-700 text-xs px-2 py-1 rounded">
            {order.cuisine_style}
          </span>
          {order.occasion_type && (
            <span className="bg-pink-100 text-pink-700 text-xs px-2 py-1 rounded">
              {order.occasion_type}
            </span>
          )}
          {order.vegetarian_options && (
            <span className="bg-green-100 text-green-700 text-xs px-2 py-1 rounded">
              Vegetarian
            </span>
          )}
        </div>
      </div>

      <div className="mb-3">
        <p className="text-xs text-gray-500">Available services:</p>
        <div className="flex space-x-2 text-xs mt-1">
          {order.delivery_available && <span className="bg-gray-100 px-2 py-1 rounded">🚚 Delivery</span>}
          {order.pickup_available && <span className="bg-gray-100 px-2 py-1 rounded">🏃 Pickup</span>}
          {order.dine_in_available && <span className="bg-gray-100 px-2 py-1 rounded">🍽️ Dine-in</span>}
        </div>
      </div>
      
      <div className="flex items-center justify-between">
        <div className="text-sm text-gray-500">
          <span>⏰ {order.preparation_time_hours}h prep</span>
        </div>
        <button className="btn-primary px-4 py-2 rounded-lg text-sm">
          View Details
        </button>
      </div>
    </div>
  </div>
);

// Home Restaurant Application Form
const HomeRestaurantApplicationForm = () => {
  const [formData, setFormData] = useState({
    legal_name: '',
    phone_number: '',
    address: '',
    city: '',
    state: '',
    postal_code: '',
    country: 'US',
    kitchen_description: '',
    dining_capacity: 4,
    cuisine_specialties: [],
    dietary_accommodations: [],
    has_food_handling_experience: false,
    years_cooking_experience: 0,
    has_liability_insurance: false,
    emergency_contact_name: '',
    emergency_contact_phone: ''
  });
  const [submitting, setSubmitting] = useState(false);

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);

    try {
      const submitData = {
        ...formData,
        vendor_type: 'home_restaurant',
        dining_capacity: parseInt(formData.dining_capacity),
        years_cooking_experience: parseInt(formData.years_cooking_experience),
        background_check_consent: true,
        terms_accepted: true,
        privacy_policy_accepted: true
      };

      await axios.post(`${API}/vendor/apply`, submitData);
      alert('Application submitted successfully! We will review it within 3-5 business days.');
    } catch (error) {
      console.error('Failed to submit application:', error);
      alert('Failed to submit application. Please try again.');
    }
    setSubmitting(false);
  };

  return (
    <div className="glass p-8">
      <h3 className="text-2xl font-bold heading-gradient mb-6">Home Restaurant Application</h3>
      
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Personal Information */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Legal Name *</label>
            <input
              type="text"
              name="legal_name"
              value={formData.legal_name}
              onChange={handleInputChange}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Phone Number *</label>
            <input
              type="tel"
              name="phone_number"
              value={formData.phone_number}
              onChange={handleInputChange}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
              required
            />
          </div>
        </div>

        {/* Address */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Home Address *</label>
          <input
            type="text"
            name="address"
            value={formData.address}
            onChange={handleInputChange}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
            required
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">City *</label>
            <input
              type="text"
              name="city"
              value={formData.city}
              onChange={handleInputChange}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">State *</label>
            <input
              type="text"
              name="state"
              value={formData.state}
              onChange={handleInputChange}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Postal Code *</label>
            <input
              type="text"
              name="postal_code"
              value={formData.postal_code}
              onChange={handleInputChange}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
              required
            />
          </div>
        </div>

        {/* Kitchen Information */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Kitchen Description *</label>
          <textarea
            name="kitchen_description"
            value={formData.kitchen_description}
            onChange={handleInputChange}
            rows="3"
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
            placeholder="Describe your kitchen setup, equipment, and dining area..."
            required
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Dining Capacity *</label>
            <select
              name="dining_capacity"
              value={formData.dining_capacity}
              onChange={handleInputChange}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
            >
              {[2,3,4,5,6,7,8,9,10,12,15,20].map(num => (
                <option key={num} value={num}>{num} guests</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Cooking Experience (years)</label>
            <input
              type="number"
              name="years_cooking_experience"
              value={formData.years_cooking_experience}
              onChange={handleInputChange}
              min="0"
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
            />
          </div>
        </div>

        {/* Emergency Contact */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Emergency Contact Name *</label>
            <input
              type="text"
              name="emergency_contact_name"
              value={formData.emergency_contact_name}
              onChange={handleInputChange}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Emergency Contact Phone *</label>
            <input
              type="tel"
              name="emergency_contact_phone"
              value={formData.emergency_contact_phone}
              onChange={handleInputChange}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
              required
            />
          </div>
        </div>

        {/* Checkboxes */}
        <div className="space-y-3">
          <label className="flex items-center">
            <input
              type="checkbox"
              name="has_food_handling_experience"
              checked={formData.has_food_handling_experience}
              onChange={handleInputChange}
              className="rounded border-gray-300 text-green-600 focus:ring-green-500"
            />
            <span className="ml-2 text-sm text-gray-700">I have food handling experience</span>
          </label>
          <label className="flex items-center">
            <input
              type="checkbox"
              name="has_liability_insurance"
              checked={formData.has_liability_insurance}
              onChange={handleInputChange}
              className="rounded border-gray-300 text-green-600 focus:ring-green-500"
            />
            <span className="ml-2 text-sm text-gray-700">I have liability insurance</span>
          </label>
        </div>

        <div className="flex justify-end pt-6">
          <button
            type="submit"
            disabled={submitting}
            className="btn-primary font-medium py-3 px-8 rounded-lg text-lg disabled:opacity-50"
          >
            {submitting ? 'Submitting Application... ⏳' : 'Submit Application ✨'}
          </button>
        </div>
      </form>
    </div>
  );
};

// Traditional Restaurant Application Form
const TraditionalRestaurantApplicationForm = () => {
  const [formData, setFormData] = useState({
    legal_name: '',
    phone_number: '',
    address: '',
    city: '',
    state: '',
    postal_code: '',
    country: 'US',
    restaurant_name: '',
    business_license_number: '',
    years_in_business: 0,
    cuisine_specialties: [],
    dietary_accommodations: [],
    has_food_handling_experience: true,
    years_cooking_experience: 0,
    has_liability_insurance: false,
    emergency_contact_name: '',
    emergency_contact_phone: ''
  });
  const [submitting, setSubmitting] = useState(false);

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);

    try {
      const submitData = {
        ...formData,
        vendor_type: 'traditional_restaurant',
        years_in_business: parseInt(formData.years_in_business),
        years_cooking_experience: parseInt(formData.years_cooking_experience),
        background_check_consent: true,
        terms_accepted: true,
        privacy_policy_accepted: true
      };

      await axios.post(`${API}/vendor/apply`, submitData);
      alert('Application submitted successfully! We will review it within 3-5 business days.');
    } catch (error) {
      console.error('Failed to submit application:', error);
      alert('Failed to submit application. Please try again.');
    }
    setSubmitting(false);
  };

  return (
    <div className="glass p-8">
      <h3 className="text-2xl font-bold heading-gradient mb-6">Traditional Restaurant Application</h3>
      
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Personal Information */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Legal Name *</label>
            <input
              type="text"
              name="legal_name"
              value={formData.legal_name}
              onChange={handleInputChange}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Phone Number *</label>
            <input
              type="tel"
              name="phone_number"
              value={formData.phone_number}
              onChange={handleInputChange}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
              required
            />
          </div>
        </div>

        {/* Restaurant Information */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Restaurant Name *</label>
            <input
              type="text"
              name="restaurant_name"
              value={formData.restaurant_name}
              onChange={handleInputChange}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Business License Number *</label>
            <input
              type="text"
              name="business_license_number"
              value={formData.business_license_number}
              onChange={handleInputChange}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
              required
            />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Years in Business *</label>
          <input
            type="number"
            name="years_in_business"
            value={formData.years_in_business}
            onChange={handleInputChange}
            min="0"
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
            required
          />
        </div>

        {/* Address */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Restaurant Address *</label>
          <input
            type="text"
            name="address"
            value={formData.address}
            onChange={handleInputChange}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
            required
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">City *</label>
            <input
              type="text"
              name="city"
              value={formData.city}
              onChange={handleInputChange}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">State *</label>
            <input
              type="text"
              name="state"
              value={formData.state}
              onChange={handleInputChange}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Postal Code *</label>
            <input
              type="text"
              name="postal_code"
              value={formData.postal_code}
              onChange={handleInputChange}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
              required
            />
          </div>
        </div>

        {/* Experience */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Professional Cooking Experience (years)</label>
          <input
            type="number"
            name="years_cooking_experience"
            value={formData.years_cooking_experience}
            onChange={handleInputChange}
            min="0"
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
          />
        </div>

        {/* Emergency Contact */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Emergency Contact Name *</label>
            <input
              type="text"
              name="emergency_contact_name"
              value={formData.emergency_contact_name}
              onChange={handleInputChange}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Emergency Contact Phone *</label>
            <input
              type="tel"
              name="emergency_contact_phone"
              value={formData.emergency_contact_phone}
              onChange={handleInputChange}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
              required
            />
          </div>
        </div>

        {/* Checkboxes */}
        <div className="space-y-3">
          <label className="flex items-center">
            <input
              type="checkbox"
              name="has_liability_insurance"
              checked={formData.has_liability_insurance}
              onChange={handleInputChange}
              className="rounded border-gray-300 text-green-600 focus:ring-green-500"
            />
            <span className="ml-2 text-sm text-gray-700">I have business liability insurance</span>
          </label>
        </div>

        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <h4 className="font-semibold text-blue-800 mb-2">💼 Traditional Restaurant Benefits</h4>
          <ul className="text-sm text-blue-700 space-y-1">
            <li>• Create custom special order proposals</li>
            <li>• Set your own pricing and menu offerings</li>
            <li>• Reach customers beyond your normal service area</li>
            <li>• Generate additional revenue stream with 15% platform fee</li>
          </ul>
        </div>

        <div className="flex justify-end pt-6">
          <button
            type="submit"
            disabled={submitting}
            className="btn-primary font-medium py-3 px-8 rounded-lg text-lg disabled:opacity-50"
          >
            {submitting ? 'Submitting Application... ⏳' : 'Submit Application ✨'}
          </button>
        </div>
      </form>
    </div>
  );
};

const HomeRestaurantPage = () => {
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState('browse'); // 'browse', 'home-restaurant', 'traditional-restaurant'
  const [restaurantType, setRestaurantType] = useState('home'); // 'home' or 'traditional'
  const [homeRestaurants, setHomeRestaurants] = useState([]);
  const [traditionalRestaurants, setTraditionalRestaurants] = useState([]);
  const [specialOrders, setSpecialOrders] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (activeTab === 'browse') {
      fetchRestaurants();
      fetchSpecialOrders();
    }
  }, [activeTab]);

  const fetchRestaurants = async () => {
    setLoading(true);
    try {
      const [homeResponse, traditionalResponse] = await Promise.all([
        axios.get(`${API}/restaurants`),
        axios.get(`${API}/traditional-restaurants`)
      ]);
      setHomeRestaurants(homeResponse.data);
      setTraditionalRestaurants(traditionalResponse.data);
    } catch (error) {
      console.error('Failed to fetch restaurants:', error);
    }
    setLoading(false);
  };

  const fetchSpecialOrders = async () => {
    try {
      const response = await axios.get(`${API}/special-orders`);
      setSpecialOrders(response.data);
    } catch (error) {
      console.error('Failed to fetch special orders:', error);
    }
  };

  const RestaurantBrowsingTab = () => (
    <div className="space-y-6">
      {/* Header */}
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold heading-gradient mb-4">Restaurant Marketplace</h2>
        <p className="text-gray-600 mb-6">Discover home kitchens and traditional restaurants offering unique dining experiences</p>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-2xl mx-auto">
          <div className="glass p-4 text-center">
            <h3 className="font-semibold mb-2">🏠 Home Restaurants</h3>
            <p className="text-sm text-gray-600">Intimate dining in local homes</p>
            <p className="font-bold text-green-600">{homeRestaurants.length} available</p>
          </div>
          <div className="glass p-4 text-center">
            <h3 className="font-semibold mb-2">🍽️ Traditional Restaurants</h3>
            <p className="text-sm text-gray-600">Special orders & custom meals</p>
            <p className="font-bold text-blue-600">{specialOrders.length} special orders</p>
          </div>
        </div>
      </div>

      {/* Home Restaurants Section */}
      <div className="mb-8">
        <h3 className="text-2xl font-bold text-gray-800 mb-4">🏠 Home Restaurants</h3>
        {loading ? (
          <div className="flex justify-center items-center h-32">
            <div className="loading text-4xl">⏳</div>
          </div>
        ) : homeRestaurants.length === 0 ? (
          <div className="text-center py-8 glass">
            <p className="text-gray-500">No home restaurants available yet.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {homeRestaurants.map((restaurant) => (
              <HomeRestaurantCard key={restaurant.id} restaurant={restaurant} />
            ))}
          </div>
        )}
      </div>

      {/* Traditional Restaurants & Special Orders Section */}
      <div>
        <h3 className="text-2xl font-bold text-gray-800 mb-4">🍽️ Special Orders from Traditional Restaurants</h3>
        {specialOrders.length === 0 ? (
          <div className="text-center py-8 glass">
            <p className="text-gray-500">No special orders available yet.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {specialOrders.map((order) => (
              <SpecialOrderCard key={order.id} order={order} />
            ))}
          </div>
        )}
      </div>
    </div>
  );

  const VendorApplicationTab = () => (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8 text-center">
        <h2 className="text-3xl font-bold heading-gradient mb-4">Become a Restaurant Partner</h2>
        <p className="text-gray-600 mb-6">Choose your restaurant type and start earning with Lambalia</p>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <div 
            className={`glass p-6 cursor-pointer transition-all ${restaurantType === 'home' ? 'ring-2 ring-green-500' : ''}`}
            onClick={() => setRestaurantType('home')}
          >
            <h3 className="text-xl font-semibold mb-3">🏠 Home Restaurant</h3>
            <ul className="text-sm space-y-2 text-left">
              <li>• Host 2-8 guests in your dining room</li>
              <li>• Share authentic home-cooked meals</li>
              <li>• Flexible scheduling</li>
              <li>• $30-80 per person</li>
            </ul>
            <div className="mt-4 text-green-600 font-semibold">Monthly potential: $500-2000+</div>
          </div>

          <div 
            className={`glass p-6 cursor-pointer transition-all ${restaurantType === 'traditional' ? 'ring-2 ring-blue-500' : ''}`}
            onClick={() => setRestaurantType('traditional')}
          >
            <h3 className="text-xl font-semibold mb-3">🍽️ Traditional Restaurant</h3>
            <ul className="text-sm space-y-2 text-left">
              <li>• Create special order proposals</li>
              <li>• Showcase signature dishes</li>
              <li>• Delivery & pickup options</li>
              <li>• $50-200 per person</li>
            </ul>
            <div className="mt-4 text-blue-600 font-semibold">Additional revenue stream</div>
          </div>
        </div>
      </div>

      {restaurantType === 'home' ? <HomeRestaurantApplicationForm /> : <TraditionalRestaurantApplicationForm />}
    </div>
  );

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Tab Navigation */}
      <div className="mb-8">
        <div className="flex space-x-1 bg-gray-100 p-1 rounded-lg max-w-md mx-auto">
          <button
            onClick={() => setActiveTab('browse')}
            className={`flex-1 px-4 py-2 text-sm font-medium rounded-md transition-all ${
              activeTab === 'browse'
                ? 'bg-white text-green-600 shadow-sm'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            🍽️ Browse Restaurants
          </button>
          <button
            onClick={() => setActiveTab('vendor')}
            className={`flex-1 px-4 py-2 text-sm font-medium rounded-md transition-all ${
              activeTab === 'vendor'
                ? 'bg-white text-green-600 shadow-sm'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            👩‍🍳 Become a Partner
          </button>
        </div>
      </div>

      {/* Tab Content */}
      {activeTab === 'browse' ? <RestaurantBrowsingTab /> : <VendorApplicationTab />}
    </div>
  );
};

// Enhanced Profile Page with Monetization Features
const ProfilePage = () => {
  const { user } = useAuth();
  const [userSnippets, setUserSnippets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [earnings, setEarnings] = useState({
    communication: 145.80,
    homeRestaurant: 890.50,
    groceryCommissions: 67.20,
    adRevenue: 23.45
  });

  useEffect(() => {
    if (user) {
      fetchUserSnippets();
    }
  }, [user]);

  const fetchUserSnippets = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API}/users/${user.id}/snippets/playlist`);
      setUserSnippets(response.data);
    } catch (error) {
      console.error('Failed to fetch user snippets:', error);
    }
    setLoading(false);
  };

  const SnippetCard = ({ snippet, playlistIndex }) => (
    <div className="recipe-card overflow-hidden">
      <div className="p-6">
        <div className="flex items-start justify-between mb-3">
          <div className="flex items-center space-x-3">
            <span className="bg-green-500 text-white w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold">
              {playlistIndex + 1}
            </span>
            <div>
              <h3 className="text-lg font-semibold text-gray-800">{snippet.title}</h3>
              {snippet.title_local && (
                <p className="text-green-600 font-medium">{snippet.title_local}</p>
              )}
            </div>
          </div>
          <span className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full capitalize">
            {snippet.snippet_type.replace('_', ' ')}
          </span>
        </div>
        
        <p className="text-gray-600 mb-3 line-clamp-2">{snippet.description}</p>
        
        <div className="flex items-center text-sm text-gray-500 mb-3">
          <span>🕒 {snippet.cooking_time_minutes} min</span>
          <span className="mx-2">•</span>
          <span>⭐ {'★'.repeat(snippet.difficulty_level)}</span>
          <span className="mx-2">•</span>
          <span>🍽️ {snippet.servings} servings</span>
          {snippet.video_duration && (
            <>
              <span className="mx-2">•</span>
              <span>🎥 {snippet.video_duration}s</span>
            </>
          )}
        </div>
        
        {/* Communication Tools for Each Snippet */}
        <div className="mb-4">
          <p className="text-sm text-gray-600 mb-2">Want to learn this recipe?</p>
          <CommunicationTools 
            recipientId={snippet.author_id} 
            recipientName={snippet.title}
          />
        </div>
        
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4 text-sm text-gray-500">
            <span>❤️ {snippet.likes_count}</span>
            <span>👁 {snippet.views_count}</span>
            <span>💾 {snippet.saves_count}</span>
          </div>
          
          {snippet.tags.length > 0 && (
            <div className="flex flex-wrap gap-1">
              {snippet.tags.slice(0, 2).map((tag, index) => (
                <span key={index} className="bg-gray-100 text-gray-600 text-xs px-2 py-1 rounded">
                  #{tag}
                </span>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );

  if (!user) return null;

  const totalEarnings = Object.values(earnings).reduce((sum, val) => sum + val, 0);

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Enhanced Profile Header */}
      <div className="glass p-8 mb-8">
        <div className="flex items-center space-x-6">
          <div className="w-24 h-24 bg-gradient-to-r from-green-400 to-blue-500 rounded-full flex items-center justify-center">
            <span className="text-3xl font-bold text-white">
              {user.username.charAt(0).toUpperCase()}
            </span>
          </div>
          
          <div className="flex-1">
            <h1 className="text-3xl font-bold text-gray-800">{user.full_name || user.username}</h1>
            <p className="text-gray-600">@{user.username}</p>
            {user.bio && <p className="text-gray-700 mt-2">{user.bio}</p>}
            
            <div className="flex items-center space-x-6 mt-4 text-sm text-gray-600">
              <span><strong>{user.recipes_count || 0}</strong> Recipes</span>
              <span><strong>{user.snippets_count || 0}</strong> Snippets</span>
              <span><strong>{user.followers_count}</strong> Followers</span>
              <span><strong>{user.following_count}</strong> Following</span>
              <span><strong className="text-green-600">${user.credits || 0}</strong> Credits</span>
            </div>
          </div>

          {/* Communication Tools in Profile */}
          <div className="text-center">
            <p className="text-sm text-gray-600 mb-2">Connect with me:</p>
            <CommunicationTools 
              recipientId={user.id} 
              recipientName={user.username}
            />
          </div>
        </div>
      </div>

      {/* Revenue Dashboard */}
      <div className="revenue-dashboard mb-8">
        <h2 className="text-2xl font-bold mb-4">💰 Your Earnings Dashboard</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
          <div className="revenue-item">
            <div>
              <p className="text-sm opacity-90">Communication Fees</p>
              <p className="text-xs opacity-75">Messages, calls, video</p>
            </div>
            <div className="revenue-amount">${earnings.communication}</div>
          </div>
          <div className="revenue-item">
            <div>
              <p className="text-sm opacity-90">Home Restaurant</p>
              <p className="text-xs opacity-75">Dining experiences</p>
            </div>
            <div className="revenue-amount">${earnings.homeRestaurant}</div>
          </div>
          <div className="revenue-item">
            <div>
              <p className="text-sm opacity-90">Grocery Commissions</p>
              <p className="text-xs opacity-75">Ingredient sales</p>
            </div>
            <div className="revenue-amount">${earnings.groceryCommissions}</div>
          </div>
          <div className="revenue-item">
            <div>
              <p className="text-sm opacity-90">Ad Revenue</p>
              <p className="text-xs opacity-75">Recipe page ads</p>
            </div>
            <div className="revenue-amount">${earnings.adRevenue}</div>
          </div>
        </div>
        <div className="text-center">
          <p className="text-xl font-bold">Total Monthly Earnings: ${totalEarnings.toFixed(2)}</p>
          <button className="btn-secondary mt-3 px-6 py-2">💳 Withdraw Earnings</button>
        </div>
      </div>

      {/* Ad Placement */}
      <AdComponent placement="profile" />

      {/* Snippets Playlist */}
      <div className="mb-6">
        <div className="flex items-center justify-between">
          <h2 className="text-2xl font-bold text-gray-800">My Recipe Snippets Playlist</h2>
          <Link
            to="/create-snippet"
            className="btn-primary px-4 py-2 rounded-lg"
          >
            Create New Snippet ✨
          </Link>
        </div>
        <p className="text-gray-600 mt-2">Your snippets are displayed in playlist order for easy viewing</p>
      </div>
      
      {loading ? (
        <div className="flex justify-center items-center h-32">
          <div className="loading text-4xl">⏳</div>
        </div>
      ) : userSnippets.length === 0 ? (
        <div className="text-center py-12 glass">
          <p className="text-gray-500 mb-4 text-lg">You haven't created any snippets yet.</p>
          <Link
            to="/create-snippet"
            className="btn-primary px-6 py-3 rounded-lg text-lg"
          >
            Create Your First Snippet 🚀
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {userSnippets.map((snippet, index) => (
            <SnippetCard key={snippet.id} snippet={snippet} playlistIndex={index} />
          ))}
        </div>
      )}

      {/* Ad between snippets */}
      {userSnippets.length > 2 && <AdComponent placement="between-snippets" />}
    </div>
  );
};

// Recipe Templates Page (keeping existing enhanced version)
const RecipeTemplatesPage = () => {
  const [referenceRecipes, setReferenceRecipes] = useState([]);
  const [nativeRecipes, setNativeRecipes] = useState({});
  const [countries, setCountries] = useState([]);
  const [selectedCountry, setSelectedCountry] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchInitialData();
  }, []);

  useEffect(() => {
    fetchReferenceRecipes();
  }, [selectedCountry, selectedCategory, searchQuery]);

  const fetchInitialData = async () => {
    try {
      const [countriesResponse, nativeResponse] = await Promise.all([
        axios.get(`${API}/countries`),
        axios.get(`${API}/native-recipes`)
      ]);
      setCountries(countriesResponse.data);
      setNativeRecipes(nativeResponse.data.native_recipes);
    } catch (error) {
      console.error('Failed to fetch initial data:', error);
    }
  };

  const fetchReferenceRecipes = async () => {
    setLoading(true);
    try {
      let url = `${API}/reference-recipes?featured_only=true&limit=50`;
      
      if (searchQuery) {
        url = `${API}/reference-recipes/search?q=${encodeURIComponent(searchQuery)}&limit=30`;
      } else {
        if (selectedCountry) url += `&country_id=${selectedCountry}`;
        if (selectedCategory) url += `&category=${selectedCategory}`;
      }
      
      const response = await axios.get(url);
      setReferenceRecipes(response.data);
    } catch (error) {
      console.error('Failed to fetch reference recipes:', error);
    }
    setLoading(false);
  };

  const ReferenceRecipeCard = ({ recipe }) => (
    <div className="recipe-card">
      <div className="p-6">
        <div className="flex items-start justify-between mb-3">
          <div>
            <h3 className="text-xl font-semibold text-gray-800">{recipe.name_english}</h3>
            {recipe.name_local !== recipe.name_english && (
              <p className="text-lg text-green-600 font-medium">{recipe.name_local}</p>
            )}
            {recipe.local_language && recipe.local_language !== 'English' && (
              <span className="inline-block bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full mt-1">
                {recipe.local_language}
              </span>
            )}
          </div>
          <div className="flex flex-col items-end space-y-1">
            <span className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded-full capitalize">
              {recipe.category}
            </span>
            <span className="bg-yellow-100 text-yellow-800 text-xs px-2 py-1 rounded-full">
              {recipe.popularity_score}/100
            </span>
          </div>
        </div>
        
        <p className="text-gray-600 mb-3 line-clamp-3">{recipe.description}</p>
        
        <div className="flex items-center text-sm text-gray-500 mb-3">
          <span>⭐ {'★'.repeat(recipe.difficulty_level)}</span>
          <span className="mx-2">•</span>
          <span>🕒 {recipe.estimated_time} min</span>
          <span className="mx-2">•</span>
          <span>🍽️ {recipe.serving_size}</span>
        </div>
        
        <div className="mb-3">
          <h4 className="font-medium text-gray-800 mb-2">Key Ingredients:</h4>
          <div className="flex flex-wrap gap-1">
            {recipe.key_ingredients.slice(0, 4).map((ingredient, index) => (
              <span key={index} className="bg-gray-100 text-gray-700 text-xs px-2 py-1 rounded">
                {ingredient}
              </span>
            ))}
            {recipe.key_ingredients.length > 4 && (
              <span className="text-gray-400 text-xs">+{recipe.key_ingredients.length - 4} more</span>
            )}
          </div>
        </div>
        
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3 mb-4">
          <p className="text-sm text-yellow-800">
            <strong>Cultural Note:</strong> {recipe.cultural_significance}
          </p>
        </div>
        
        <div className="flex justify-between items-center">
          <div className="text-sm text-gray-500">
            <span className="capitalize">{recipe.country_id.replace('_', ' ')}</span>
            {recipe.is_featured && (
              <span className="ml-2 bg-red-100 text-red-800 text-xs px-2 py-1 rounded-full">
                Featured
              </span>
            )}
          </div>
          <Link
            to={`/create-snippet?template=${recipe.id}`}
            className="btn-primary px-4 py-2 rounded-lg text-sm"
          >
            Use This Template
          </Link>
        </div>
      </div>
    </div>
  );

  const CountryRecipesList = ({ countryName, recipes }) => (
    <div key={countryName} className="bg-white rounded-lg p-4 mb-4 shadow-sm">
      <h4 className="font-semibold text-gray-800 mb-2">{countryName} ({recipes.length - 1} recipes)</h4>
      <div className="flex flex-wrap gap-2">
        {recipes.filter(recipe => recipe !== 'Other').map((recipe, index) => (
          <span 
            key={index} 
            className="bg-blue-50 text-blue-700 text-sm px-3 py-1 rounded-full hover:bg-blue-100 cursor-pointer transition-colors"
            onClick={() => setSearchQuery(recipe)}
          >
            {recipe}
          </span>
        ))}
      </div>
    </div>
  );

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h2 className="text-3xl font-bold heading-gradient mb-4">Traditional Recipe Templates</h2>
        <p className="text-gray-600 mb-6">Choose from {Object.keys(nativeRecipes).length} countries with hundreds of authentic recipes</p>
        
        {/* Search and Filters */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <input
            type="text"
            placeholder="Search recipes or ingredients..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 transition-all"
          />
          
          <select
            value={selectedCountry}
            onChange={(e) => {
              setSelectedCountry(e.target.value);
              setSearchQuery('');
            }}
            className="px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 transition-all"
          >
            <option value="">All Countries ({Object.keys(nativeRecipes).length})</option>
            {Object.keys(nativeRecipes).sort().map(country => (
              <option key={country} value={country.toLowerCase().replace(' ', '_')}>
                {country} ({nativeRecipes[country].length - 1} recipes)
              </option>
            ))}
          </select>
          
          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            className="px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 transition-all"
          >
            <option value="">All Categories</option>
            <option value="main">Main Dishes</option>
            <option value="appetizer">Appetizers</option>
            <option value="dessert">Desserts</option>
            <option value="soup">Soups</option>
            <option value="breakfast">Breakfast</option>
          </select>
       </div>

        {/* Quick Clear Filters */}
        {(selectedCountry || selectedCategory || searchQuery) && (
          <div className="mb-6">
            <button
              onClick={() => {
                setSelectedCountry('');
                setSelectedCategory('');
                setSearchQuery('');
              }}
              className="text-green-600 text-sm hover:text-green-700 font-medium"
            >
              Clear all filters
            </button>
          </div>
        )}
      </div>

      {/* Ad Placement */}
      <AdComponent placement="templates-top" />

      {/* Native Recipes Overview */}
      {!searchQuery && !selectedCountry && !selectedCategory && (
        <div className="mb-8">
          <h3 className="text-xl font-semibold text-gray-800 mb-4">Browse by Country</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 max-h-96 overflow-y-auto">
            {Object.entries(nativeRecipes).sort().map(([countryName, recipes]) => (
              <CountryRecipesList key={countryName} countryName={countryName} recipes={recipes} />
            ))}
          </div>
        </div>
      )}

      {/* Reference Recipes Results */}
      {loading ? (
        <div className="flex justify-center items-center h-64">
          <div className="loading text-6xl">👩‍🍳</div>
        </div>
      ) : (
        <div>
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-xl font-semibold text-gray-800">
              {searchQuery ? `Search Results for "${searchQuery}"` : 
               selectedCountry ? `${selectedCountry.replace('_', ' ')} Recipes` : 
               'Featured Traditional Recipes'} 
              ({referenceRecipes.length})
            </h3>
          </div>
          
          {referenceRecipes.length === 0 ? (
            <div className="text-center py-12 glass">
              <p className="text-gray-500 text-lg mb-4">No recipes found. Try adjusting your search or filters.</p>
              <button
                onClick={() => {
                  setSelectedCountry('');
                  setSelectedCategory('');
                  setSearchQuery('');
                }}
                className="btn-primary px-6 py-3 rounded-lg"
              >
                Show All Recipes
              </button>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {referenceRecipes.map((recipe, index) => (
                <React.Fragment key={recipe.id}>
                  <ReferenceRecipeCard recipe={recipe} />
                  {/* Insert ad every 6 recipes */}
                  {(index + 1) % 6 === 0 && (
                    <div className="md:col-span-2 lg:col-span-3">
                      <AdComponent placement="between-recipes" />
                    </div>
                  )}
                </React.Fragment>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

// Keep existing components (CreateSnippetPage, GroceryPage, HomePage) with minor styling updates

// Enhanced Home Page with ads and monetization features
const HomePage = () => {
  const [snippets, setSnippets] = useState([]);
  const [loading, setLoading] = useState(true);
  const { t } = useTranslation();

  useEffect(() => {
    fetchSnippets();
  }, []);

  const fetchSnippets = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API}/snippets?limit=12`);
      setSnippets(response.data);
    } catch (error) {
      console.error('Failed to fetch snippets:', error);
    }
    setLoading(false);
  };

  const handleLike = async (snippetId) => {
    try {
      const response = await axios.post(`${API}/snippets/${snippetId}/like`);
      setSnippets(prev => prev.map(snippet => 
        snippet.id === snippetId 
          ? { ...snippet, likes_count: response.data.liked ? snippet.likes_count + 1 : snippet.likes_count - 1 }
          : snippet
      ));
    } catch (error) {
      console.error('Failed to like snippet:', error);
    }
  };

  const SnippetCard = ({ snippet }) => (
    <div className="recipe-card">
      <div className="p-6">
        <div className="flex items-start justify-between mb-3">
          <div>
            <h3 className="text-lg font-semibold text-gray-800">{snippet.title}</h3>
            {snippet.title_local && (
              <p className="text-green-600 font-medium">{snippet.title_local}</p>
            )}
            <p className="text-sm text-gray-500">by @{snippet.author_username}</p>
          </div>
          <span className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full capitalize">
            {snippet.snippet_type.replace('_', ' ')}
          </span>
        </div>
        
        <p className="text-gray-600 mb-3 line-clamp-2">{snippet.description}</p>
        
        <div className="flex items-center text-sm text-gray-500 mb-3">
          <span>🕒 {snippet.cooking_time_minutes} min</span>
          <span className="mx-2">•</span>
          <span>⭐ {'★'.repeat(snippet.difficulty_level)}</span>
          <span className="mx-2">•</span>
          <span>🍽️ {snippet.servings} servings</span>
        </div>

        {/* Communication Tools */}
        <div className="mb-4">
          <p className="text-sm text-gray-600 mb-2">Want to learn this recipe?</p>
          <CommunicationTools 
            recipientId={snippet.author_id} 
            recipientName={snippet.title}
          />
        </div>
        
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4 text-sm text-gray-500">
            <button
              onClick={() => handleLike(snippet.id)}
              className="flex items-center space-x-1 hover:text-red-500 transition-colors"
            >
              <span>❤️</span>
              <span>{snippet.likes_count}</span>
            </button>
            <span>👁 {snippet.views_count}</span>
            <span>💾 {snippet.saves_count}</span>
          </div>
          
          {snippet.video_duration && (
            <span className="bg-red-100 text-red-800 text-xs px-2 py-1 rounded-full">
              🎥 {snippet.video_duration}s video
            </span>
          )}
        </div>
      </div>
    </div>
  );

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h2 className="text-3xl font-bold heading-gradient mb-4">{t('home.title')}</h2>
        <p className="text-gray-600 mb-6">{t('home.subtitle')}</p>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-7 gap-4">
          <Link
            to="/templates"
            className="btn-primary text-center p-4 rounded-lg no-underline text-white"
          >
            {t('home.actions.browseName')}
          </Link>
          <Link
            to="/create-snippet"
            className="btn-secondary text-center p-4 rounded-lg no-underline text-white"
          >
            {t('home.actions.createName')}
          </Link>
          <Link
            to="/grocery"
            className="bg-blue-500 hover:bg-blue-600 text-center p-4 rounded-lg no-underline text-white transition-all"
          >
            {t('home.actions.ingredientsName')}
          </Link>
          <Link
            to="/home-restaurant"
            className="bg-purple-500 hover:bg-purple-600 text-center p-4 rounded-lg no-underline text-white transition-all"
          >
            {t('home.actions.restaurantName')}
          </Link>
          <Link
            to="/local-marketplace"
            className="bg-green-500 hover:bg-green-600 text-center p-4 rounded-lg no-underline text-white transition-all"
          >
            {t('home.actions.marketplaceName')}
          </Link>
          <Link
            to="/charity-program"
            className="bg-red-500 hover:bg-red-600 text-center p-4 rounded-lg no-underline text-white transition-all"
          >
            {t('home.actions.charityName')}
          </Link>
          <Link
            to="/lambalia-eats"
            className="bg-orange-500 hover:bg-orange-600 text-center p-4 rounded-lg no-underline text-white transition-all"
          >
            {t('home.actions.eatsName')}
          </Link>
        </div>
      </div>

      {/* Ad Placement */}
      <AdComponent placement="home-top" />

      {loading ? (
        <div className="flex justify-center items-center h-64">
          <div className="loading text-6xl">👩‍🍳</div>
        </div>
      ) : snippets.length === 0 ? (
        <div className="text-center py-12 glass">
          <p className="text-gray-500 text-lg">No recipe snippets found. Be the first to share your traditional recipe snippet on Lambalia!</p>
        </div>
      ) : (
        <div>
          <h3 className="text-xl font-semibold text-gray-800 mb-6">Latest Recipe Snippets</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {snippets.map((snippet, index) => (
              <React.Fragment key={snippet.id}>
                <SnippetCard snippet={snippet} />
                {/* Insert ad every 4 snippets */}
                {(index + 1) % 4 === 0 && (
                  <div className="md:col-span-2 lg:col-span-3">
                    <AdComponent placement="between-snippets" />
                  </div>
                )}
              </React.Fragment>
            ))}
          </div>
        </div>
      )}

      {/* Floating Action Button */}
      <Link to="/create-snippet" className="fab">
        ➕
      </Link>
    </div>
  );
};

// Keep existing CreateSnippetPage and GroceryPage components (too long for single response)
// Just need to add enhanced styling classes

// Create Snippet Page with Enhanced Monetization
const CreateSnippetPage = () => {
  const [formData, setFormData] = useState({
    title: '',
    title_local: '',
    local_language: '',
    description: '',
    snippet_type: 'quick_recipe',
    ingredients: [{ name: '', amount: '', unit: '' }],
    preparation_steps: [{ step_number: '1', description: '' }],
    cooking_time_minutes: '',
    difficulty_level: 3,
    servings: '',
    tags: [],
    video_duration: ''
  });
  const [submitting, setSubmitting] = useState(false);
  const navigate = useNavigate();

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const addIngredient = () => {
    setFormData(prev => ({
      ...prev,
      ingredients: [...prev.ingredients, { name: '', amount: '', unit: '' }]
    }));
  };

  const updateIngredient = (index, field, value) => {
    setFormData(prev => ({
      ...prev,
      ingredients: prev.ingredients.map((ing, i) => 
        i === index ? { ...ing, [field]: value } : ing
      )
    }));
  };

  const removeIngredient = (index) => {
    setFormData(prev => ({
      ...prev,
      ingredients: prev.ingredients.filter((_, i) => i !== index)
    }));
  };

  const addStep = () => {
    setFormData(prev => ({
      ...prev,
      preparation_steps: [...prev.preparation_steps, { 
        step_number: (prev.preparation_steps.length + 1).toString(), 
        description: '' 
      }]
    }));
  };

  const updateStep = (index, value) => {
    setFormData(prev => ({
      ...prev,
      preparation_steps: prev.preparation_steps.map((step, i) => 
        i === index ? { ...step, description: value } : step
      )
    }));
  };

  const removeStep = (index) => {
    setFormData(prev => ({
      ...prev,
      preparation_steps: prev.preparation_steps.filter((_, i) => i !== index).map((step, i) => ({
        ...step,
        step_number: (i + 1).toString()
      }))
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);

    try {
      const submitData = {
        ...formData,
        cooking_time_minutes: parseInt(formData.cooking_time_minutes),
        servings: parseInt(formData.servings),
        video_duration: formData.video_duration ? parseInt(formData.video_duration) : null,
        ingredients: formData.ingredients.filter(ing => ing.name.trim()),
        preparation_steps: formData.preparation_steps.filter(step => step.description.trim())
      };

      await axios.post(`${API}/snippets`, submitData);
      navigate('/profile');
    } catch (error) {
      console.error('Failed to create snippet:', error);
      alert('Failed to create snippet. Please try again.');
    }
    setSubmitting(false);
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="glass p-8">
        <h2 className="text-3xl font-bold heading-gradient mb-6">Create Recipe Snippet</h2>
        
        {/* Monetization Info */}
        <div className="bg-gradient-to-r from-green-100 to-blue-100 p-4 rounded-lg mb-6">
          <h3 className="font-semibold text-gray-800 mb-2">💰 Monetize This Snippet</h3>
          <p className="text-sm text-gray-600">
            Enable communication tools so other users can pay to learn from you! 
            Earn $2.99-$12.99 per consultation.
          </p>
        </div>
        
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Basic Info */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Recipe Title (English) *</label>
              <input
                type="text"
                name="title"
                value={formData.title}
                onChange={handleInputChange}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 transition-all"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Local Name (Optional)</label>
              <input
                type="text"
                name="title_local"
                value={formData.title_local}
                onChange={handleInputChange}
                placeholder="e.g., Pasta alla Carbonara"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 transition-all"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Local Language</label>
              <input
                type="text"
                name="local_language"
                value={formData.local_language}
                onChange={handleInputChange}
                placeholder="e.g., Italian, Spanish, Hindi"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 transition-all"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Snippet Type</label>
              <select
                name="snippet_type"
                value={formData.snippet_type}
                onChange={handleInputChange}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 transition-all"
              >
                <option value="quick_recipe">Quick Recipe</option>
                <option value="cooking_tip">Cooking Tip</option>
                <option value="ingredient_spotlight">Ingredient Spotlight</option>
                <option value="traditional_method">Traditional Method</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Description *</label>
            <textarea
              name="description"
              value={formData.description}
              onChange={handleInputChange}
              rows="3"
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 transition-all"
              placeholder="Brief description of your recipe snippet..."
              required
            />
          </div>

          {/* Recipe Details */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Cooking Time (minutes) *</label>
              <input
                type="number"
                name="cooking_time_minutes"
                value={formData.cooking_time_minutes}
                onChange={handleInputChange}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 transition-all"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Servings *</label>
              <input
                type="number"
                name="servings"
                value={formData.servings}
                onChange={handleInputChange}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 transition-all"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Difficulty Level</label>
              <select
                name="difficulty_level"
                value={formData.difficulty_level}
                onChange={handleInputChange}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 transition-all"
              >
                <option value={1}>⭐ Easy</option>
                <option value={2}>⭐⭐ Medium</option>
                <option value={3}>⭐⭐⭐ Hard</option>
                <option value={4}>⭐⭐⭐⭐ Expert</option>
                <option value={5}>⭐⭐⭐⭐⭐ Master Chef</option>
              </select>
            </div>
          </div>

          {/* Video Info */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Video Duration (seconds)</label>
            <input
              type="number"
              name="video_duration"
              value={formData.video_duration}
              onChange={handleInputChange}
              max="60"
              placeholder="Max 60 seconds for snippet videos"
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 transition-all"
            />
            <p className="text-sm text-gray-500 mt-1">Leave empty if no video. Max 60 seconds for snippets.</p>
          </div>

          {/* Ingredients */}
          <div>
            <div className="flex items-center justify-between mb-3">
              <label className="block text-sm font-medium text-gray-700">Ingredients *</label>
              <button
                type="button"
                onClick={addIngredient}
                className="btn-primary text-sm px-4 py-2 rounded-lg"
              >
                + Add Ingredient
              </button>
            </div>
            <div className="space-y-2">
              {formData.ingredients.map((ingredient, index) => (
                <div key={index} className="flex gap-2 items-center">
                  <input
                    type="text"
                    placeholder="Ingredient name"
                    value={ingredient.name}
                    onChange={(e) => updateIngredient(index, 'name', e.target.value)}
                    className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 transition-all"
                  />
                  <input
                    type="text"
                    placeholder="Amount"
                    value={ingredient.amount}
                    onChange={(e) => updateIngredient(index, 'amount', e.target.value)}
                    className="w-24 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 transition-all"
                  />
                  <input
                    type="text"
                    placeholder="Unit"
                    value={ingredient.unit}
                    onChange={(e) => updateIngredient(index, 'unit', e.target.value)}
                    className="w-24 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 transition-all"
                  />
                  <button
                    type="button"
                    onClick={() => removeIngredient(index)}
                    className="text-red-500 hover:text-red-700 p-3 rounded-lg hover:bg-red-50"
                  >
                    ✕
                  </button>
                </div>
              ))}
            </div>
          </div>

          {/* Preparation Steps */}
          <div>
            <div className="flex items-center justify-between mb-3">
              <label className="block text-sm font-medium text-gray-700">Preparation Steps *</label>
              <button
                type="button"
                onClick={addStep}
                className="btn-primary text-sm px-4 py-2 rounded-lg"
              >
                + Add Step
              </button>
            </div>
            <div className="space-y-3">
              {formData.preparation_steps.map((step, index) => (
                <div key={index} className="flex gap-3 items-start">
                  <span className="bg-green-500 text-white w-10 h-10 rounded-full flex items-center justify-center text-sm font-medium mt-1">
                    {step.step_number}
                  </span>
                  <textarea
                    value={step.description}
                    onChange={(e) => updateStep(index, e.target.value)}
                    placeholder="Describe this preparation step..."
                    rows="2"
                    className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 transition-all"
                  />
                  <button
                    type="button"
                    onClick={() => removeStep(index)}
                    className="text-red-500 hover:text-red-700 p-3 rounded-lg hover:bg-red-50 mt-1"
                  >
                    ✕
                  </button>
                </div>
              ))}
            </div>
          </div>

          {/* Submit */}
          <div className="flex justify-end pt-6">
            <button
              type="submit"
              disabled={submitting}
              className="btn-primary font-medium py-3 px-8 rounded-lg text-lg disabled:opacity-50"
            >
              {submitting ? 'Creating Snippet... ⏳' : 'Create Snippet ✨'}
            </button>
          </div>
        </form>
      </div>

      {/* Ad Placement */}
      <AdComponent placement="create-snippet" />
    </div>
  );
};

// Enhanced Grocery Page with Monetization
const GroceryPage = () => {
  const [ingredients, setIngredients] = useState(['']);
  const [postalCode, setPostalCode] = useState('');
  const [searchResults, setSearchResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const { user } = useAuth();

  useEffect(() => {
    if (user?.postal_code) {
      setPostalCode(user.postal_code);
    }
  }, [user]);

  const addIngredient = () => {
    setIngredients([...ingredients, '']);
  };

  const updateIngredient = (index, value) => {
    const newIngredients = [...ingredients];
    newIngredients[index] = value;
    setIngredients(newIngredients);
  };

  const removeIngredient = (index) => {
    setIngredients(ingredients.filter((_, i) => i !== index));
  };

  const searchGroceryStores = async () => {
    if (!postalCode.trim()) {
      alert('Please enter your postal code');
      return;
    }

    const validIngredients = ingredients.filter(ing => ing.trim());
    if (validIngredients.length === 0) {
      alert('Please add at least one ingredient');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post(`${API}/grocery/search`, {
        ingredients: validIngredients,
        user_postal_code: postalCode,
        max_distance_km: 15,
        budget_preference: "medium",
        delivery_preference: "either"
      });
      setSearchResults(response.data);
    } catch (error) {
      console.error('Failed to search grocery stores:', error);
      alert('Failed to search grocery stores. Please try again.');
    }
    setLoading(false);
  };

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h2 className="text-3xl font-bold heading-gradient mb-4">Find Local Ingredients</h2>
        <p className="text-gray-600">Search for ingredients at nearby grocery stores and get pricing information</p>
      </div>

      <div className="glass p-8 mb-8">
        <h3 className="text-xl font-semibold text-gray-800 mb-4">Search Ingredients</h3>
        
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">Your Postal Code</label>
          <input
            type="text"
            value={postalCode}
            onChange={(e) => setPostalCode(e.target.value)}
            placeholder="Enter your postal code"
            className="w-full md:w-64 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 transition-all"
          />
        </div>

        <div className="mb-6">
          <div className="flex items-center justify-between mb-3">
            <label className="block text-sm font-medium text-gray-700">Ingredients</label>
            <button
              type="button"
              onClick={addIngredient}
              className="btn-primary text-sm px-4 py-2 rounded-lg"
            >
              + Add Ingredient
            </button>
          </div>
          <div className="space-y-2">
            {ingredients.map((ingredient, index) => (
              <div key={index} className="flex gap-2 items-center">
                <input
                  type="text"
                  value={ingredient}
                  onChange={(e) => updateIngredient(index, e.target.value)}
                  placeholder="Enter ingredient name"
                  className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 transition-all"
                />
                {ingredients.length > 1 && (
                  <button
                    type="button"
                    onClick={() => removeIngredient(index)}
                    className="text-red-500 hover:text-red-700 p-3 rounded-lg hover:bg-red-50"
                  >
                    ✕
                  </button>
                )}
              </div>
            ))}
          </div>
        </div>

        <button
          onClick={searchGroceryStores}
          disabled={loading}
          className="btn-primary font-medium py-3 px-6 rounded-lg disabled:opacity-50"
        >
          {loading ? 'Searching... 🔍' : 'Find Stores & Prices 🛒'}
        </button>
      </div>

      {/* Ad Placement */}
      <AdComponent placement="grocery-search" />

      {searchResults && (
        <div className="space-y-6">
          <div className="glass p-8">
            <h3 className="text-xl font-semibold text-gray-800 mb-4">Nearby Grocery Stores</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {searchResults.stores.map((store, index) => (
                <div key={index} className={`grocery-store ${store.id === searchResults.recommended_store_id ? 'border-green-500 bg-green-50' : 'border-gray-200'}`}>
                  {store.id === searchResults.recommended_store_id && (
                    <span className="bg-green-500 text-white text-xs px-2 py-1 rounded-full mb-2 inline-block">
                      💰 Best Value
                    </span>
                  )}
                  <div className="flex justify-between items-start mb-2">
                    <div>
                      <h4 className="store-logo">{store.name}</h4>
                      <p className="text-sm text-gray-600">{store.chain}</p>
                      <p className="store-distance">{store.address}</p>
                      <p className="store-distance">{store.distance_km} km away</p>
                    </div>
                    <div className="text-right">
                      <p className="store-price text-xl">${store.estimated_total}</p>
                      <p className="text-xs text-gray-500">Est. total</p>
                    </div>
                  </div>
                  
                  <div className="flex justify-between items-center mt-3">
                    {store.supports_delivery && (
                      <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">
                        🚚 Delivery
                      </span>
                    )}
                    <button className="btn-primary text-xs px-3 py-1 rounded">
                      💰 Order & Earn
                    </button>
                  </div>
                  
                  <div className="mt-2 text-xs text-green-600">
                    <p>Platform earns {(store.commission_rate * 100).toFixed(0)}% commission</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="glass p-8">
            <h3 className="text-xl font-semibold text-gray-800 mb-4">Ingredient Availability & Pricing</h3>
            <div className="space-y-4">
              {Object.entries(searchResults.ingredient_availability).map(([ingredient, stores]) => (
                <div key={ingredient} className="border-b border-gray-200 pb-4">
                  <h4 className="font-medium text-gray-800 mb-2 capitalize">{ingredient}</h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-2">
                    {stores.map((item, index) => (
                      <div key={index} className="bg-gray-50 rounded-lg p-3 hover:bg-gray-100 transition-colors">
                        <div className="flex justify-between items-center">
                          <span className="text-sm font-medium">{item.brand}</span>
                          <span className="font-semibold text-green-600">${item.price}</span>
                        </div>
                        <div className="text-xs text-gray-500 mt-1">
                          {item.package_size} • {item.in_stock ? '✅ In Stock' : '❌ Out of Stock'}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="glass p-8">
            <h3 className="text-xl font-semibold text-gray-800 mb-4">Order Options</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
              {searchResults.delivery_options.map((option, index) => (
                <div key={index} className="border border-gray-200 rounded-lg p-4 hover:border-green-500 transition-colors cursor-pointer">
                  <h4 className="font-semibold text-gray-800 capitalize flex items-center">
                    {option.type === 'pickup' ? '🏪' : option.type === 'delivery' ? '🚚' : '⚡'} {option.type}
                  </h4>
                  <p className="text-gray-600 text-sm mt-1">{option.time_estimate}</p>
                  <p className="font-semibold text-green-600 mt-2">
                    {option.fee === 0 ? 'Free' : `$${option.fee} fee`}
                  </p>
                  <button className="w-full btn-primary mt-3 py-2 text-sm rounded-lg">
                    Select {option.type}
                  </button>
                </div>
              ))}
            </div>
            
            {/* Monetization Explanation */}
            <div className="grocery-integration">
              <h4 className="text-lg font-semibold mb-3">💰 How Lambalia Monetizes Grocery Integration</h4>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                <div className="bg-white bg-opacity-20 p-3 rounded">
                  <strong>Store Partnerships:</strong> We earn 5-8% commission from partner stores when you shop through Lambalia
                </div>
                <div className="bg-white bg-opacity-20 p-3 rounded">
                  <strong>Delivery Fees:</strong> Small service fee added to delivery orders for platform maintenance
                </div>
                <div className="bg-white bg-opacity-20 p-3 rounded">
                  <strong>Premium Features:</strong> Advanced meal planning and bulk ordering for subscribers
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

// Protected Route Component
const ProtectedRoute = ({ children }) => {
  const { user, loading } = useAuth();
  
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center landing-page">
        <div className="loading text-8xl">👩‍🍳</div>
      </div>
    );
  }
  
  return user ? children : <Navigate to="/login" />;
};

// Main App Component
function App() {
  return (
    <div className="App min-h-screen bg-gray-50">
      <AuthProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route 
              path="/" 
              element={
                <ProtectedRoute>
                  <>
                    <Header />
                    <HomePage />
                  </>
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/templates" 
              element={
                <ProtectedRoute>
                  <>
                    <Header />
                    <RecipeTemplatesPage />
                  </>
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/create-snippet" 
              element={
                <ProtectedRoute>
                  <>
                    <Header />
                    <CreateSnippetPage />
                  </>
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/grocery" 
              element={
                <ProtectedRoute>
                  <>
                    <Header />
                    <GroceryPage />
                  </>
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/home-restaurant" 
              element={
                <ProtectedRoute>
                  <>
                    <Header />
                    <HomeRestaurantPage />
                  </>
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/local-marketplace" 
              element={
                <ProtectedRoute>
                  <>
                    <Header />
                    <LocalMarketplacePage />
                  </>
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/charity-program" 
              element={
                <ProtectedRoute>
                  <>
                    <Header />
                    <CharityProgramPage />
                  </>
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/lambalia-eats" 
              element={
                <>
                  <LambaliaEatsApp />
                </>
              } 
            />
            <Route 
              path="/profile" 
              element={
                <ProtectedRoute>
                  <>
                    <Header />
                    <ProfilePage />
                  </>
                </ProtectedRoute>
              } 
            />
          </Routes>
        </BrowserRouter>
      </AuthProvider>
    </div>
  );
}

export default App;