// Professional Contact Page Component
import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import ContactInfo from './ContactInfo';

const ContactPage = () => {
  const { t } = useTranslation();
  const [selectedCategory, setSelectedCategory] = useState('all');

  const supportCategories = [
    { id: 'all', name: 'All Contacts', icon: '📧' },
    { id: 'business', name: 'Business & Sales', icon: '💼' },
    { id: 'support', name: 'Customer Support', icon: '🛟' },
    { id: 'technical', name: 'Technical Help', icon: '🔧' }
  ];

  const faqItems = [
    {
      question: "How do I contact customer support?",
      answer: "For customer support issues like order problems, account questions, or general assistance, email customer@lambalia.net. Our team typically responds within 24 hours."
    },
    {
      question: "Who should I contact for business partnerships?",
      answer: "For business inquiries, partnerships, or sales questions, please reach out to sales@lambalia.net. For executive-level discussions, contact issantu@lambalia.net."
    },
    {
      question: "What if I'm having technical issues with the platform?",
      answer: "Technical problems, platform bugs, or troubleshooting assistance can be reported to help@lambalia.net. Include details about your issue for faster resolution."
    },
    {
      question: "How can I provide general feedback?",
      answer: "General feedback, suggestions, or inquiries can be sent to contact@lambalia.net. We value your input and read every message."
    }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="text-center">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">
              📞 Contact Lambalia
            </h1>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              We're here to help! Choose the best way to reach our team for your specific needs.
            </p>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Category Filter */}
        <div className="mb-8">
          <div className="flex flex-wrap justify-center gap-4">
            {supportCategories.map((category) => (
              <button
                key={category.id}
                onClick={() => setSelectedCategory(category.id)}
                className={`px-6 py-3 rounded-lg font-medium transition-all duration-200 flex items-center space-x-2 ${
                  selectedCategory === category.id
                    ? 'bg-blue-600 text-white shadow-md'
                    : 'bg-white text-gray-700 hover:bg-gray-50 border border-gray-200'
                }`}
              >
                <span>{category.icon}</span>
                <span>{category.name}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Contact Information */}
        <div className="mb-12">
          <ContactInfo />
        </div>

        {/* Response Time Information */}
        <div className="bg-white p-8 rounded-xl shadow-sm border border-gray-200 mb-12">
          <h2 className="text-2xl font-bold text-gray-900 mb-6 text-center">
            ⏰ Expected Response Times
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="text-center">
              <div className="text-3xl mb-2">🚀</div>
              <h3 className="font-semibold text-gray-900">Technical Issues</h3>
              <p className="text-sm text-gray-600">help@lambalia.net</p>
              <p className="text-blue-600 font-medium">2-4 hours</p>
            </div>
            <div className="text-center">
              <div className="text-3xl mb-2">🛟</div>
              <h3 className="font-semibold text-gray-900">Customer Support</h3>
              <p className="text-sm text-gray-600">customer@lambalia.net</p>
              <p className="text-green-600 font-medium">4-24 hours</p>
            </div>
            <div className="text-center">
              <div className="text-3xl mb-2">💼</div>
              <h3 className="font-semibold text-gray-900">Business Inquiries</h3>
              <p className="text-sm text-gray-600">sales@lambalia.net</p>
              <p className="text-purple-600 font-medium">1-2 business days</p>
            </div>
            <div className="text-center">
              <div className="text-3xl mb-2">👔</div>
              <h3 className="font-semibold text-gray-900">Executive</h3>
              <p className="text-sm text-gray-600">issantu@lambalia.net</p>
              <p className="text-orange-600 font-medium">2-3 business days</p>
            </div>
          </div>
        </div>

        {/* FAQ Section */}
        <div className="bg-white p-8 rounded-xl shadow-sm border border-gray-200">
          <h2 className="text-2xl font-bold text-gray-900 mb-6 text-center">
            ❓ Frequently Asked Questions
          </h2>
          <div className="space-y-6">
            {faqItems.map((item, index) => (
              <div key={index} className="border-b border-gray-200 pb-6 last:border-b-0">
                <h3 className="text-lg font-semibold text-gray-900 mb-3">
                  {item.question}
                </h3>
                <p className="text-gray-700 leading-relaxed">
                  {item.answer}
                </p>
              </div>
            ))}
          </div>
        </div>

        {/* Emergency Contact */}
        <div className="mt-8 bg-red-50 border border-red-200 p-6 rounded-xl">
          <div className="text-center">
            <h3 className="text-lg font-semibold text-red-800 mb-2">
              🚨 Urgent Issues?
            </h3>
            <p className="text-red-700 mb-4">
              For platform outages, security issues, or urgent business matters:
            </p>
            <div className="space-y-2">
              <a
                href="mailto:help@lambalia.net?subject=URGENT%20-%20Platform%20Issue"
                className="inline-block bg-red-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-red-700 transition-colors"
              >
                📧 Email Technical Support
              </a>
              <p className="text-sm text-red-600">
                Mark subject line with "URGENT" for priority handling
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ContactPage;