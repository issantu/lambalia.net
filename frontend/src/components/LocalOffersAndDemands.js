import React from 'react';

const LocalOffersAndDemands = () => {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-2">🍽️ Local Offers and Demands</h1>
      <p className="text-lg text-gray-600 mb-6">Chef-Eater Marketplace</p>
      
      <div className="bg-blue-50 p-4 rounded-lg mb-6">
        <p className="text-blue-800">
          <strong>Different from Local Market:</strong> This is where chefs and eaters connect. 
          Chefs post what they can cook, eaters post what they want to order.
        </p>
      </div>
      
      <div className="grid md:grid-cols-2 gap-6">
        <div className="bg-green-50 p-6 rounded-lg border-l-4 border-green-500">
          <h2 className="text-xl font-semibold mb-3">👨‍🍳 Food Offers</h2>
          <p>Chefs post dishes they have cooked or can cook</p>
          <ul className="mt-2 text-sm text-gray-600">
            <li>• Share your culinary creations</li>
            <li>• Set your prices</li>
            <li>• Connect with food lovers</li>
          </ul>
        </div>
        
        <div className="bg-orange-50 p-6 rounded-lg border-l-4 border-orange-500">
          <h2 className="text-xl font-semibold mb-3">🍽️ Food Demands</h2>
          <p>Eaters post what they want to order from local chefs</p>
          <ul className="mt-2 text-sm text-gray-600">
            <li>• Request specific dishes</li>
            <li>• Find local chef talent</li>
            <li>• Enjoy home-cooked meals</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default LocalOffersAndDemands;
