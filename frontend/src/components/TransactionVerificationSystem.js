// Transaction Verification System - GPS + Barcode + Payment Hold/Release
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Icon, AnimatedIcon } from './ProfessionalIcons';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

const TransactionVerificationSystem = ({ user, transactionType = 'home_restaurant' }) => {
  const [currentStep, setCurrentStep] = useState('meal_planning'); // meal_planning, pricing, verification, monitoring
  const [mealPackage, setMealPackage] = useState({
    entree: { name: '', price: 0, description: '' },
    main_course: { name: '', price: 0, description: '' },
    dessert: { name: '', price: 0, description: '' },
    beverage: { name: '', price: 0, description: '' }
  });
  const [pricingJustification, setPricingJustification] = useState({
    meal_complexity: 'Moderate',
    ingredient_quality: 'Premium',
    preparation_time: 60,
    cultural_authenticity: 'Traditional',
    presentation_level: 'Elegant',
    unique_value_proposition: '',
    competitive_analysis: '',
    justification_text: ''
  });
  const [selectedServices, setSelectedServices] = useState(['table_setting', 'cleanup_service']);
  const [serviceFees, setServiceFees] = useState(null);
  const [transaction, setTransaction] = useState(null);
  const [customerBarcode, setCustomerBarcode] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Service types with descriptions
  const availableServices = [
    { id: 'table_setting', name: 'Table Setting', description: 'Professional table arrangement and setup', icon: 'Utensils' },
    { id: 'ambiance_creation', name: 'Ambiance Creation', description: 'Lighting, music, and atmosphere preparation', icon: 'Star' },
    { id: 'hosting_welcome', name: 'Hosting & Welcome', description: 'Personal greeting and seating service', icon: 'Heart' },
    { id: 'meal_presentation', name: 'Meal Presentation', description: 'Artistic plating and presentation', icon: 'Recipe' },
    { id: 'cleanup_service', name: 'Cleanup Service', description: 'Post-meal cleaning and table reset', icon: 'Settings' },
    { id: 'farewell_service', name: 'Farewell Service', description: 'Goodbye and customer satisfaction check', icon: 'Heart' }
  ];

  // Calculate service fees when meal price or services change
  useEffect(() => {
    const calculateFees = async () => {
      if (getMealTotalPrice() > 0 && selectedServices.length > 0) {
        try {
          const response = await axios.get(
            `${BACKEND_URL}/api/transaction-verification/service-fee-calculator?meal_price=${getMealTotalPrice()}&services=${selectedServices.join(',')}`
          );
          setServiceFees(response.data);
        } catch (error) {
          console.error('Failed to calculate service fees:', error);
        }
      }
    };
    calculateFees();
  }, [mealPackage, selectedServices]);

  const getMealTotalPrice = () => {
    return Object.values(mealPackage).reduce((sum, item) => sum + (item.price || 0), 0);
  };

  const handleMealComponentChange = (component, field, value) => {
    setMealPackage(prev => ({
      ...prev,
      [component]: {
        ...prev[component],
        [field]: field === 'price' ? parseFloat(value) || 0 : value
      }
    }));
  };

  const toggleService = (serviceId) => {
    setSelectedServices(prev => 
      prev.includes(serviceId) 
        ? prev.filter(s => s !== serviceId)
        : [...prev, serviceId]
    );
  };

  const validatePricing = async () => {
    setLoading(true);
    try {
      const response = await axios.post(`${BACKEND_URL}/api/transaction-verification/validate-pricing`, {
        justification: pricingJustification,
        meal_price: getMealTotalPrice()
      });
      
      if (response.data.success) {
        return response.data.pricing_analysis;
      }
    } catch (error) {
      setError('Failed to validate pricing');
    }
    setLoading(false);
    return null;
  };

  const createTransaction = async (customerData) => {
    setLoading(true);
    try {
      const transactionData = {
        transaction_type: transactionType,
        customer_id: customerData.customer_id,
        meal_components: mealPackage,
        pricing_justification: pricingJustification,
        services_selected: selectedServices,
        restaurant_location: {
          latitude: customerData.restaurant_location.latitude,
          longitude: customerData.restaurant_location.longitude,
          accuracy: 10.0
        }
      };

      const response = await axios.post(
        `${BACKEND_URL}/api/transaction-verification/create-transaction`,
        transactionData
      );

      if (response.data.success) {
        setTransaction(response.data.transaction);
        setCustomerBarcode(response.data.customer_barcode);
        setCurrentStep('verification');
      }
    } catch (error) {
      setError('Failed to create transaction');
    }
    setLoading(false);
  };

  const renderMealPlanningStep = () => (
    <div className="space-y-6">
      <div className="text-center mb-6">
        <Icon name="ChefHat" size={48} className="text-orange-600 mx-auto mb-4" />
        <h2 className="text-2xl font-bold text-gray-800">Create Complete Meal Experience</h2>
        <p className="text-gray-600">Lambalia encourages complete dining experiences with entrée, main course, dessert, and beverage</p>
      </div>

      {Object.entries(mealPackage).map(([component, details]) => (
        <div key={component} className="bg-white p-6 rounded-lg border shadow-sm">
          <h3 className="font-semibold text-gray-800 mb-4 capitalize flex items-center">
            <Icon name="Recipe" size={20} className="text-green-600 mr-2" />
            {component.replace('_', ' ')}
            <span className="text-red-500 ml-1">*</span>
          </h3>
          
          <div className="grid md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Dish Name</label>
              <input
                type="text"
                value={details.name}
                onChange={(e) => handleMealComponentChange(component, 'name', e.target.value)}
                className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                placeholder={`Enter ${component.replace('_', ' ')} name`}
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Price ($)</label>
              <input
                type="number"
                step="0.01"
                value={details.price}
                onChange={(e) => handleMealComponentChange(component, 'price', e.target.value)}
                className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                placeholder="0.00"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
              <input
                type="text"
                value={details.description}
                onChange={(e) => handleMealComponentChange(component, 'description', e.target.value)}
                className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                placeholder="Brief description"
              />
            </div>
          </div>
        </div>
      ))}

      {/* Meal Package Summary */}
      <div className="bg-gradient-to-r from-green-50 to-blue-50 p-6 rounded-lg border">
        <h3 className="font-semibold text-gray-800 mb-4">Complete Meal Package</h3>
        <div className="grid md:grid-cols-2 gap-4">
          <div>
            <div className="text-2xl font-bold text-green-600">${getMealTotalPrice().toFixed(2)}</div>
            <div className="text-sm text-gray-600">Individual Total</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-blue-600">${(getMealTotalPrice() * 0.85).toFixed(2)}</div>
            <div className="text-sm text-gray-600">Package Price (15% savings)</div>
          </div>
        </div>
        <div className="mt-4 p-3 bg-green-100 rounded-lg">
          <div className="flex items-center text-green-800">
            <Icon name="Star" size={16} className="mr-2" />
            <span className="font-medium">Customers save ${(getMealTotalPrice() * 0.15).toFixed(2)} with complete package!</span>
          </div>
        </div>
      </div>

      <button
        onClick={() => setCurrentStep('pricing')}
        disabled={getMealTotalPrice() === 0 || Object.values(mealPackage).some(item => !item.name)}
        className="w-full btn-primary py-3 rounded-lg font-medium disabled:opacity-50"
      >
        Continue to Pricing & Services
        <Icon name="ChevronRight" size={20} className="ml-2" />
      </button>
    </div>
  );

  const renderPricingStep = () => (
    <div className="space-y-6">
      <div className="text-center mb-6">
        <Icon name="Dollar" size={48} className="text-blue-600 mx-auto mb-4" />
        <h2 className="text-2xl font-bold text-gray-800">Pricing Justification & Services</h2>
        <p className="text-gray-600">Explain your pricing to help customers understand the value they receive</p>
      </div>

      {/* Pricing Justification */}
      <div className="bg-white p-6 rounded-lg border">
        <h3 className="font-semibold text-gray-800 mb-4">Why This Price?</h3>
        
        <div className="grid md:grid-cols-2 gap-4 mb-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Meal Complexity</label>
            <select
              value={pricingJustification.meal_complexity}
              onChange={(e) => setPricingJustification({...pricingJustification, meal_complexity: e.target.value})}
              className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="Simple">Simple</option>
              <option value="Moderate">Moderate</option>
              <option value="Complex">Complex</option>
              <option value="Gourmet">Gourmet</option>
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Ingredient Quality</label>
            <select
              value={pricingJustification.ingredient_quality}
              onChange={(e) => setPricingJustification({...pricingJustification, ingredient_quality: e.target.value})}
              className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="Basic">Basic</option>
              <option value="Premium">Premium</option>
              <option value="Organic">Organic</option>
              <option value="Exotic">Exotic</option>
            </select>
          </div>
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Preparation Time: {pricingJustification.preparation_time} minutes
          </label>
          <input
            type="range"
            min="30"
            max="300" 
            step="15"
            value={pricingJustification.preparation_time}
            onChange={(e) => setPricingJustification({...pricingJustification, preparation_time: parseInt(e.target.value)})}
            className="w-full"
          />
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-1">Unique Value Proposition</label>
          <textarea
            value={pricingJustification.unique_value_proposition}
            onChange={(e) => setPricingJustification({...pricingJustification, unique_value_proposition: e.target.value})}
            className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            rows="3"
            placeholder="What makes your dining experience special and worth the price?"
          />
        </div>
      </div>

      {/* Service Selection */}
      <div className="bg-white p-6 rounded-lg border">
        <h3 className="font-semibold text-gray-800 mb-4">Select Services</h3>
        <p className="text-sm text-gray-600 mb-4">Add professional services to enhance the dining experience</p>
        
        <div className="grid md:grid-cols-2 gap-4">
          {availableServices.map(service => (
            <div key={service.id} 
                 className={`p-4 border rounded-lg cursor-pointer transition-all ${
                   selectedServices.includes(service.id) 
                     ? 'border-green-500 bg-green-50' 
                     : 'border-gray-300 hover:border-gray-400'
                 }`}
                 onClick={() => toggleService(service.id)}
            >
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center">
                  <Icon name={service.icon} size={20} className={selectedServices.includes(service.id) ? 'text-green-600' : 'text-gray-600'} />
                  <span className="font-medium ml-2">{service.name}</span>
                </div>
                <div className={`w-5 h-5 rounded border-2 flex items-center justify-center ${
                  selectedServices.includes(service.id) ? 'border-green-500 bg-green-500' : 'border-gray-300'
                }`}>
                  {selectedServices.includes(service.id) && (
                    <Icon name="ChevronRight" size={12} className="text-white rotate-90" />
                  )}
                </div>
              </div>
              <p className="text-sm text-gray-600">{service.description}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Service Fees Summary */}
      {serviceFees && (
        <div className="bg-gradient-to-r from-blue-50 to-purple-50 p-6 rounded-lg border">
          <h3 className="font-semibold text-gray-800 mb-4">Service Fees (Regulated by Lambalia)</h3>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span>Meal Package:</span>
              <span className="font-medium">${(getMealTotalPrice() * 0.85).toFixed(2)}</span>
            </div>
            <div className="flex justify-between">
              <span>Service Fees:</span>
              <span className="font-medium">${serviceFees.total_service_fee.toFixed(2)}</span>
            </div>
            <div className="border-t pt-2 flex justify-between font-semibold text-lg">
              <span>Total Transaction:</span>
              <span className="text-green-600">${((getMealTotalPrice() * 0.85) + serviceFees.total_service_fee).toFixed(2)}</span>
            </div>
          </div>
          <p className="text-xs text-blue-600 mt-3">
            Service fees are regulated to ensure competitive pricing with local restaurants
          </p>
        </div>
      )}

      <div className="flex justify-between">
        <button
          onClick={() => setCurrentStep('meal_planning')}
          className="px-6 py-2 text-gray-600 hover:text-gray-800"
        >
          <Icon name="ChevronRight" size={16} className="mr-1 rotate-180" />
          Back to Meal Planning
        </button>
        <button
          onClick={() => setCurrentStep('verification')}
          className="btn-primary px-6 py-2 rounded-lg"
        >
          Continue to Transaction Setup
          <Icon name="Shield" size={16} className="ml-2" />
        </button>
      </div>
    </div>
  );

  const renderVerificationStep = () => (
    <div className="space-y-6">
      <div className="text-center mb-6">
        <Icon name="Shield" size={48} className="text-purple-600 mx-auto mb-4" />
        <h2 className="text-2xl font-bold text-gray-800">Transaction Verification System</h2>
        <p className="text-gray-600">GPS tracking + Barcode verification ensures secure transactions</p>
      </div>

      <div className="bg-gradient-to-r from-purple-50 to-blue-50 p-6 rounded-lg border">
        <h3 className="font-semibold text-purple-800 mb-4">How It Works</h3>
        <div className="grid md:grid-cols-2 gap-6">
          <div className="space-y-4">
            <div className="flex items-start space-x-3">
              <div className="bg-purple-600 text-white rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold">1</div>
              <div>
                <h4 className="font-medium text-gray-800">Payment Hold</h4>
                <p className="text-sm text-gray-600">Customer funds are held securely until service completion</p>
              </div>
            </div>
            
            <div className="flex items-start space-x-3">
              <div className="bg-purple-600 text-white rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold">2</div>
              <div>
                <h4 className="font-medium text-gray-800">GPS + Barcode Entry</h4>
                <p className="text-sm text-gray-600">Customer scans barcode upon arrival, GPS verifies location</p>
              </div>
            </div>
            
            <div className="flex items-start space-x-3">
              <div className="bg-purple-600 text-white rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold">3</div>
              <div>
                <h4 className="font-medium text-gray-800">Service Period</h4>
                <p className="text-sm text-gray-600">Enjoy complete dining experience with selected services</p>
              </div>
            </div>
            
            <div className="flex items-start space-x-3">
              <div className="bg-purple-600 text-white rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold">4</div>
              <div>
                <h4 className="font-medium text-gray-800">Exit Scan & Payment</h4>
                <p className="text-sm text-gray-600">Customer scans again before leaving, payment released automatically</p>
              </div>
            </div>
          </div>
          
          <div className="bg-white p-4 rounded-lg">
            <h4 className="font-medium text-gray-800 mb-3">Security Features</h4>
            <ul className="space-y-2 text-sm text-gray-600">
              <li className="flex items-center">
                <Icon name="Shield" size={16} className="text-green-600 mr-2" />
                GPS location verification (50m radius)
              </li>
              <li className="flex items-center">
                <Icon name="Settings" size={16} className="text-green-600 mr-2" />
                Unique barcode for each transaction
              </li>
              <li className="flex items-center">
                <Icon name="Lock" size={16} className="text-green-600 mr-2" />
                Secure payment hold system
              </li>
              <li className="flex items-center">
                <Icon name="Message" size={16} className="text-green-600 mr-2" />
                Automatic notifications to both parties
              </li>
            </ul>
          </div>
        </div>
      </div>

      {/* Restaurant Sign Order */}
      <div className="bg-white p-6 rounded-lg border">
        <h3 className="font-semibold text-gray-800 mb-4 flex items-center">
          <Icon name="Store" size={24} className="text-orange-600 mr-2" />
          Restaurant Identification Sign
        </h3>
        <p className="text-gray-600 mb-4">
          Order a professional weather-resistant sign with your restaurant's QR code for easy customer verification.
        </p>
        
        <div className="grid md:grid-cols-2 gap-4">
          <div>
            <h4 className="font-medium text-gray-700 mb-2">Sign Features:</h4>
            <ul className="text-sm text-gray-600 space-y-1">
              <li>• 12" x 18" professional size</li>
              <li>• Weather-resistant aluminum</li>
              <li>• UV-protected lamination</li>
              <li>• Pre-drilled mounting holes</li>
              <li>• Custom QR code for your restaurant</li>
            </ul>
          </div>
          <div>
            <div className="text-2xl font-bold text-green-600">$53.50</div>
            <div className="text-sm text-gray-600">Including shipping</div>
            <div className="text-sm text-gray-500">5-7 business days delivery</div>
          </div>
        </div>
        
        <button className="mt-4 bg-orange-600 hover:bg-orange-700 text-white px-6 py-2 rounded-lg">
          <Icon name="Store" size={16} className="mr-2" />
          Order Restaurant Sign
        </button>
      </div>

      <div className="text-center">
        <button
          onClick={() => setCurrentStep('monitoring')}
          className="btn-primary px-8 py-3 rounded-lg font-medium"
        >
          Start Transaction Verification
          <Icon name="Shield" size={20} className="ml-2" />
        </button>
      </div>
    </div>
  );

  return (
    <div className="max-w-4xl mx-auto p-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-green-600 to-purple-600 text-white p-6 rounded-xl mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold">Transaction Verification System</h1>
            <p className="text-green-100">GPS Tracking + Barcode Verification + Secure Payment</p>
          </div>
          <Icon name="Shield" size={48} className="text-white opacity-80" />
        </div>
        
        {/* Progress Bar */}
        <div className="mt-6">
          <div className="flex items-center space-x-2 text-sm">
            <span className={currentStep === 'meal_planning' ? 'font-semibold' : 'opacity-70'}>Meal Planning</span>
            <span className="opacity-50">→</span>
            <span className={currentStep === 'pricing' ? 'font-semibold' : 'opacity-70'}>Pricing & Services</span>
            <span className="opacity-50">→</span>
            <span className={currentStep === 'verification' ? 'font-semibold' : 'opacity-70'}>Verification Setup</span>
            <span className="opacity-50">→</span>
            <span className={currentStep === 'monitoring' ? 'font-semibold' : 'opacity-70'}>Transaction Monitoring</span>
          </div>
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
          <div className="flex items-center">
            <Icon name="Shield" size={16} className="mr-2" />
            {error}
            <button onClick={() => setError('')} className="ml-auto text-red-500 hover:text-red-700">×</button>
          </div>
        </div>
      )}

      {/* Content */}
      <div className="bg-gray-50 rounded-xl p-6">
        {currentStep === 'meal_planning' && renderMealPlanningStep()}
        {currentStep === 'pricing' && renderPricingStep()}
        {currentStep === 'verification' && renderVerificationStep()}
        {currentStep === 'monitoring' && (
          <div className="text-center py-12">
            <Icon name="Settings" size={64} className="mx-auto mb-4 text-gray-400 animate-spin" />
            <h3 className="text-xl font-semibold text-gray-700 mb-2">Transaction Monitoring</h3>
            <p className="text-gray-600">Real-time transaction status and verification monitoring will be displayed here.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default TransactionVerificationSystem;