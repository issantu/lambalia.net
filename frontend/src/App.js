import React, { useState, useEffect, createContext, useContext } from 'react';
import { BrowserRouter, Routes, Route, Navigate, Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useTranslation } from 'react-i18next';
import './i18n'; // Initialize i18n
import LanguageSwitcher from './LanguageSwitcher';
import './App.css';
import LocalMarketplacePage from './LocalMarketplace';
import LocalOffersAndDemands from './components/LocalOffersAndDemands';
import CharityProgramPage from './CharityProgram';
import LambaliaEatsApp from './LambaliaEats';
import { Icon, AnimatedIcon } from './components/ProfessionalIcons';
import SmartCookingTool from './components/SmartCookingTool';
import HomeRestaurantTraining from './components/HomeRestaurantTraining';
import ChefMarket from './ChefMarket';
import QuickEatsTraining from './components/QuickEatsTraining';

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
    phone_number: '', 
    postal_code: '',
    preferred_language: 'en',
    native_dishes: '',
    consultation_specialties: '',
    cultural_background: ''
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
      {/* Language Switcher for Login Page */}
      <div className="absolute top-4 right-4 z-50">
        <LanguageSwitcher />
      </div>
      
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
          <p className="text-gray-600 mt-2 font-medium">Taste the World's Heritage</p>
          <div className="mt-4 text-sm text-gray-500">
            <p>🌍 80+ Cultural Communities • 🥄 Heritage Recipes • 🛒 Specialty Ingredients</p>
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
               <label className="block text-xs font-medium text-gray-700 mb-1">
               Phone Number
               </label>
               <input
               type="tel"
               name="phone_number"
               value={formData.phone_number || ''}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500"
              placeholder="Enter your phone number"
              required
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
            
            {/* NEW: Native Dishes Question */}
            <div className="bg-gradient-to-r from-orange-50 to-yellow-50 p-4 rounded-lg border border-orange-200">
              <label className="block text-sm font-medium text-orange-800 mb-2">
                💰 Your Cultural Heritage & Earning Potential
              </label>
              <div className="space-y-3">
                <div>
                  <label className="block text-xs font-medium text-gray-700 mb-1">
                    What native dishes from your culture can you cook? (This helps users find and pay you for authentic recipes)
                  </label>
                  <textarea
                    name="native_dishes"
                    value={formData.native_dishes || ''}
                    onChange={handleInputChange}
                    placeholder="e.g., Jollof Rice, Plantain Fufu, Suya, Pounded Yam... (Nigerian) or Pad Thai, Tom Yum, Green Curry... (Thai)"
                    rows="2"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-400 text-sm"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-gray-700 mb-1">
                    What would you like other users to contact you for? (Paid consultations - you set your rates!)
                  </label>
                  <textarea
                    name="consultation_specialties"
                    value={formData.consultation_specialties || ''}
                    onChange={handleInputChange}
                    placeholder="e.g., Traditional spice blending, Authentic fermentation techniques, Holiday cooking traditions, Secret family recipes..."
                    rows="2"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-400 text-sm"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-gray-700 mb-1">
                    Your Cultural Background (helps us connect you with the right community)
                  </label>
                  <input
                    type="text"
                    name="cultural_background"
                    value={formData.cultural_background || ''}
                    onChange={handleInputChange}
                    placeholder="e.g., Nigerian (Yoruba), Mexican (Oaxacan), Korean, Vietnamese, etc."
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-400 text-sm"
                  />
                </div>
              </div>
              <p className="text-xs text-orange-700 mt-2">
                💡 Users pay $2.99-$12.99 for recipe consultations. The more specific your expertise, the more you can earn!
              </p>
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

// Enhanced Navigation Header with Professional Icons and Smart Cooking Tool
const Header = () => {
  const { user, logout } = useAuth();
  const { t } = useTranslation();
  const [showSmartCooking, setShowSmartCooking] = useState(false);

  return (
    <>
      <header className="nav-header shadow-lg border-b bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo Section */}
            <div className="flex items-center space-x-4">
              <Link to="/" className="flex items-center space-x-3 group">
                <img 
                  src="https://customer-assets.emergentagent.com/job_lambalia-recipes/artifacts/qzs71f09_2.png" 
                  alt="Lambalia - Global Heritage Recipes" 
                  className="w-10 h-10 transition-transform group-hover:scale-110 drop-shadow-md"
                />
                <h1 className="text-xl font-bold heading-gradient">Lambalia</h1>
              </Link>
            </div>
            
            {/* Main Navigation */}
            <nav className="hidden lg:flex items-center space-x-1">
              <Link to="/templates" className="nav-link text-gray-700 hover:text-green-600 px-2 py-1.5 rounded-md text-sm font-medium flex items-center space-x-1.5">
                <Icon name="Browse" size={14} className="text-gray-600" />
                <span>{t('nav.browse')}</span>
              </Link>
              
              <Link to="/create-snippet" className="nav-link text-gray-700 hover:text-green-600 px-2 py-1.5 rounded-md text-sm font-medium flex items-center space-x-1.5">
                <Icon name="Create" size={14} className="text-gray-600" />
                <span>{t('nav.create')}</span>
              </Link>
              
              <Link to="/grocery" className="nav-link text-gray-700 hover:text-green-600 px-2 py-1.5 rounded-md text-sm font-medium flex items-center space-x-1.5">
                <Icon name="Store" size={14} className="text-gray-600" />
                <span className="hidden xl:inline">{t('nav.ingredients')}</span>
                <span className="xl:hidden">Store</span>
              </Link>
              
              <Link to="/home-restaurant" className="nav-link text-gray-700 hover:text-green-600 px-2 py-1.5 rounded-md text-sm font-medium flex items-center space-x-1.5">
                <Icon name="Restaurant" size={14} className="text-gray-600" />
                <span className="hidden xl:inline">{t('nav.restaurant')}</span>
                <span className="xl:hidden">Restaurant</span>
              </Link>
              
              <Link to="/local-marketplace" className="nav-link text-gray-700 hover:text-green-600 px-2 py-1.5 rounded-md text-sm font-medium flex items-center space-x-1.5">
                <Icon name="Marketplace" size={14} className="text-gray-600" />
                <span className="hidden xl:inline">{t('nav.marketplace')}</span>
                <span className="xl:hidden">Market</span>
              </Link>
              
              <Link to="/charity-program" className="nav-link text-gray-700 hover:text-green-600 px-2 py-1.5 rounded-md text-sm font-medium flex items-center space-x-1.5">
                <Icon name="Heart" size={14} className="text-gray-600" />
                <span className="hidden xl:inline">{t('nav.charity')}</span>
                <span className="xl:hidden">Charity</span>
              </Link>
              
              <Link to="/lambalia-eats" className="nav-link text-gray-700 hover:text-orange-600 px-2 py-1.5 rounded-md text-sm font-medium flex items-center space-x-1.5">
                <Icon name="Utensils" size={14} className="text-gray-600" />
                <span className="hidden xl:inline">{t('nav.eats')}</span>
                <span className="xl:hidden">Eats</span>
              </Link>
            </nav>

            {/* User Actions */}
            <div className="flex items-center space-x-3">
              {/* Smart Cooking Tool - Small and unobtrusive */}
              <button
                onClick={() => setShowSmartCooking(true)}
                className="bg-orange-500 hover:bg-orange-600 text-white px-2 py-1 rounded text-xs font-medium transition-colors flex items-center space-x-1"
              >
                <AnimatedIcon name="SmartCooking" size={12} className="text-white" />
                <span className="hidden md:inline">AI Cook</span>
                <span className="bg-white bg-opacity-20 px-1 py-0.5 rounded text-xs">$3</span>
              </button>
              
              <LanguageSwitcher />
              
              {user ? (
                <div className="flex items-center space-x-3">
                  <span className="text-sm text-gray-700 flex items-center space-x-1.5">
                    <Icon name="Profile" size={14} className="text-green-600" />
                    <span className="hidden md:inline">{t('common.welcome', { name: user.username || user.full_name })}</span>
                  </span>
                  <button 
                    onClick={logout}
                    className="text-sm text-gray-500 hover:text-gray-700 flex items-center space-x-1"
                  >
                    <Icon name="Settings" size={12} />
                    <span className="hidden md:inline">{t('auth.logout')}</span>
                  </button>
                </div>
              ) : (
                <div className="flex items-center space-x-2">
                  <Link to="/login" className="text-sm text-gray-700 hover:text-green-600 flex items-center space-x-1">
                    <Icon name="Lock" size={12} />
                    <span>{t('auth.login')}</span>
                  </Link>
                  <Link to="/register" className="btn-primary px-3 py-1.5 rounded-md text-sm flex items-center space-x-1.5">
                    <Icon name="Profile" size={12} className="text-white" />
                    <span>{t('auth.joinLambalia')}</span>
                  </Link>
                </div>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Smart Cooking Tool Modal */}
      {showSmartCooking && (
        <SmartCookingTool 
          user={user} 
          onClose={() => setShowSmartCooking(false)}
        />
      )}
    </>
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

// Ad Component - External Revenue Generation
const ExternalAdBanner = ({ placement = "header", size = "728x90" }) => {
  const [adContent, setAdContent] = useState(null);
  
  useEffect(() => {
    // Simulate ad loading - in production would integrate with Google AdSense, Facebook Audience Network
    const loadAd = async () => {
      try {
        // This would be actual ad network integration
        const adResponse = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/ads/external-placements`);
        const adData = await adResponse.json();
        
        // Select appropriate ad based on placement
        const placementAd = adData.ad_placements?.google_adsense?.ad_units?.find(
          unit => unit.placement === placement
        ) || {
          placement: placement,
          size: size,
          category: "cultural_food",
          estimated_cpm: "$2.00"
        };
        
        setAdContent(placementAd);
      } catch (error) {
        console.log('Ad loading error:', error);
      }
    };
    
    loadAd();
  }, [placement, size]);

  if (!adContent) return null;

  return (
    <div className={`external-ad-container bg-gray-50 border border-gray-200 rounded-lg p-4 text-center ${
      size === '728x90' ? 'h-24' : size === '300x250' ? 'h-64 w-80' : 'h-16'
    } mx-auto mb-4`}>
      <div className="flex flex-col items-center justify-center h-full">
        <div className="text-xs text-gray-500 mb-1">Advertisement</div>
        <div className="text-sm text-gray-600">
          🍴 Authentic Cultural Ingredients & Cookware
        </div>
        <div className="text-xs text-gray-400 mt-1">
          Revenue: ~{adContent.estimated_cpm} CPM | {adContent.category}
        </div>
      </div>
    </div>
  );
};

// User Earnings Dashboard Component
const UserEarningsDashboard = () => {
  const [earnings, setEarnings] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showPayoutSetup, setShowPayoutSetup] = useState(false);
  const [payoutData, setPayoutData] = useState({
    payout_method: 'stripe',
    minimum_payout_amount: 25.00,
    stripe_account_id: '',
    paypal_email: '',
    account_number: '',
    routing_number: '',
    bank_name: ''
  });

  useEffect(() => {
    fetchEarnings();
  }, []);

  const fetchEarnings = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/payments/my-earnings`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      const data = await response.json();
      setEarnings(data);
    } catch (error) {
      console.error('Failed to fetch earnings:', error);
    } finally {
      setLoading(false);
    }
  };

  const handlePayoutSetup = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/payments/setup-payout-profile`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify(payoutData)
      });
      
      if (response.ok) {
        alert('Payout profile updated successfully!');
        setShowPayoutSetup(false);
        fetchEarnings();
      } else {
        alert('Failed to update payout profile');
      }
    } catch (error) {
      console.error('Payout setup error:', error);
    }
  };

  if (loading) return <div className="text-center p-8">Loading earnings...</div>;

  if (!earnings) return <div className="text-center p-8">Unable to load earnings data</div>;

  const { earnings_summary, earnings_breakdown, payout_info, recent_transactions } = earnings;

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold heading-gradient mb-2">💰 My Earnings Dashboard</h1>
        <p className="text-gray-600">Track your Lambalia earnings and manage payouts</p>
      </div>

      {/* Earnings Summary Cards */}
      <div className="grid md:grid-cols-4 gap-6 mb-8">
        <div className="bg-gradient-to-r from-green-50 to-emerald-50 p-6 rounded-xl text-center">
          <div className="text-2xl font-bold text-green-600">
            ${earnings_summary.current_week_earnings.toFixed(2)}
          </div>
          <div className="text-sm text-gray-600">This Week</div>
        </div>
        
        <div className="bg-gradient-to-r from-blue-50 to-cyan-50 p-6 rounded-xl text-center">
          <div className="text-2xl font-bold text-blue-600">
            ${earnings_summary.total_lifetime_earnings.toFixed(2)}
          </div>
          <div className="text-sm text-gray-600">Total Earned</div>
        </div>
        
        <div className="bg-gradient-to-r from-purple-50 to-pink-50 p-6 rounded-xl text-center">
          <div className="text-2xl font-bold text-purple-600">
            ${earnings_summary.pending_payout_amount.toFixed(2)}
          </div>
          <div className="text-sm text-gray-600">Pending Payout</div>
        </div>
        
        <div className="bg-gradient-to-r from-orange-50 to-yellow-50 p-6 rounded-xl text-center">
          <div className="text-2xl font-bold text-orange-600">
            ${earnings_summary.total_platform_commission.toFixed(2)}
          </div>
          <div className="text-sm text-gray-600">Platform Commission (15%)</div>
        </div>
      </div>

      {/* Earnings Breakdown */}
      <div className="grid md:grid-cols-2 gap-8 mb-8">
        <div className="bg-white p-6 rounded-xl shadow-lg">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">💼 Earnings by Service</h3>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-gray-600">Consultations</span>
              <span className="font-semibold text-green-600">${earnings_breakdown.consultation_earnings.toFixed(2)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Lambalia Eats</span>
              <span className="font-semibold text-orange-600">${earnings_breakdown.lambalia_eats_earnings.toFixed(2)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Home Restaurants</span>
              <span className="font-semibold text-purple-600">${earnings_breakdown.home_restaurant_earnings.toFixed(2)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Other Services</span>
              <span className="font-semibold text-blue-600">${earnings_breakdown.other_earnings.toFixed(2)}</span>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-xl shadow-lg">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">🏦 Payout Information</h3>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-gray-600">Payout Method</span>
              <span className="font-semibold capitalize">{payout_info.payout_method}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Minimum Payout</span>
              <span className="font-semibold">${payout_info.minimum_payout.toFixed(2)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Next Payout</span>
              <span className="font-semibold text-blue-600">{payout_info.next_payout_date}</span>
            </div>
            <button 
              onClick={() => setShowPayoutSetup(true)}
              className="w-full btn-primary mt-4 py-2 rounded-lg"
            >
              {payout_info.payout_profile_setup ? 'Update Payout Settings' : 'Setup Payout Method'}
            </button>
          </div>
        </div>
      </div>

      {/* Recent Transactions */}
      <div className="bg-white p-6 rounded-xl shadow-lg mb-8">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">📊 Recent Transactions</h3>
        <div className="space-y-3">
          {recent_transactions && recent_transactions.length > 0 ? (
            recent_transactions.map((transaction, index) => (
              <div key={index} className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                <div>
                  <div className="font-medium text-gray-800">
                    {transaction.service_description}
                  </div>
                  <div className="text-sm text-gray-500">
                    {new Date(transaction.created_at).toLocaleDateString()}
                  </div>
                </div>
                <div className="text-right">
                  <div className="font-semibold text-green-600">
                    +${transaction.user_earnings.toFixed(2)}
                  </div>
                  <div className="text-xs text-gray-500">
                    (${transaction.platform_commission.toFixed(2)} commission)
                  </div>
                </div>
              </div>
            ))
          ) : (
            <p className="text-gray-500 text-center py-4">No transactions yet</p>
          )}
        </div>
      </div>

      {/* Payout Setup Modal */}
      {showPayoutSetup && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white p-8 rounded-xl max-w-md w-full mx-4">
            <h3 className="text-xl font-semibold mb-4">Setup Payout Method</h3>
            
            <form onSubmit={handlePayoutSetup}>
              <div className="mb-4">
                <label className="block text-sm font-medium mb-2">Payout Method</label>
                <select 
                  value={payoutData.payout_method}
                  onChange={(e) => setPayoutData({...payoutData, payout_method: e.target.value})}
                  className="w-full px-3 py-2 border rounded-lg"
                >
                  <option value="stripe">Stripe</option>
                  <option value="paypal">PayPal</option>
                  <option value="bank_transfer">Bank Transfer</option>
                </select>
              </div>

              <div className="mb-4">
                <label className="block text-sm font-medium mb-2">Minimum Payout Amount</label>
                <input 
                  type="number"
                  min="10"
                  step="0.01"
                  value={payoutData.minimum_payout_amount}
                  onChange={(e) => setPayoutData({...payoutData, minimum_payout_amount: parseFloat(e.target.value)})}
                  className="w-full px-3 py-2 border rounded-lg"
                />
              </div>

              {payoutData.payout_method === 'paypal' && (
                <div className="mb-4">
                  <label className="block text-sm font-medium mb-2">PayPal Email</label>
                  <input 
                    type="email"
                    value={payoutData.paypal_email}
                    onChange={(e) => setPayoutData({...payoutData, paypal_email: e.target.value})}
                    className="w-full px-3 py-2 border rounded-lg"
                  />
                </div>
              )}

              {payoutData.payout_method === 'bank_transfer' && (
                <>
                  <div className="mb-4">
                    <label className="block text-sm font-medium mb-2">Bank Name</label>
                    <input 
                      type="text"
                      value={payoutData.bank_name}
                      onChange={(e) => setPayoutData({...payoutData, bank_name: e.target.value})}
                      className="w-full px-3 py-2 border rounded-lg"
                    />
                  </div>
                  <div className="mb-4">
                    <label className="block text-sm font-medium mb-2">Account Number</label>
                    <input 
                      type="text"
                      value={payoutData.account_number}
                      onChange={(e) => setPayoutData({...payoutData, account_number: e.target.value})}
                      className="w-full px-3 py-2 border rounded-lg"
                    />
                  </div>
                  <div className="mb-4">
                    <label className="block text-sm font-medium mb-2">Routing Number</label>
                    <input 
                      type="text"
                      value={payoutData.routing_number}
                      onChange={(e) => setPayoutData({...payoutData, routing_number: e.target.value})}
                      className="w-full px-3 py-2 border rounded-lg"
                    />
                  </div>
                </>
              )}

              <div className="flex space-x-4">
                <button type="submit" className="flex-1 btn-primary py-2 rounded-lg">
                  Save Settings
                </button>
                <button 
                  type="button"
                  onClick={() => setShowPayoutSetup(false)}
                  className="flex-1 bg-gray-300 text-gray-700 py-2 rounded-lg"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Pricing Structure Info */}
      <div className="bg-gradient-to-r from-blue-50 to-purple-50 p-6 rounded-xl">
        <h3 className="text-lg font-semibold text-blue-800 mb-4">💵 Service Pricing Structure</h3>
        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <h4 className="font-medium text-gray-800 mb-2">Consultation Services</h4>
            <div className="space-y-1 text-sm">
              <div>💬 Message Consultation: $2.50 (you earn $2.13)</div>
              <div>🎵 Audio Consultation: $3.50 (you earn $2.98)</div>
              <div>🎥 Video Consultation: $4.50 (you earn $3.83)</div>
            </div>
          </div>
          <div>
            <h4 className="font-medium text-gray-800 mb-2">Lambalia Eats</h4>
            <div className="space-y-1 text-sm">
              <div>🍽️ Base Meal Price: $10.00 (you earn $8.50)</div>
              <div>🚚 Delivery Fee: $2.00 + $0.75/km</div>
              <div>📊 Platform Commission: 15% on all transactions</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
const RevenueDashboard = () => {
  const [revenueData, setRevenueData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchRevenueData = async () => {
      try {
        const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/revenue/comprehensive-dashboard`);
        const data = await response.json();
        setRevenueData(data);
      } catch (error) {
        console.error('Revenue data fetch error:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchRevenueData();
  }, []);

  if (loading) return <div className="text-center p-8">Loading revenue analytics...</div>;

  if (!revenueData) return <div className="text-center p-8">Revenue data unavailable</div>;

  const { summary, revenue_streams, recommendations, immediate_implementations } = revenueData;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold heading-gradient mb-4">💰 Revenue Analytics Dashboard</h1>
        <p className="text-xl text-gray-600">Comprehensive monetization overview for Lambalia platform</p>
      </div>

      {/* Revenue Summary Cards */}
      <div className="grid md:grid-cols-4 gap-6 mb-12">
        <div className="bg-gradient-to-r from-green-50 to-emerald-50 p-6 rounded-xl text-center">
          <div className="text-3xl font-bold text-green-600">
            ${summary.current_monthly_revenue.toLocaleString()}
          </div>
          <div className="text-sm text-gray-600">Current Monthly Revenue</div>
        </div>
        
        <div className="bg-gradient-to-r from-blue-50 to-cyan-50 p-6 rounded-xl text-center">
          <div className="text-3xl font-bold text-blue-600">
            ${summary.projected_monthly_revenue.toLocaleString()}
          </div>
          <div className="text-sm text-gray-600">Projected Monthly Revenue</div>
        </div>
        
        <div className="bg-gradient-to-r from-purple-50 to-pink-50 p-6 rounded-xl text-center">
          <div className="text-3xl font-bold text-purple-600">
            ${(summary.annual_projection / 1000000).toFixed(1)}M
          </div>
          <div className="text-sm text-gray-600">Annual Projection</div>
        </div>
        
        <div className="bg-gradient-to-r from-orange-50 to-yellow-50 p-6 rounded-xl text-center">
          <div className="text-3xl font-bold text-orange-600">
            {summary.growth_potential}
          </div>
          <div className="text-sm text-gray-600">Growth Potential</div>
        </div>
      </div>

      {/* Revenue Streams Breakdown */}
      <section className="mb-12">
        <h2 className="text-2xl font-bold text-gray-800 mb-6">💼 Revenue Stream Analysis</h2>
        <div className="grid md:grid-cols-2 gap-6">
          {Object.entries(revenue_streams).map(([streamName, streamData]) => (
            <div key={streamName} className="bg-white p-6 rounded-xl shadow-lg">
              <h3 className="text-lg font-semibold text-gray-800 mb-3 capitalize">
                {streamName.replace('_', ' ')}
              </h3>
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm text-gray-600">Current Monthly:</span>
                <span className="font-semibold text-green-600">
                  ${(streamData.total_monthly || streamData.current_monthly || 0).toLocaleString()}
                </span>
              </div>
              <div className="flex justify-between items-center mb-3">
                <span className="text-sm text-gray-600">Projected Monthly:</span>
                <span className="font-semibold text-blue-600">
                  ${streamData.projected_monthly?.toLocaleString() || '0'}
                </span>
              </div>
              {streamData.commission_rate && (
                <div className="text-xs text-gray-500">
                  Commission: {streamData.commission_rate}
                </div>
              )}
            </div>
          ))}
        </div>
      </section>

      {/* Recommendations */}
      <section className="grid md:grid-cols-2 gap-6">
        <div className="bg-gradient-to-r from-green-50 to-blue-50 p-6 rounded-xl">
          <h3 className="text-lg font-semibold text-green-800 mb-4">🚀 Top Recommendations</h3>
          <ul className="space-y-2">
            {recommendations.map((rec, idx) => (
              <li key={idx} className="text-sm text-gray-700 flex items-start">
                <span className="text-green-600 mr-2">•</span>
                {rec}
              </li>
            ))}
          </ul>
        </div>
        
        <div className="bg-gradient-to-r from-orange-50 to-yellow-50 p-6 rounded-xl">
          <h3 className="text-lg font-semibold text-orange-800 mb-4">⚡ Immediate Actions</h3>
          <ul className="space-y-2">
            {immediate_implementations.map((action, idx) => (
              <li key={idx} className="text-sm text-gray-700 flex items-start">
                <span className="text-orange-600 mr-2">•</span>
                {action}
              </li>
            ))}
          </ul>
        </div>
      </section>

      {/* External Ad Revenue Section */}
      <section className="mt-12 bg-gray-50 p-8 rounded-xl">
        <h3 className="text-xl font-semibold text-gray-800 mb-4">🎯 External Ad Revenue Generation</h3>
        <p className="text-gray-600 mb-6">
          Automatic ad placement generates revenue without disrupting user experience. 
          Projected $4,200/month from Google AdSense, Facebook Network, and affiliate marketing.
        </p>
        
        <div className="space-y-4">
          <div className="text-center">
            <div className="text-sm text-gray-600 mb-2">Sample Header Banner Ad (728x90)</div>
            <ExternalAdBanner placement="recipe_header" size="728x90" />
          </div>
          
          <div className="flex justify-center">
            <div className="text-center">
              <div className="text-sm text-gray-600 mb-2">Sample Sidebar Ad (300x250)</div>
              <ExternalAdBanner placement="sidebar_recipes" size="300x250" />
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};
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

// Vendor Conversion Hub Component
const VendorConversionHub = () => {
  const [activeVendorTab, setActiveVendorTab] = useState('overview');
  const [showApplicationForm, setShowApplicationForm] = useState(null);

  const vendorTabs = [
    { id: 'overview', title: 'Start Earning', icon: 'Dollar' },
    { id: 'home-restaurant', title: 'Home Restaurant Training', icon: 'Restaurant' },
    { id: 'quick-eats', title: 'Quick Eats Training', icon: 'Utensils' },
    { id: 'delivery', title: 'Delivery Partner', icon: 'Truck' },
    { id: 'applications', title: 'My Applications', icon: 'FileText' }
  ];

  const renderOverview = () => (
    <div className="space-y-8">
      {/* Hero Section */}
      <div className="bg-gradient-to-r from-green-500 to-blue-600 text-white p-8 rounded-xl">
        <div className="text-center">
          <h2 className="text-3xl font-bold mb-4">Transform Your Kitchen Into Income</h2>
          <p className="text-xl mb-6 text-green-100">
            Today you eat somewhere, tomorrow someone eats at your place. Turn your passion into profit!
          </p>
          <div className="grid md:grid-cols-3 gap-6 mt-8">
            <div className="bg-white bg-opacity-20 p-6 rounded-lg">
              <Icon name="Restaurant" size={32} className="text-white mx-auto mb-3" />
              <h3 className="font-bold text-lg mb-2">Home Restaurant</h3>
              <p className="text-sm text-green-100">Host intimate dining experiences</p>
              <p className="text-green-200 font-semibold mt-2">$50-200 per person</p>
            </div>
            <div className="bg-white bg-opacity-20 p-6 rounded-lg">
              <Icon name="Utensils" size={32} className="text-white mx-auto mb-3" />
              <h3 className="font-bold text-lg mb-2">Quick Eats</h3>
              <p className="text-sm text-green-100">Fast, authentic meals on-demand</p>
              <p className="text-green-200 font-semibold mt-2">$8-25 per order</p>
            </div>
            <div className="bg-white bg-opacity-20 p-6 rounded-lg">
              <Icon name="Truck" size={32} className="text-white mx-auto mb-3" />
              <h3 className="font-bold text-lg mb-2">Delivery Partner</h3>
              <p className="text-sm text-green-100">Deliver meals in your area</p>
              <p className="text-green-200 font-semibold mt-2">$15-30 per hour</p>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="grid md:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-lg border-l-4 border-green-500">
          <h3 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
            <Icon name="Restaurant" size={24} className="text-green-600 mr-3" />
            Home Restaurant Host
          </h3>
          <p className="text-gray-600 mb-4">
            Create authentic dining experiences in your home. Perfect for special occasions and cultural sharing.
          </p>
          <div className="space-y-2 mb-4">
            <div className="flex items-center text-sm text-gray-600">
              <Icon name="CheckCircle" size={16} className="text-green-500 mr-2" />
              <span>Earn $50-200 per person</span>
            </div>
            <div className="flex items-center text-sm text-gray-600">
              <Icon name="CheckCircle" size={16} className="text-green-500 mr-2" />
              <span>Flexible scheduling</span>
            </div>
            <div className="flex items-center text-sm text-gray-600">
              <Icon name="CheckCircle" size={16} className="text-green-500 mr-2" />
              <span>Cultural preservation</span>
            </div>
          </div>
          <div className="flex space-x-3">
            <button
              onClick={() => setActiveVendorTab('home-restaurant')}
              className="flex-1 bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg font-medium"
            >
              View Training
            </button>
            <button
              onClick={() => setShowApplicationForm('home-restaurant')}
              className="flex-1 bg-green-100 hover:bg-green-200 text-green-700 px-4 py-2 rounded-lg font-medium"
            >
              Apply Now
            </button>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-lg border-l-4 border-blue-500">
          <h3 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
            <Icon name="Utensils" size={24} className="text-blue-600 mr-3" />
            Quick Eats Provider
          </h3>
          <p className="text-gray-600 mb-4">
            Serve fast, authentic meals for busy people. The modern food truck without the truck!
          </p>
          <div className="space-y-2 mb-4">
            <div className="flex items-center text-sm text-gray-600">
              <Icon name="CheckCircle" size={16} className="text-blue-500 mr-2" />
              <span>Earn $8-25 per order</span>
            </div>
            <div className="flex items-center text-sm text-gray-600">
              <Icon name="CheckCircle" size={16} className="text-blue-500 mr-2" />
              <span>High volume potential</span>
            </div>
            <div className="flex items-center text-sm text-gray-600">
              <Icon name="CheckCircle" size={16} className="text-blue-500 mr-2" />
              <span>Daily earning opportunities</span>
            </div>
          </div>
          <div className="flex space-x-3">
            <button
              onClick={() => setActiveVendorTab('quick-eats')}
              className="flex-1 bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg font-medium"
            >
              View Training
            </button>
            <button
              onClick={() => setShowApplicationForm('quick-eats')}
              className="flex-1 bg-blue-100 hover:bg-blue-200 text-blue-700 px-4 py-2 rounded-lg font-medium"
            >
              Apply Now
            </button>
          </div>
        </div>
      </div>

      {/* Success Stories */}
      <div className="bg-gray-50 p-6 rounded-lg">
        <h3 className="text-xl font-semibold text-gray-800 mb-6 text-center">Success Stories</h3>
        <div className="grid md:grid-cols-3 gap-6">
          <div className="bg-white p-4 rounded-lg shadow-sm">
            <div className="text-center mb-3">
              <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-2">
                <span className="text-green-600 font-bold">M</span>
              </div>
              <h4 className="font-semibold">Maria</h4>
              <p className="text-sm text-gray-600">Mexican Home Restaurant</p>
            </div>
            <p className="text-sm text-gray-700">
              "Started hosting family dinners and now earn $3,200/month sharing our traditions!"
            </p>
          </div>
          <div className="bg-white p-4 rounded-lg shadow-sm">
            <div className="text-center mb-3">
              <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-2">
                <span className="text-blue-600 font-bold">A</span>
              </div>
              <h4 className="font-semibold">Ahmed</h4>
              <p className="text-sm text-gray-600">Middle Eastern Quick Eats</p>
            </div>
            <p className="text-sm text-gray-700">
              "Quick shawarma and falafel orders helped me earn $2,800 last month!"
            </p>
          </div>
          <div className="bg-white p-4 rounded-lg shadow-sm">
            <div className="text-center mb-3">
              <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-2">
                <span className="text-purple-600 font-bold">K</span>
              </div>
              <h4 className="font-semibold">Kenji</h4>
              <p className="text-sm text-gray-600">Japanese Delivery Partner</p>
            </div>
            <p className="text-sm text-gray-700">
              "Perfect part-time income! $1,800/month delivering authentic meals."
            </p>
          </div>
        </div>
      </div>

      {/* Getting Started Steps */}
      <div className="bg-white p-6 rounded-lg shadow-lg">
        <h3 className="text-xl font-semibold text-gray-800 mb-6 text-center">Getting Started is Easy</h3>
        <div className="grid md:grid-cols-4 gap-6">
          <div className="text-center">
            <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-3">
              <span className="text-green-600 font-bold">1</span>
            </div>
            <h4 className="font-medium mb-2">Choose Your Path</h4>
            <p className="text-sm text-gray-600">Select from Home Restaurant, Quick Eats, or Delivery Partner</p>
          </div>
          <div className="text-center">
            <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-3">
              <span className="text-blue-600 font-bold">2</span>
            </div>
            <h4 className="font-medium mb-2">Complete Training</h4>
            <p className="text-sm text-gray-600">Learn best practices, safety, and success strategies</p>
          </div>
          <div className="text-center">
            <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-3">
              <span className="text-purple-600 font-bold">3</span>
            </div>
            <h4 className="font-medium mb-2">Submit Application</h4>
            <p className="text-sm text-gray-600">Apply for certification with our guided process</p>
          </div>
          <div className="text-center">
            <div className="w-12 h-12 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-3">
              <span className="text-orange-600 font-bold">4</span>
            </div>
            <h4 className="font-medium mb-2">Start Earning</h4>
            <p className="text-sm text-gray-600">Get certified and begin your vendor journey</p>
          </div>
        </div>
      </div>
    </div>
  );

  const renderApplications = () => (
    <div className="space-y-6">
      <div className="text-center">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">My Vendor Applications</h2>
        <p className="text-gray-600">Track your certification progress and application status</p>
      </div>

      <div className="grid gap-6">
        <div className="bg-white p-6 rounded-lg shadow-lg border-l-4 border-yellow-500">
          <div className="flex justify-between items-start mb-4">
            <div>
              <h3 className="text-lg font-semibold text-gray-800">Home Restaurant Host</h3>
              <p className="text-sm text-gray-600">Application submitted 3 days ago</p>
            </div>
            <span className="bg-yellow-100 text-yellow-800 text-sm px-3 py-1 rounded-full">
              Under Review
            </span>
          </div>
          <div className="space-y-2">
            <div className="flex items-center text-sm">
              <Icon name="CheckCircle" size={16} className="text-green-500 mr-2" />
              <span>Training completed</span>
            </div>
            <div className="flex items-center text-sm">
              <Icon name="CheckCircle" size={16} className="text-green-500 mr-2" />
              <span>Application submitted</span>
            </div>
            <div className="flex items-center text-sm">
              <Icon name="Clock" size={16} className="text-yellow-500 mr-2" />
              <span>Background check in progress</span>
            </div>
            <div className="flex items-center text-sm">
              <Icon name="Clock" size={16} className="text-gray-400 mr-2" />
              <span>Final approval pending</span>
            </div>
          </div>
          <div className="mt-4 bg-gray-50 p-3 rounded-lg">
            <p className="text-sm text-gray-600">
              <strong>Next step:</strong> Our team will contact you within 2-3 business days for kitchen inspection.
            </p>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-lg border-l-4 border-gray-300">
          <div className="flex justify-between items-start mb-4">
            <div>
              <h3 className="text-lg font-semibold text-gray-800">Quick Eats Provider</h3>
              <p className="text-sm text-gray-600">Not started</p>
            </div>
            <span className="bg-gray-100 text-gray-600 text-sm px-3 py-1 rounded-full">
              Available
            </span>
          </div>
          <p className="text-gray-600 mb-4">Complete the Quick Eats training to unlock this opportunity.</p>
          <button
            onClick={() => setActiveVendorTab('quick-eats')}
            className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg"
          >
            Start Training
          </button>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-lg border-l-4 border-gray-300">
          <div className="flex justify-between items-start mb-4">
            <div>
              <h3 className="text-lg font-semibold text-gray-800">Delivery Partner</h3>
              <p className="text-sm text-gray-600">Not started</p>
            </div>
            <span className="bg-gray-100 text-gray-600 text-sm px-3 py-1 rounded-full">
              Available
            </span>
          </div>
          <p className="text-gray-600 mb-4">Join our delivery network and start earning immediately.</p>
          <button
            onClick={() => setShowApplicationForm('delivery')}
            className="bg-purple-500 hover:bg-purple-600 text-white px-4 py-2 rounded-lg"
          >
            Apply Now
          </button>
        </div>
      </div>

      <div className="bg-blue-50 p-6 rounded-lg border border-blue-200">
        <h3 className="text-lg font-semibold text-blue-800 mb-3">💡 Pro Tip</h3>
        <p className="text-blue-700 text-sm">
          You can apply for multiple vendor types! Many successful vendors combine Home Restaurant hosting 
          with Quick Eats to maximize their earning potential. Start with one, master it, then expand.
        </p>
      </div>
    </div>
  );

  return (
    <div className="space-y-6">
      {/* Vendor Hub Navigation */}
      <div className="bg-white rounded-lg shadow-lg">
        <div className="flex flex-wrap justify-center border-b">
          {vendorTabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveVendorTab(tab.id)}
              className={`flex items-center space-x-2 px-4 py-3 border-b-2 transition-colors ${
                activeVendorTab === tab.id
                  ? 'border-green-500 text-green-600 bg-green-50'
                  : 'border-transparent text-gray-600 hover:text-green-600 hover:bg-gray-50'
              }`}
            >
              <Icon name={tab.icon} size={16} />
              <span className="font-medium">{tab.title}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Tab Content */}
      {activeVendorTab === 'overview' && renderOverview()}
      {activeVendorTab === 'home-restaurant' && <HomeRestaurantTraining />}
      {activeVendorTab === 'quick-eats' && <QuickEatsTraining />}
      {activeVendorTab === 'delivery' && <DeliveryPartnerInfo />}
      {activeVendorTab === 'applications' && renderApplications()}

      {/* Application Forms Modal */}
      {showApplicationForm && (
        <VendorApplicationModal 
          type={showApplicationForm} 
          onClose={() => setShowApplicationForm(null)} 
        />
      )}
    </div>
  );
};

// Delivery Partner Info Component
const DeliveryPartnerInfo = () => (
  <div className="space-y-6">
    <div className="text-center mb-8">
      <Icon name="Truck" size={48} className="text-purple-600 mx-auto mb-4" />
      <h2 className="text-2xl font-bold text-gray-800">Delivery Partner Program</h2>
      <p className="text-gray-600">Earn money delivering authentic meals in your area</p>
    </div>

    <div className="bg-gradient-to-r from-purple-50 to-pink-50 p-8 rounded-xl">
      <h3 className="text-xl font-semibold text-purple-800 mb-6 text-center">Why Join Our Delivery Network?</h3>
      <div className="grid md:grid-cols-2 gap-6">
        <div className="space-y-4">
          <div className="flex items-start space-x-3">
            <Icon name="Dollar" size={20} className="text-green-600 mt-1" />
            <div>
              <h4 className="font-semibold text-gray-800">Competitive Pay</h4>
              <p className="text-sm text-gray-600">$15-30 per hour including tips and bonuses</p>
            </div>
          </div>
          <div className="flex items-start space-x-3">
            <Icon name="Clock" size={20} className="text-blue-600 mt-1" />
            <div>
              <h4 className="font-semibold text-gray-800">Flexible Schedule</h4>
              <p className="text-sm text-gray-600">Work when you want, as much as you want</p>
            </div>
          </div>
          <div className="flex items-start space-x-3">
            <Icon name="MapPin" size={20} className="text-red-600 mt-1" />
            <div>
              <h4 className="font-semibold text-gray-800">Local Focus</h4>
              <p className="text-sm text-gray-600">Short delivery distances, know your community</p>
            </div>
          </div>
        </div>
        <div className="space-y-4">
          <div className="flex items-start space-x-3">
            <Icon name="Community" size={20} className="text-purple-600 mt-1" />
            <div>
              <h4 className="font-semibold text-gray-800">Cultural Impact</h4>
              <p className="text-sm text-gray-600">Help preserve food traditions in your community</p>
            </div>
          </div>
          <div className="flex items-start space-x-3">
            <Icon name="Star" size={20} className="text-yellow-600 mt-1" />
            <div>
              <h4 className="font-semibold text-gray-800">Quality Products</h4>
              <p className="text-sm text-gray-600">Deliver authentic, homemade meals people love</p>
            </div>
          </div>
          <div className="flex items-start space-x-3">
            <Icon name="Shield" size={20} className="text-green-600 mt-1" />
            <div>
              <h4 className="font-semibold text-gray-800">Full Support</h4>
              <p className="text-sm text-gray-600">Insurance, equipment, and 24/7 support included</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div className="grid md:grid-cols-2 gap-8">
      <div className="bg-white p-6 rounded-lg shadow-lg">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">Requirements</h3>
        <div className="space-y-3">
          <div className="flex items-center text-sm">
            <Icon name="CheckCircle" size={16} className="text-green-500 mr-3" />
            <span>Valid driver's license</span>
          </div>
          <div className="flex items-center text-sm">
            <Icon name="CheckCircle" size={16} className="text-green-500 mr-3" />
            <span>Reliable vehicle (car, bike, or scooter)</span>
          </div>
          <div className="flex items-center text-sm">
            <Icon name="CheckCircle" size={16} className="text-green-500 mr-3" />
            <span>Smartphone with GPS</span>
          </div>
          <div className="flex items-center text-sm">
            <Icon name="CheckCircle" size={16} className="text-green-500 mr-3" />
            <span>Age 18+ with clean driving record</span>
          </div>
          <div className="flex items-center text-sm">
            <Icon name="CheckCircle" size={16} className="text-green-500 mr-3" />
            <span>Pass background check</span>
          </div>
        </div>
      </div>

      <div className="bg-white p-6 rounded-lg shadow-lg">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">What We Provide</h3>
        <div className="space-y-3">
          <div className="flex items-center text-sm">
            <Icon name="CheckCircle" size={16} className="text-blue-500 mr-3" />
            <span>Insulated delivery bags</span>
          </div>
          <div className="flex items-center text-sm">
            <Icon name="CheckCircle" size={16} className="text-blue-500 mr-3" />
            <span>Mobile app for easy order management</span>
          </div>
          <div className="flex items-center text-sm">
            <Icon name="CheckCircle" size={16} className="text-blue-500 mr-3" />
            <span>Liability insurance coverage</span>
          </div>
          <div className="flex items-center text-sm">
            <Icon name="CheckCircle" size={16} className="text-blue-500 mr-3" />
            <span>24/7 driver support hotline</span>
          </div>
          <div className="flex items-center text-sm">
            <Icon name="CheckCircle" size={16} className="text-blue-500 mr-3" />
            <span>Weekly earnings statements</span>
          </div>
        </div>
      </div>
    </div>

    <div className="bg-white p-6 rounded-lg shadow-lg">
      <h3 className="text-lg font-semibold text-gray-800 mb-4 text-center">Typical Earnings</h3>
      <div className="grid md:grid-cols-3 gap-6 text-center">
        <div className="bg-green-50 p-4 rounded-lg">
          <div className="text-2xl font-bold text-green-600">$18/hour</div>
          <div className="text-sm text-gray-600">Part-time (10-20 hours/week)</div>
          <div className="text-xs text-gray-500 mt-1">Including tips</div>
        </div>
        <div className="bg-blue-50 p-4 rounded-lg">
          <div className="text-2xl font-bold text-blue-600">$22/hour</div>
          <div className="text-sm text-gray-600">Full-time (30-40 hours/week)</div>
          <div className="text-xs text-gray-500 mt-1">Including bonuses</div>
        </div>
        <div className="bg-purple-50 p-4 rounded-lg">
          <div className="text-2xl font-bold text-purple-600">$28/hour</div>
          <div className="text-sm text-gray-600">Peak hours & weekends</div>
          <div className="text-xs text-gray-500 mt-1">High demand periods</div>
        </div>
      </div>
    </div>

    <div className="text-center">
      <button className="bg-purple-500 hover:bg-purple-600 text-white px-8 py-3 rounded-lg text-lg font-semibold">
        Apply to Become a Delivery Partner
      </button>
      <p className="text-sm text-gray-600 mt-2">Application takes 5 minutes • Start earning within 48 hours</p>
    </div>
  </div>
);

// Vendor Application Modal Component
const VendorApplicationModal = ({ type, onClose }) => {
  const [formData, setFormData] = useState({});
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 2000));
      alert(`${type.replace('-', ' ')} application submitted successfully!`);
      onClose();
    } catch (error) {
      alert('Application submission failed. Please try again.');
    }
    setSubmitting(false);
  };

  const getFormContent = () => {
    switch (type) {
      case 'home-restaurant':
        return {
          title: 'Home Restaurant Host Application',
          description: 'Start hosting authentic dining experiences in your home',
          fields: [
            { name: 'legal_name', label: 'Legal Name', type: 'text', required: true },
            { name: 'phone_number', label: 'Phone Number', type: 'tel', required: true },
            { name: 'address', label: 'Home Address', type: 'text', required: true },
            { name: 'dining_capacity', label: 'Maximum Guests', type: 'select', options: [2,4,6,8,10,12,15,20], required: true },
            { name: 'cuisine_specialties', label: 'Cuisine Specialties', type: 'textarea', placeholder: 'e.g., Italian, Mexican, Thai...' },
            { name: 'years_cooking_experience', label: 'Years of Cooking Experience', type: 'number', min: 0 }
          ]
        };
      case 'quick-eats':
        return {
          title: 'Quick Eats Provider Application',
          description: 'Provide fast, authentic meals for busy customers',
          fields: [
            { name: 'legal_name', label: 'Legal Name', type: 'text', required: true },
            { name: 'phone_number', label: 'Phone Number', type: 'tel', required: true },
            { name: 'kitchen_address', label: 'Kitchen Address', type: 'text', required: true },
            { name: 'service_radius', label: 'Service Radius (km)', type: 'number', min: 1, max: 25 },
            { name: 'menu_items', label: 'Sample Menu Items', type: 'textarea', placeholder: 'List 5-10 items you plan to offer...' },
            { name: 'daily_capacity', label: 'Daily Order Capacity', type: 'number', min: 5, max: 200 }
          ]
        };
        case 'delivery':
        return {
          title: 'Delivery Partner Application',
          description: 'Join our delivery network and start earning today',
          fields: [
            { name: 'legal_name', label: 'Legal Name', type: 'text', required: true },
            { name: 'phone_number', label: 'Phone Number', type: 'tel', required: true },
            { name: 'email', label: 'Email Address', type: 'email', required: true },
            { name: 'vehicle_type', label: 'Vehicle Type', type: 'select', options: ['Car', 'Motorcycle', 'Bicycle', 'Scooter'], required: true },
            { name: 'license_number', label: 'Driver License Number', type: 'text', required: true },
            { name: 'service_areas', label: 'Preferred Service Areas', type: 'textarea', placeholder: 'List neighborhoods or zip codes...' },
            { name: 'availability', label: 'Availability', type: 'textarea', placeholder: 'Days and hours you can work...' }
          ]
        };
      default:
        return { title: 'Application', description: '', fields: [] };
    }
  };

  const form = getFormContent();

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6 border-b">
          <div className="flex justify-between items-center">
            <div>
              <h3 className="text-xl font-semibold text-gray-800">{form.title}</h3>
              <p className="text-gray-600">{form.description}</p>
            </div>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600"
            >
              <Icon name="X" size={24} />
            </button>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          {form.fields.map((field) => (
            <div key={field.name}>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                {field.label} {field.required && '*'}
              </label>
              {field.type === 'select' ? (
                <select
                  name={field.name}
                  required={field.required}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                >
                  <option value="">Select...</option>
                  {field.options.map((option) => (
                    <option key={option} value={option}>
                      {typeof option === 'number' ? `${option}` : option}
                    </option>
                  ))}
                </select>
              ) : field.type === 'textarea' ? (
                <textarea
                  name={field.name}
                  placeholder={field.placeholder}
                  rows="3"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                />
              ) : (
                <input
                  type={field.type}
                  name={field.name}
                  placeholder={field.placeholder}
                  min={field.min}
                  max={field.max}
                  required={field.required}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                />
              )}
            </div>
          ))}

          <div className="bg-yellow-50 p-4 rounded-lg border border-yellow-200">
            <h4 className="font-medium text-yellow-800 mb-2">Next Steps</h4>
            <ul className="text-sm text-yellow-700 space-y-1">
              <li>• Application review within 3-5 business days</li>
              <li>• Background check and verification</li>
              <li>• Kitchen inspection (for food services)</li>
              <li>• Final approval and account activation</li>
            </ul>
          </div>

          <div className="flex space-x-4 pt-4">
            <button
              type="submit"
              disabled={submitting}
              className="flex-1 bg-green-500 hover:bg-green-600 text-white py-3 rounded-lg font-semibold disabled:opacity-50"
            >
              {submitting ? 'Submitting...' : 'Submit Application'}
            </button>
            <button
              type="button"
              onClick={onClose}
              className="flex-1 bg-gray-200 hover:bg-gray-300 text-gray-700 py-3 rounded-lg font-semibold"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

// Enhanced Profile Page with Monetization Features and Vendor Conversion Hub
const ProfilePage = () => {
  const { user } = useAuth();
  const [userSnippets, setUserSnippets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeProfileTab, setActiveProfileTab] = useState('overview');
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

      {/* Profile Navigation Tabs */}
      <div className="bg-white rounded-lg shadow-lg mb-8">
        <div className="flex flex-wrap justify-center border-b">
          {[
            { id: 'overview', title: 'Overview', icon: 'Profile' },
            { id: 'vendor-hub', title: 'Become a Vendor', icon: 'Restaurant' },
            { id: 'snippets', title: 'My Snippets', icon: 'Recipe' },
            { id: 'earnings', title: 'Earnings', icon: 'Dollar' }
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveProfileTab(tab.id)}
              className={`flex items-center space-x-2 px-4 py-3 border-b-2 transition-colors ${
                activeProfileTab === tab.id
                  ? 'border-green-500 text-green-600 bg-green-50'
                  : 'border-transparent text-gray-600 hover:text-green-600 hover:bg-gray-50'
              }`}
            >
              <Icon name={tab.icon} size={16} />
              <span className="font-medium">{tab.title}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Tab Content */}
      {activeProfileTab === 'overview' && (
        <>
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
        </>
      )}

      {activeProfileTab === 'vendor-hub' && <VendorConversionHub />}
      
      {activeProfileTab === 'snippets' && (
        <>
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
        </>
      )}

      {activeProfileTab === 'earnings' && <UserEarningsDashboard />}
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
            <option value="">All Countries (80+)</option>
            {/* Caribbean Islands */}
            <option value="jamaica">🇯🇲 Jamaica</option>
            <option value="trinidad_tobago">🇹🇹 Trinidad & Tobago</option>
            <option value="barbados">🇧🇧 Barbados</option>
            <option value="haiti">🇭🇹 Haiti</option>
            <option value="dominican_republic">🇩🇴 Dominican Republic</option>
            <option value="puerto_rico">🇵🇷 Puerto Rico</option>
            <option value="cuba">🇨🇺 Cuba</option>
            <option value="grenada">🇬🇩 Grenada</option>
            
            {/* Asian Heritage */}
            <option value="china">🇨🇳 China</option>
            <option value="japan">🇯🇵 Japan</option>
            <option value="korea">🇰🇷 Korea</option>
            <option value="vietnam">🇻🇳 Vietnam</option>
            <option value="thailand">🇹🇭 Thailand</option>
            <option value="cambodia">🇰🇭 Cambodia</option>
            <option value="laos">🇱🇦 Laos</option>
            <option value="philippines">🇵🇭 Philippines</option>
            <option value="indonesia">🇮🇩 Indonesia</option>
            <option value="malaysia">🇲🇾 Malaysia</option>
            <option value="india">🇮🇳 India</option>
            <option value="pakistan">🇵🇰 Pakistan</option>
            <option value="bangladesh">🇧🇩 Bangladesh</option>
            <option value="sri_lanka">🇱🇰 Sri Lanka</option>
            
            {/* African Heritage */}
            <option value="nigeria">🇳🇬 Nigeria</option>
            <option value="ghana">🇬🇭 Ghana</option>
            <option value="senegal">🇸🇳 Senegal</option>
            <option value="mali">🇲🇱 Mali</option>
            <option value="ivory_coast">🇨🇮 Côte d'Ivoire</option>
            <option value="cameroon">🇨🇲 Cameroon</option>
            <option value="congo">🇨🇬 Congo</option>
            <option value="ethiopia">🇪🇹 Ethiopia</option>
            <option value="kenya">🇰🇪 Kenya</option>
            <option value="tanzania">🇹🇿 Tanzania</option>
            <option value="uganda">🇺🇬 Uganda</option>
            <option value="somalia">🇸🇴 Somalia</option>
            
            {/* Latin American */}
            <option value="mexico">🇲🇽 Mexico</option>
            <option value="guatemala">🇬🇹 Guatemala</option>
            <option value="honduras">🇭🇳 Honduras</option>
            <option value="el_salvador">🇸🇻 El Salvador</option>
            <option value="colombia">🇨🇴 Colombia</option>
            <option value="venezuela">🇻🇪 Venezuela</option>
            <option value="peru">🇵🇪 Peru</option>
            <option value="ecuador">🇪🇨 Ecuador</option>
            <option value="bolivia">🇧🇴 Bolivia</option>
            <option value="chile">🇨🇱 Chile</option>
            <option value="argentina">🇦🇷 Argentina</option>
            <option value="brazil">🇧🇷 Brazil</option>
            
            {/* Middle Eastern */}
            <option value="turkey">🇹🇷 Turkey</option>
            <option value="iran">🇮🇷 Iran</option>
            <option value="lebanon">🇱🇧 Lebanon</option>
            <option value="syria">🇸🇾 Syria</option>
            <option value="jordan">🇯🇴 Jordan</option>
            <option value="afghanistan">🇦🇫 Afghanistan</option>
            
            {/* European Heritage */}
            <option value="italy">🇮🇹 Italy</option>
            <option value="spain">🇪🇸 Spain</option>
            <option value="portugal">🇵🇹 Portugal</option>
            <option value="france">🇫🇷 France</option>
            <option value="germany">🇩🇪 Germany</option>
            <option value="poland">🇵🇱 Poland</option>
            <option value="russia">🇷🇺 Russia</option>
            <option value="ukraine">🇺🇦 Ukraine</option>
            <option value="greece">🇬🇷 Greece</option>
            
            {/* Additional entries for other countries */}
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
              {/* External Ad - Revenue Generation */}
              {referenceRecipes.length > 0 && (
                <div className="md:col-span-2 lg:col-span-3">
                  <ExternalAdBanner placement="recipe_header" size="728x90" />
                </div>
              )}
              
              {referenceRecipes.map((recipe) => (
                <ReferenceRecipeCard key={recipe.id} recipe={recipe} />
              ))}
              
              {/* Sidebar Ad for larger screens */}
              {referenceRecipes.length > 3 && (
                <div className="hidden lg:block">
                  <ExternalAdBanner placement="sidebar_recipes" size="300x250" />
                </div>
              )}
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
        
        {/* External Ad - Revenue Generation */}
        <ExternalAdBanner placement="homepage_header" size="728x90" />
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-7 gap-4">
          <Link
            to="/templates"
            className="btn-primary text-center p-4 rounded-lg no-underline text-white flex flex-col items-center space-y-2"
          >
            <img src="https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=60&h=60&fit=crop&crop=center" 
                 alt="Browse Heritage Recipes" className="w-12 h-12 rounded-lg object-cover" />
            <span className="text-sm font-medium">{t('home.actions.browseName')}</span>
          </Link>
          <Link
            to="/create-snippet"
            className="btn-secondary text-center p-4 rounded-lg no-underline text-white flex flex-col items-center space-y-2"
          >
            <img src="https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=60&h=60&fit=crop&crop=center" 
                 alt="Create Recipe" className="w-12 h-12 rounded-lg object-cover" />
            <span className="text-sm font-medium">{t('home.actions.createName')}</span>
          </Link>
          <Link
            to="/grocery"
            className="bg-blue-500 hover:bg-blue-600 text-center p-4 rounded-lg no-underline text-white transition-all flex flex-col items-center space-y-2"
          >
            <img src="https://images.unsplash.com/photo-1542838132-92c53300491e?w=60&h=60&fit=crop&crop=center" 
                 alt="Specialty Ingredients" className="w-12 h-12 rounded-lg object-cover" />
            <span className="text-sm font-medium">{t('home.actions.ingredientsName')}</span>
          </Link>
          <Link
            to="/home-restaurant"
            className="bg-purple-500 hover:bg-purple-600 text-center p-4 rounded-lg no-underline text-white transition-all flex flex-col items-center space-y-2"
          >
            <img src="https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=60&h=60&fit=crop&crop=center" 
                 alt="Home Restaurant" className="w-12 h-12 rounded-lg object-cover" />
            <span className="text-sm font-medium">{t('home.actions.restaurantName')}</span>
          </Link>
          <Link
            to="/local-marketplace"
            className="bg-green-500 hover:bg-green-600 text-center p-4 rounded-lg no-underline text-white transition-all flex flex-col items-center space-y-2"
          >
            <img src="https://images.unsplash.com/photo-1488459716781-31db52582fe9?w=60&h=60&fit=crop&crop=center" 
                 alt="Local Marketplace" className="w-12 h-12 rounded-lg object-cover" />
            <span className="text-sm font-medium">{t('home.actions.marketplaceName')}</span>
          </Link>
          <Link
            to="/charity-program"
            className="bg-red-500 hover:bg-red-600 text-center p-4 rounded-lg no-underline text-white transition-all flex flex-col items-center space-y-2"
          >
            <img src="https://images.unsplash.com/photo-1559027615-cd4628902d4a?w=60&h=60&fit=crop&crop=center" 
                 alt="Charity Program" className="w-12 h-12 rounded-lg object-cover" />
            <span className="text-sm font-medium">{t('home.actions.charityName')}</span>
          </Link>
          <Link
            to="/lambalia-eats"
            className="bg-orange-500 hover:bg-orange-600 text-center p-4 rounded-lg no-underline text-white transition-all flex flex-col items-center space-y-2"
          >
            <img src="https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=60&h=60&fit=crop&crop=center" 
                 alt="Lambalia Eats" className="w-12 h-12 rounded-lg object-cover" />
            <span className="text-sm font-medium">{t('home.actions.eatsName')}</span>
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

// About Page Component
const AboutPage = () => {
  const { t } = useTranslation();
  
  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="text-center mb-12">
        <img 
          src="https://customer-assets.emergentagent.com/job_lambalia-recipes/artifacts/qzs71f09_2.png" 
          alt="Lambalia Heritage Logo" 
          className="w-24 h-24 mx-auto mb-6"
        />
        <h1 className="text-4xl font-bold heading-gradient mb-4">About Lambalia</h1>
        <p className="text-xl text-gray-600">Preserving Global Culinary Heritage Through Technology</p>
      </div>

      <div className="space-y-8">
        <section className="bg-gradient-to-r from-orange-50 to-yellow-50 p-8 rounded-xl">
          <div className="flex items-center mb-4">
            <Icon name="Heritage" size={32} className="text-orange-600 mr-3" />
            <h2 className="text-2xl font-bold text-orange-800">Our Mission</h2>
          </div>
          <p className="text-gray-700 text-lg leading-relaxed">
            Lambalia is the world's first comprehensive cultural culinary ecosystem, designed to preserve, share, and monetize global food heritage. 
            We connect diaspora communities with authentic ingredients, traditional recipes, and cultural cooking wisdom while empowering home cooks to transform their kitchens into sources of income.
          </p>
        </section>

        <section className="grid md:grid-cols-2 gap-8">
          <div className="bg-white p-6 rounded-xl shadow-lg">
            <div className="flex items-center mb-3">
              <Icon name="Recipe" size={24} className="text-green-600 mr-3" />
              <h3 className="text-xl font-semibold text-green-700">Heritage Preservation</h3>
            </div>
            <p className="text-gray-600">
              We preserve traditional recipes from 80+ global communities, ensuring cultural food knowledge passes to future generations. 
              Our AI-powered translation maintains cultural authenticity while making recipes accessible worldwide.
            </p>
          </div>
          
          <div className="bg-white p-6 rounded-xl shadow-lg">
            <div className="flex items-center mb-3">
              <Icon name="Dollar" size={24} className="text-blue-600 mr-3" />
              <h3 className="text-xl font-semibold text-blue-700">Economic Empowerment</h3>
            </div>
            <p className="text-gray-600">
              Through our multi-marketplace ecosystem, home cooks earn $50-$200 per experience, recipe consultations generate $2.99-$12.99, 
              and our 15% commission structure supports sustainable income generation.
            </p>
          </div>
        </section>

        <section>
          <div className="flex items-center justify-center mb-6">
            <Icon name="SmartCooking" size={32} className="text-gray-700 mr-3" />
            <h2 className="text-2xl font-bold text-gray-800 text-center">Our Platform Ecosystem</h2>
          </div>
          <div className="grid md:grid-cols-3 gap-6">
            <div className="text-center p-6 bg-purple-50 rounded-lg hover:shadow-lg transition-shadow">
              <AnimatedIcon name="Restaurant" size={48} className="text-purple-600 mx-auto mb-3" />
              <h4 className="font-semibold text-purple-800">Home Restaurants</h4>
              <p className="text-sm text-gray-600">Transform kitchens into dining experiences</p>
            </div>
            
            <div className="text-center p-6 bg-green-50 rounded-lg hover:shadow-lg transition-shadow">
              <AnimatedIcon name="Utensils" size={48} className="text-green-600 mx-auto mb-3" />
              <h4 className="font-semibold text-green-800">Lambalia Eats</h4>
              <p className="text-sm text-gray-600">Real-time food marketplace</p>
            </div>
            
            <div className="text-center p-6 bg-blue-50 rounded-lg hover:shadow-lg transition-shadow">
              <AnimatedIcon name="Farm" size={48} className="text-blue-600 mx-auto mb-3" />
              <h4 className="font-semibold text-blue-800">Farm Ecosystem</h4>
              <p className="text-sm text-gray-600">Direct farm-to-table connections</p>
            </div>
            
            <div className="text-center p-6 bg-red-50 rounded-lg hover:shadow-lg transition-shadow">
              <AnimatedIcon name="Heart" size={48} className="text-red-600 mx-auto mb-3" />
              <h4 className="font-semibold text-red-800">Charity Program</h4>
              <p className="text-sm text-gray-600">Social impact through food sharing</p>
            </div>
            
            <div className="text-center p-6 bg-orange-50 rounded-lg hover:shadow-lg transition-shadow">
              <AnimatedIcon name="Store" size={48} className="text-orange-600 mx-auto mb-3" />
              <h4 className="font-semibold text-orange-800">Specialty Ingredients</h4>
              <p className="text-sm text-gray-600">Ethnic grocery store network</p>
            </div>
            
            <div className="text-center p-6 bg-indigo-50 rounded-lg hover:shadow-lg transition-shadow">
              <AnimatedIcon name="Heritage" size={48} className="text-indigo-600 mx-auto mb-3" />
              <h4 className="font-semibold text-indigo-800">Heritage Recipes</h4>
              <p className="text-sm text-gray-600">Global cultural preservation</p>
            </div>
            
            {/* New Smart Cooking Tool Feature */}
            <div className="text-center p-6 bg-gradient-to-br from-orange-50 to-red-50 rounded-lg hover:shadow-lg transition-shadow border-2 border-orange-200">
              <AnimatedIcon name="SmartCooking" size={48} className="text-orange-600 mx-auto mb-3" />
              <h4 className="font-semibold text-orange-800">Smart Cooking Assistant</h4>
              <p className="text-sm text-gray-600">AI-powered recipe generation from your ingredients</p>
              <div className="mt-2">
                <span className="bg-orange-100 text-orange-800 px-2 py-1 rounded-full text-xs font-medium">
                  New Feature - $2.99
                </span>
              </div>
            </div>
          </div>
        </section>

        <section className="bg-gray-50 p-8 rounded-xl">
          <div className="flex items-center justify-center mb-4">
            <Icon name="Star" size={32} className="text-gray-700 mr-3" />
            <h2 className="text-2xl font-bold text-gray-800">Our Impact</h2>
          </div>
          <div className="grid md:grid-cols-4 gap-6 text-center">
            <div>
              <div className="text-3xl font-bold text-green-600">80+</div>
              <div className="text-sm text-gray-600">Cultural Communities</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-blue-600">300+</div>
              <div className="text-sm text-gray-600">Partner Stores</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-orange-600">15%</div>
              <div className="text-sm text-gray-600">Platform Commission</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-purple-600">76+</div>
              <div className="text-sm text-gray-600">Languages Supported</div>
            </div>
          </div>
        </section>

        <section className="text-center">
          <h2 className="text-2xl font-bold text-gray-800 mb-4">🤝 Join Our Mission</h2>
          <p className="text-gray-600 mb-6">
            Whether you're a home cook, cultural food expert, or someone passionate about preserving culinary heritage, 
            Lambalia provides the platform to share your knowledge and earn from your skills.
          </p>
          <div className="flex justify-center space-x-4">
            <Link to="/register" className="btn-primary px-6 py-3 rounded-lg">
              Join Lambalia
            </Link>
            <Link to="/careers" className="btn-secondary px-6 py-3 rounded-lg">
              Work With Us
            </Link>
          </div>
        </section>
      </div>
    </div>
  );
};

// Contact Page Component with Enhanced User Feedback System  
const ContactPage = () => {
  const { t } = useTranslation();
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState('contact');
  const [feedbackForm, setFeedbackForm] = useState({
    type: 'general',
    rating: 5,
    subject: '',
    message: '',
    category: '',
    urgency: 'low',
    email: user?.email || '',
    name: user?.full_name || user?.username || ''
  });
  const [submitting, setSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  const handleFeedbackSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    
    try {
      // Submit to actual feedback API
      const response = await axios.post(`${API}/feedback/submit`, feedbackForm);
      
      if (response.data.success) {
        setSubmitted(true);
        console.log('Feedback submitted successfully:', response.data);
        
        // Reset form
        setFeedbackForm({
          ...feedbackForm,
          subject: '',
          message: '',
          rating: 5
        });
      } else {
        throw new Error('Feedback submission failed');
      }
      
    } catch (error) {
      console.error('Feedback submission error:', error);
      alert('Failed to submit feedback. Please try again or contact support directly.');
    }
    
    setSubmitting(false);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFeedbackForm(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const feedbackTypes = [
    { value: 'general', label: 'General Feedback', icon: '💬' },
    { value: 'bug', label: 'Bug Report', icon: '🐛' },
    { value: 'feature', label: 'Feature Request', icon: '💡' },
    { value: 'ui', label: 'UI/UX Issues', icon: '🎨' },
    { value: 'performance', label: 'Performance Issues', icon: '⚡' },
    { value: 'recipe', label: 'Recipe/Content Issues', icon: '🍳' },
    { value: 'payment', label: 'Payment/Earnings Issues', icon: '💰' },
    { value: 'vendor', label: 'Vendor Program Feedback', icon: '🏪' },
    { value: 'compliment', label: 'Compliments & Praise', icon: '⭐' }
  ];

  const urgencyLevels = [
    { value: 'low', label: 'Low', color: 'text-green-600', desc: 'General feedback, suggestions' },
    { value: 'medium', label: 'Medium', color: 'text-yellow-600', desc: 'Minor issues, improvements' },
    { value: 'high', label: 'High', color: 'text-orange-600', desc: 'Significant problems' },
    { value: 'critical', label: 'Critical', color: 'text-red-600', desc: 'Platform broken, urgent issues' }
  ];

  const renderFeedbackForm = () => (
    <div className="space-y-6">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-gray-800 mb-4">📝 Share Your Experience</h2>
        <p className="text-gray-600">
          Your feedback helps us improve Lambalia for everyone in our global culinary community
        </p>
      </div>

      {submitted && (
        <div className="bg-green-50 border border-green-200 rounded-lg p-6 mb-6">
          <div className="flex items-center">
            <Icon name="CheckCircle" size={24} className="text-green-600 mr-3" />
            <div>
              <h3 className="text-green-800 font-semibold">Feedback Submitted Successfully!</h3>
              <p className="text-green-700 text-sm mt-1">
                Thank you for helping us improve Lambalia. We'll review your feedback and get back to you if needed.
              </p>
            </div>
          </div>
        </div>
      )}

      <form onSubmit={handleFeedbackSubmit} className="space-y-6">
        {/* User Info */}
        <div className="grid md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Name</label>
            <input
              type="text"
              name="name"
              value={feedbackForm.name}
              onChange={handleInputChange}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Email</label>
            <input
              type="email"
              name="email"
              value={feedbackForm.email}
              onChange={handleInputChange}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
              required
            />
          </div>
        </div>

        {/* Feedback Type */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-3">Feedback Type</label>
          <div className="grid md:grid-cols-3 gap-3">
            {feedbackTypes.map(type => (
              <button
                key={type.value}
                type="button"
                onClick={() => setFeedbackForm(prev => ({ ...prev, type: type.value }))}
                className={`p-3 rounded-lg border text-left transition-all ${
                  feedbackForm.type === type.value
                    ? 'border-green-500 bg-green-50 text-green-800'
                    : 'border-gray-300 hover:border-green-300 hover:bg-green-50'
                }`}
              >
                <div className="flex items-center space-x-2">
                  <span className="text-lg">{type.icon}</span>
                  <span className="text-sm font-medium">{type.label}</span>
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Rating */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-3">
            Overall Experience Rating
          </label>
          <div className="flex items-center space-x-2">
            {[1, 2, 3, 4, 5].map(rating => (
              <button
                key={rating}
                type="button"
                onClick={() => setFeedbackForm(prev => ({ ...prev, rating }))}
                className={`text-2xl transition-colors ${
                  rating <= feedbackForm.rating ? 'text-yellow-400' : 'text-gray-300'
                }`}
              >
                ⭐
              </button>
            ))}
            <span className="ml-3 text-sm text-gray-600">
              {feedbackForm.rating}/5 - {
                feedbackForm.rating === 5 ? 'Excellent' :
                feedbackForm.rating === 4 ? 'Good' :
                feedbackForm.rating === 3 ? 'Average' :
                feedbackForm.rating === 2 ? 'Poor' : 'Very Poor'
              }
            </span>
          </div>
        </div>

        {/* Urgency */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-3">Priority Level</label>
          <div className="grid md:grid-cols-2 gap-3">
            {urgencyLevels.map(level => (
              <button
                key={level.value}
                type="button"
                onClick={() => setFeedbackForm(prev => ({ ...prev, urgency: level.value }))}
                className={`p-3 rounded-lg border text-left transition-all ${
                  feedbackForm.urgency === level.value
                    ? 'border-green-500 bg-green-50'
                    : 'border-gray-300 hover:border-green-300 hover:bg-green-50'
                }`}
              >
                <div className={`font-medium ${level.color}`}>{level.label}</div>
                <div className="text-xs text-gray-600">{level.desc}</div>
              </button>
            ))}
          </div>
        </div>

        {/* Subject */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Subject</label>
          <input
            type="text"
            name="subject"
            value={feedbackForm.subject}
            onChange={handleInputChange}
            placeholder="Brief summary of your feedback..."
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
            required
          />
        </div>

        {/* Message */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Detailed Feedback
          </label>
          <textarea
            name="message"
            value={feedbackForm.message}
            onChange={handleInputChange}
            rows="6"
            placeholder="Please provide detailed feedback. Include steps to reproduce if reporting a bug, or describe your experience in detail..."
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
            required
          />
        </div>

        {/* Submit Button */}
        <div className="text-center">
          <button
            type="submit"
            disabled={submitting}
            className="bg-green-500 hover:bg-green-600 text-white px-8 py-3 rounded-lg font-semibold disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {submitting ? 'Submitting Feedback...' : 'Submit Feedback'}
          </button>
        </div>
      </form>

      {/* Quick Feedback Options */}
      <div className="mt-12 bg-gray-50 p-6 rounded-lg">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">Quick Feedback Options</h3>
        <div className="grid md:grid-cols-2 gap-4">
          <a
            href="mailto:feedback@lambalia.com?subject=Quick Feedback"
            className="bg-white p-4 rounded-lg shadow-sm hover:shadow-md transition-shadow border border-gray-200"
          >
            <div className="flex items-center space-x-3">
              <span className="text-2xl">📧</span>
              <div>
                <h4 className="font-medium text-gray-800">Email Direct</h4>
                <p className="text-sm text-gray-600">feedback@lambalia.com</p>
              </div>
            </div>
          </a>
          
          <a
            href="https://forms.google.com/lambalia-feedback"
            target="_blank"
            rel="noopener noreferrer"
            className="bg-white p-4 rounded-lg shadow-sm hover:shadow-md transition-shadow border border-gray-200"
          >
            <div className="flex items-center space-x-3">
              <span className="text-2xl">📋</span>
              <div>
                <h4 className="font-medium text-gray-800">Survey Form</h4>
                <p className="text-sm text-gray-600">Detailed questionnaire</p>
              </div>
            </div>
          </a>
        </div>
      </div>
    </div>
  );

  const renderContactInfo = () => (
    <div>
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold heading-gradient mb-4">Contact Lambalia</h1>
        <p className="text-xl text-gray-600">Get in touch with our global culinary community</p>
      </div>

      <div className="grid md:grid-cols-2 gap-12">
        <section>
          <h2 className="text-2xl font-bold text-gray-800 mb-6">🏢 Company Information</h2>
          
          <div className="space-y-6">
            <div className="bg-white p-6 rounded-xl shadow-lg">
              <h3 className="font-semibold text-green-700 mb-2">📍 Headquarters</h3>
              <p className="text-gray-600">
                Lambalia Global Inc.<br />
                Digital Culinary Innovation Center<br />
                San Francisco, CA, USA
              </p>
            </div>

            <div className="bg-white p-6 rounded-xl shadow-lg">
              <h3 className="font-semibold text-blue-700 mb-2">🌐 Global Operations</h3>
              <p className="text-gray-600">
                Operating in 15+ countries<br />
                Supporting 80+ cultural communities<br />
                24/7 multilingual support
              </p>
            </div>

            <div className="bg-white p-6 rounded-xl shadow-lg">
              <h3 className="font-semibold text-purple-700 mb-2">🏪 Partner Network</h3>
              <p className="text-gray-600">
                H-Mart • Patel Brothers<br />
                99 Ranch Market • Fresh Thyme<br />
                300+ specialty grocery stores
              </p>
            </div>
          </div>
        </section>

        <section>
          <h2 className="text-2xl font-bold text-gray-800 mb-6">📞 Get In Touch</h2>
          
          <div className="space-y-6">
            <div className="bg-gradient-to-r from-green-50 to-blue-50 p-6 rounded-xl">
              <h3 className="font-semibold text-green-800 mb-3">💼 Business Partnerships</h3>
              <p className="text-sm text-gray-600 mb-2">Grocery chains, restaurant groups, cultural organizations</p>
              <a href="mailto:partnerships@lambalia.com" className="text-green-600 font-medium">
                partnerships@lambalia.com
              </a>
            </div>

            <div className="bg-gradient-to-r from-orange-50 to-yellow-50 p-6 rounded-xl">
              <h3 className="font-semibold text-orange-800 mb-3">🎯 Media & Press</h3>
              <p className="text-sm text-gray-600 mb-2">Press inquiries, interviews, feature stories</p>
              <a href="mailto:press@lambalia.com" className="text-orange-600 font-medium">
                press@lambalia.com
              </a>
            </div>

            <div className="bg-gradient-to-r from-purple-50 to-pink-50 p-6 rounded-xl">
              <h3 className="font-semibold text-purple-800 mb-3">🤝 Community Support</h3>
              <p className="text-sm text-gray-600 mb-2">User support, cultural authenticity, recipe verification</p>
              <a href="mailto:support@lambalia.com" className="text-purple-600 font-medium">
                support@lambalia.com
              </a>
            </div>

            <div className="bg-gradient-to-r from-blue-50 to-indigo-50 p-6 rounded-xl">
              <h3 className="font-semibold text-blue-800 mb-3">💼 Careers</h3>
              <p className="text-sm text-gray-600 mb-2">Join our mission to preserve global culinary heritage</p>
              <Link to="/careers" className="text-blue-600 font-medium">
                View Open Positions →
              </Link>
            </div>

            <div className="bg-gradient-to-r from-red-50 to-pink-50 p-6 rounded-xl">
              <h3 className="font-semibold text-red-800 mb-3">🚨 Report Issues</h3>
              <p className="text-sm text-gray-600 mb-2">Technical problems, content concerns, fraud prevention</p>
              <a href="mailto:security@lambalia.com" className="text-red-600 font-medium">
                security@lambalia.com
              </a>
            </div>

            <div className="bg-gradient-to-r from-pink-50 to-rose-50 p-6 rounded-xl">
              <h3 className="font-semibold text-pink-800 mb-3">💝 User Feedback</h3>
              <p className="text-sm text-gray-600 mb-2">Experience feedback, suggestions, compliments</p>
              <button
                onClick={() => setActiveTab('feedback')}
                className="text-pink-600 font-medium hover:text-pink-800"
              >
                Submit Feedback →
              </button>
            </div>
          </div>
        </section>
      </div>

      <section className="mt-12 text-center bg-gray-50 p-8 rounded-xl">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">🌍 Follow Our Global Journey</h2>
        <p className="text-gray-600 mb-6">
          Stay updated on new cultural communities, partner integrations, and platform developments
        </p>
        <div className="flex justify-center space-x-6">
          <a href="#" className="text-blue-600 hover:text-blue-800 font-medium">LinkedIn</a>
          <a href="#" className="text-pink-600 hover:text-pink-800 font-medium">Instagram</a>
          <a href="#" className="text-blue-500 hover:text-blue-700 font-medium">Twitter</a>
          <a href="#" className="text-red-600 hover:text-red-800 font-medium">YouTube</a>
        </div>
      </section>
    </div>
  );
  
  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      {/* Tab Navigation */}
      <div className="flex justify-center mb-8">
        <div className="bg-white rounded-lg shadow-lg p-1">
          <button
            onClick={() => setActiveTab('contact')}
            className={`px-6 py-2 rounded-md font-medium transition-colors ${
              activeTab === 'contact'
                ? 'bg-green-500 text-white'
                : 'text-gray-600 hover:text-green-600'
            }`}
          >
            📞 Contact Info
          </button>
          <button
            onClick={() => setActiveTab('feedback')}
            className={`px-6 py-2 rounded-md font-medium transition-colors ${
              activeTab === 'feedback'
                ? 'bg-green-500 text-white'
                : 'text-gray-600 hover:text-green-600'
            }`}
          >
            📝 Share Feedback
          </button>
        </div>
      </div>

      {/* Tab Content */}
      {activeTab === 'contact' && renderContactInfo()}
      {activeTab === 'feedback' && renderFeedbackForm()}
    </div>
  );
};

// Careers Page Component
const CareersPage = () => {
  const { t } = useTranslation();
  
  const jobOpenings = [
    {
      id: 1,
      title: "Senior Full-Stack Engineer",
      department: "Engineering",
      location: "Remote/San Francisco",
      type: "Full-time",
      urgency: "Critical",
      description: "Lead development of our multi-marketplace ecosystem. Backend expertise with FastAPI, MongoDB, real-time systems.",
      requirements: ["5+ years full-stack development", "FastAPI/Python expertise", "MongoDB/NoSQL experience", "Real-time systems knowledge"],
      whyCritical: "Platform scaling requires expert architectural decisions for 80+ country support and real-time food marketplace."
    },
    {
      id: 2,
      title: "Cultural Community Manager",
      department: "Community",
      location: "Global Remote",
      type: "Full-time", 
      urgency: "Critical",
      description: "Build relationships with cultural communities globally. Ensure authentic recipe representation and cultural sensitivity.",
      requirements: ["Multilingual capabilities", "Cultural sensitivity expertise", "Community management experience", "Heritage food knowledge"],
      whyCritical: "Authenticity is our core value - improper cultural representation could damage trust with diaspora communities."
    },
    {
      id: 3,
      title: "DevOps/Platform Engineer", 
      department: "Infrastructure",
      location: "Remote",
      type: "Full-time",
      urgency: "High",
      description: "Scale infrastructure for global usage. Manage containerized services, databases, and real-time systems.",
      requirements: ["Kubernetes expertise", "CI/CD pipelines", "Database scaling", "Monitoring systems"],
      whyCritical: "Platform downtime affects thousands of daily food transactions and cultural recipe sharing."
    },
    {
      id: 4,
      title: "Business Development Manager - Grocery Partnerships",
      department: "Partnerships", 
      location: "Remote/Travel",
      type: "Full-time",
      urgency: "High",
      description: "Expand partnerships with ethnic grocery chains (H-Mart, Patel Brothers, etc.). Drive specialty ingredient sourcing.",
      requirements: ["B2B partnership experience", "Retail/grocery industry knowledge", "Negotiation skills", "Travel flexibility"],
      whyCritical: "Ingredient availability determines user satisfaction - partnerships drive 40% of platform value."
    },
    {
      id: 5,
      title: "Data Scientist - Matching Algorithms",
      department: "Data Science",
      location: "Remote/San Francisco", 
      type: "Full-time",
      urgency: "High",
      description: "Optimize food matching algorithms, cultural preference analysis, and demand prediction for Lambalia Eats.",
      requirements: ["ML/AI experience", "Python/scikit-learn", "Real-time recommendation systems", "Cultural data analysis"],
      whyCritical: "Poor matching affects earnings potential for home cooks and user satisfaction for food requests."
    },
    {
      id: 6,
      title: "Product Manager - Marketplace Systems",
      department: "Product",
      location: "San Francisco/Remote",
      type: "Full-time",
      urgency: "High", 
      description: "Coordinate development across 6 marketplace systems. Balance cultural preservation with commercial viability.",
      requirements: ["5+ years product management", "Marketplace experience", "Cultural sensitivity", "Data-driven decisions"],
      whyCritical: "Multiple complex systems require coordination - poor prioritization could fragment user experience."
    },
    {
      id: 7,
      title: "Frontend/UI Engineer - Mobile Experience",
      department: "Engineering",
      location: "Remote",
      type: "Full-time",
      urgency: "Medium",
      description: "Optimize mobile experience for real-time food ordering and cultural recipe discovery.",
      requirements: ["React/React Native", "Mobile-first design", "Performance optimization", "Multilingual UI"],
      whyCritical: "70% of food orders happen on mobile - poor mobile experience directly impacts revenue."
    },
    {
      id: 8,
      title: "Customer Success Manager - Multilingual",
      department: "Support",
      location: "Global Remote",
      type: "Full-time",
      urgency: "Medium",
      description: "Provide 24/7 support across 76+ languages. Handle cultural disputes and authenticity questions.",
      requirements: ["3+ languages fluency", "Customer service excellence", "Cultural mediation skills", "Food industry knowledge"],
      whyCritical: "Cultural food disputes require sensitive handling - poor support could damage community relationships."
    },
    {
      id: 9,
      title: "Content Moderator - Recipe Authenticity",
      department: "Community",
      location: "Remote",
      type: "Part-time/Contract",
      urgency: "Medium", 
      description: "Verify cultural authenticity of submitted recipes. Prevent cultural appropriation while encouraging sharing.",
      requirements: ["Deep cultural food knowledge", "Multiple heritage backgrounds preferred", "Diplomatic communication", "Research skills"],
      whyCritical: "Recipe authenticity maintains platform credibility - incorrect cultural representation damages trust."
    },
    {
      id: 10,
      title: "Marketing Manager - Global Expansion",
      department: "Marketing",
      location: "Remote/Travel",
      type: "Full-time",
      urgency: "Medium",
      description: "Drive user acquisition in new cultural communities. Understand diaspora marketing and cultural sensitivity.",
      requirements: ["Global marketing experience", "Cultural community knowledge", "Digital marketing expertise", "Diaspora outreach"],
      whyCritical: "Growth depends on authentic cultural community adoption - generic marketing approaches fail with heritage communities."
    }
  ];

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold heading-gradient mb-4">Join the Lambalia Team</h1>
        <p className="text-xl text-gray-600 mb-6">Help us preserve global culinary heritage while building the future of food commerce</p>
        
        <div className="bg-gradient-to-r from-orange-50 to-yellow-50 p-6 rounded-xl max-w-2xl mx-auto">
          <h2 className="text-lg font-semibold text-orange-800 mb-2">🚀 We're Growing Fast!</h2>
          <p className="text-gray-700">
            Lambalia serves 80+ cultural communities, processes thousands of daily food transactions, 
            and partners with 300+ specialty grocery stores. Join us in scaling globally while preserving cultural authenticity.
          </p>
        </div>
      </div>

      <div className="grid gap-8 mb-12">
        <div className="grid md:grid-cols-3 gap-6">
          <div className="bg-red-50 p-6 rounded-xl text-center">
            <div className="text-3xl mb-2">🔥</div>
            <h3 className="font-semibold text-red-800">Critical Positions</h3>
            <p className="text-sm text-gray-600">Platform survival depends on these roles</p>
            <div className="text-2xl font-bold text-red-600 mt-2">
              {jobOpenings.filter(job => job.urgency === 'Critical').length}
            </div>
          </div>
          
          <div className="bg-yellow-50 p-6 rounded-xl text-center">
            <div className="text-3xl mb-2">⚡</div>
            <h3 className="font-semibold text-yellow-800">High Priority</h3>
            <p className="text-sm text-gray-600">Growth acceleration positions</p>
            <div className="text-2xl font-bold text-yellow-600 mt-2">
              {jobOpenings.filter(job => job.urgency === 'High').length}
            </div>
          </div>
          
          <div className="bg-green-50 p-6 rounded-xl text-center">
            <div className="text-3xl mb-2">📈</div>
            <h3 className="font-semibold text-green-800">Scale & Polish</h3>
            <p className="text-sm text-gray-600">Enhancement and optimization roles</p>
            <div className="text-2xl font-bold text-green-600 mt-2">
              {jobOpenings.filter(job => job.urgency === 'Medium').length}
            </div>
          </div>
        </div>
      </div>

      <section>
        <h2 className="text-2xl font-bold text-gray-800 mb-8">🎯 Open Positions</h2>
        
        <div className="space-y-6">
          {jobOpenings.map((job) => (
            <div key={job.id} className={`bg-white p-6 rounded-xl shadow-lg border-l-4 ${
              job.urgency === 'Critical' ? 'border-red-500' :
              job.urgency === 'High' ? 'border-yellow-500' : 'border-green-500'
            }`}>
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-xl font-semibold text-gray-800">{job.title}</h3>
                  <div className="flex items-center space-x-4 text-sm text-gray-600 mt-1">
                    <span>🏢 {job.department}</span>
                    <span>📍 {job.location}</span>
                    <span>⏰ {job.type}</span>
                  </div>
                </div>
                <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                  job.urgency === 'Critical' ? 'bg-red-100 text-red-800' :
                  job.urgency === 'High' ? 'bg-yellow-100 text-yellow-800' : 'bg-green-100 text-green-800'
                }`}>
                  {job.urgency} Priority
                </span>
              </div>
              
              <p className="text-gray-700 mb-4">{job.description}</p>
              
              <div className="grid md:grid-cols-2 gap-6 mb-4">
                <div>
                  <h4 className="font-semibold text-gray-800 mb-2">📋 Requirements:</h4>
                  <ul className="text-sm text-gray-600 space-y-1">
                    {job.requirements.map((req, idx) => (
                      <li key={idx}>• {req}</li>
                    ))}
                  </ul>
                </div>
                
                <div>
                  <h4 className="font-semibold text-orange-800 mb-2">🚨 Why Critical:</h4>
                  <p className="text-sm text-gray-700">{job.whyCritical}</p>
                </div>
              </div>
              
              <div className="flex justify-between items-center">
                <div className="text-sm text-gray-600">
                  💰 Competitive salary + equity + cultural food stipend
                </div>
                <button className="btn-primary px-6 py-2 rounded-lg text-sm">
                  Apply Now
                </button>
              </div>
            </div>
          ))}
        </div>
      </section>

      <section className="mt-16 text-center bg-gradient-to-r from-green-50 to-blue-50 p-8 rounded-xl">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">🌍 Why Work at Lambalia?</h2>
        
        <div className="grid md:grid-cols-2 gap-8 mt-8">
          <div className="text-left">
            <h3 className="font-semibold text-green-800 mb-3">🎯 Mission-Driven Work</h3>
            <ul className="text-sm text-gray-700 space-y-2">
              <li>• Preserve disappearing cultural food knowledge</li>
              <li>• Empower home cooks to earn sustainable income</li>
              <li>• Connect diaspora communities with heritage</li>
              <li>• Support local ethnic businesses globally</li>
            </ul>
          </div>
          
          <div className="text-left">
            <h3 className="font-semibold text-blue-800 mb-3">💼 Career Growth</h3>
            <ul className="text-sm text-gray-700 space-y-2">
              <li>• Rapid scaling company with global impact</li>
              <li>• Work with cutting-edge food technology</li>
              <li>• Cultural expertise valued and rewarded</li>
              <li>• Remote-first with global team collaboration</li>
            </ul>
          </div>
        </div>
        
        <div className="mt-8">
          <a href="mailto:careers@lambalia.com" className="btn-primary px-8 py-3 rounded-lg">
            Start Your Application 🚀
          </a>
        </div>
      </section>
    </div>
  );
};

// Footer Component  
const Footer = () => {
  const { t } = useTranslation();
  
  return (
    <footer className="bg-gray-900 text-white mt-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Company Info */}
          <div className="md:col-span-1">
            <div className="flex items-center space-x-3 mb-4">
              <img 
                src="https://customer-assets.emergentagent.com/job_lambalia-recipes/artifacts/qzs71f09_2.png" 
                alt="Lambalia" 
                className="w-10 h-10"
              />
              <h3 className="text-xl font-bold">Lambalia</h3>
            </div>
            <p className="text-gray-400 text-sm leading-relaxed">
              Preserving global culinary heritage through technology. 
              Connecting 80+ cultural communities with authentic recipes and sustainable income opportunities.
            </p>
            <div className="flex space-x-4 mt-4">
              <a href="#" className="text-gray-400 hover:text-white">LinkedIn</a>
              <a href="#" className="text-gray-400 hover:text-white">Twitter</a>
              <a href="#" className="text-gray-400 hover:text-white">Instagram</a>
            </div>
          </div>

          {/* Platform Links */}
          <div>
            <h4 className="text-lg font-semibold mb-4">Platform</h4>
            <ul className="space-y-2 text-sm">
              <li><Link to="/templates" className="text-gray-400 hover:text-white">Heritage Recipes</Link></li>
              <li><Link to="/lambalia-eats" className="text-gray-400 hover:text-white">Lambalia Eats</Link></li>
              <li><Link to="/home-restaurant" className="text-gray-400 hover:text-white">Home Restaurants</Link></li>
              <li><Link to="/local-marketplace" className="text-gray-400 hover:text-white">Local Marketplace</Link></li>
              <li><Link to="/charity-program" className="text-gray-400 hover:text-white">Charity Program</Link></li>
              <li><Link to="/grocery" className="text-gray-400 hover:text-white">Specialty Ingredients</Link></li>
            </ul>
          </div>

          {/* Company Links */}
          <div>
            <h4 className="text-lg font-semibold mb-4">Company</h4>
            <ul className="space-y-2 text-sm">
              <li><Link to="/about" className="text-gray-400 hover:text-white">About Us</Link></li>
              <li><Link to="/careers" className="text-gray-400 hover:text-white">Careers</Link></li>
              <li><Link to="/contact" className="text-gray-400 hover:text-white">Contact</Link></li>
              <li><a href="mailto:press@lambalia.com" className="text-gray-400 hover:text-white">Press</a></li>
              <li><a href="mailto:partnerships@lambalia.com" className="text-gray-400 hover:text-white">Partnerships</a></li>
            </ul>
          </div>

          {/* Support Links */}
          <div>
            <h4 className="text-lg font-semibold mb-4">Support</h4>
            <ul className="space-y-2 text-sm">
              <li><a href="mailto:support@lambalia.com" className="text-gray-400 hover:text-white">Help Center</a></li>
              <li><Link to="/contact" className="text-gray-400 hover:text-white">Community Guidelines</Link></li>
              <li><Link to="/contact" className="text-gray-400 hover:text-white">Privacy Policy</Link></li>
              <li><Link to="/contact" className="text-gray-400 hover:text-white">Terms of Service</Link></li>
              <li><a href="mailto:security@lambalia.com" className="text-gray-400 hover:text-white">Report Issue</a></li>
            </ul>
          </div>
        </div>

        <div className="border-t border-gray-800 mt-8 pt-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <p className="text-gray-400 text-sm">
              © 2024 Lambalia Global Inc. All rights reserved. Preserving culinary heritage worldwide.
            </p>
            <div className="flex items-center space-x-6 mt-4 md:mt-0">
              <span className="text-xs text-gray-500">🌍 Operating in 15+ countries</span>
              <span className="text-xs text-gray-500">📞 24/7 Multilingual Support</span>
              <span className="text-xs text-gray-500">🔒 SOC 2 Compliant</span>
            </div>
          </div>
        </div>
      </div>
    </footer>
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
                   </ProtectedRoute>
}
/>
<Route path="/chef-market" element={
  <ProtectedRoute>
    <>
      <Header />
      <ChefMarket />
      <Footer />
    </>
  </ProtectedRoute>
} />
<Route
                <HomePage />
                    <Footer />
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
                    <Footer />
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
                    <Footer />
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
                    <Footer />
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
                    <Footer />
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
                    <Footer />
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
                    <Footer />
                  </>
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/lambalia-eats" 
              element={
                <>
                  <LambaliaEatsApp />
                  <Footer />
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
                    <Footer />
                  </>
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/about" 
              element={
                <>
                  <Header />
                  <AboutPage />
                  <Footer />
                </>
              } 
            />
            <Route 
              path="/contact" 
              element={
                <>
                  <Header />
                  <ContactPage />
                  <Footer />
                </>
              } 
            />
            <Route 
              path="/careers" 
              element={
                <>
                  <Header />
                  <CareersPage />
                  <Footer />
                </>
              } 
            />
            <Route 
              path="/admin/revenue" 
              element={
                <ProtectedRoute>
                  <>
                    <Header />
                    <RevenueDashboard />
                    <Footer />
                  </>
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/my-earnings" 
              element={
                <ProtectedRoute>
                  <>
                    <Header />
                    <UserEarningsDashboard />
                    <Footer />
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
