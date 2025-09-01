// Smart Cooking Tool - AI-Powered Recipe Generation
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Icon, AnimatedIcon } from './ProfessionalIcons';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

const SmartCookingTool = ({ user, onClose }) => {
  const [currentStep, setCurrentStep] = useState('welcome'); // welcome, ingredients, preferences, recipes, premium
  const [session, setSession] = useState(null);
  const [ingredients, setIngredients] = useState([]);
  const [newIngredient, setNewIngredient] = useState({ name: '', quantity: '', unit: 'cup' });
  const [preferences, setPreferences] = useState({
    difficulty_level: 'medium',
    cooking_time_max: 60,
    cuisine_preferences: [],
    dietary_restrictions: [],
    skill_level: 'intermediate'
  });
  const [recipes, setRecipes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [selectedRecipe, setSelectedRecipe] = useState(null);

  // Units for ingredient measurement
  const units = ['cup', 'tbsp', 'tsp', 'oz', 'lb', 'g', 'kg', 'ml', 'L', 'piece', 'clove', 'bunch'];
  
  // Cuisine options
  const cuisineOptions = ['Italian', 'Asian', 'Mexican', 'Indian', 'Mediterranean', 'American', 'French', 'Thai', 'Japanese', 'Korean', 'African', 'Caribbean'];
  
  // Dietary restrictions
  const dietaryOptions = ['Vegetarian', 'Vegan', 'Gluten-free', 'Dairy-free', 'Keto', 'Paleo', 'Low-carb', 'Low-sodium'];

  useEffect(() => {
    if (currentStep === 'welcome') {
      createSession();
    }
  }, []);

  const createSession = async () => {
    setLoading(true);
    try {
      const response = await axios.post(`${BACKEND_URL}/api/smart-cooking/session/create`, {
        session_name: 'My Smart Kitchen'
      });
      
      if (response.data.success) {
        setSession(response.data);
        setCurrentStep('ingredients');
      }
    } catch (error) {
      setError('Failed to create cooking session. Please try again.');
      console.error('Session creation failed:', error);
    }
    setLoading(false);
  };

  const addIngredient = () => {
    if (newIngredient.name.trim()) {
      setIngredients([...ingredients, { 
        ...newIngredient, 
        id: Date.now(),
        freshness: 'fresh'
      }]);
      setNewIngredient({ name: '', quantity: '', unit: 'cup' });
    }
  };

  const removeIngredient = (id) => {
    setIngredients(ingredients.filter(ing => ing.id !== id));
  };

  const saveIngredients = async () => {
    if (ingredients.length === 0) {
      setError('Please add at least one ingredient');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post(
        `${BACKEND_URL}/api/smart-cooking/session/${session.session_id}/ingredients`,
        ingredients
      );
      
      if (response.data.success) {
        setCurrentStep('preferences');
      }
    } catch (error) {
      setError('Failed to save ingredients. Please try again.');
      console.error('Ingredient saving failed:', error);
    }
    setLoading(false);
  };

  const generateRecipes = async () => {
    setLoading(true);
    try {
      const response = await axios.post(
        `${BACKEND_URL}/api/smart-cooking/session/${session.session_id}/generate-recipes`,
        preferences
      );
      
      if (response.data.success) {
        setRecipes(response.data.recipes);
        setCurrentStep('recipes');
      }
    } catch (error) {
      setError('Failed to generate recipes. Please try again.');
      console.error('Recipe generation failed:', error);
    }
    setLoading(false);
  };

  const activatePremium = async (amount) => {
    setLoading(true);
    try {
      const response = await axios.post(
        `${BACKEND_URL}/api/smart-cooking/session/${session.session_id}/activate-premium`,
        { amount, method: 'stripe' }
      );
      
      if (response.data.success) {
        alert('Premium features activated! 🎉');
        // Regenerate recipes with premium features
        await generateRecipes();
      }
    } catch (error) {
      setError('Payment failed. Please try again.');
      console.error('Premium activation failed:', error);
    }
    setLoading(false);
  };

  const renderWelcomeStep = () => (
    <div className="text-center">
      <AnimatedIcon name="SmartCooking" size={64} className="text-green-600 mb-4" />
      <h2 className="text-2xl font-bold text-gray-800 mb-4">Smart Cooking Assistant</h2>
      <p className="text-gray-600 mb-6">
        AI-powered recipe generation from your available ingredients. 
        Discover what you can cook with what you have!
      </p>
      
      <div className="bg-gradient-to-r from-green-50 to-blue-50 p-4 rounded-lg mb-6">
        <h3 className="font-semibold text-gray-800 mb-2">How it works:</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
          <div className="flex items-center space-x-2">
            <Icon name="Ingredients" size={20} className="text-green-600" />
            <span>Add your ingredients</span>
          </div>
          <div className="flex items-center space-x-2">
            <Icon name="AI" size={20} className="text-blue-600" />
            <span>AI analyzes & suggests</span>
          </div>
          <div className="flex items-center space-x-2">
            <Icon name="ChefHat" size={20} className="text-orange-600" />
            <span>Cook amazing dishes</span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <div className="bg-white p-4 border rounded-lg">
          <h4 className="font-semibold text-green-600">$2.99 Basic</h4>
          <ul className="text-sm text-gray-600 mt-2">
            <li>• Unlimited AI recipes</li>
            <li>• Ingredient optimization</li>
            <li>• Basic nutrition info</li>
          </ul>
        </div>
        <div className="bg-gradient-to-r from-blue-50 to-purple-50 p-4 border rounded-lg">
          <h4 className="font-semibold text-blue-600">$4.99 Premium</h4>
          <ul className="text-sm text-gray-600 mt-2">
            <li>• Everything in Basic</li>
            <li>• Video tutorials</li>
            <li>• Chef tips & techniques</li>
            <li>• Wine pairings</li>
          </ul>
        </div>
      </div>

      {loading ? (
        <div className="flex items-center justify-center">
          <Icon name="Settings" size={24} className="animate-spin text-green-600 mr-2" />
          <span>Setting up your kitchen...</span>
        </div>
      ) : (
        <button
          onClick={() => setCurrentStep('ingredients')}
          className="btn-primary px-6 py-3 rounded-lg font-medium"
        >
          Start Cooking Smart
          <Icon name="ChevronRight" size={20} className="ml-2" />
        </button>
      )}
    </div>
  );

  const renderIngredientsStep = () => (
    <div>
      <div className="flex items-center mb-6">
        <Icon name="Ingredients" size={32} className="text-green-600 mr-3" />
        <div>
          <h2 className="text-xl font-bold text-gray-800">Your Kitchen Ingredients</h2>
          <p className="text-gray-600">Add what you have available to cook with</p>
        </div>
      </div>

      {/* Add Ingredient Form */}
      <div className="bg-gray-50 p-4 rounded-lg mb-6">
        <div className="grid grid-cols-12 gap-2">
          <input
            type="text"
            placeholder="Ingredient name..."
            value={newIngredient.name}
            onChange={(e) => setNewIngredient({...newIngredient, name: e.target.value})}
            className="col-span-6 px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
            onKeyPress={(e) => e.key === 'Enter' && addIngredient()}
          />
          <input
            type="text"
            placeholder="Amount"
            value={newIngredient.quantity}
            onChange={(e) => setNewIngredient({...newIngredient, quantity: e.target.value})}
            className="col-span-3 px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
          />
          <select
            value={newIngredient.unit}
            onChange={(e) => setNewIngredient({...newIngredient, unit: e.target.value})}
            className="col-span-2 px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
          >
            {units.map(unit => (
              <option key={unit} value={unit}>{unit}</option>
            ))}
          </select>
          <button
            onClick={addIngredient}
            className="col-span-1 btn-primary px-3 py-2 rounded-lg"
          >
            <Icon name="Create" size={16} />
          </button>
        </div>
      </div>

      {/* Ingredients List */}
      <div className="space-y-2 mb-6">
        {ingredients.map((ingredient) => (
          <div key={ingredient.id} className="flex items-center justify-between bg-white p-3 border rounded-lg">
            <div className="flex items-center space-x-3">
              <Icon name="Ingredients" size={20} className="text-green-600" />
              <span className="font-medium">{ingredient.name}</span>
              {ingredient.quantity && (
                <span className="text-gray-500">
                  {ingredient.quantity} {ingredient.unit}
                </span>
              )}
            </div>
            <button
              onClick={() => removeIngredient(ingredient.id)}
              className="text-red-500 hover:text-red-700"
            >
              ×
            </button>
          </div>
        ))}
      </div>

      {ingredients.length === 0 && (
        <div className="text-center py-8 text-gray-500">
          <Icon name="Ingredients" size={48} className="mx-auto mb-4 text-gray-300" />
          <p>No ingredients added yet.</p>
          <p className="text-sm">Start by adding what you have in your kitchen!</p>
        </div>
      )}

      {/* Quick Add Suggestions */}
      <div className="mb-6">
        <h3 className="font-medium text-gray-700 mb-2">Quick Add:</h3>
        <div className="flex flex-wrap gap-2">
          {['Onion', 'Garlic', 'Tomato', 'Chicken Breast', 'Rice', 'Pasta', 'Olive Oil', 'Salt', 'Pepper'].map(item => (
            <button
              key={item}
              onClick={() => setNewIngredient({...newIngredient, name: item})}
              className="px-3 py-1 bg-gray-100 hover:bg-gray-200 rounded-full text-sm"
            >
              {item}
            </button>
          ))}
        </div>
      </div>

      <div className="flex justify-between">
        <button
          onClick={() => setCurrentStep('welcome')}
          className="px-4 py-2 text-gray-600 hover:text-gray-800"
        >
          <Icon name="ChevronRight" size={16} className="mr-1 rotate-180" />
          Back
        </button>
        <button
          onClick={saveIngredients}
          disabled={ingredients.length === 0 || loading}
          className="btn-primary px-6 py-2 rounded-lg disabled:opacity-50"
        >
          {loading ? (
            <>
              <Icon name="Settings" size={16} className="animate-spin mr-2" />
              Saving...
            </>
          ) : (
            <>
              Next: Set Preferences
              <Icon name="ChevronRight" size={16} className="ml-2" />
            </>
          )}
        </button>
      </div>
    </div>
  );

  const renderPreferencesStep = () => (
    <div>
      <div className="flex items-center mb-6">
        <Icon name="Settings" size={32} className="text-blue-600 mr-3" />
        <div>
          <h2 className="text-xl font-bold text-gray-800">Cooking Preferences</h2>
          <p className="text-gray-600">Tell us about your cooking style and preferences</p>
        </div>
      </div>

      <div className="space-y-6">
        {/* Difficulty Level */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Difficulty Level
          </label>
          <div className="grid grid-cols-3 gap-2">
            {['easy', 'medium', 'hard'].map(level => (
              <button
                key={level}
                onClick={() => setPreferences({...preferences, difficulty_level: level})}
                className={`p-3 rounded-lg border text-center capitalize ${
                  preferences.difficulty_level === level
                    ? 'bg-blue-100 border-blue-500 text-blue-700'
                    : 'bg-white border-gray-300 hover:border-gray-400'
                }`}
              >
                {level}
              </button>
            ))}
          </div>
        </div>

        {/* Cooking Time */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Maximum Cooking Time: {preferences.cooking_time_max} minutes
          </label>
          <input
            type="range"
            min="15"
            max="180"
            step="15"
            value={preferences.cooking_time_max}
            onChange={(e) => setPreferences({...preferences, cooking_time_max: parseInt(e.target.value)})}
            className="w-full"
          />
          <div className="flex justify-between text-xs text-gray-500 mt-1">
            <span>15 min</span>
            <span>Quick</span>
            <span>Slow</span>
            <span>180 min</span>
          </div>
        </div>

        {/* Cuisine Preferences */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Preferred Cuisines (optional)
          </label>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
            {cuisineOptions.map(cuisine => (
              <button
                key={cuisine}
                onClick={() => {
                  const updated = preferences.cuisine_preferences.includes(cuisine)
                    ? preferences.cuisine_preferences.filter(c => c !== cuisine)
                    : [...preferences.cuisine_preferences, cuisine];
                  setPreferences({...preferences, cuisine_preferences: updated});
                }}
                className={`p-2 rounded-lg border text-sm ${
                  preferences.cuisine_preferences.includes(cuisine)
                    ? 'bg-green-100 border-green-500 text-green-700'
                    : 'bg-white border-gray-300 hover:border-gray-400'
                }`}
              >
                {cuisine}
              </button>
            ))}
          </div>
        </div>

        {/* Dietary Restrictions */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Dietary Restrictions (optional)
          </label>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
            {dietaryOptions.map(diet => (
              <button
                key={diet}
                onClick={() => {
                  const updated = preferences.dietary_restrictions.includes(diet)
                    ? preferences.dietary_restrictions.filter(d => d !== diet)
                    : [...preferences.dietary_restrictions, diet];
                  setPreferences({...preferences, dietary_restrictions: updated});
                }}
                className={`p-2 rounded-lg border text-sm ${
                  preferences.dietary_restrictions.includes(diet)
                    ? 'bg-red-100 border-red-500 text-red-700'
                    : 'bg-white border-gray-300 hover:border-gray-400'
                }`}
              >
                {diet}
              </button>
            ))}
          </div>
        </div>

        {/* Skill Level */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Your Cooking Skill Level
          </label>
          <div className="grid grid-cols-3 gap-2">
            {['beginner', 'intermediate', 'advanced'].map(skill => (
              <button
                key={skill}
                onClick={() => setPreferences({...preferences, skill_level: skill})}
                className={`p-3 rounded-lg border text-center capitalize ${
                  preferences.skill_level === skill
                    ? 'bg-purple-100 border-purple-500 text-purple-700'
                    : 'bg-white border-gray-300 hover:border-gray-400'
                }`}
              >
                {skill}
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="flex justify-between mt-8">
        <button
          onClick={() => setCurrentStep('ingredients')}
          className="px-4 py-2 text-gray-600 hover:text-gray-800"
        >
          <Icon name="ChevronRight" size={16} className="mr-1 rotate-180" />
          Back
        </button>
        <button
          onClick={generateRecipes}
          disabled={loading}
          className="btn-primary px-6 py-2 rounded-lg"
        >
          {loading ? (
            <>
              <Icon name="AI" size={16} className="animate-spin mr-2" />
              AI is thinking...
            </>
          ) : (
            <>
              Generate AI Recipes
              <Icon name="AI" size={16} className="ml-2" />
            </>
          )}
        </button>
      </div>
    </div>
  );

  const renderRecipesStep = () => (
    <div>
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center">
          <Icon name="ChefHat" size={32} className="text-orange-600 mr-3" />
          <div>
            <h2 className="text-xl font-bold text-gray-800">AI-Generated Recipes</h2>
            <p className="text-gray-600">Personalized recipes based on your ingredients</p>
          </div>
        </div>
        <div className="text-right text-sm text-gray-500">
          <div>Ingredients: {ingredients.length}</div>
          <div>Recipes: {recipes.length}</div>
        </div>
      </div>

      {recipes.length === 0 ? (
        <div className="text-center py-12">
          <Icon name="AI" size={64} className="mx-auto mb-4 text-gray-300" />
          <p className="text-gray-500">No recipes generated yet.</p>
        </div>
      ) : (
        <div className="space-y-4">
          {recipes.map((recipe, index) => (
            <div key={recipe.id || index} className="bg-white border rounded-lg p-6 hover:shadow-lg transition-shadow">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-lg font-semibold text-gray-800">{recipe.recipe_name}</h3>
                  <div className="flex items-center space-x-4 text-sm text-gray-600 mt-1">
                    <span className="flex items-center">
                      <Icon name="Settings" size={16} className="mr-1" />
                      {recipe.difficulty_level}
                    </span>
                    <span className="flex items-center">
                      <Icon name="Settings" size={16} className="mr-1" />
                      {recipe.preparation_time + recipe.cooking_time} min total
                    </span>
                    <span className="flex items-center">
                      <Icon name="Heritage" size={16} className="mr-1" />
                      {recipe.cuisine_type}
                    </span>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-lg font-semibold text-green-600">
                    ${recipe.estimated_cost?.toFixed(2) || '8.50'}
                  </div>
                  <div className="text-sm text-gray-500">Estimated cost</div>
                </div>
              </div>

              <p className="text-gray-600 mb-4">{recipe.description}</p>

              <div className="grid md:grid-cols-2 gap-4 mb-4">
                <div>
                  <h4 className="font-medium text-gray-700 mb-2">Using Your Ingredients:</h4>
                  <div className="flex flex-wrap gap-1">
                    {recipe.ingredients_used?.map((ingredient, i) => (
                      <span key={i} className="bg-green-100 text-green-700 px-2 py-1 rounded-full text-xs">
                        {ingredient}
                      </span>
                    ))}
                  </div>
                </div>
                <div>
                  <h4 className="font-medium text-gray-700 mb-2">Need to Buy:</h4>
                  <div className="flex flex-wrap gap-1">
                    {recipe.additional_ingredients?.map((ingredient, i) => (
                      <span key={i} className="bg-orange-100 text-orange-700 px-2 py-1 rounded-full text-xs">
                        {ingredient.name}
                      </span>
                    ))}
                  </div>
                </div>
              </div>

              <div className="bg-gray-50 p-3 rounded-lg mb-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="font-medium text-gray-700">Ingredient Utilization</span>
                  <span className="text-green-600 font-semibold">
                    {Math.round((recipe.ingredient_utilization_score || 0.8) * 100)}%
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-green-500 h-2 rounded-full" 
                    style={{ width: `${Math.round((recipe.ingredient_utilization_score || 0.8) * 100)}%` }}
                  ></div>
                </div>
              </div>

              <div className="flex justify-between items-center">
                <button
                  onClick={() => setSelectedRecipe(recipe)}
                  className="btn-primary px-4 py-2 rounded-lg"
                >
                  <Icon name="Recipe" size={16} className="mr-2" />
                  View Full Recipe
                </button>
                <div className="text-sm text-gray-500">
                  {recipe.servings} servings • {recipe.preparation_time + recipe.cooking_time} min
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Premium Upgrade Banner */}
      <div className="bg-gradient-to-r from-blue-50 to-purple-50 border border-blue-200 rounded-lg p-6 mt-6">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="font-semibold text-blue-800 mb-2">Unlock Premium Features</h3>
            <ul className="text-sm text-blue-700 space-y-1">
              <li>• Video cooking tutorials</li>
              <li>• Professional chef tips</li>
              <li>• Advanced nutritional analysis</li>
              <li>• Wine pairing suggestions</li>
            </ul>
          </div>
          <div className="text-right">
            <button
              onClick={() => activatePremium(4.99)}
              disabled={loading}
              className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium mb-2"
            >
              {loading ? 'Processing...' : 'Upgrade $4.99'}
            </button>
            <div className="text-xs text-blue-600">
              <button onClick={() => activatePremium(2.99)} className="underline">
                Basic $2.99
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="flex justify-between mt-6">
        <button
          onClick={() => setCurrentStep('preferences')}
          className="px-4 py-2 text-gray-600 hover:text-gray-800"
        >
          <Icon name="ChevronRight" size={16} className="mr-1 rotate-180" />
          Back
        </button>
        <button
          onClick={generateRecipes}
          disabled={loading}
          className="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded-lg"
        >
          <Icon name="AI" size={16} className="mr-2" />
          Generate New Recipes
        </button>
      </div>
    </div>
  );

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-hidden">
        {/* Header */}
        <div className="bg-gradient-to-r from-green-600 to-blue-600 text-white p-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Icon name="SmartCooking" size={32} className="text-white" />
              <div>
                <h1 className="text-xl font-bold">Smart Cooking Assistant</h1>
                <p className="text-green-100">AI-powered recipe generation</p>
              </div>
            </div>
            <button
              onClick={onClose}
              className="text-white hover:text-gray-200 text-2xl"
            >
              ×
            </button>
          </div>
          
          {/* Progress Bar */}
          <div className="mt-4">
            <div className="flex items-center space-x-2 text-sm">
              <span className={currentStep === 'welcome' ? 'font-semibold' : 'opacity-70'}>Welcome</span>
              <span className="opacity-50">→</span>
              <span className={currentStep === 'ingredients' ? 'font-semibold' : 'opacity-70'}>Ingredients</span>
              <span className="opacity-50">→</span>
              <span className={currentStep === 'preferences' ? 'font-semibold' : 'opacity-70'}>Preferences</span>
              <span className="opacity-50">→</span>
              <span className={currentStep === 'recipes' ? 'font-semibold' : 'opacity-70'}>Recipes</span>
            </div>
          </div>
        </div>

        {/* Error Display */}
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3">
            <div className="flex items-center">
              <Icon name="Shield" size={16} className="mr-2" />
              {error}
              <button onClick={() => setError('')} className="ml-auto text-red-500 hover:text-red-700">×</button>
            </div>
          </div>
        )}

        {/* Content */}
        <div className="p-6 overflow-y-auto" style={{ maxHeight: 'calc(90vh - 200px)' }}>
          {currentStep === 'welcome' && renderWelcomeStep()}
          {currentStep === 'ingredients' && renderIngredientsStep()}
          {currentStep === 'preferences' && renderPreferencesStep()}
          {currentStep === 'recipes' && renderRecipesStep()}
        </div>

        {/* Recipe Detail Modal */}
        {selectedRecipe && (
          <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-60 p-4">
            <div className="bg-white rounded-xl max-w-2xl w-full max-h-[80vh] overflow-y-auto">
              <div className="p-6">
                <div className="flex justify-between items-start mb-4">
                  <h2 className="text-2xl font-bold text-gray-800">{selectedRecipe.recipe_name}</h2>
                  <button
                    onClick={() => setSelectedRecipe(null)}
                    className="text-gray-500 hover:text-gray-700 text-xl"
                  >
                    ×
                  </button>
                </div>
                
                <div className="space-y-4">
                  <p className="text-gray-600">{selectedRecipe.description}</p>
                  
                  <div>
                    <h3 className="font-semibold text-gray-800 mb-2">Instructions:</h3>
                    <ol className="list-decimal list-inside space-y-2 text-gray-600">
                      {selectedRecipe.instructions?.map((step, i) => (
                        <li key={i}>{step}</li>
                      ))}
                    </ol>
                  </div>
                  
                  <div className="grid md:grid-cols-2 gap-4">
                    <div>
                      <h3 className="font-semibold text-gray-800 mb-2">Your Ingredients:</h3>
                      <ul className="space-y-1">
                        {selectedRecipe.ingredients_used?.map((ingredient, i) => (
                          <li key={i} className="text-green-700">✓ {ingredient}</li>
                        ))}
                      </ul>
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-800 mb-2">Additional Ingredients:</h3>
                      <ul className="space-y-1">
                        {selectedRecipe.additional_ingredients?.map((ingredient, i) => (
                          <li key={i} className="text-orange-700">
                            + {ingredient.name} ({ingredient.quantity})
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default SmartCookingTool;