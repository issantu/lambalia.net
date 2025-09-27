import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useTranslation } from 'react-i18next';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Enhanced Local Marketplace - Farm Ecosystem & Charity Integration
const LocalMarketplacePage = () => {
  const { t } = useTranslation();
  const [activeTab, setActiveTab] = useState('browse'); // 'browse', 'sell', 'charity', 'impact'
  const [localFarms, setLocalFarms] = useState([]);
  const [farmProducts, setFarmProducts] = useState([]);
  const [charityProgram, setCharityProgram] = useState(null);
  const [communityImpact, setCommunityImpact] = useState(null);
  const [loading, setLoading] = useState(false);
  const [postalCode, setPostalCode] = useState('10001');
  const [filters, setFilters] = useState({
    vendor_type: '',
    certifications: '',
    max_distance: 50
  });

  useEffect(() => {
    if (activeTab === 'browse') {
      fetchLocalFarms();
      fetchSeasonalProducts();
    } else if (activeTab === 'charity') {
      fetchCharityDashboard();
    } else if (activeTab === 'impact') {
      fetchCommunityImpact();
    }
  }, [activeTab]);

  const fetchLocalFarms = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API}/farms/local`, {
        params: {
          postal_code: postalCode,
          max_distance_km: filters.max_distance,
          vendor_type: filters.vendor_type,
          certifications: filters.certifications
        }
      });
      setLocalFarms(response.data);
    } catch (error) {
      console.error('Failed to fetch local farms:', error);
    }
    setLoading(false);
  };

  const fetchSeasonalProducts = async () => {
    try {
      const response = await axios.get(`${API}/farms/seasonal-calendar`, {
        params: { postal_code: postalCode }
      });
      setFarmProducts(response.data.seasonal_calendar?.summer || []);
    } catch (error) {
      console.error('Failed to fetch seasonal products:', error);
    }
  };

  const fetchCharityDashboard = async () => {
    try {
      const response = await axios.get(`${API}/charity/dashboard`);
      setCharityProgram(response.data);
    } catch (error) {
      console.error('Failed to fetch charity dashboard:', error);
    }
  };

  const fetchCommunityImpact = async () => {
    try {
      const response = await axios.get(`${API}/charity/community-impact`);
      setCommunityImpact(response.data.community_impact);
    } catch (error) {
      console.error('Failed to fetch community impact:', error);
    }
  };

  const FarmCard = ({ farm }) => (
    <div className="recipe-card">
      <div className="p-6">
        <div className="flex items-start justify-between mb-3">
          <div>
            <h3 className="text-lg font-semibold text-gray-800">{farm.farm_name}</h3>
            <p className="text-sm text-gray-500">{farm.vendor_type.replace('_', ' ')}</p>
            <p className="text-xs text-gray-500">{farm.distance_km}km away</p>
          </div>
          <div className="flex flex-col items-end space-y-1">
            {farm.certifications.slice(0, 2).map((cert, index) => (
              <span key={index} className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded-full">
                {cert.replace('_', ' ')}
              </span>
            ))}
          </div>
        </div>
        
        <p className="text-gray-600 mb-3 line-clamp-2">{farm.description}</p>
        
        <div className="flex items-center text-sm text-gray-500 mb-3">
          <span>🏡 {farm.total_acres} acres</span>
          <span className="mx-2">•</span>
          <span>🌱 {farm.farming_methods.join(', ')}</span>
          <span className="mx-2">•</span>
          <span>⭐ {farm.average_rating || 'New'}</span>
        </div>

        <div className="mb-3">
          <p className="text-sm font-medium text-gray-700 mb-1">Available Products ({farm.product_count})</p>
          <div className="flex flex-wrap gap-1">
            {farm.sustainability_practices.slice(0, 3).map((practice, index) => (
              <span key={index} className="bg-blue-100 text-blue-700 text-xs px-2 py-1 rounded">
                {practice}
              </span>
            ))}
          </div>
        </div>
        
        <div className="flex items-center justify-between">
          <div className="text-sm text-gray-500">
            {farm.is_accepting_orders ? (
              <span className="text-green-600">✅ Taking orders</span>
            ) : (
              <span className="text-red-600">❌ Currently unavailable</span>
            )}
            {farm.offers_farm_dining && (
              <span className="ml-2 text-purple-600">🍽️ Farm dining</span>
            )}
          </div>
          <button className="btn-primary px-4 py-2 rounded-lg text-sm">
            Visit Farm
          </button>
        </div>
      </div>
    </div>
  );

  const ProductCard = ({ product }) => (
    <div className="bg-white rounded-lg p-4 shadow-sm border">
      <div className="flex items-start justify-between mb-2">
        <div>
          <h4 className="font-medium text-gray-800">{product.product_name}</h4>
          <p className="text-sm text-gray-500">from {product.farm_name}</p>
        </div>
        <span className="text-lg font-bold text-green-600">
          ${product.price_per_unit}/{product.unit_type}
        </span>
      </div>
      
      <div className="flex items-center text-xs text-gray-500 mb-2">
        <span>{product.distance_km}{t('marketplace.browse.kmAway')}</span>
        <span className="mx-2">•</span>
        <span>{product.growing_method}</span>
        {product.certifications.length > 0 && (
          <>
            <span className="mx-2">•</span>
            <span className="text-green-600">{product.certifications[0].replace('_', ' ')}</span>
          </>
        )}
      </div>
      
      <div className="flex items-center justify-between">
        <span>{t('marketplace.browse.available', {count: product.quantity_available}) || (product.quantity_available ? `${product.quantity_available} ${t('marketplace.browse.available')}` : t('marketplace.browse.inSeason'))}</span>
        <button className="bg-green-600 hover:bg-green-700 text-white px-3 py-1 rounded text-sm">
          {t('marketplace.browse.addToCart')}
        </button>
      </div>
    </div>
  );

  const CharityProgramCard = () => (
    <div className="glass p-6 mb-6">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-xl font-bold text-gray-800">{t('marketplace.charity.title')}</h3>
          <p className="text-gray-600">{t('marketplace.charity.subtitle')}</p>
        </div>
        <div className="text-right">
          <p className="text-2xl font-bold text-green-600">{t('marketplace.charity.free')}</p>
          <p className="text-sm text-gray-500">{t('marketplace.charity.premiumMembership')}</p>
        </div>
      </div>

      <div className="bg-gradient-to-r from-green-50 to-blue-50 p-4 rounded-lg mb-4">
        <h4 className="font-semibold text-gray-800 mb-2">{t('marketplace.charity.howItWorks')}</h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm">
          <div className="flex items-start space-x-2">
            <span className="text-green-600">1.</span>
            <span>{t('marketplace.charity.step1')}</span>
          </div>
          <div className="flex items-start space-x-2">
            <span className="text-green-600">2.</span>
            <span>{t('marketplace.charity.step2')}</span>
          </div>
          <div className="flex items-start space-x-2">
            <span className="text-green-600">3.</span>
            <span>{t('marketplace.charity.step3')}</span>
          </div>
          <div className="flex items-start space-x-2">
            <span className="text-green-600">4.</span>
            <span>{t('marketplace.charity.step4')}</span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
        <div className="text-center p-3 bg-white rounded-lg">
          <p className="text-2xl font-bold text-green-600">14%</p>
          <p className="text-sm text-gray-600">{t('marketplace.charity.commissionRate')}</p>
          <p className="text-xs text-gray-500">(1% {t('marketplace.charity.savings')})</p>
        </div>
        <div className="text-center p-3 bg-white rounded-lg">
          <p className="text-2xl font-bold text-blue-600">4hrs</p>
          <p className="text-sm text-gray-600">{t('marketplace.charity.monthlyVolunteering')}</p>
          <p className="text-xs text-gray-500">{t('marketplace.charity.required')}</p>
        </div>
        <div className="text-center p-3 bg-white rounded-lg">
          <p className="text-2xl font-bold text-purple-600">5lbs</p>
          <p className="text-sm text-gray-600">{t('marketplace.charity.foodDonation')}</p>
          <p className="text-xs text-gray-500">{t('marketplace.charity.monthlyMinimum')}</p>
        </div>
      </div>

      {charityProgram?.success ? (
        <div className="bg-green-50 border border-green-200 rounded-lg p-4">
          <h4 className="font-semibold text-green-800 mb-2">✅ You're Enrolled!</h4>
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <p className="text-green-700">This Month's Impact:</p>
              <p className="font-bold">{charityProgram.statistics?.monthly_impact} points</p>
            </div>
            <div>
              <p className="text-green-700">Community Rank:</p>
              <p className="font-bold">#{charityProgram.community_ranking?.rank}</p>
            </div>
          </div>
        </div>
      ) : (
        <button 
          onClick={() => handleRegisterCharity()}
          className="w-full btn-primary py-3 rounded-lg text-lg font-medium"
        >
          {t('marketplace.charity.joinProgram')}
        </button>
      )}
    </div>
  );

  const handleRegisterCharity = async () => {
    try {
      const response = await axios.post(`${API}/charity/register`, {
        committed_hours_per_month: 4,
        preferred_charity_types: ['food_bank', 'community_kitchen'],
        preferred_locations: [postalCode],
        monthly_impact_goal: 50.0
      });
      
      if (response.data.success) {
        alert('Successfully registered for charity program! Start making a difference in your community.');
        fetchCharityDashboard();
      }
    } catch (error) {
      console.error('Failed to register for charity program:', error);
      alert('Registration failed. Please try again.');
    }
  };

  const CommunityImpactDisplay = () => (
    <div className="space-y-6">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold heading-gradient mb-4">🌍 Community Impact</h2>
        <p className="text-gray-600">See how our local marketplace community is making a difference</p>
      </div>

      {communityImpact && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="glass p-6 text-center">
            <div className="text-3xl mb-2">🥬</div>
            <p className="text-2xl font-bold text-green-600">{communityImpact.total_food_donated_lbs}</p>
            <p className="text-sm text-gray-600">Pounds of Food Donated</p>
            <p className="text-xs text-gray-500">Diverted from waste</p>
          </div>
          
          <div className="glass p-6 text-center">
            <div className="text-3xl mb-2">🍽️</div>
            <p className="text-2xl font-bold text-blue-600">{communityImpact.total_meals_provided}</p>
            <p className="text-sm text-gray-600">Meals Provided</p>
            <p className="text-xs text-gray-500">To those in need</p>
          </div>
          
          <div className="glass p-6 text-center">
            <div className="text-3xl mb-2">👥</div>
            <p className="text-2xl font-bold text-purple-600">{communityImpact.total_people_helped}</p>
            <p className="text-sm text-gray-600">People Helped</p>
            <p className="text-xs text-gray-500">Community members</p>
          </div>
          
          <div className="glass p-6 text-center">
            <div className="text-3xl mb-2">⏰</div>
            <p className="text-2xl font-bold text-orange-600">{communityImpact.total_volunteer_hours}</p>
            <p className="text-sm text-gray-600">Volunteer Hours</p>
            <p className="text-xs text-gray-500">Community service</p>
          </div>
        </div>
      )}

      <div className="glass p-6">
        <h4 className="text-xl font-semibold mb-4">🌱 Environmental Impact</h4>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-green-50 p-4 rounded-lg">
            <p className="text-lg font-bold text-green-600">
              {communityImpact?.estimated_environmental_impact?.co2_saved_lbs || 0} lbs
            </p>
            <p className="text-sm text-gray-600">CO2 Emissions Saved</p>
          </div>
          <div className="bg-blue-50 p-4 rounded-lg">
            <p className="text-lg font-bold text-blue-600">
              {communityImpact?.estimated_environmental_impact?.water_saved_gallons || 0} gallons
            </p>
            <p className="text-sm text-gray-600">Water Conserved</p>
          </div>
          <div className="bg-purple-50 p-4 rounded-lg">
            <p className="text-lg font-bold text-purple-600">
              ${communityImpact?.estimated_environmental_impact?.economic_value_created || 0}
            </p>
            <p className="text-sm text-gray-600">Economic Value Created</p>
          </div>
        </div>
      </div>

      {communityImpact?.top_contributors && (
        <div className="glass p-6">
          <h4 className="text-xl font-semibold mb-4">🏆 Community Champions</h4>
          <div className="space-y-3">
            {communityImpact.top_contributors.slice(0, 5).map((contributor, index) => (
              <div key={contributor.user_id} className="flex items-center space-x-4">
                <span className="flex-shrink-0 w-8 h-8 bg-gradient-to-r from-yellow-400 to-orange-500 rounded-full flex items-center justify-center text-white font-bold">
                  {index + 1}
                </span>
                <div className="flex-1">
                  <p className="font-medium text-gray-800">{contributor.full_name || contributor.username}</p>
                  <p className="text-sm text-gray-500">{contributor.total_impact_score} impact points</p>
                </div>
                <span className="text-yellow-500">
                  {index === 0 ? '👑' : index === 1 ? '🥈' : index === 2 ? '🥉' : '⭐'}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );

  const GardenerApplicationForm = () => {
    const [formData, setFormData] = useState({
      vendor_type: 'backyard_gardener',
      farm_name: '',
      business_name: '',
      farm_description: '',
      established_year: 2020,
      growing_experience_level: 'hobbyist',
      primary_motivation: 'share_excess',
      legal_name: '',
      phone_number: '',
      email: '',
      farm_address: '',
      city: '',
      state: '',
      postal_code: '',
      total_acres: 0.01,
      growing_area_type: 'backyard',
      farming_methods: [],
      primary_products: [],
      certifications: [],
      years_farming_experience: 1,
      has_business_insurance: false,
      has_food_handler_license: false,
      terms_accepted: false,
      food_safety_training: false
    });

    const [submitting, setSubmitting] = useState(false);

    const handleInputChange = (e) => {
      const { name, value, type, checked } = e.target;
      setFormData(prev => ({
        ...prev,
        [name]: type === 'checkbox' ? checked : 
                type === 'number' ? parseFloat(value) || 0 : 
                value
      }));
    };

    const handleArrayChange = (name, value) => {
      setFormData(prev => ({
        ...prev,
        [name]: prev[name].includes(value) 
          ? prev[name].filter(item => item !== value)
          : [...prev[name], value]
      }));
    };

    const handleSubmit = async (e) => {
      e.preventDefault();
      setSubmitting(true);

      try {
        const response = await axios.post(`${API}/farm-vendors/apply`, formData);
        
        if (response.data.success) {
          alert('Application submitted successfully! Welcome to the local gardener community. We\'ll review your application within 3-5 business days.');
          setActiveTab('browse');
        }
      } catch (error) {
        console.error('Failed to submit application:', error);
        alert('Failed to submit application. Please try again.');
      }
      setSubmitting(false);
    };

    return (
      <div className="max-w-4xl mx-auto">
        <div className="glass p-8">
          <h3 className="text-2xl font-bold heading-gradient mb-6">🌱 Join as Local Grower</h3>
          <p className="text-gray-600 mb-6">
            Share your homegrown treasures with the community! Whether you're growing tomatoes in your backyard, 
            herbs on your windowsill, or managing a small urban garden - your excess produce can nourish neighbors 
            while earning you extra income.
          </p>
          
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Grower Type */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">What type of grower are you?</label>
              <select
                name="vendor_type"
                value={formData.vendor_type}
                onChange={handleInputChange}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
              >
                <option value="backyard_gardener">🏡 Backyard Gardener</option>
                <option value="hobby_farmer">🌾 Hobby Farmer</option>
                <option value="urban_farmer">🏙️ Urban Farmer</option>
                <option value="community_garden">🤝 Community Garden Member</option>
                <option value="local_farm">🚜 Local Farm</option>
                <option value="organic_grower">🌱 Organic Grower</option>
                <option value="specialty_producer">⭐ Specialty Producer</option>
              </select>
            </div>

            {/* Basic Information */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Garden/Farm Name *</label>
                <input
                  type="text"
                  name="farm_name"
                  value={formData.farm_name}
                  onChange={handleInputChange}
                  placeholder="e.g., Sarah's Backyard Garden"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Business Name (if any)</label>
                <input
                  type="text"
                  name="business_name"
                  value={formData.business_name}
                  onChange={handleInputChange}
                  placeholder="Leave blank if personal garden"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                />
              </div>
            </div>

            {/* Description */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Tell us about your garden *</label>
              <textarea
                name="farm_description"
                value={formData.farm_description}
                onChange={handleInputChange}
                rows="4"
                placeholder="Describe what you grow, your gardening philosophy, what makes your produce special..."
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                required
              />
            </div>

            {/* Experience */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Experience Level</label>
                <select
                  name="growing_experience_level"
                  value={formData.growing_experience_level}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                >
                  <option value="hobbyist">🌱 Hobbyist (1-3 years)</option>
                  <option value="experienced">🌾 Experienced (3+ years)</option>
                  <option value="professional">👨‍🌾 Professional</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Started Growing</label>
                <select
                  name="established_year"
                  value={formData.established_year}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                >
                  {Array.from({length: 25}, (_, i) => 2025 - i).map(year => (
                    <option key={year} value={year}>{year}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Primary Motivation</label>
                <select
                  name="primary_motivation"
                  value={formData.primary_motivation}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                >
                  <option value="share_excess">🤝 Share Excess Produce</option>
                  <option value="supplement_income">💰 Supplement Income</option>
                  <option value="build_community">🏘️ Build Community</option>
                </select>
              </div>
            </div>

            {/* Contact Information */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Your Name *</label>
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
              <label className="block text-sm font-medium text-gray-700 mb-2">Garden Address *</label>
              <input
                type="text"
                name="farm_address"
                value={formData.farm_address}
                onChange={handleInputChange}
                placeholder="Street address where you grow"
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

            {/* Growing Details */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Growing Area Size</label>
                <input
                  type="number"
                  step="0.01"
                  name="total_acres"
                  value={formData.total_acres}
                  onChange={handleInputChange}
                  placeholder="0.01 acres = ~436 sq ft"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                />
                <p className="text-xs text-gray-500 mt-1">In acres (0.01 = small backyard, 0.25 = large yard)</p>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Growing Space Type</label>
                <select
                  name="growing_area_type"
                  value={formData.growing_area_type}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                >
                  <option value="backyard">🏡 Backyard Garden</option>
                  <option value="community_plot">🤝 Community Garden Plot</option>
                  <option value="rooftop">🏢 Rooftop Garden</option>
                  <option value="greenhouse">🏠 Greenhouse</option>
                  <option value="farm_field">🚜 Farm Field</option>
                </select>
              </div>
            </div>

            {/* What You Grow */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">What do you grow? (Select all that apply)</label>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                {[
                  { value: 'tomatoes', label: '🍅 Tomatoes' },
                  { value: 'peppers', label: '🌶️ Peppers' },
                  { value: 'herbs_spices', label: '🌿 Herbs & Spices' },
                  { value: 'leafy_greens', label: '🥬 Leafy Greens' },
                  { value: 'cucumbers', label: '🥒 Cucumbers' },
                  { value: 'squash_zucchini', label: '🥒 Squash & Zucchini' },
                  { value: 'berries', label: '🫐 Berries' },
                  { value: 'fresh_vegetables', label: '🥕 Other Vegetables' },
                  { value: 'fruits', label: '🍎 Fruits' },
                  { value: 'microgreens', label: '🌱 Microgreens' }
                ].map(product => (
                  <label key={product.value} className="flex items-center space-x-2 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={formData.primary_products.includes(product.value)}
                      onChange={() => handleArrayChange('primary_products', product.value)}
                      className="rounded border-gray-300 text-green-600 focus:ring-green-500"
                    />
                    <span className="text-sm">{product.label}</span>
                  </label>
                ))}
              </div>
            </div>

            {/* Growing Methods */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">Growing Methods (Select all that apply)</label>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                {[
                  { value: 'organic', label: 'Organic' },
                  { value: 'sustainable', label: 'Sustainable' },
                  { value: 'permaculture', label: 'Permaculture' },
                  { value: 'hydroponic', label: 'Hydroponic' },
                  { value: 'conventional', label: 'Conventional' }
                ].map(method => (
                  <label key={method.value} className="flex items-center space-x-2 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={formData.farming_methods.includes(method.value)}
                      onChange={() => handleArrayChange('farming_methods', method.value)}
                      className="rounded border-gray-300 text-green-600 focus:ring-green-500"
                    />
                    <span className="text-sm">{method.label}</span>
                  </label>
                ))}
              </div>
            </div>

            {/* Terms */}
            <div className="space-y-3">
              <label className="flex items-start space-x-3">
                <input
                  type="checkbox"
                  name="terms_accepted"
                  checked={formData.terms_accepted}
                  onChange={handleInputChange}
                  className="rounded border-gray-300 text-green-600 focus:ring-green-500 mt-1"
                  required
                />
                <span className="text-sm text-gray-700">
                  I accept the 15% commission rate on all sales and agree to platform terms & conditions
                </span>
              </label>
              <label className="flex items-start space-x-3">
                <input
                  type="checkbox"
                  name="food_safety_training"
                  checked={formData.food_safety_training}
                  onChange={handleInputChange}
                  className="rounded border-gray-300 text-green-600 focus:ring-green-500 mt-1"
                />
                <span className="text-sm text-gray-700">
                  I commit to basic food safety practices and will complete any required training
                </span>
              </label>
            </div>

            {/* Commission Info */}
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
              <h4 className="font-semibold text-yellow-800 mb-2">💰 Earnings Example</h4>
              <div className="text-sm text-yellow-700 space-y-1">
                <p>• Sell tomatoes for $5/lb → You earn $4.25 (15% platform fee)</p>
                <p>• Join charity program → Earn at 14% rate ($4.30 per lb)</p>
                <p>• Monthly potential: $50-500+ depending on harvest</p>
              </div>
            </div>

            <div className="flex justify-end pt-6">
              <button
                type="submit"
                disabled={submitting}
                className="btn-primary font-medium py-3 px-8 rounded-lg text-lg disabled:opacity-50"
              >
                {submitting ? 'Submitting Application... ⏳' : 'Join Local Marketplace 🌱'}
              </button>
            </div>
          </form>
        </div>
      </div>
    );
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Tab Navigation */}
      <div className="mb-8">
        <div className="flex space-x-1 bg-gray-100 p-1 rounded-lg max-w-2xl mx-auto">
          <button
            onClick={() => setActiveTab('browse')}
            className={`flex-1 px-4 py-2 text-sm font-medium rounded-md transition-all ${
              activeTab === 'browse'
                ? 'bg-white text-green-600 shadow-sm'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            🛒 {t('marketplace.tabs.browse')}
          </button>
          <button
            onClick={() => setActiveTab('sell')}
            className={`flex-1 px-4 py-2 text-sm font-medium rounded-md transition-all ${
              activeTab === 'sell'
                ? 'bg-white text-green-600 shadow-sm'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            🌱 {t('marketplace.tabs.sell')}
          </button>
          <button
            onClick={() => setActiveTab('charity')}
            className={`flex-1 px-4 py-2 text-sm font-medium rounded-md transition-all ${
              activeTab === 'charity'
                ? 'bg-white text-green-600 shadow-sm'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            🤝 {t('marketplace.tabs.charity')}
          </button>
          <button
            onClick={() => setActiveTab('impact')}
            className={`flex-1 px-4 py-2 text-sm font-medium rounded-md transition-all ${
              activeTab === 'impact'
                ? 'bg-white text-green-600 shadow-sm'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            🌍 {t('marketplace.tabs.impact')}
          </button>
        </div>
      </div>

      {/* Tab Content */}
      {activeTab === 'browse' && (
        <div className="space-y-6">
          {/* Header */}
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold heading-gradient mb-4">{t('marketplace.title')}</h2>
            <p className="text-gray-600 mb-6">
              {t('marketplace.subtitle')}
            </p>
            
            {/* Search Filters */}
            <div className="max-w-2xl mx-auto">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                <input
                  type="text"
                  placeholder={t('marketplace.browse.enterPostalCode')}
                  value={postalCode}
                  onChange={(e) => setPostalCode(e.target.value)}
                  className="px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                />
                <select
                  value={filters.vendor_type}
                  onChange={(e) => setFilters({...filters, vendor_type: e.target.value})}
                  className="px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                >
                  <option value="">{t('marketplace.browse.allGrowers')}</option>
                  <option value="backyard_gardener">{t('marketplace.browse.backyardGardeners')}</option>
                  <option value="local_farm">{t('marketplace.browse.localFarms')}</option>
                  <option value="organic_grower">{t('marketplace.browse.organicGrowers')}</option>
                  <option value="hobby_farmer">{t('marketplace.browse.hobbyFarmers')}</option>
                </select>
                <select
                  value={filters.max_distance}
                  onChange={(e) => setFilters({...filters, max_distance: parseInt(e.target.value)})}
                  className="px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                >
                  <option value={10}>{t('marketplace.browse.within10km')}</option>
                  <option value={25}>{t('marketplace.browse.within25km')}</option>
                  <option value={50}>{t('marketplace.browse.within50km')}</option>
                  <option value={100}>{t('marketplace.browse.within100km')}</option>
                </select>
              </div>
              <button
                onClick={fetchLocalFarms}
                className="btn-primary px-6 py-2 rounded-lg"
              >
                {t('marketplace.browse.searchLocalGrowers')}
              </button>
            </div>
          </div>

          <CharityProgramCard />

          {/* Local Farms */}
          <div className="mb-8">
            <h3 className="text-2xl font-bold text-gray-800 mb-4">🌱 Local Growers</h3>
            {loading ? (
              <div className="flex justify-center items-center h-32">
                <div className="loading text-4xl">⏳</div>
              </div>
            ) : localFarms.length === 0 ? (
              <div className="text-center py-8 glass">
                <p className="text-gray-500">No local growers found in this area yet.</p>
                <p className="text-sm text-gray-400 mt-2">Be the first to join and share your garden's bounty!</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {localFarms.map((farm) => (
                  <FarmCard key={farm.id} farm={farm} />
                ))}
              </div>
            )}
          </div>

          {/* Seasonal Products */}
          {farmProducts.length > 0 && (
            <div>
              <h3 className="text-2xl font-bold text-gray-800 mb-4">🌞 Available This Season</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                {farmProducts.slice(0, 8).map((product, index) => (
                  <ProductCard key={index} product={product} />
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {activeTab === 'sell' && <GardenerApplicationForm />}
      {activeTab === 'charity' && <CharityProgramCard />}
      {activeTab === 'impact' && <CommunityImpactDisplay />}
    </div>
  );
};

export default LocalMarketplacePage;