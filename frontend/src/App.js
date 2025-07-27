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
    preferred_language: 'en'
  });
  const { login, register } = useAuth();
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    
    const result = await login(email, password);
    if (result.success) {
      navigate('/');
    } else {
      setError(result.error);
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setError('');
    
    const result = await register(formData);
    if (result.success) {
      navigate('/');
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
          <h1 className="text-3xl font-bold text-gray-800">CulinaryConnect</h1>
          <p className="text-gray-600 mt-2">Share traditional recipes from around the world</p>
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
              Register
            </button>
          </form>
        )}

        <div className="text-center mt-6">
          <p className="text-sm text-gray-600">
            Join our community of food lovers sharing authentic recipes!
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
          <Link to="/" className="flex items-center">
            <h1 className="text-2xl font-bold text-orange-600">CulinaryConnect</h1>
          </Link>
          
          <nav className="flex items-center space-x-4">
            <Link to="/" className="text-gray-700 hover:text-orange-600 px-3 py-2 rounded-md">
              Home
            </Link>
            <Link to="/create" className="text-gray-700 hover:text-orange-600 px-3 py-2 rounded-md">
              Create Recipe
            </Link>
            <Link to="/profile" className="text-gray-700 hover:text-orange-600 px-3 py-2 rounded-md">
              Profile
            </Link>
            
            <div className="flex items-center space-x-3 ml-4 pl-4 border-l">
              <span className="text-sm text-gray-600">
                Welcome, {user?.username || 'User'}
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

// Recipe Card Component
const RecipeCard = ({ recipe, onLike }) => {
  const [liked, setLiked] = useState(false);
  const [likesCount, setLikesCount] = useState(recipe.likes_count);

  const handleLike = async () => {
    try {
      const response = await axios.post(`${API}/recipes/${recipe.id}/like`);
      setLiked(response.data.liked);
      setLikesCount(prev => response.data.liked ? prev + 1 : prev - 1);
    } catch (error) {
      console.error('Failed to like recipe:', error);
    }
  };

  const handlePurchase = async () => {
    try {
      const response = await axios.post(`${API}/recipes/${recipe.id}/purchase`);
      alert(response.data.message);
      // Refresh the recipe to show ingredients
      window.location.reload();
    } catch (error) {
      alert(error.response?.data?.detail || 'Failed to purchase recipe');
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-lg transition-shadow">
      {recipe.main_image && (
        <img 
          src={recipe.main_image} 
          alt={recipe.title}
          className="w-full h-48 object-cover"
        />
      )}
      
      <div className="p-6">
        <div className="flex items-start justify-between mb-3">
          <h3 className="text-xl font-semibold text-gray-800 line-clamp-2">{recipe.title}</h3>
          {recipe.is_premium && !recipe.is_purchased && (
            <span className="bg-yellow-100 text-yellow-800 text-xs px-2 py-1 rounded-full">
              Premium
            </span>
          )}
        </div>
        
        <p className="text-gray-600 mb-3 line-clamp-3">{recipe.description}</p>
        
        <div className="flex items-center text-sm text-gray-500 mb-3">
          <span>By {recipe.author_username}</span>
          {recipe.cooking_time_minutes && (
            <>
              <span className="mx-2">•</span>
              <span>{recipe.cooking_time_minutes} min</span>
            </>
          )}
          {recipe.difficulty_level && (
            <>
              <span className="mx-2">•</span>
              <span>{'★'.repeat(recipe.difficulty_level)}</span>
            </>
          )}
        </div>
        
        {recipe.dietary_preferences?.length > 0 && (
          <div className="flex flex-wrap gap-1 mb-3">
            {recipe.dietary_preferences.map((pref, index) => (
              <span key={index} className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded-full">
                {pref.replace('_', ' ')}
              </span>
            ))}
          </div>
        )}
        
        {recipe.is_premium && !recipe.is_purchased ? (
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3 mb-4">
            <p className="text-sm text-yellow-800 mb-2">
              Ingredients are hidden. Purchase to unlock full recipe!
            </p>
            <button
              onClick={handlePurchase}
              className="bg-yellow-500 hover:bg-yellow-600 text-white text-sm px-3 py-1 rounded transition-colors"
            >
              Unlock for {recipe.premium_price} credits
            </button>
          </div>
        ) : recipe.ingredients && (
          <div className="mb-4">
            <h4 className="font-medium text-gray-800 mb-2">Ingredients:</h4>
            <ul className="text-sm text-gray-600 space-y-1">
              {recipe.ingredients.slice(0, 3).map((ingredient, index) => (
                <li key={index}>• {ingredient.amount} {ingredient.unit} {ingredient.name}</li>
              ))}
              {recipe.ingredients.length > 3 && (
                <li className="text-gray-400">... and {recipe.ingredients.length - 3} more</li>
              )}
            </ul>
          </div>
        )}
        
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4 text-sm text-gray-500">
            <button
              onClick={handleLike}
              className={`flex items-center space-x-1 hover:text-red-500 transition-colors ${
                liked ? 'text-red-500' : ''
              }`}
            >
              <span>{liked ? '❤️' : '🤍'}</span>
              <span>{likesCount}</span>
            </button>
            <span>💬 {recipe.comments_count}</span>
            <span>👁 {recipe.views_count}</span>
          </div>
          
          <Link
            to={`/recipe/${recipe.id}`}
            className="text-orange-600 hover:text-orange-700 font-medium text-sm"
          >
            View Recipe →
          </Link>
        </div>
      </div>
    </div>
  );
};

// Home Page Component
const HomePage = () => {
  const [recipes, setRecipes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState({
    country_id: '',
    cuisine_type: '',
    dietary_preference: ''
  });

  useEffect(() => {
    fetchRecipes();
  }, [filter]);

  const fetchRecipes = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (filter.country_id) params.append('country_id', filter.country_id);
      if (filter.cuisine_type) params.append('cuisine_type', filter.cuisine_type);
      if (filter.dietary_preference) params.append('dietary_preference', filter.dietary_preference);
      
      const response = await axios.get(`${API}/recipes?${params}`);
      setRecipes(response.data);
    } catch (error) {
      console.error('Failed to fetch recipes:', error);
    }
    setLoading(false);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h2 className="text-3xl font-bold text-gray-800 mb-4">Discover Traditional Recipes</h2>
        
        {/* Filters */}
        <div className="flex flex-wrap gap-4 mb-6">
          <select
            value={filter.dietary_preference}
            onChange={(e) => setFilter({...filter, dietary_preference: e.target.value})}
            className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
          >
            <option value="">All Diets</option>
            <option value="vegetarian">Vegetarian</option>
            <option value="vegan">Vegan</option>
            <option value="gluten_free">Gluten Free</option>
            <option value="organic">Organic</option>
          </select>
          
          <input
            type="text"
            placeholder="Cuisine type (e.g., Italian, Mexican)"
            value={filter.cuisine_type}
            onChange={(e) => setFilter({...filter, cuisine_type: e.target.value})}
            className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
          />
        </div>
      </div>

      {loading ? (
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-500"></div>
        </div>
      ) : recipes.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-500 text-lg">No recipes found. Be the first to share a traditional recipe!</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {recipes.map(recipe => (
            <RecipeCard key={recipe.id} recipe={recipe} />
          ))}
        </div>
      )}
    </div>
  );
};

// Create Recipe Component
const CreateRecipePage = () => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    ingredients: [{ name: '', amount: '', unit: '' }],
    steps: [{ step_number: 1, description: '' }],
    cooking_time_minutes: '',
    difficulty_level: 3,
    servings: '',
    cuisine_type: '',
    dietary_preferences: [],
    tags: [],
    is_premium: false,
    premium_price: 0
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
      steps: [...prev.steps, { step_number: prev.steps.length + 1, description: '' }]
    }));
  };

  const updateStep = (index, value) => {
    setFormData(prev => ({
      ...prev,
      steps: prev.steps.map((step, i) => 
        i === index ? { ...step, description: value } : step
      )
    }));
  };

  const removeStep = (index) => {
    setFormData(prev => ({
      ...prev,
      steps: prev.steps.filter((_, i) => i !== index).map((step, i) => ({
        ...step,
        step_number: i + 1
      }))
    }));
  };

  const handleDietaryPreferenceChange = (pref) => {
    setFormData(prev => ({
      ...prev,
      dietary_preferences: prev.dietary_preferences.includes(pref)
        ? prev.dietary_preferences.filter(p => p !== pref)
        : [...prev.dietary_preferences, pref]
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);

    try {
      const submitData = {
        ...formData,
        cooking_time_minutes: formData.cooking_time_minutes ? parseInt(formData.cooking_time_minutes) : null,
        servings: formData.servings ? parseInt(formData.servings) : null,
        ingredients: formData.ingredients.filter(ing => ing.name.trim()),
        steps: formData.steps.filter(step => step.description.trim())
      };

      await axios.post(`${API}/recipes`, submitData);
      navigate('/');
    } catch (error) {
      console.error('Failed to create recipe:', error);
      alert('Failed to create recipe. Please try again.');
    }
    setSubmitting(false);
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="bg-white rounded-xl shadow-lg p-8">
        <h2 className="text-3xl font-bold text-gray-800 mb-6">Share Your Traditional Recipe</h2>
        
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Basic Info */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Recipe Title *</label>
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
              <label className="block text-sm font-medium text-gray-700 mb-2">Cuisine Type</label>
              <input
                type="text"
                name="cuisine_type"
                value={formData.cuisine_type}
                onChange={handleInputChange}
                placeholder="e.g., Italian, Mexican, Thai"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Description *</label>
            <textarea
              name="description"
              value={formData.description}
              onChange={handleInputChange}
              rows="4"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
              placeholder="Tell us about this traditional recipe, its origin, and what makes it special..."
              required
            />
          </div>

          {/* Recipe Details */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Cooking Time (minutes)</label>
              <input
                type="number"
                name="cooking_time_minutes"
                value={formData.cooking_time_minutes}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Servings</label>
              <input
                type="number"
                name="servings"
                value={formData.servings}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
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

          {/* Dietary Preferences */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Dietary Preferences</label>
            <div className="flex flex-wrap gap-2">
              {['vegetarian', 'vegan', 'gluten_free', 'keto', 'paleo', 'organic'].map(pref => (
                <label key={pref} className="flex items-center">
                  <input
                    type="checkbox"
                    checked={formData.dietary_preferences.includes(pref)}
                    onChange={() => handleDietaryPreferenceChange(pref)}
                    className="mr-2"
                  />
                  <span className="text-sm capitalize">{pref.replace('_', ' ')}</span>
                </label>
              ))}
            </div>
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

          {/* Steps */}
          <div>
            <div className="flex items-center justify-between mb-3">
              <label className="block text-sm font-medium text-gray-700">Cooking Steps *</label>
              <button
                type="button"
                onClick={addStep}
                className="bg-orange-500 hover:bg-orange-600 text-white text-sm px-3 py-1 rounded transition-colors"
              >
                + Add Step
              </button>
            </div>
            <div className="space-y-3">
              {formData.steps.map((step, index) => (
                <div key={index} className="flex gap-3 items-start">
                  <span className="bg-orange-500 text-white w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium mt-1">
                    {step.step_number}
                  </span>
                  <textarea
                    value={step.description}
                    onChange={(e) => updateStep(index, e.target.value)}
                    placeholder="Describe this cooking step..."
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

          {/* Premium Options */}
          <div className="border-t pt-6">
            <div className="flex items-center mb-4">
              <input
                type="checkbox"
                name="is_premium"
                checked={formData.is_premium}
                onChange={handleInputChange}
                className="mr-3"
              />
              <label className="text-sm font-medium text-gray-700">
                Make this a premium recipe (hide ingredients until purchased)
              </label>
            </div>
            
            {formData.is_premium && (
              <div className="ml-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">Price (credits)</label>
                <input
                  type="number"
                  name="premium_price"
                  value={formData.premium_price}
                  onChange={handleInputChange}
                  step="0.1"
                  min="0"
                  className="w-32 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
                />
              </div>
            )}
          </div>

          {/* Submit */}
          <div className="flex justify-end pt-6">
            <button
              type="submit"
              disabled={submitting}
              className="bg-orange-500 hover:bg-orange-600 disabled:bg-orange-300 text-white font-medium py-3 px-8 rounded-md transition-colors"
            >
              {submitting ? 'Sharing Recipe...' : 'Share Recipe'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

// Profile Page Component
const ProfilePage = () => {
  const { user } = useAuth();
  const [userRecipes, setUserRecipes] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (user) {
      fetchUserRecipes();
    }
  }, [user]);

  const fetchUserRecipes = async () => {
    setLoading(true);
    try {
      // This would need a new endpoint to get recipes by user
      const response = await axios.get(`${API}/recipes`);
      // Filter by current user (temporary solution)
      const filteredRecipes = response.data.filter(recipe => recipe.author_id === user.id);
      setUserRecipes(filteredRecipes);
    } catch (error) {
      console.error('Failed to fetch user recipes:', error);
    }
    setLoading(false);
  };

  if (!user) return null;

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
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
              <span><strong>{user.recipes_count}</strong> Recipes</span>
              <span><strong>{user.followers_count}</strong> Followers</span>
              <span><strong>{user.following_count}</strong> Following</span>
              <span><strong>{user.credits}</strong> Credits</span>
            </div>
          </div>
        </div>
      </div>

      <div>
        <h2 className="text-2xl font-bold text-gray-800 mb-6">My Recipes</h2>
        
        {loading ? (
          <div className="flex justify-center items-center h-32">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-orange-500"></div>
          </div>
        ) : userRecipes.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-500 mb-4">You haven't shared any recipes yet.</p>
            <Link
              to="/create"
              className="bg-orange-500 hover:bg-orange-600 text-white px-6 py-2 rounded-md transition-colors"
            >
              Share Your First Recipe
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {userRecipes.map(recipe => (
              <RecipeCard key={recipe.id} recipe={recipe} />
            ))}
          </div>
        )}
      </div>
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
              path="/create" 
              element={
                <ProtectedRoute>
                  <>
                    <Header />
                    <CreateRecipePage />
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