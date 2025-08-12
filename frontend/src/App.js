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

// Login Component
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
    <div className="min-h-screen bg-gradient-to-br from-orange-50 to-red-50 flex items-center justify-center px-4">
      <div className="max-w-md w-full bg-white rounded-xl shadow-lg p-8">
        <div className="text-center mb-8">
          <img 
            src="https://customer-assets.emergentagent.com/job_completion-quest/artifacts/gpq5b6s8_Image%20%2821%29.png" 
            alt="Lambalia Logo" 
            className="w-32 h-32 mx-auto mb-4"
          />
          <h1 className="text-3xl font-bold text-gray-800">Lambalia</h1>
          <p className="text-gray-600 mt-2">& pperian an · taf culiticly</p>
        </div>

        <div className="flex mb-6">
          <button
            className={`flex-1 py-2 px-4 rounded-l-lg font-medium ${
              isLogin ? 'bg-orange-500 text-white' : 'bg-gray-200 text-gray-700'
            }`}
            onClick={() => setIsLogin(true)}
          >
            Login
          </button>
          <button
            className={`flex-1 py-2 px-4 rounded-r-lg font-medium ${
              !isLogin ? 'bg-orange-500 text-white' : 'bg-gray-200 text-gray-700'
            }`}
            onClick={() => setIsLogin(false)}
          >
            Register
          </button>
        </div>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
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
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
                required
              />
            </div>
            <button
              type="submit"
              className="w-full bg-orange-500 hover:bg-orange-600 text-white font-medium py-2 px-4 rounded-md transition-colors"
            >
              Login
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
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
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
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
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
                placeholder="For grocery store integration"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
              <input
                type="password"
                name="password"
                value={formData.password}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
                required
              />
            </div>
            <button
              type="submit"
              className="w-full bg-orange-500 hover:bg-orange-600 text-white font-medium py-2 px-4 rounded-md transition-colors"
            >
              Join Lambalia
            </button>
          </form>
        )}

        <div className="text-center mt-6">
          <p className="text-sm text-gray-600">
            Join our community of food lovers sharing authentic recipes from around the world!
          </p>
        </div>
      </div>
    </div>
  );
};

// Navigation Header Component
const Header = () => {
  const { user, logout } = useAuth();

  return (
    <header className="bg-white shadow-sm border-b">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="flex items-center space-x-3">
            <img 
              src="https://customer-assets.emergentagent.com/job_completion-quest/artifacts/gpq5b6s8_Image%20%2821%29.png" 
              alt="Lambalia Logo" 
              className="w-10 h-10"
            />
            <h1 className="text-2xl font-bold text-orange-600">Lambalia</h1>
          </Link>
          
          <nav className="flex items-center space-x-4">
            <Link to="/" className="text-gray-700 hover:text-orange-600 px-3 py-2 rounded-md">
              Home
            </Link>
            <Link to="/templates" className="text-gray-700 hover:text-orange-600 px-3 py-2 rounded-md">
              Recipe Templates
            </Link>
            <Link to="/create-snippet" className="text-gray-700 hover:text-orange-600 px-3 py-2 rounded-md">
              Create Snippet
            </Link>
            <Link to="/grocery" className="text-gray-700 hover:text-orange-600 px-3 py-2 rounded-md">
              Find Ingredients
            </Link>
            <Link to="/profile" className="text-gray-700 hover:text-orange-600 px-3 py-2 rounded-md">
              Profile
            </Link>
            
            <div className="flex items-center space-x-3 ml-4 pl-4 border-l">
              <span className="text-sm text-gray-600">
                {user?.username} ({user?.credits || 0} credits)
              </span>
              <button
                onClick={logout}
                className="bg-gray-100 hover:bg-gray-200 text-gray-700 px-3 py-1 rounded-md text-sm transition-colors"
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

// Recipe Templates Page
const RecipeTemplatesPage = () => {
  const [referenceRecipes, setReferenceRecipes] = useState([]);
  const [countries, setCountries] = useState([]);
  const [selectedCountry, setSelectedCountry] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchReferenceRecipes();
    fetchCountries();
  }, [selectedCountry]);

  const fetchReferenceRecipes = async () => {
    setLoading(true);
    try {
      const params = selectedCountry ? `?country_id=${selectedCountry}&featured_only=true` : '?featured_only=true';
      const response = await axios.get(`${API}/reference-recipes${params}`);
      setReferenceRecipes(response.data);
    } catch (error) {
      console.error('Failed to fetch reference recipes:', error);
    }
    setLoading(false);
  };

  const fetchCountries = async () => {
    try {
      const response = await axios.get(`${API}/countries`);
      setCountries(response.data);
    } catch (error) {
      console.error('Failed to fetch countries:', error);
    }
  };

  const ReferenceRecipeCard = ({ recipe }) => (
    <div className="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-lg transition-shadow">
      <div className="p-6">
        <div className="flex items-start justify-between mb-3">
          <div>
            <h3 className="text-xl font-semibold text-gray-800">{recipe.name_english}</h3>
            {recipe.name_local !== recipe.name_english && (
              <p className="text-lg text-orange-600 font-medium">{recipe.name_local}</p>
            )}
          </div>
          <span className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full">
            {recipe.category}
          </span>
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
          <span className="text-sm text-gray-500">Popularity: {recipe.popularity_score}/100</span>
          <Link
            to={`/create-snippet?template=${recipe.id}`}
            className="bg-orange-500 hover:bg-orange-600 text-white px-4 py-2 rounded-md text-sm transition-colors"
          >
            Use This Template
          </Link>
        </div>
      </div>
    </div>
  );

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h2 className="text-3xl font-bold text-gray-800 mb-4">Traditional Recipe Templates</h2>
        <p className="text-gray-600 mb-6">Choose from authentic recipes around the world to create your own snippet</p>
        
        <div className="flex gap-4 mb-6">
          <select
            value={selectedCountry}
            onChange={(e) => setSelectedCountry(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
          >
            <option value="">All Countries</option>
            {countries.map(country => (
              <option key={country.id} value={country.code.toLowerCase()}>
                {country.name}
              </option>
            ))}
          </select>
        </div>
      </div>

      {loading ? (
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-500"></div>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {referenceRecipes.map(recipe => (
            <ReferenceRecipeCard key={recipe.id} recipe={recipe} />
          ))}
        </div>
      )}
    </div>
  );
};

// Create Snippet Page
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
      <div className="bg-white rounded-xl shadow-lg p-8">
        <h2 className="text-3xl font-bold text-gray-800 mb-6">Create Recipe Snippet</h2>
        
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
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
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
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
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
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Snippet Type</label>
              <select
                name="snippet_type"
                value={formData.snippet_type}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
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
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
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
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
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
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Difficulty Level</label>
              <select
                name="difficulty_level"
                value={formData.difficulty_level}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
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
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
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
                className="bg-orange-500 hover:bg-orange-600 text-white text-sm px-3 py-1 rounded transition-colors"
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
                    className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
                  />
                  <input
                    type="text"
                    placeholder="Amount"
                    value={ingredient.amount}
                    onChange={(e) => updateIngredient(index, 'amount', e.target.value)}
                    className="w-20 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
                  />
                  <input
                    type="text"
                    placeholder="Unit"
                    value={ingredient.unit}
                    onChange={(e) => updateIngredient(index, 'unit', e.target.value)}
                    className="w-20 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
                  />
                  <button
                    type="button"
                    onClick={() => removeIngredient(index)}
                    className="text-red-500 hover:text-red-700 p-2"
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
                className="bg-orange-500 hover:bg-orange-600 text-white text-sm px-3 py-1 rounded transition-colors"
              >
                + Add Step
              </button>
            </div>
            <div className="space-y-3">
              {formData.preparation_steps.map((step, index) => (
                <div key={index} className="flex gap-3 items-start">
                  <span className="bg-orange-500 text-white w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium mt-1">
                    {step.step_number}
                  </span>
                  <textarea
                    value={step.description}
                    onChange={(e) => updateStep(index, e.target.value)}
                    placeholder="Describe this preparation step..."
                    rows="2"
                    className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
                  />
                  <button
                    type="button"
                    onClick={() => removeStep(index)}
                    className="text-red-500 hover:text-red-700 p-2 mt-1"
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
              className="bg-orange-500 hover:bg-orange-600 disabled:bg-orange-300 text-white font-medium py-3 px-8 rounded-md transition-colors"
            >
              {submitting ? 'Creating Snippet...' : 'Create Snippet'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

// Grocery Search Page
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
        <h2 className="text-3xl font-bold text-gray-800 mb-4">Find Local Ingredients</h2>
        <p className="text-gray-600">Search for ingredients at nearby grocery stores and get pricing information</p>
      </div>

      <div className="bg-white rounded-xl shadow-lg p-8 mb-8">
        <h3 className="text-xl font-semibold text-gray-800 mb-4">Search Ingredients</h3>
        
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">Your Postal Code</label>
          <input
            type="text"
            value={postalCode}
            onChange={(e) => setPostalCode(e.target.value)}
            placeholder="Enter your postal code"
            className="w-full md:w-64 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
          />
        </div>

        <div className="mb-6">
          <div className="flex items-center justify-between mb-3">
            <label className="block text-sm font-medium text-gray-700">Ingredients</label>
            <button
              type="button"
              onClick={addIngredient}
              className="bg-orange-500 hover:bg-orange-600 text-white text-sm px-3 py-1 rounded transition-colors"
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
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
                />
                {ingredients.length > 1 && (
                  <button
                    type="button"
                    onClick={() => removeIngredient(index)}
                    className="text-red-500 hover:text-red-700 p-2"
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
          className="bg-orange-500 hover:bg-orange-600 disabled:bg-orange-300 text-white font-medium py-2 px-6 rounded-md transition-colors"
        >
          {loading ? 'Searching...' : 'Find Stores & Prices'}
        </button>
      </div>

      {searchResults && (
        <div className="space-y-6">
          <div className="bg-white rounded-xl shadow-lg p-8">
            <h3 className="text-xl font-semibold text-gray-800 mb-4">Nearby Grocery Stores</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {searchResults.stores.map((store, index) => (
                <div key={index} className={`border rounded-lg p-4 ${store.id === searchResults.recommended_store_id ? 'border-green-500 bg-green-50' : 'border-gray-200'}`}>
                  {store.id === searchResults.recommended_store_id && (
                    <span className="bg-green-500 text-white text-xs px-2 py-1 rounded-full mb-2 inline-block">
                      Recommended
                    </span>
                  )}
                  <h4 className="font-semibold text-gray-800">{store.name}</h4>
                  <p className="text-sm text-gray-600">{store.chain}</p>
                  <p className="text-sm text-gray-600">{store.address}</p>
                  <div className="mt-2 flex justify-between items-center">
                    <span className="text-sm text-gray-500">{store.distance_km} km away</span>
                    <span className="font-semibold text-green-600">${store.estimated_total}</span>
                  </div>
                  {store.supports_delivery && (
                    <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded mt-2 inline-block">
                      Delivery Available
                    </span>
                  )}
                </div>
              ))}
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-8">
            <h3 className="text-xl font-semibold text-gray-800 mb-4">Ingredient Availability & Pricing</h3>
            <div className="space-y-4">
              {Object.entries(searchResults.ingredient_availability).map(([ingredient, stores]) => (
                <div key={ingredient} className="border-b pb-4">
                  <h4 className="font-medium text-gray-800 mb-2 capitalize">{ingredient}</h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                    {stores.map((item, index) => (
                      <div key={index} className="bg-gray-50 rounded p-3">
                        <div className="flex justify-between items-center">
                          <span className="text-sm font-medium">{item.brand}</span>
                          <span className="font-semibold text-green-600">${item.price}</span>
                        </div>
                        <div className="text-xs text-gray-500">
                          {item.package_size} • {item.in_stock ? 'In Stock' : 'Out of Stock'}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-8">
            <h3 className="text-xl font-semibold text-gray-800 mb-4">Order Options</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {searchResults.delivery_options.map((option, index) => (
                <div key={index} className="border rounded-lg p-4">
                  <h4 className="font-semibold text-gray-800 capitalize">{option.type}</h4>
                  <p className="text-gray-600">{option.time_estimate}</p>
                  <p className="font-semibold text-green-600">
                    {option.fee === 0 ? 'Free' : `$${option.fee} fee`}
                  </p>
                </div>
              ))}
            </div>
            <div className="mt-4 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
              <p className="text-sm text-yellow-800">
                <strong>💰 Revenue Opportunity:</strong> Lambalia earns a small commission from partner stores when you shop through our platform, helping us keep the service free for users!
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

// Enhanced Profile Page with Snippets Playlist
const ProfilePage = () => {
  const { user } = useAuth();
  const [userSnippets, setUserSnippets] = useState([]);
  const [loading, setLoading] = useState(true);

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
    <div className="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-lg transition-shadow">
      <div className="p-6">
        <div className="flex items-start justify-between mb-3">
          <div className="flex items-center space-x-3">
            <span className="bg-orange-500 text-white w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold">
              {playlistIndex + 1}
            </span>
            <div>
              <h3 className="text-lg font-semibold text-gray-800">{snippet.title}</h3>
              {snippet.title_local && (
                <p className="text-orange-600 font-medium">{snippet.title_local}</p>
              )}
            </div>
          </div>
          <span className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full">
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
        
        <div className="mb-3">
          <h4 className="font-medium text-gray-800 mb-2">Ingredients:</h4>
          <div className="text-sm text-gray-600 space-y-1">
            {snippet.ingredients.slice(0, 3).map((ingredient, index) => (
              <div key={index}>• {ingredient.amount} {ingredient.unit} {ingredient.name}</div>
            ))}
            {snippet.ingredients.length > 3 && (
              <div className="text-gray-400">... and {snippet.ingredients.length - 3} more</div>
            )}
          </div>
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

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="bg-white rounded-xl shadow-lg p-8 mb-8">
        <div className="flex items-center space-x-6">
          <div className="w-24 h-24 bg-gradient-to-r from-orange-400 to-red-500 rounded-full flex items-center justify-center">
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
              <span><strong>{user.credits}</strong> Credits</span>
            </div>
          </div>
        </div>
      </div>

      <div className="mb-6">
        <div className="flex items-center justify-between">
          <h2 className="text-2xl font-bold text-gray-800">My Recipe Snippets Playlist</h2>
          <Link
            to="/create-snippet"
            className="bg-orange-500 hover:bg-orange-600 text-white px-4 py-2 rounded-md transition-colors"
          >
            Create New Snippet
          </Link>
        </div>
        <p className="text-gray-600 mt-2">Your snippets are displayed in playlist order for easy viewing</p>
      </div>
      
      {loading ? (
        <div className="flex justify-center items-center h-32">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-orange-500"></div>
        </div>
      ) : userSnippets.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-500 mb-4">You haven't created any snippets yet.</p>
          <Link
            to="/create-snippet"
            className="bg-orange-500 hover:bg-orange-600 text-white px-6 py-2 rounded-md transition-colors"
          >
            Create Your First Snippet
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {userSnippets.map((snippet, index) => (
            <SnippetCard key={snippet.id} snippet={snippet} playlistIndex={index} />
          ))}
        </div>
      )}
    </div>
  );
};

// Enhanced Home Page with Snippets
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
    <div className="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-lg transition-shadow">
      <div className="p-6">
        <div className="flex items-start justify-between mb-3">
          <div>
            <h3 className="text-lg font-semibold text-gray-800">{snippet.title}</h3>
            {snippet.title_local && (
              <p className="text-orange-600 font-medium">{snippet.title_local}</p>
            )}
            <p className="text-sm text-gray-500">by @{snippet.author_username}</p>
          </div>
          <span className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full">
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
        <h2 className="text-3xl font-bold text-gray-800 mb-4">Discover Traditional Recipes</h2>
        <p className="text-gray-600 mb-6">Explore authentic culinary treasures from every corner of the world</p>
        
        <div className="flex flex-wrap gap-4">
          <Link
            to="/templates"
            className="bg-orange-500 hover:bg-orange-600 text-white px-6 py-2 rounded-md transition-colors"
          >
            Browse Recipe Templates
          </Link>
          <Link
            to="/create-snippet"
            className="bg-green-500 hover:bg-green-600 text-white px-6 py-2 rounded-md transition-colors"
          >
            Create Your Snippet
          </Link>
          <Link
            to="/grocery"
            className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded-md transition-colors"
          >
            Find Local Ingredients
          </Link>
        </div>
      </div>

      {loading ? (
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-500"></div>
        </div>
      ) : snippets.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-500 text-lg">No recipe snippets found. Be the first to share your traditional recipe snippet on Lambalia!</p>
        </div>
      ) : (
        <div>
          <h3 className="text-xl font-semibold text-gray-800 mb-6">Latest Recipe Snippets</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {snippets.map(snippet => (
              <SnippetCard key={snippet.id} snippet={snippet} />
            ))}
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
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-500"></div>
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