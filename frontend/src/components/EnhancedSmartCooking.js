// Enhanced Smart Cooking Tool - SuperCook Style + HackTheMenu Integration
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

const EnhancedSmartCooking = ({ user, onClose }) => {
  const [currentView, setCurrentView] = useState('pantry'); // pantry, recipes, fastfood, ai
  const [pantry, setPantry] = useState({ ingredients: [], ingredient_count: 0 });
  const [newIngredient, setNewIngredient] = useState('');
  const [ingredientSuggestions, setIngredientSuggestions] = useState([]);
  const [recipes, setRecipes] = useState([]);
  const [fastfoodItems, setFastfoodItems] = useState([]);
  const [secretMenuItems, setSecretMenuItems] = useState([]);
  const [maxMissing, setMaxMissing] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [selectedRestaurant, setSelectedRestaurant] = useState('');
  const [restaurants, setRestaurants] = useState([]);

  useEffect(() => {
    initializePantry();
    loadRestaurants();
  }, []);

  const initializePantry = async () => {
    try {
      const response = await axios.get(`${BACKEND_URL}/api/enhanced-cooking/pantry`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      
      if (response.data.success) {
        setPantry(response.data.pantry);
      } else {
        // Create new pantry if none exists
        await axios.post(`${BACKEND_URL}/api/enhanced-cooking/pantry/create`, 
          { pantry_name: "My Kitchen" },
          { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }}
        );
        setPantry({ ingredients: [], ingredient_count: 0 });
      }
    } catch (error) {
      console.error('Failed to initialize pantry:', error);
    }
  };

  const loadRestaurants = async () => {
    try {
      const response = await axios.get(`${BACKEND_URL}/api/enhanced-cooking/fastfood/restaurants`);
      if (response.data.success) {
        setRestaurants(response.data.restaurants);
      }
    } catch (error) {
      console.error('Failed to load restaurants:', error);
    }
  };

  const handleIngredientSearch = async (query) => {
    if (query.length < 2) {
      setIngredientSuggestions([]);
      return;
    }

    try {
      const response = await axios.get(`${BACKEND_URL}/api/enhanced-cooking/ingredients/suggestions?query=${query}`);
      setIngredientSuggestions(response.data.suggestions || []);
    } catch (error) {
      console.error('Ingredient search failed:', error);
    }
  };

  const addIngredient = async (ingredient) => {
    if (!ingredient.trim()) return;

    try {
      const response = await axios.post(
        `${BACKEND_URL}/api/enhanced-cooking/pantry/add-ingredients`,
        { ingredients: [ingredient] },
        { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }}
      );

      if (response.data.success) {
        await initializePantry(); // Refresh pantry
        setNewIngredient('');
        setIngredientSuggestions([]);
      }
    } catch (error) {
      setError('Failed to add ingredient. Please try again.');
    }
  };

  const removeIngredient = async (ingredient) => {
    try {
      const response = await axios.post(
        `${BACKEND_URL}/api/enhanced-cooking/pantry/remove-ingredients`,
        { ingredients: [ingredient] },
        { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }}
      );

      if (response.data.success) {
        await initializePantry();
      }
    } catch (error) {
      setError('Failed to remove ingredient.');
    }
  };

  const findRecipes = async () => {
    setLoading(true);
    try {
      const response = await axios.get(
        `${BACKEND_URL}/api/enhanced-cooking/recipes/find?max_missing=${maxMissing}`,
        { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }}
      );

      if (response.data.success) {
        setRecipes(response.data.recipes);
        setCurrentView('recipes');
      } else {
        setError(response.data.error || 'No recipes found');
      }
    } catch (error) {
      setError('Failed to find recipes. Please try again.');
    }
    setLoading(false);
  };

  const loadFastFoodItems = async (restaurant) => {
    setLoading(true);
    try {
      const response = await axios.get(`${BACKEND_URL}/api/enhanced-cooking/recipes/fastfood/${restaurant}`);
      if (response.data.success) {
        setFastfoodItems(response.data.items);
        setSelectedRestaurant(restaurant);
      }
    } catch (error) {
      setError('Failed to load fast food items.');
    }
    setLoading(false);
  };

  const loadSecretMenu = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${BACKEND_URL}/api/enhanced-cooking/recipes/secret-menu`);
      if (response.data.success) {
        setSecretMenuItems(response.data.secret_menu_items);
      }
    } catch (error) {
      setError('Failed to load secret menu items.');
    }
    setLoading(false);
  };

  const generateAIRecipe = async () => {
    if (pantry.ingredient_count < 3) {
      setError('Please add at least 3 ingredients for AI recipe generation.');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post(
        `${BACKEND_URL}/api/enhanced-cooking/recipes/generate-ai`,
        {},
        { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }}
      );

      if (response.data.success) {
        setRecipes(response.data.ai_recipes);
        setCurrentView('recipes');
      }
    } catch (error) {
      setError('AI recipe generation failed. Please try again.');
    }
    setLoading(false);
  };

  const renderPantryView = () => (
    <div className="space-y-6">
      {/* Header */}
      <div className="text-center">
        <h2 className="text-2xl font-bold text-gray-800 mb-2">🥘 My Virtual Pantry</h2>
        <p className="text-gray-600">Add ingredients you have at home (SuperCook style)</p>
      </div>

      {/* Add Ingredient */}
      <div className="bg-white p-6 rounded-xl shadow-lg">
        <h3 className="text-lg font-semibold mb-4">Add Ingredients</h3>
        <div className="relative">
          <input
            type="text"
            value={newIngredient}
            onChange={(e) => {
              setNewIngredient(e.target.value);
              handleIngredientSearch(e.target.value);
            }}
            placeholder="Start typing an ingredient (e.g. chicken, rice, tomato)..."
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
            onKeyPress={(e) => e.key === 'Enter' && addIngredient(newIngredient)}
          />
          
          {/* Ingredient Suggestions */}
          {ingredientSuggestions.length > 0 && (
            <div className="absolute z-10 w-full mt-1 bg-white border border-gray-300 rounded-lg shadow-lg max-h-60 overflow-y-auto">
              {ingredientSuggestions.map((suggestion, index) => (
                <div
                  key={index}
                  onClick={() => addIngredient(suggestion.name)}
                  className="px-4 py-3 hover:bg-gray-50 cursor-pointer border-b border-gray-100 last:border-b-0"
                >
                  <div className="font-medium">{suggestion.name}</div>
                  <div className="text-sm text-gray-500">
                    Category: {suggestion.category} 
                    {suggestion.common_names.length > 0 && ` • Also known as: ${suggestion.common_names.join(', ')}`}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
        
        <button
          onClick={() => addIngredient(newIngredient)}
          className="mt-3 px-6 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors"
        >
          Add Ingredient
        </button>
      </div>

      {/* Current Pantry */}
      <div className="bg-white p-6 rounded-xl shadow-lg">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-semibold">Your Ingredients ({pantry.ingredient_count})</h3>
          <div className="text-sm text-gray-500">
            {pantry.ingredient_count === 0 ? 'Add ingredients to get started' : 'Ready to find recipes!'}
          </div>
        </div>
        
        {pantry.ingredients && pantry.ingredients.length > 0 ? (
          <div className="flex flex-wrap gap-2">
            {pantry.ingredients.map((ingredient, index) => (
              <span
                key={index}
                className="inline-flex items-center px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm"
              >
                {ingredient}
                <button
                  onClick={() => removeIngredient(ingredient)}
                  className="ml-2 text-green-600 hover:text-green-800"
                >
                  ×
                </button>
              </span>
            ))}
          </div>
        ) : (
          <p className="text-gray-500 text-center py-8">
            No ingredients yet. Add some to start finding recipes! 🥕🍅🥖
          </p>
        )}
      </div>

      {/* Recipe Search Options */}
      {pantry.ingredient_count > 0 && (
        <div className="bg-white p-6 rounded-xl shadow-lg">
          <h3 className="text-lg font-semibold mb-4">Find Recipes</h3>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Missing Ingredients Tolerance
              </label>
              <select
                value={maxMissing}
                onChange={(e) => setMaxMissing(parseInt(e.target.value))}
                className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
              >
                <option value={0}>Use only my ingredients (0 missing)</option>
                <option value={1}>Allow 1 missing ingredient</option>
                <option value={2}>Allow 2 missing ingredients</option>
                <option value={3}>Allow 3 missing ingredients</option>
              </select>
            </div>
            
            <div className="flex space-x-3">
              <button
                onClick={findRecipes}
                disabled={loading}
                className="flex-1 bg-green-500 text-white py-3 px-4 rounded-lg hover:bg-green-600 transition-colors disabled:opacity-50"
              >
                {loading ? 'Searching...' : '🔍 Find Recipes'}
              </button>
              
              <button
                onClick={generateAIRecipe}
                disabled={loading || pantry.ingredient_count < 3}
                className="flex-1 bg-purple-500 text-white py-3 px-4 rounded-lg hover:bg-purple-600 transition-colors disabled:opacity-50"
              >
                {loading ? 'Generating...' : '🤖 AI Recipe'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );

  const renderRecipesView = () => (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-800">🍳 Recipe Results</h2>
        <button
          onClick={() => setCurrentView('pantry')}
          className="px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition-colors"
        >
          Back to Pantry
        </button>
      </div>

      {recipes.length === 0 ? (
        <div className="text-center py-12 bg-white rounded-xl shadow-lg">
          <div className="text-6xl mb-4">🍽️</div>
          <h3 className="text-xl font-medium text-gray-600 mb-2">No recipes found</h3>
          <p className="text-gray-500">Try adding more ingredients or allowing missing ingredients.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {recipes.map((recipe, index) => (
            <div key={index} className="bg-white p-6 rounded-xl shadow-lg">
              <div className="flex justify-between items-start mb-4">
                <h3 className="text-lg font-semibold text-gray-800">{recipe.name}</h3>
                <div className="text-right text-sm text-gray-500">
                  <div>{recipe.prep_time + recipe.cook_time} min total</div>
                  <div>{recipe.servings} servings</div>
                </div>
              </div>

              {recipe.source && (
                <div className="mb-3">
                  <span className={`px-2 py-1 rounded-full text-xs ${
                    recipe.source === 'hackthemenu' ? 'bg-red-100 text-red-800' :
                    recipe.source === 'lambalia_ai' ? 'bg-purple-100 text-purple-800' :
                    'bg-blue-100 text-blue-800'
                  }`}>
                    {recipe.source === 'hackthemenu' ? '🍟 Fast Food Clone' :
                     recipe.source === 'lambalia_ai' ? '🤖 AI Generated' :
                     '👨‍🍳 SuperCook Style'}
                  </span>
                  {recipe.is_secret_menu && (
                    <span className="ml-2 px-2 py-1 bg-yellow-100 text-yellow-800 rounded-full text-xs">
                      🤫 Secret Menu
                    </span>
                  )}
                </div>
              )}

              <div className="mb-4">
                <h4 className="font-medium text-gray-700 mb-2">Ingredients Used:</h4>
                <div className="flex flex-wrap gap-1">
                  {recipe.ingredients_used.map((ingredient, idx) => (
                    <span key={idx} className="px-2 py-1 bg-green-100 text-green-800 rounded text-xs">
                      {ingredient}
                    </span>
                  ))}
                </div>
              </div>

              {recipe.missing_ingredients && recipe.missing_ingredients.length > 0 && (
                <div className="mb-4">
                  <h4 className="font-medium text-orange-700 mb-2">Missing Ingredients:</h4>
                  <div className="flex flex-wrap gap-1">
                    {recipe.missing_ingredients.map((ingredient, idx) => (
                      <span key={idx} className="px-2 py-1 bg-orange-100 text-orange-800 rounded text-xs">
                        {ingredient}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              <div className="mb-4">
                <h4 className="font-medium text-gray-700 mb-2">Instructions:</h4>
                <ol className="text-sm text-gray-600 space-y-1">
                  {recipe.instructions.map((step, idx) => (
                    <li key={idx} className="flex">
                      <span className="font-medium mr-2">{idx + 1}.</span>
                      <span>{step}</span>
                    </li>
                  ))}
                </ol>
              </div>

              {recipe.fast_food_restaurant && (
                <div className="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
                  <p className="text-sm text-yellow-700">
                    <strong>🍟 {recipe.fast_food_restaurant} Clone:</strong> Recreate your favorite fast food at home!
                  </p>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );

  const renderFastFoodView = () => (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-800">🍟 Fast Food Clones</h2>
        <button
          onClick={() => setCurrentView('pantry')}
          className="px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition-colors"
        >
          Back to Pantry
        </button>
      </div>

      {/* Restaurant Selection */}
      <div className="bg-white p-6 rounded-xl shadow-lg">
        <h3 className="text-lg font-semibold mb-4">Choose Restaurant</h3>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
          {restaurants.map((restaurant, index) => (
            <button
              key={index}
              onClick={() => loadFastFoodItems(restaurant.name)}
              className={`p-4 border-2 rounded-lg text-center transition-colors ${
                selectedRestaurant === restaurant.name
                  ? 'border-red-500 bg-red-50'
                  : 'border-gray-300 hover:border-red-300'
              }`}
            >
              <div className="font-medium">{restaurant.name}</div>
              <div className="text-sm text-gray-500">{restaurant.items_available} items</div>
              <div className="text-xs text-orange-600">{restaurant.secret_menu_items} secret</div>
            </button>
          ))}
        </div>

        <button
          onClick={loadSecretMenu}
          className="mt-4 w-full bg-yellow-500 text-white py-3 px-4 rounded-lg hover:bg-yellow-600 transition-colors"
        >
          🤫 View All Secret Menu Items
        </button>
      </div>

      {/* Fast Food Items */}
      {(fastfoodItems.length > 0 || secretMenuItems.length > 0) && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {(secretMenuItems.length > 0 ? secretMenuItems : fastfoodItems).map((item, index) => (
            <div key={index} className="bg-white p-6 rounded-xl shadow-lg">
              <div className="flex justify-between items-start mb-4">
                <h3 className="text-lg font-semibold text-gray-800">{item.name}</h3>
                <div className="text-right">
                  <div className="text-sm font-medium text-red-600">{item.restaurant}</div>
                  {item.is_secret_menu && (
                    <div className="text-xs bg-yellow-100 text-yellow-800 px-2 py-1 rounded mt-1">
                      Secret Menu
                    </div>
                  )}
                </div>
              </div>

              <div className="mb-4">
                <h4 className="font-medium text-gray-700 mb-2">Ingredients Needed:</h4>
                <div className="flex flex-wrap gap-1">
                  {item.ingredients.map((ingredient, idx) => (
                    <span
                      key={idx}
                      className={`px-2 py-1 rounded text-xs ${
                        pantry.ingredients && pantry.ingredients.includes(ingredient.toLowerCase())
                          ? 'bg-green-100 text-green-800'
                          : 'bg-gray-100 text-gray-700'
                      }`}
                    >
                      {ingredient}
                      {pantry.ingredients && pantry.ingredients.includes(ingredient.toLowerCase()) && ' ✓'}
                    </span>
                  ))}
                </div>
              </div>

              <div className="mb-4">
                <h4 className="font-medium text-gray-700 mb-2">Instructions:</h4>
                <p className="text-sm text-gray-600">{item.instructions}</p>
              </div>

              {item.popularity_score > 0 && (
                <div className="text-xs text-orange-600">
                  Popularity: {item.popularity_score}/100
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-gray-50 rounded-xl max-w-6xl w-full max-h-[90vh] overflow-hidden">
        {/* Header */}
        <div className="bg-white px-6 py-4 border-b border-gray-200 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-800">
            🍳 Enhanced Smart Cooking Tool
          </h1>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 text-2xl"
          >
            ×
          </button>
        </div>

        {/* Navigation */}
        <div className="bg-white px-6 py-3 border-b border-gray-200">
          <div className="flex space-x-4">
            <button
              onClick={() => setCurrentView('pantry')}
              className={`px-4 py-2 rounded-lg transition-colors ${
                currentView === 'pantry'
                  ? 'bg-green-500 text-white'
                  : 'text-gray-600 hover:text-green-600'
              }`}
            >
              🥘 My Pantry
            </button>
            <button
              onClick={() => setCurrentView('fastfood')}
              className={`px-4 py-2 rounded-lg transition-colors ${
                currentView === 'fastfood'
                  ? 'bg-red-500 text-white'
                  : 'text-gray-600 hover:text-red-600'
              }`}
            >
              🍟 Fast Food Clones
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="p-6 overflow-y-auto max-h-[calc(90vh-140px)]">
          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
              {error}
              <button
                onClick={() => setError('')}
                className="float-right font-bold"
              >
                ×
              </button>
            </div>
          )}

          {currentView === 'pantry' && renderPantryView()}
          {currentView === 'recipes' && renderRecipesView()}
          {currentView === 'fastfood' && renderFastFoodView()}
        </div>
      </div>
    </div>
  );
};

export default EnhancedSmartCooking;