import React, { useState, useEffect } from 'react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const AdminDashboard = () => {
  const [activeTab, setActiveTab] = useState('campaigns');
  const [campaigns, setCampaigns] = useState([]);
  const [showCreateCampaign, setShowCreateCampaign] = useState(false);
  const [campaignForm, setCampaignForm] = useState({
    campaign_name: '',
    campaign_type: 'free_meal',
    description: '',
    discount_type: 'free',
    discount_value: 0,
    total_quota: 150,
    target_cities: ['Champaign'],
    target_states: ['IL'],
    valid_zip_codes: ['61820', '61821', '61822', '61824', '61825', '61826'],
    start_date: '',
    end_date: '',
    minimum_order_amount: 0,
    new_users_only: true
  });
  const [creating, setCreating] = useState(false);
  const [message, setMessage] = useState('');

  const handleCreateCampaign = async (e) => {
    e.preventDefault();
    setCreating(true);
    setMessage('');

    try {
      // Convert dates to ISO format
      const campaignData = {
        ...campaignForm,
        start_date: new Date(campaignForm.start_date).toISOString(),
        end_date: new Date(campaignForm.end_date).toISOString(),
        participating_chef_ids: [],
        all_chefs_eligible: true
      };

      const response = await axios.post(`${API}/campaigns`, campaignData);
      setMessage(`✅ Campaign "${response.data.campaign_name}" created successfully!`);
      setShowCreateCampaign(false);
      setCampaignForm({
        campaign_name: '',
        campaign_type: 'free_meal',
        description: '',
        discount_type: 'free',
        discount_value: 0,
        total_quota: 150,
        target_cities: ['Champaign'],
        target_states: ['IL'],
        valid_zip_codes: ['61820', '61821', '61822', '61824', '61825', '61826'],
        start_date: '',
        end_date: '',
        minimum_order_amount: 0,
        new_users_only: true
      });
    } catch (error) {
      setMessage(`❌ Error: ${error.response?.data?.detail || 'Failed to create campaign'}`);
    }
    setCreating(false);
  };

  return (
    <div className="max-w-7xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">🔧 Admin Dashboard</h1>

      {/* Tabs */}
      <div className="flex space-x-4 mb-6 border-b">
        <button
          onClick={() => setActiveTab('campaigns')}
          className={`px-4 py-2 font-medium ${activeTab === 'campaigns' ? 'border-b-2 border-blue-500 text-blue-600' : 'text-gray-600'}`}
        >
          📢 Campaigns
        </button>
        <button
          onClick={() => setActiveTab('documents')}
          className={`px-4 py-2 font-medium ${activeTab === 'documents' ? 'border-b-2 border-blue-500 text-blue-600' : 'text-gray-600'}`}
        >
          📄 Document Review
        </button>
        <button
          onClick={() => setActiveTab('analytics')}
          className={`px-4 py-2 font-medium ${activeTab === 'analytics' ? 'border-b-2 border-blue-500 text-blue-600' : 'text-gray-600'}`}
        >
          📊 Analytics
        </button>
      </div>

      {message && (
        <div className={`mb-4 p-4 rounded-lg ${message.startsWith('✅') ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
          {message}
        </div>
      )}

      {/* Campaign Management Tab */}
      {activeTab === 'campaigns' && (
        <div>
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold">Campaign Management</h2>
            <button
              onClick={() => setShowCreateCampaign(!showCreateCampaign)}
              className="btn-primary px-6 py-2 rounded-lg"
            >
              {showCreateCampaign ? 'Cancel' : '+ Create Campaign'}
            </button>
          </div>

          {/* Create Campaign Form */}
          {showCreateCampaign && (
            <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
              <h3 className="text-xl font-bold mb-4">Create New Campaign</h3>
              <form onSubmit={handleCreateCampaign} className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-1">Campaign Name</label>
                    <input
                      type="text"
                      value={campaignForm.campaign_name}
                      onChange={(e) => setCampaignForm({...campaignForm, campaign_name: e.target.value})}
                      className="w-full px-3 py-2 border rounded-lg"
                      placeholder="e.g., Lambalia Free Meal Launch - Champaign IL"
                      required
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-1">Campaign Type</label>
                    <select
                      value={campaignForm.campaign_type}
                      onChange={(e) => setCampaignForm({...campaignForm, campaign_type: e.target.value})}
                      className="w-full px-3 py-2 border rounded-lg"
                    >
                      <option value="free_meal">Free Meal</option>
                      <option value="referral">Referral Discount</option>
                      <option value="discount">General Discount</option>
                      <option value="first_order">First Order Special</option>
                    </select>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-1">Description</label>
                  <textarea
                    value={campaignForm.description}
                    onChange={(e) => setCampaignForm({...campaignForm, description: e.target.value})}
                    className="w-full px-3 py-2 border rounded-lg"
                    rows="3"
                    placeholder="Describe the campaign..."
                    required
                  />
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-1">Discount Type</label>
                    <select
                      value={campaignForm.discount_type}
                      onChange={(e) => setCampaignForm({...campaignForm, discount_type: e.target.value})}
                      className="w-full px-3 py-2 border rounded-lg"
                    >
                      <option value="free">Free (100% off)</option>
                      <option value="fixed_amount">Fixed Amount</option>
                      <option value="percentage">Percentage</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-1">Discount Value</label>
                    <input
                      type="number"
                      value={campaignForm.discount_value}
                      onChange={(e) => setCampaignForm({...campaignForm, discount_value: parseFloat(e.target.value)})}
                      className="w-full px-3 py-2 border rounded-lg"
                      placeholder="0 for free"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-1">Total Quota (Codes)</label>
                    <input
                      type="number"
                      value={campaignForm.total_quota}
                      onChange={(e) => setCampaignForm({...campaignForm, total_quota: parseInt(e.target.value)})}
                      className="w-full px-3 py-2 border rounded-lg"
                      required
                    />
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-1">Start Date</label>
                    <input
                      type="datetime-local"
                      value={campaignForm.start_date}
                      onChange={(e) => setCampaignForm({...campaignForm, start_date: e.target.value})}
                      className="w-full px-3 py-2 border rounded-lg"
                      required
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-1">End Date</label>
                    <input
                      type="datetime-local"
                      value={campaignForm.end_date}
                      onChange={(e) => setCampaignForm({...campaignForm, end_date: e.target.value})}
                      className="w-full px-3 py-2 border rounded-lg"
                      required
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-1">Valid Zip Codes (comma-separated)</label>
                  <input
                    type="text"
                    value={campaignForm.valid_zip_codes.join(', ')}
                    onChange={(e) => setCampaignForm({...campaignForm, valid_zip_codes: e.target.value.split(',').map(z => z.trim())})}
                    className="w-full px-3 py-2 border rounded-lg"
                    placeholder="61820, 61821, 61822"
                  />
                </div>

                <div className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    checked={campaignForm.new_users_only}
                    onChange={(e) => setCampaignForm({...campaignForm, new_users_only: e.target.checked})}
                    className="w-4 h-4"
                  />
                  <label className="text-sm">New users only</label>
                </div>

                <button
                  type="submit"
                  disabled={creating}
                  className="w-full btn-primary py-3 rounded-lg font-medium disabled:opacity-50"
                >
                  {creating ? 'Creating Campaign...' : 'Create Campaign'}
                </button>
              </form>
            </div>
          )}

          {/* Campaign List Placeholder */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <p className="text-gray-600">No campaigns yet. Create your first campaign above!</p>
          </div>
        </div>
      )}

      {/* Document Review Tab */}
      {activeTab === 'documents' && (
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h2 className="text-2xl font-bold mb-4">Document Review Queue</h2>
          <p className="text-gray-600">No pending documents to review.</p>
        </div>
      )}

      {/* Analytics Tab */}
      {activeTab === 'analytics' && (
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h2 className="text-2xl font-bold mb-4">Platform Analytics</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-blue-50 p-6 rounded-lg">
              <p className="text-sm text-blue-600 mb-2">Total Users</p>
              <p className="text-3xl font-bold text-blue-900">-</p>
            </div>
            <div className="bg-green-50 p-6 rounded-lg">
              <p className="text-sm text-green-600 mb-2">Active Chefs</p>
              <p className="text-3xl font-bold text-green-900">-</p>
            </div>
            <div className="bg-purple-50 p-6 rounded-lg">
              <p className="text-sm text-purple-600 mb-2">Campaigns Active</p>
              <p className="text-3xl font-bold text-purple-900">-</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdminDashboard;
