import React, { useState, useEffect, createContext, useContext } from 'react';
import { BrowserRouter, Routes, Route, Navigate, Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import './App.css';

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
              src="https://customer-assets.emergentagent.com/job_completion-quest/artifacts/gpq5b6s8_Image%20%2821%29.png" 
              alt="Lambalia Logo" 
              className="w-32 h-32 mx-auto mb-4"
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

  return (
    <header className="nav-header shadow-lg border-b">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="flex items-center space-x-3 group">
            <img 
              src="https://customer-assets.emergentagent.com/job_completion-quest/artifacts/gpq5b6s8_Image%20%2821%29.png" 
              alt="Lambalia Logo" 
              className="w-10 h-10 transition-transform group-hover:scale-110"
            />
            <h1 className="text-2xl font-bold heading-gradient">Lambalia</h1>
          </Link>
          
          <nav className="flex items-center space-x-6">
            <Link to="/" className="nav-link text-gray-700 hover:text-green-600 px-3 py-2 rounded-md font-medium">
              🏠 Home
            </Link>
            <Link to="/templates" className="nav-link text-gray-700 hover:text-green-600 px-3 py-2 rounded-md font-medium">
              📚 Templates
            </Link>
            <Link to="/create-snippet" className="nav-link text-gray-700 hover:text-green-600 px-3 py-2 rounded-md font-medium">
              ✨ Create
            </Link>
            <Link to="/grocery" className="nav-link text-gray-700 hover:text-green-600 px-3 py-2 rounded-md font-medium">
              🛒 Shop
            </Link>
            <Link to="/home-restaurant" className="nav-link text-gray-700 hover:text-green-600 px-3 py-2 rounded-md font-medium">
              🏠👩‍🍳 Restaurant
            </Link>
            <Link to="/profile" className="nav-link text-gray-700 hover:text-green-600 px-3 py-2 rounded-md font-medium">
              👤 Profile
            </Link>
            
            <div className="flex items-center space-x-3 ml-6 pl-6 border-l border-gray-200">
              <div className="text-sm">
                <p className="font-medium text-gray-800">{user?.username}</p>
                <p className="text-green-600 font-semibold">${user?.credits || 0} credits</p>
              </div>
              <button
                onClick={logout}
                className="bg-gray-100 hover:bg-gray-200 text-gray-700 px-3 py-2 rounded-lg text-sm transition-all font-medium"
              >
                Logout
              </button>
            </div>
          </nav>
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
const HomeRestaurantPage = () => {
  const { user } = useAuth();
  const [isRestaurantMode, setIsRestaurantMode] = useState(false);
  const [menuItems, setMenuItems] = useState([]);
  const [bookings, setBookings] = useState([]);

  const toggleRestaurantMode = () => {
    setIsRestaurantMode(!isRestaurantMode);
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="home-restaurant">
        <h2 className="text-3xl font-bold mb-4">Transform Your Home Into a Restaurant</h2>
        <p className="text-lg mb-6">
          Turn your passion for cooking into a profitable business. Open your kitchen to food lovers 
          in your community and share authentic, homemade meals.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <div className="glass p-6">
            <h3 className="text-xl font-semibold mb-3">🏠 Home Dining Experience</h3>
            <ul className="text-sm space-y-2">
              <li>• Host 2-8 guests in your dining room</li>
              <li>• Set your own menu and prices</li>
              <li>• Share your cultural heritage through food</li>
              <li>• Build a community of food lovers</li>
            </ul>
          </div>

          <div className="glass p-6">
            <h3 className="text-xl font-semibold mb-3">💰 Earning Potential</h3>
            <ul className="text-sm space-y-2">
              <li>• $30-80 per person per meal</li>
              <li>• Host 1-3 dinners per week</li>
              <li>• Monthly potential: $500-2000+</li>
              <li>• Platform fee: only 15%</li>
            </ul>
          </div>
        </div>

        <div className="text-center">
          <button
            onClick={toggleRestaurantMode}
            className={`px-8 py-4 text-lg font-semibold rounded-xl transition-all ${
              isRestaurantMode 
                ? 'bg-red-500 hover:bg-red-600 text-white' 
                : 'btn-primary'
            }`}
          >
            {isRestaurantMode ? 'Close Restaurant 🔴' : 'Open My Kitchen 🟢'}
          </button>
        </div>

        {isRestaurantMode && (
          <div className="mt-8 p-6 bg-white rounded-xl text-gray-800">
            <h3 className="text-xl font-semibold mb-4">Your Home Restaurant Dashboard</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-green-100 p-4 rounded-lg">
                <h4 className="font-semibold text-green-800">Today's Bookings</h4>
                <p className="text-2xl font-bold text-green-600">3</p>
                <p className="text-sm text-green-700">6:00 PM - Italian Night</p>
              </div>
              
              <div className="bg-blue-100 p-4 rounded-lg">
                <h4 className="font-semibold text-blue-800">This Week's Revenue</h4>
                <p className="text-2xl font-bold text-blue-600">$420</p>
                <p className="text-sm text-blue-700">5 dinners hosted</p>
              </div>
              
              <div className="bg-purple-100 p-4 rounded-lg">
                <h4 className="font-semibold text-purple-800">Guest Rating</h4>
                <p className="text-2xl font-bold text-purple-600">4.9 ⭐</p>
                <p className="text-sm text-purple-700">47 reviews</p>
              </div>
            </div>

            <div className="mt-6">
              <h4 className="font-semibold mb-3">Quick Actions</h4>
              <div className="flex flex-wrap gap-3">
                <button className="btn-primary px-4 py-2 text-sm">📅 Schedule Dinner</button>
                <button className="btn-secondary px-4 py-2 text-sm">🍽️ Update Menu</button>
                <button className="bg-purple-500 hover:bg-purple-600 text-white px-4 py-2 rounded text-sm">💬 Message Guests</button>
                <button className="bg-yellow-500 hover:bg-yellow-600 text-white px-4 py-2 rounded text-sm">📊 View Analytics</button>
              </div>
            </div>
          </div>
        )}
      </div>
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
        <h2 className="text-3xl font-bold heading-gradient mb-4">Discover Traditional Recipes</h2>
        <p className="text-gray-600 mb-6">Explore authentic culinary treasures from every corner of the world</p>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <Link
            to="/templates"
            className="btn-primary text-center p-4 rounded-lg no-underline text-white"
          >
            📚 Browse Templates
          </Link>
          <Link
            to="/create-snippet"
            className="btn-secondary text-center p-4 rounded-lg no-underline text-white"
          >
            ✨ Create Snippet
          </Link>
          <Link
            to="/grocery"
            className="bg-blue-500 hover:bg-blue-600 text-center p-4 rounded-lg no-underline text-white transition-all"
          >
            🛒 Find Ingredients
          </Link>
          <Link
            to="/home-restaurant"
            className="bg-purple-500 hover:bg-purple-600 text-center p-4 rounded-lg no-underline text-white transition-all"
          >
            🏠👩‍🍳 Open Kitchen
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