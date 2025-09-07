// Professional Contact Information Component
import React from 'react';
import { useTranslation } from 'react-i18next';

const ContactInfo = ({ className = '', showAll = true }) => {
  const { t } = useTranslation();

  const contactEmails = [
    {
      email: 'sales@lambalia.net',
      purpose: 'Sales & Partnerships',
      icon: '💼',
      description: 'Business inquiries, partnerships, and sales questions',
      category: 'business'
    },
    {
      email: 'contact@lambalia.net', 
      purpose: 'General Inquiries',
      icon: '📧',
      description: 'General questions and information requests',
      category: 'general'
    },
    {
      email: 'customer@lambalia.net',
      purpose: 'Customer Support',
      icon: '🛟',
      description: 'Order issues, account problems, and customer service',
      category: 'support'
    },
    {
      email: 'help@lambalia.net',
      purpose: 'Technical Support',
      icon: '🔧',
      description: 'Technical issues, platform problems, and troubleshooting',
      category: 'technical'
    },
    {
      email: 'issantu@lambalia.net',
      purpose: 'Executive Office',
      icon: '👔',
      description: 'Executive inquiries and leadership communication',
      category: 'executive'
    }
  ];

  const copyToClipboard = (email) => {
    navigator.clipboard.writeText(email).then(() => {
      // Show temporary feedback
      const button = document.querySelector(`[data-email="${email}"]`);
      if (button) {
        const originalText = button.textContent;
        button.textContent = 'Copied!';
        button.classList.add('bg-green-100', 'text-green-800');
        setTimeout(() => {
          button.textContent = originalText;
          button.classList.remove('bg-green-100', 'text-green-800');
        }, 2000);
      }
    });
  };

  return (
    <div className={`contact-info ${className}`}>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {contactEmails.map((contact, index) => (
          <div key={contact.email} className="bg-white p-6 rounded-xl shadow-sm border border-gray-200 hover:shadow-md transition-shadow">
            <div className="flex items-start space-x-4">
              <div className="text-3xl">{contact.icon}</div>
              <div className="flex-1">
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  {contact.purpose}
                </h3>
                <p className="text-sm text-gray-600 mb-3">
                  {contact.description}
                </p>
                <div className="space-y-2">
                  <button
                    onClick={() => copyToClipboard(contact.email)}
                    data-email={contact.email}
                    className="w-full px-4 py-2 bg-blue-50 hover:bg-blue-100 text-blue-700 rounded-lg text-sm font-medium transition-colors duration-200 flex items-center justify-center space-x-2"
                  >
                    <span>📋</span>
                    <span>{contact.email}</span>
                  </button>
                  <a
                    href={`mailto:${contact.email}`}
                    className="w-full px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg text-sm font-medium transition-colors duration-200 flex items-center justify-center space-x-2"
                  >
                    <span>✉️</span>
                    <span>Send Email</span>
                  </a>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Quick Contact Summary */}
      <div className="mt-8 bg-gradient-to-r from-green-50 to-blue-50 p-6 rounded-xl border border-green-200">
        <h3 className="text-lg font-semibold text-gray-900 mb-4 text-center">
          📞 Quick Contact Guide
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
          <div>
            <h4 className="font-medium text-gray-800 mb-2">For Business:</h4>
            <ul className="space-y-1 text-gray-600">
              <li>• Partnerships → <span className="font-mono">sales@lambalia.net</span></li>
              <li>• General Info → <span className="font-mono">contact@lambalia.net</span></li>
              <li>• Executive → <span className="font-mono">issantu@lambalia.net</span></li>
            </ul>
          </div>
          <div>
            <h4 className="font-medium text-gray-800 mb-2">For Support:</h4>
            <ul className="space-y-1 text-gray-600">
              <li>• Order Issues → <span className="font-mono">customer@lambalia.net</span></li>
              <li>• Technical Help → <span className="font-mono">help@lambalia.net</span></li>
              <li>• Account Problems → <span className="font-mono">customer@lambalia.net</span></li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

// Simplified Contact Widget for Footer/Sidebar
export const ContactWidget = () => {
  const contactEmails = [
    { email: 'contact@lambalia.net', label: 'General Inquiries', icon: '📧' },
    { email: 'customer@lambalia.net', label: 'Customer Support', icon: '🛟' },
    { email: 'help@lambalia.net', label: 'Technical Help', icon: '🔧' }
  ];

  return (
    <div className="contact-widget">
      <h4 className="text-lg font-semibold text-gray-900 mb-3">📞 Contact Us</h4>
      <div className="space-y-2">
        {contactEmails.map((contact) => (
          <a
            key={contact.email}
            href={`mailto:${contact.email}`}
            className="flex items-center space-x-2 text-sm text-blue-600 hover:text-blue-800 transition-colors"
          >
            <span>{contact.icon}</span>
            <span>{contact.label}</span>
          </a>
        ))}
      </div>
      <div className="mt-3 text-xs text-gray-500">
        For executive inquiries: <span className="font-mono">issantu@lambalia.net</span>
      </div>
    </div>
  );
};

export default ContactInfo;