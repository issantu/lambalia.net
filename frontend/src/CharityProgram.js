import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useTranslation } from 'react-i18next';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Charity Program - Complete Community Impact System
const CharityProgramPage = () => {
  const { t } = useTranslation();
  const [activeSection, setActiveSection] = useState('overview'); // 'overview', 'register', 'submit', 'dashboard', 'organizations'
  const [charityProgram, setCharityProgram] = useState(null);
  const [communityImpact, setCommunityImpact] = useState(null);
  const [localOrganizations, setLocalOrganizations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [postalCode, setPostalCode] = useState('10001');

  useEffect(() => {
    fetchCharityDashboard();
    fetchCommunityImpact();
  }, []);

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

  const fetchLocalOrganizations = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API}/charity/local-organizations`, {
        params: { postal_code: postalCode }
      });
      setLocalOrganizations(response.data);
    } catch (error) {
      console.error('Failed to fetch local organizations:', error);
    }
    setLoading(false);
  };

  const ProgramOverview = () => (
    <div className="space-y-8">
      <div className="text-center mb-8">
        <h2 className="text-4xl font-bold heading-gradient mb-4">{t('charity.title')}</h2>
        <p className="text-xl text-gray-600 mb-6">
          {t('charity.subtitle')}
        </p>
        <div className="bg-gradient-to-r from-green-100 to-blue-100 p-6 rounded-lg max-w-4xl mx-auto">
          <p className="text-lg text-gray-700">
            <strong>The Problem:</strong> Millions of pounds of homegrown produce go to waste each year while communities struggle with food insecurity.
          </p>
          <p className="text-lg text-gray-700 mt-2">
            <strong>Our Solution:</strong> Connect gardeners, farmers, and home cooks with local food banks, shelters, and community kitchens.
          </p>
        </div>
      </div>

      {/* How It Works */}
      <div className="glass p-8 mb-8">
        <h3 className="text-2xl font-bold text-gray-800 mb-6 text-center">🌱 How It Works</h3>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="text-center">
            <div className="bg-green-100 w-16 h-16 mx-auto rounded-full flex items-center justify-center mb-4">
              <span className="text-2xl">🍅</span>
            </div>
            <h4 className="font-semibold text-gray-800 mb-2">1. Grow & Harvest</h4>
            <p className="text-sm text-gray-600">Tend your backyard garden, grow excess tomatoes, peppers, herbs, or any produce</p>
          </div>
          <div className="text-center">
            <div className="bg-blue-100 w-16 h-16 mx-auto rounded-full flex items-center justify-center mb-4">
              <span className="text-2xl">🏪</span>
            </div>
            <h4 className="font-semibold text-gray-800 mb-2">2. Donate Locally</h4>
            <p className="text-sm text-gray-600">Instead of throwing away surplus, donate to food banks, shelters, or community kitchens</p>
          </div>
          <div className="text-center">
            <div className="bg-purple-100 w-16 h-16 mx-auto rounded-full flex items-center justify-center mb-4">
              <span className="text-2xl">📱</span>
            </div>
            <h4 className="font-semibold text-gray-800 mb-2">3. Submit Evidence</h4>
            <p className="text-sm text-gray-600">Upload photos, receipts, volunteer verification from organizations</p>
          </div>
          <div className="text-center">
            <div className="bg-yellow-100 w-16 h-16 mx-auto rounded-full flex items-center justify-center mb-4">
              <span className="text-2xl">⭐</span>
            </div>
            <h4 className="font-semibold text-gray-800 mb-2">4. Earn Benefits</h4>
            <p className="text-sm text-gray-600">Get premium membership, reduced commission rates, community recognition</p>
          </div>
        </div>
      </div>

      {/* Premium Membership Tiers */}
      <div className="glass p-8 mb-8">
        <h3 className="text-2xl font-bold text-gray-800 mb-6 text-center">🎖️ Premium Membership Tiers</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-green-50 p-6 rounded-lg border-2 border-green-200">
            <div className="text-center mb-4">
              <h4 className="text-xl font-bold text-green-800">Community Helper</h4>
              <p className="text-sm text-green-600">Entry Level</p>
            </div>
            <div className="text-center mb-4">
              <p className="text-3xl font-bold text-green-600">FREE</p>
              <p className="text-sm text-gray-600">Through Charity Work</p>
            </div>
            <div className="space-y-2 mb-4">
              <div className="flex items-center space-x-2">
                <span className="text-green-600">✅</span>
                <span className="text-sm">14% Commission Rate (1% savings)</span>
              </div>
              <div className="flex items-center space-x-2">
                <span className="text-green-600">✅</span>
                <span className="text-sm">Community Helper Badge</span>
              </div>
              <div className="flex items-center space-x-2">
                <span className="text-green-600">✅</span>
                <span className="text-sm">Priority Customer Support</span>
              </div>
              <div className="flex items-center space-x-2">
                <span className="text-green-600">✅</span>
                <span className="text-sm">Monthly Impact Report</span>
              </div>
            </div>
            <div className="border-t pt-4">
              <p className="text-xs text-gray-600"><strong>Requirements:</strong></p>
              <p className="text-xs text-gray-600">• 4 hours monthly volunteering</p>
              <p className="text-xs text-gray-600">• 2 charity activities</p>
              <p className="text-xs text-gray-600">• 5 lbs food donated monthly</p>
            </div>
          </div>

          <div className="bg-blue-50 p-6 rounded-lg border-2 border-blue-200 relative">
            <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
              <span className="bg-blue-600 text-white px-3 py-1 rounded-full text-xs font-bold">POPULAR</span>
            </div>
            <div className="text-center mb-4">
              <h4 className="text-xl font-bold text-blue-800">Garden Supporter</h4>
              <p className="text-sm text-blue-600">Enhanced Benefits</p>
            </div>
            <div className="text-center mb-4">
              <p className="text-3xl font-bold text-blue-600">$4.99/mo</p>
              <p className="text-sm text-gray-600">OR 8 hours charity work</p>
            </div>
            <div className="space-y-2 mb-4">
              <div className="flex items-center space-x-2">
                <span className="text-blue-600">✅</span>
                <span className="text-sm">13% Commission Rate (2% savings)</span>
              </div>
              <div className="flex items-center space-x-2">
                <span className="text-blue-600">✅</span>
                <span className="text-sm">Featured Product Listings</span>
              </div>
              <div className="flex items-center space-x-2">
                <span className="text-blue-600">✅</span>
                <span className="text-sm">Advanced Analytics Dashboard</span>
              </div>
              <div className="flex items-center space-x-2">
                <span className="text-blue-600">✅</span>
                <span className="text-sm">Garden Supporter Badge</span>
              </div>
              <div className="flex items-center space-x-2">
                <span className="text-blue-600">✅</span>
                <span className="text-sm">Seasonal Harvest Calendar</span>
              </div>
            </div>
            <div className="border-t pt-4">
              <p className="text-xs text-gray-600"><strong>Requirements:</strong></p>
              <p className="text-xs text-gray-600">• 8 hours monthly volunteering</p>
              <p className="text-xs text-gray-600">• 3 charity activities</p>
              <p className="text-xs text-gray-600">• 15 lbs food donated monthly</p>
            </div>
          </div>

          <div className="bg-purple-50 p-6 rounded-lg border-2 border-purple-200">
            <div className="text-center mb-4">
              <h4 className="text-xl font-bold text-purple-800">Local Champion</h4>
              <p className="text-sm text-purple-600">Premium Experience</p>
            </div>
            <div className="text-center mb-4">
              <p className="text-3xl font-bold text-purple-600">$9.99/mo</p>
              <p className="text-sm text-gray-600">OR 12 hours charity work</p>
            </div>
            <div className="space-y-2 mb-4">
              <div className="flex items-center space-x-2">
                <span className="text-purple-600">✅</span>
                <span className="text-sm">12% Commission Rate (3% savings)</span>
              </div>
              <div className="flex items-center space-x-2">
                <span className="text-purple-600">✅</span>
                <span className="text-sm">Premium Product Placement</span>
              </div>
              <div className="flex items-center space-x-2">
                <span className="text-purple-600">✅</span>
                <span className="text-sm">Local Champion Badge</span>
              </div>
              <div className="flex items-center space-x-2">
                <span className="text-purple-600">✅</span>
                <span className="text-sm">Exclusive Community Events</span>
              </div>
              <div className="flex items-center space-x-2">
                <span className="text-purple-600">✅</span>
                <span className="text-sm">Advanced Marketing Tools</span>
              </div>
              <div className="flex items-center space-x-2">
                <span className="text-purple-600">✅</span>
                <span className="text-sm">Direct Customer Messaging</span>
              </div>
            </div>
            <div className="border-t pt-4">
              <p className="text-xs text-gray-600"><strong>Requirements:</strong></p>
              <p className="text-xs text-gray-600">• 12 hours monthly volunteering</p>
              <p className="text-xs text-gray-600">• 5 charity activities</p>
              <p className="text-xs text-gray-600">• 30 lbs food donated monthly</p>
            </div>
          </div>
        </div>
      </div>

      {/* Call to Action */}
      <div className="text-center">
        <button
          onClick={() => setActiveSection('register')}
          className="btn-primary text-xl font-bold py-4 px-8 rounded-lg"
        >
          Join Community Program 🌱
        </button>
        <p className="text-gray-600 mt-4">Start making a difference in your community today!</p>
      </div>
    </div>
  );

  const RegistrationForm = () => {
    const [formData, setFormData] = useState({
      committed_hours_per_month: 4,
      preferred_charity_types: [],
      preferred_locations: [postalCode],
      monthly_impact_goal: 50.0
    });
    const [submitting, setSubmitting] = useState(false);

    const handleInputChange = (e) => {
      const { name, value, type } = e.target;
      setFormData(prev => ({
        ...prev,
        [name]: type === 'number' ? parseFloat(value) || 0 : value
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
        const response = await axios.post(`${API}/charity/register`, formData);
        
        if (response.data.success) {
          alert('🎉 Welcome to the Community Food Sharing Program! Start making a positive impact in your community.');
          setActiveSection('dashboard');
          fetchCharityDashboard();
        }
      } catch (error) {
        console.error('Failed to register for charity program:', error);
        alert('Registration failed. Please try again.');
      }
      setSubmitting(false);
    };

    return (
      <div className="max-w-2xl mx-auto">
        <div className="glass p-8">
          <h3 className="text-2xl font-bold heading-gradient mb-6">Join the Community Program</h3>
          <p className="text-gray-600 mb-6">
            Registration is quick and free. Choose your commitment level and start earning premium benefits through community service.
          </p>
          
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Monthly Volunteer Hours Commitment
              </label>
              <select
                name="committed_hours_per_month"
                value={formData.committed_hours_per_month}
                onChange={handleInputChange}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
              >
                <option value={2}>2 hours/month (Minimum)</option>
                <option value={4}>4 hours/month (Community Helper)</option>
                <option value={8}>8 hours/month (Garden Supporter)</option>
                <option value={12}>12 hours/month (Local Champion)</option>
                <option value={16}>16 hours/month (Super Volunteer)</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">
                Preferred Charity Activities (Select all that interest you)
              </label>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {[
                  { value: 'food_bank', label: '🏪 Food Bank Volunteering' },
                  { value: 'homeless_shelter', label: '🏠 Homeless Shelter Support' },
                  { value: 'community_kitchen', label: '👩‍🍳 Community Kitchen' },
                  { value: 'seniors_center', label: '👵 Seniors Center' },
                  { value: 'school_program', label: '🏫 School Programs' },
                  { value: 'emergency_relief', label: '🚨 Emergency Relief' }
                ].map(type => (
                  <label key={type.value} className="flex items-center space-x-3 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={formData.preferred_charity_types.includes(type.value)}
                      onChange={() => handleArrayChange('preferred_charity_types', type.value)}
                      className="rounded border-gray-300 text-green-600 focus:ring-green-500"
                    />
                    <span className="text-sm">{type.label}</span>
                  </label>
                ))}
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Monthly Impact Goal (Points)
              </label>
              <select
                name="monthly_impact_goal"
                value={formData.monthly_impact_goal}
                onChange={handleInputChange}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
              >
                <option value={30}>30 points (Community Helper)</option>
                <option value={50}>50 points (Balanced)</option>
                <option value={75}>75 points (Garden Supporter)</option>
                <option value={120}>120 points (Local Champion)</option>
                <option value={200}>200 points (Super Volunteer)</option>
              </select>
              <p className="text-xs text-gray-500 mt-1">
                Examples: 10 lbs food donated = 20 points, 1 hour volunteering = 8 points, 1 meal served = 5 points
              </p>
            </div>

            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h4 className="font-semibold text-blue-800 mb-2">🎯 Your Plan</h4>
              <div className="text-sm text-blue-700 space-y-1">
                <p>• {formData.committed_hours_per_month} hours monthly volunteering</p>
                <p>• {formData.monthly_impact_goal} impact points goal</p>
                <p>• {formData.preferred_charity_types.length} charity activity types selected</p>
                <p>• Premium tier: {
                  formData.committed_hours_per_month >= 12 ? 'Local Champion' :
                  formData.committed_hours_per_month >= 8 ? 'Garden Supporter' :
                  'Community Helper'
                }</p>
              </div>
            </div>

            <div className="flex justify-end pt-6">
              <button
                type="submit"
                disabled={submitting}
                className="btn-primary font-medium py-3 px-8 rounded-lg text-lg disabled:opacity-50"
              >
                {submitting ? 'Joining Program... ⏳' : 'Join Community Program 🤝'}
              </button>
            </div>
          </form>
        </div>
      </div>
    );
  };

  const ActivitySubmissionForm = () => {
    const [formData, setFormData] = useState({
      activity_type: 'food_bank',
      charity_organization_name: '',
      activity_description: '',
      activity_date: new Date().toISOString().split('T')[0],
      food_donated_lbs: '',
      meals_provided: '',
      people_helped: '',
      volunteer_hours: '',
      location_address: '',
      city: '',
      state: '',
      postal_code: postalCode,
      photo_urls: [],
      video_urls: [],
      witness_contacts: []
    });
    const [submitting, setSubmitting] = useState(false);
    const [impactPreview, setImpactPreview] = useState(null);

    const calculateImpactPreview = async () => {
      try {
        const params = new URLSearchParams({
          activity_type: formData.activity_type,
          ...(formData.food_donated_lbs && { food_donated_lbs: formData.food_donated_lbs }),
          ...(formData.meals_provided && { meals_provided: formData.meals_provided }),
          ...(formData.people_helped && { people_helped: formData.people_helped }),
          ...(formData.volunteer_hours && { volunteer_hours: formData.volunteer_hours })
        });

        const response = await axios.get(`${API}/charity/impact-calculator?${params}`);
        setImpactPreview(response.data);
      } catch (error) {
        console.error('Failed to calculate impact preview:', error);
      }
    };

    useEffect(() => {
      if (formData.food_donated_lbs || formData.meals_provided || formData.people_helped || formData.volunteer_hours) {
        calculateImpactPreview();
      }
    }, [formData.food_donated_lbs, formData.meals_provided, formData.people_helped, formData.volunteer_hours, formData.activity_type]);

    const handleInputChange = (e) => {
      const { name, value, type } = e.target;
      setFormData(prev => ({
        ...prev,
        [name]: type === 'number' ? (value ? parseFloat(value) : '') : value
      }));
    };

    const handleSubmit = async (e) => {
      e.preventDefault();
      setSubmitting(true);

      try {
        const submitData = {
          ...formData,
          activity_date: new Date(formData.activity_date).toISOString()
        };

        const response = await axios.post(`${API}/charity/submit-activity`, submitData);
        
        if (response.data.success) {
          alert(`🎉 Activity submitted successfully! You earned ${response.data.impact_score} impact points. Your activity is now under committee review.`);
          setActiveSection('dashboard');
          fetchCharityDashboard();
        }
      } catch (error) {
        console.error('Failed to submit charity activity:', error);
        alert('Submission failed. Please try again.');
      }
      setSubmitting(false);
    };

    return (
      <div className="max-w-4xl mx-auto">
        <div className="glass p-8">
          <h3 className="text-2xl font-bold heading-gradient mb-6">Submit Charity Activity</h3>
          <p className="text-gray-600 mb-6">
            Document your volunteer work and food donations to earn impact points and premium benefits.
          </p>
          
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Activity Type *</label>
                <select
                  name="activity_type"
                  value={formData.activity_type}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                  required
                >
                  <option value="food_bank">🏪 Food Bank Volunteering</option>
                  <option value="homeless_shelter">🏠 Homeless Shelter</option>
                  <option value="community_kitchen">👩‍🍳 Community Kitchen</option>
                  <option value="seniors_center">👵 Seniors Center</option>
                  <option value="school_program">🏫 School Program</option>
                  <option value="emergency_relief">🚨 Emergency Relief</option>
                  <option value="local_charity">❤️ Local Charity</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Activity Date *</label>
                <input
                  type="date"
                  name="activity_date"
                  value={formData.activity_date}
                  onChange={handleInputChange}
                  max={new Date().toISOString().split('T')[0]}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                  required
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Organization Name *</label>
              <input
                type="text"
                name="charity_organization_name"
                value={formData.charity_organization_name}
                onChange={handleInputChange}
                placeholder="e.g., Downtown Food Bank, Community Shelter"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Activity Description *</label>
              <textarea
                name="activity_description"
                value={formData.activity_description}
                onChange={handleInputChange}
                rows="3"
                placeholder="Describe what you did, who you helped, and any special circumstances..."
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                required
              />
            </div>

            {/* Impact Metrics */}
            <div className="bg-green-50 border border-green-200 rounded-lg p-4">
              <h4 className="font-semibold text-green-800 mb-3">🎯 Impact Metrics (Fill what applies)</h4>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div>
                  <label className="block text-sm font-medium text-green-700 mb-1">Food Donated (lbs)</label>
                  <input
                    type="number"
                    step="0.1"
                    name="food_donated_lbs"
                    value={formData.food_donated_lbs}
                    onChange={handleInputChange}
                    placeholder="0"
                    className="w-full px-3 py-2 border border-green-300 rounded focus:outline-none focus:ring-2 focus:ring-green-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-green-700 mb-1">Meals Provided</label>
                  <input
                    type="number"
                    name="meals_provided"
                    value={formData.meals_provided}
                    onChange={handleInputChange}
                    placeholder="0"
                    className="w-full px-3 py-2 border border-green-300 rounded focus:outline-none focus:ring-2 focus:ring-green-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-green-700 mb-1">People Helped</label>
                  <input
                    type="number"
                    name="people_helped"
                    value={formData.people_helped}
                    onChange={handleInputChange}
                    placeholder="0"
                    className="w-full px-3 py-2 border border-green-300 rounded focus:outline-none focus:ring-2 focus:ring-green-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-green-700 mb-1">Volunteer Hours</label>
                  <input
                    type="number"
                    step="0.5"
                    name="volunteer_hours"
                    value={formData.volunteer_hours}
                    onChange={handleInputChange}
                    placeholder="0"
                    className="w-full px-3 py-2 border border-green-300 rounded focus:outline-none focus:ring-2 focus:ring-green-500"
                  />
                </div>
              </div>
              
              {impactPreview && (
                <div className="mt-4 p-3 bg-white rounded-lg">
                  <p className="text-sm font-medium text-green-800">
                    Estimated Impact Score: {impactPreview.estimated_impact_score} points
                  </p>
                  {impactPreview.next_tier_info && (
                    <p className="text-xs text-green-600 mt-1">
                      Progress toward {impactPreview.next_tier_info.tier_name}: {impactPreview.next_tier_info.progress_percentage}%
                    </p>
                  )}
                </div>
              )}
            </div>

            {/* Location */}
            <div>
              <h4 className="font-semibold text-gray-800 mb-3">📍 Location</h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Address *</label>
                  <input
                    type="text"
                    name="location_address"
                    value={formData.location_address}
                    onChange={handleInputChange}
                    placeholder="Organization address"
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">City *</label>
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
                  <label className="block text-sm font-medium text-gray-700 mb-1">State *</label>
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
                  <label className="block text-sm font-medium text-gray-700 mb-1">Postal Code *</label>
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
            </div>

            <div className="flex justify-end pt-6">
              <button
                type="submit"
                disabled={submitting}
                className="btn-primary font-medium py-3 px-8 rounded-lg text-lg disabled:opacity-50"
              >
                {submitting ? 'Submitting Activity... ⏳' : 'Submit for Verification 📋'}
              </button>
            </div>
          </form>
        </div>
      </div>
    );
  };

  const Dashboard = () => {
    if (!charityProgram || !charityProgram.success) {
      return (
        <div className="text-center py-12">
          <h3 className="text-2xl font-bold text-gray-800 mb-4">Not Enrolled Yet</h3>
          <p className="text-gray-600 mb-6">Join the Community Food Sharing Program to start earning premium benefits through charity work.</p>
          <button
            onClick={() => setActiveSection('register')}
            className="btn-primary px-6 py-3 rounded-lg"
          >
            Join Program 🤝
          </button>
        </div>
      );
    }

    const stats = charityProgram.statistics || {};
    const ranking = charityProgram.community_ranking || {};
    const membership = charityProgram.membership_info || {};

    return (
      <div className="space-y-8">
        <div className="text-center mb-8">
          <h2 className="text-3xl font-bold heading-gradient mb-4">🎯 Your Impact Dashboard</h2>
          <p className="text-gray-600">Track your community contributions and premium benefits</p>
        </div>

        {/* Current Status */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="glass p-6 text-center">
            <div className="text-3xl mb-2">🏆</div>
            <p className="text-2xl font-bold text-green-600">{stats.monthly_impact || 0}</p>
            <p className="text-sm text-gray-600">This Month's Impact</p>
          </div>
          
          <div className="glass p-6 text-center">
            <div className="text-3xl mb-2">📊</div>
            <p className="text-2xl font-bold text-blue-600">#{ranking.rank || 'N/A'}</p>
            <p className="text-sm text-gray-600">Community Rank</p>
          </div>
          
          <div className="glass p-6 text-center">
            <div className="text-3xl mb-2">⭐</div>
            <p className="text-2xl font-bold text-purple-600">{membership.tier?.replace('_', ' ') || 'Community Helper'}</p>
            <p className="text-sm text-gray-600">Premium Tier</p>
          </div>
          
          <div className="glass p-6 text-center">
            <div className="text-3xl mb-2">💰</div>
            <p className="text-2xl font-bold text-orange-600">{membership.commission_rate || '14'}%</p>
            <p className="text-sm text-gray-600">Commission Rate</p>
          </div>
        </div>

        {/* Recent Activities */}
        {charityProgram.recent_activities && charityProgram.recent_activities.length > 0 && (
          <div className="glass p-6 mb-8">
            <h4 className="text-xl font-semibold mb-4">📋 Recent Activities</h4>
            <div className="space-y-3">
              {charityProgram.recent_activities.slice(0, 5).map((activity, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div>
                    <p className="font-medium text-gray-800">{activity.charity_organization_name}</p>
                    <p className="text-sm text-gray-600">{activity.activity_type.replace('_', ' ')} • {new Date(activity.activity_date).toLocaleDateString()}</p>
                  </div>
                  <div className="text-right">
                    <p className="font-bold text-green-600">{activity.calculated_impact_score} pts</p>
                    <p className="text-xs text-gray-500">{activity.verification_status}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <button
            onClick={() => setActiveSection('submit')}
            className="glass p-6 text-left hover:shadow-lg transition-all"
          >
            <div className="flex items-center space-x-4">
              <div className="bg-green-100 w-12 h-12 rounded-full flex items-center justify-center">
                <span className="text-2xl">📝</span>
              </div>
              <div>
                <h4 className="font-semibold text-gray-800">Submit New Activity</h4>
                <p className="text-sm text-gray-600">Log your volunteer work and donations</p>
              </div>
            </div>
          </button>
          
          <button
            onClick={() => setActiveSection('organizations')}
            className="glass p-6 text-left hover:shadow-lg transition-all"
          >
            <div className="flex items-center space-x-4">
              <div className="bg-blue-100 w-12 h-12 rounded-full flex items-center justify-center">
                <span className="text-2xl">🏪</span>
              </div>
              <div>
                <h4 className="font-semibold text-gray-800">Find Organizations</h4>
                <p className="text-sm text-gray-600">Discover local volunteer opportunities</p>
              </div>
            </div>
          </button>
        </div>
      </div>
    );
  };

  const LocalOrganizations = () => (
    <div className="space-y-6">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold heading-gradient mb-4">🏪 Local Organizations</h2>
        <p className="text-gray-600 mb-6">Find volunteer opportunities near you</p>
        
        <div className="flex items-center justify-center space-x-4">
          <input
            type="text"
            placeholder="Enter postal code"
            value={postalCode}
            onChange={(e) => setPostalCode(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
          />
          <button
            onClick={fetchLocalOrganizations}
            disabled={loading}
            className="btn-primary px-6 py-2 rounded-lg disabled:opacity-50"
          >
            {loading ? 'Searching...' : 'Find Organizations'}
          </button>
        </div>
      </div>

      {localOrganizations.length === 0 ? (
        <div className="text-center py-8 glass">
          <p className="text-gray-500">Click "Find Organizations" to discover local volunteer opportunities.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {localOrganizations.map((org, index) => (
            <div key={index} className="glass p-6">
              <div className="flex items-start justify-between mb-3">
                <div>
                  <h4 className="font-semibold text-gray-800">{org.name}</h4>
                  <p className="text-sm text-gray-500 capitalize">{org.type.replace('_', ' ')}</p>
                </div>
                <span className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded-full">
                  Active
                </span>
              </div>
              
              <p className="text-gray-600 mb-3 text-sm">{org.description}</p>
              
              <div className="space-y-2 mb-4">
                <div className="flex items-center text-sm text-gray-600">
                  <span className="font-medium mr-2">📍</span>
                  <span>{org.address}</span>
                </div>
                <div className="flex items-center text-sm text-gray-600">
                  <span className="font-medium mr-2">📞</span>
                  <span>{org.phone}</span>
                </div>
                <div className="flex items-center text-sm text-gray-600">
                  <span className="font-medium mr-2">✉️</span>
                  <span>{org.email}</span>
                </div>
              </div>

              {org.volunteer_opportunities && (
                <div className="mb-4">
                  <p className="text-sm font-medium text-gray-700 mb-2">🤝 Volunteer Opportunities:</p>
                  <div className="flex flex-wrap gap-1">
                    {org.volunteer_opportunities.slice(0, 3).map((opp, idx) => (
                      <span key={idx} className="bg-blue-100 text-blue-700 text-xs px-2 py-1 rounded">
                        {opp}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {org.current_needs && org.current_needs.length > 0 && (
                <div className="mb-4">
                  <p className="text-sm font-medium text-gray-700 mb-2">🎯 Current Needs:</p>
                  <div className="text-xs text-gray-600">
                    {org.current_needs.join(', ')}
                  </div>
                </div>
              )}

              {org.impact_last_month && (
                <div className="bg-green-50 p-3 rounded-lg">
                  <p className="text-sm font-semibold text-green-800 mb-1">Last Month's Impact:</p>
                  <div className="grid grid-cols-3 gap-2 text-xs text-green-700">
                    <div className="text-center">
                      <p className="font-bold">{org.impact_last_month.people_served}</p>
                      <p>People</p>
                    </div>
                    <div className="text-center">
                      <p className="font-bold">{org.impact_last_month.meals_provided}</p>
                      <p>Meals</p>
                    </div>
                    <div className="text-center">
                      <p className="font-bold">{org.impact_last_month.volunteer_hours}</p>
                      <p>Hours</p>
                    </div>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Tab Navigation */}
      <div className="mb-8">
        <div className="flex space-x-1 bg-gray-100 p-1 rounded-lg max-w-4xl mx-auto">
          <button
            onClick={() => setActiveSection('overview')}
            className={`flex-1 px-4 py-2 text-sm font-medium rounded-md transition-all ${
              activeSection === 'overview'
                ? 'bg-white text-green-600 shadow-sm'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            🌟 Overview
          </button>
          <button
            onClick={() => setActiveSection('register')}
            className={`flex-1 px-4 py-2 text-sm font-medium rounded-md transition-all ${
              activeSection === 'register'
                ? 'bg-white text-green-600 shadow-sm'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            📝 Register
          </button>
          <button
            onClick={() => setActiveSection('submit')}
            className={`flex-1 px-4 py-2 text-sm font-medium rounded-md transition-all ${
              activeSection === 'submit'
                ? 'bg-white text-green-600 shadow-sm'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            📋 Submit Activity
          </button>
          <button
            onClick={() => setActiveSection('dashboard')}
            className={`flex-1 px-4 py-2 text-sm font-medium rounded-md transition-all ${
              activeSection === 'dashboard'
                ? 'bg-white text-green-600 shadow-sm'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            🎯 Dashboard
          </button>
          <button
            onClick={() => setActiveSection('organizations')}
            className={`flex-1 px-4 py-2 text-sm font-medium rounded-md transition-all ${
              activeSection === 'organizations'
                ? 'bg-white text-green-600 shadow-sm'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            🏪 Organizations
          </button>
        </div>
      </div>

      {/* Tab Content */}
      <div className="mb-8">
        {activeSection === 'overview' && <ProgramOverview />}
        {activeSection === 'register' && <RegistrationForm />}
        {activeSection === 'submit' && <ActivitySubmissionForm />}
        {activeSection === 'dashboard' && <Dashboard />}
        {activeSection === 'organizations' && <LocalOrganizations />}
      </div>

      {/* Community Impact Display */}
      {communityImpact && (
        <div className="glass p-8 mt-8">
          <h3 className="text-2xl font-bold text-gray-800 mb-6 text-center">🌍 Platform Community Impact</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            <div className="text-center">
              <p className="text-2xl font-bold text-green-600">{communityImpact.total_food_donated_lbs || 0}</p>
              <p className="text-sm text-gray-600">Pounds Donated</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-blue-600">{communityImpact.total_meals_provided || 0}</p>
              <p className="text-sm text-gray-600">Meals Provided</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-purple-600">{communityImpact.total_people_helped || 0}</p>
              <p className="text-sm text-gray-600">People Helped</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-orange-600">{communityImpact.active_participants || 0}</p>
              <p className="text-sm text-gray-600">Active Volunteers</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CharityProgramPage;