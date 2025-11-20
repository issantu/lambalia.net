import React, { useState, useEffect } from 'react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const UserProfileExtended = ({ user }) => {
  const [userTypes, setUserTypes] = useState(null);
  const [promoCodes, setPromoCodes] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchUserData();
  }, []);

  const fetchUserData = async () => {
    try {
      const [typesResponse, codesResponse] = await Promise.all([
        axios.get(`${API}/user/types`),
        axios.get(`${API}/user/promo-codes`)
      ]);
      setUserTypes(typesResponse.data);
      setPromoCodes(codesResponse.data.promo_codes || []);
    } catch (error) {
      console.error('Failed to fetch user data:', error);
    }
    setLoading(false);
  };

  if (loading) {
    return <div className="text-center py-8">Loading profile...</div>;
  }

  const getRoleBadge = (role) => {
    const badges = {
      'food_enthusiast': { icon: '🍽️', label: 'Food Enthusiast', color: 'bg-blue-100 text-blue-800' },
      'home_chef': { icon: '👨‍🍳', label: 'Home Chef', color: 'bg-green-100 text-green-800' },
      'home_restaurant': { icon: '🏠', label: 'Home Restaurant', color: 'bg-purple-100 text-purple-800' },
      'recipe_creator': { icon: '📝', label: 'Recipe Creator', color: 'bg-yellow-100 text-yellow-800' },
      'food_reviewer': { icon: '⭐', label: 'Food Reviewer', color: 'bg-pink-100 text-pink-800' },
      'farm_vendor': { icon: '🌾', label: 'Farm Vendor', color: 'bg-orange-100 text-orange-800' }
    };
    return badges[role] || { icon: '👤', label: role, color: 'bg-gray-100 text-gray-800' };
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      {/* User Roles Section */}
      <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
        <h2 className="text-2xl font-bold mb-4">Your Roles on Lambalia</h2>
        <div className="flex flex-wrap gap-3 mb-4">
          {userTypes?.user_types.map((role) => {
            const badge = getRoleBadge(role);
            return (
              <div
                key={role}
                className={`${badge.color} px-4 py-2 rounded-full font-medium flex items-center space-x-2`}
              >
                <span>{badge.icon}</span>
                <span>{badge.label}</span>
                {role === userTypes.primary_type && (
                  <span className="ml-2 bg-white px-2 py-0.5 rounded text-xs">Primary</span>
                )}
              </div>
            );
          })}
        </div>

        {/* Capabilities */}
        <div className="bg-gray-50 p-4 rounded-lg">
          <p className="text-sm font-medium text-gray-700 mb-2">What you can do:</p>
          <ul className="space-y-1 text-sm text-gray-600">
            {userTypes?.can_sell_packaged_foods && (
              <li>✅ Sell packaged foods (cottage food)</li>
            )}
            {userTypes?.can_serve_meals && (
              <li>✅ Serve meals at home</li>
            )}
            {userTypes?.can_create_content && (
              <li>✅ Create and share recipes</li>
            )}
            {userTypes?.can_review && (
              <li>✅ Write reviews and ratings</li>
            )}
            <li>✅ Browse and buy food from other chefs</li>
          </ul>
        </div>

        <div className="mt-4 text-center">
          <button className="text-blue-600 hover:text-blue-700 font-medium text-sm">
            + Add New Role
          </button>
        </div>
      </div>

      {/* Location Info */}
      {userTypes && (
        <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
          <h3 className="text-xl font-bold mb-4">📍 Location</h3>
          <div className="flex items-center space-x-2">
            <span className="text-2xl">🗺️</span>
            <div>
              <p className="font-medium">{userTypes.state_name}</p>
              <p className="text-sm text-gray-600">
                {userTypes.state_category === 'food_freedom' ? '✨ Food Freedom State' : 
                 userTypes.state_category === 'permissive' ? '🟢 Permissive State' :
                 userTypes.state_category === 'moderate' ? '🟡 Moderate State' :
                 '🔴 Restrictive State'}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Promo Codes Section */}
      {promoCodes.length > 0 && (
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-xl font-bold mb-4">🎟️ Your Promo Codes</h3>
          <div className="space-y-4">
            {promoCodes.map((promo, idx) => (
              <div key={idx} className="border border-green-300 rounded-lg p-4 bg-gradient-to-r from-green-50 to-blue-50">
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <p className="text-2xl font-bold text-green-600 tracking-wider">{promo.code}</p>
                    <p className="text-sm text-gray-700 mt-1">{promo.campaign_name}</p>
                  </div>
                  <div className={`px-3 py-1 rounded-full text-xs font-medium ${
                    promo.status === 'active' ? 'bg-green-200 text-green-800' :
                    promo.status === 'redeemed' ? 'bg-gray-200 text-gray-800' :
                    'bg-red-200 text-red-800'
                  }`}>
                    {promo.status}
                  </div>
                </div>
                <p className="text-green-800 font-medium mb-2">💰 {promo.discount_description}</p>
                <p className="text-sm text-gray-600 mb-2">{promo.instructions}</p>
                <p className="text-xs text-gray-500">
                  Valid until: {new Date(promo.valid_until).toLocaleDateString()}
                  {promo.redemptions_remaining > 0 && ` • ${promo.redemptions_remaining} use remaining`}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* No Promo Codes Message */}
      {promoCodes.length === 0 && (
        <div className="bg-gray-50 rounded-xl p-8 text-center">
          <p className="text-4xl mb-4">🎟️</p>
          <p className="text-gray-600 mb-2">No active promo codes</p>
          <p className="text-sm text-gray-500">Check back during promotional campaigns!</p>
        </div>
      )}
    </div>
  );
};

export default UserProfileExtended;
