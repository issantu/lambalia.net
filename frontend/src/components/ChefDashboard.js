import React, { useState, useEffect } from 'react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const ChefDashboard = ({ user }) => {
  const [compliance, setCompliance] = useState(null);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [selectedDocType, setSelectedDocType] = useState('');
  const [documentFile, setDocumentFile] = useState(null);
  const [documentDetails, setDocumentDetails] = useState({
    document_number: '',
    issued_date: '',
    expiry_date: ''
  });
  const [uploadSuccess, setUploadSuccess] = useState('');
  const [uploadError, setUploadError] = useState('');

  useEffect(() => {
    fetchCompliance();
  }, []);

  const fetchCompliance = async () => {
    try {
      const response = await axios.get(`${API}/chef/compliance`);
      setCompliance(response.data);
    } catch (error) {
      console.error('Failed to fetch compliance:', error);
    }
    setLoading(false);
  };

  const handleFileChange = (e) => {
    setDocumentFile(e.target.files[0]);
  };

  const handleDocumentUpload = async (e) => {
    e.preventDefault();
    if (!documentFile || !selectedDocType) {
      setUploadError('Please select document type and file');
      return;
    }

    setUploading(true);
    setUploadError('');
    setUploadSuccess('');

    const formData = new FormData();
    formData.append('file', documentFile);
    formData.append('document_type', selectedDocType);
    formData.append('document_number', documentDetails.document_number);
    formData.append('issued_date', documentDetails.issued_date);
    formData.append('expiry_date', documentDetails.expiry_date);

    try {
      await axios.post(`${API}/chef/compliance/documents/upload`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setUploadSuccess('Document uploaded successfully! Pending admin review.');
      setDocumentFile(null);
      setSelectedDocType('');
      setDocumentDetails({ document_number: '', issued_date: '', expiry_date: '' });
      // Refresh compliance data
      fetchCompliance();
    } catch (error) {
      setUploadError(error.response?.data?.detail || 'Upload failed');
    }
    setUploading(false);
  };

  const getTierBadge = (tier) => {
    const badges = {
      'fully_certified': { text: '🌟 Fully Certified', color: 'bg-green-100 text-green-800' },
      'certified_no_insurance': { text: '✅ Certified', color: 'bg-yellow-100 text-yellow-800' },
      'pending': { text: '⏳ Pending', color: 'bg-gray-100 text-gray-800' }
    };
    return badges[tier] || badges.pending;
  };

  if (loading) {
    return <div className="text-center py-8">Loading your compliance dashboard...</div>;
  }

  if (!compliance) {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <div className="bg-yellow-50 border border-yellow-300 rounded-lg p-6">
          <h2 className="text-xl font-bold text-yellow-900 mb-2">👨‍🍳 Become a Chef</h2>
          <p className="text-yellow-800 mb-4">
            You haven't set up your chef profile yet. To start selling food, you need to complete compliance requirements.
          </p>
          <button className="btn-primary py-2 px-6 rounded-lg">
            Start Chef Application
          </button>
        </div>
      </div>
    );
  }

  const tierBadge = getTierBadge(compliance.tier);
  const salesPercentage = compliance.sales_limit 
    ? (compliance.annual_sales / compliance.sales_limit) * 100 
    : 0;

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">👨‍🍳 Chef Compliance Dashboard</h1>

      {/* Compliance Status Card */}
      <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">{user.full_name || user.username}</h2>
            <p className="text-gray-600">{compliance.state_name}</p>
          </div>
          <div className={`px-4 py-2 rounded-full ${tierBadge.color} font-semibold`}>
            {tierBadge.text}
          </div>
        </div>

        {/* Badges */}
        {compliance.badges.length > 0 && (
          <div className="flex flex-wrap gap-2 mb-4">
            {compliance.badges.map((badge, idx) => (
              <span key={idx} className="bg-blue-100 text-blue-800 text-sm px-3 py-1 rounded-full">
                {badge}
              </span>
            ))}
          </div>
        )}

        {/* Order Limits */}
        {compliance.daily_order_limit && (
          <div className="bg-orange-50 border border-orange-200 rounded-lg p-4 mb-4">
            <p className="text-orange-900 font-medium">
              ⚠️ Daily Order Limit: {compliance.daily_order_limit} orders per day
            </p>
            <p className="text-sm text-orange-700 mt-1">
              Upgrade to unlimited by adding liability insurance
            </p>
          </div>
        )}

        {/* Warnings */}
        {compliance.warnings.length > 0 && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-4">
            {compliance.warnings.map((warning, idx) => (
              <p key={idx} className="text-red-800">⚠️ {warning}</p>
            ))}
          </div>
        )}

        {/* Sales Tracking */}
        {compliance.sales_limit && (
          <div className="mb-4">
            <div className="flex justify-between text-sm mb-2">
              <span className="text-gray-600">Annual Sales</span>
              <span className="font-semibold">
                ${compliance.annual_sales.toFixed(2)} / ${compliance.sales_limit.toFixed(2)}
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-3">
              <div 
                className={`h-3 rounded-full ${salesPercentage > 90 ? 'bg-red-500' : salesPercentage > 75 ? 'bg-yellow-500' : 'bg-green-500'}`}
                style={{ width: `${Math.min(salesPercentage, 100)}%` }}
              ></div>
            </div>
          </div>
        )}
      </div>

      {/* Document Status */}
      <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
        <h3 className="text-xl font-bold mb-4">📄 Required Documents</h3>
        
        <div className="space-y-3 mb-6">
          {compliance.documents_required.map((docType) => {
            const uploaded = compliance.documents_uploaded.includes(docType);
            const verified = compliance.documents_verified.includes(docType);
            
            return (
              <div key={docType} className="flex items-center justify-between p-3 border rounded-lg">
                <div className="flex items-center space-x-3">
                  {verified ? (
                    <span className="text-2xl">✅</span>
                  ) : uploaded ? (
                    <span className="text-2xl">⏳</span>
                  ) : (
                    <span className="text-2xl">❌</span>
                  )}
                  <div>
                    <p className="font-medium capitalize">
                      {docType.replace(/_/g, ' ')}
                    </p>
                    <p className="text-sm text-gray-600">
                      {verified ? 'Verified ✓' : uploaded ? 'Pending Review' : 'Not Uploaded'}
                    </p>
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {/* Upload Form */}
        <div className="border-t pt-6">
          <h4 className="font-bold mb-4">Upload New Document</h4>
          
          {uploadSuccess && (
            <div className="bg-green-100 border border-green-400 text-green-800 px-4 py-3 rounded mb-4">
              {uploadSuccess}
            </div>
          )}
          
          {uploadError && (
            <div className="bg-red-100 border border-red-400 text-red-800 px-4 py-3 rounded mb-4">
              {uploadError}
            </div>
          )}

          <form onSubmit={handleDocumentUpload} className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1">Document Type</label>
              <select
                value={selectedDocType}
                onChange={(e) => setSelectedDocType(e.target.value)}
                className="w-full px-3 py-2 border rounded-lg"
                required
              >
                <option value="">Select document type</option>
                <option value="food_handler_cert">Food Handler Certification</option>
                <option value="cottage_permit">Cottage Food Permit</option>
                <option value="insurance">Liability Insurance</option>
                <option value="business_license">Business License</option>
                <option value="government_id">Government ID</option>
                <option value="proof_of_address">Proof of Address</option>
              </select>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium mb-1">Document Number (Optional)</label>
                <input
                  type="text"
                  value={documentDetails.document_number}
                  onChange={(e) => setDocumentDetails({...documentDetails, document_number: e.target.value})}
                  className="w-full px-3 py-2 border rounded-lg"
                  placeholder="e.g., License #12345"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Issued Date (Optional)</label>
                <input
                  type="date"
                  value={documentDetails.issued_date}
                  onChange={(e) => setDocumentDetails({...documentDetails, issued_date: e.target.value})}
                  className="w-full px-3 py-2 border rounded-lg"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Expiry Date (Optional)</label>
                <input
                  type="date"
                  value={documentDetails.expiry_date}
                  onChange={(e) => setDocumentDetails({...documentDetails, expiry_date: e.target.value})}
                  className="w-full px-3 py-2 border rounded-lg"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Upload File (PDF, JPG, PNG - Max 10MB)</label>
              <input
                type="file"
                accept=".pdf,.jpg,.jpeg,.png"
                onChange={handleFileChange}
                className="w-full px-3 py-2 border rounded-lg"
                required
              />
            </div>

            <button
              type="submit"
              disabled={uploading}
              className="w-full btn-primary py-3 rounded-lg font-medium disabled:opacity-50"
            >
              {uploading ? 'Uploading...' : 'Upload Document'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default ChefDashboard;
