// Quick Eats Provider Training Guide
import React, { useState } from 'react';
import { Icon, AnimatedIcon } from './ProfessionalIcons';
import { useTranslation } from 'react-i18next';

const QuickEatsTraining = () => {
  const { t } = useTranslation();
  const [activeSection, setActiveSection] = useState('introduction');

  const sections = [
    { id: 'introduction', title: 'Your Quick Service Edge', icon: 'Utensils' },
    { id: 'competition', title: 'Fast Food Competition', icon: 'Settings' },
    { id: 'advantages', title: 'Why You Win', icon: 'Star' },
    { id: 'efficiency', title: 'Speed & Quality', icon: 'Settings' },
    { id: 'offerings', title: 'Perfect Menu Items', icon: 'Recipe' },
    { id: 'operations', title: 'Smooth Operations', icon: 'Settings' },
    { id: 'success', title: 'Building Success', icon: 'Community' }
  ];

  const renderIntroduction = () => (
    <div className="space-y-6">
      <div className="text-center">
        <AnimatedIcon name="Utensils" size={64} className="text-orange-500 mx-auto mb-4" />
        <h2 className="text-3xl font-bold text-gray-800 mb-4">{t('quickeats.welcomeTitle')}</h2>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          You're bringing authentic, homemade flavors to the fast-casual dining world. Your mission: deliver quality, culture, and care at the speed modern life demands.
        </p>
      </div>

      <div className="bg-gradient-to-r from-blue-50 to-purple-50 p-8 rounded-xl border-l-4 border-blue-500">
        <h3 className="text-xl font-semibold text-blue-800 mb-4">Your Unique Position</h3>
        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <h4 className="font-medium text-gray-800 mb-2">🏃‍♀️ What You Provide:</h4>
            <ul className="text-gray-600 space-y-1 text-sm">
              <li>• Quick, ready-to-eat authentic meals</li>
              <li>• Home-cooked quality at fast-food speed</li>
              <li>• Cultural flavors for busy professionals</li>
              <li>• Personal touch in a grab-and-go format</li>
              <li>• Healthy alternatives to fast food chains</li>
            </ul>
          </div>
          <div>
            <h4 className="font-medium text-gray-800 mb-2">🍔 What Fast Food Offers:</h4>
            <ul className="text-gray-600 space-y-1 text-sm">
              <li>• Standardized, processed meals</li>
              <li>• Speed but low nutritional value</li>
              <li>• Generic flavors and ingredients</li>
              <li>• No cultural authenticity or story</li>
              <li>• Mass-produced with preservatives</li>
            </ul>
          </div>
        </div>
      </div>

      <div className="bg-green-50 p-6 rounded-lg">
        <h3 className="text-lg font-semibold text-green-800 mb-3">Your Mission Statement</h3>
        <p className="text-green-700 italic text-lg text-center">
          "I bring the comfort and authenticity of home cooking to people who need good food fast. 
          Every meal carries the love and tradition of my kitchen, served with the convenience modern life requires."
        </p>
      </div>

      <div className="grid md:grid-cols-3 gap-4">
        <div className="text-center p-4 bg-orange-50 rounded-lg">
          <Icon name="Settings" size={32} className="text-orange-600 mx-auto mb-2" />
          <h4 className="font-semibold text-orange-800">Fast</h4>
          <p className="text-sm text-orange-700">Ready in under 10 minutes</p>
        </div>
        <div className="text-center p-4 bg-green-50 rounded-lg">
          <Icon name="Heart" size={32} className="text-green-600 mx-auto mb-2" />
          <h4 className="font-semibold text-green-800">Fresh</h4>
          <p className="text-sm text-green-700">Made with love and quality ingredients</p>
        </div>
        <div className="text-center p-4 bg-blue-50 rounded-lg">
          <Icon name="Heritage" size={32} className="text-blue-600 mx-auto mb-2" />
          <h4 className="font-semibold text-blue-800">Flavorful</h4>
          <p className="text-sm text-blue-700">Authentic cultural tastes</p>
        </div>
      </div>
    </div>
  );

  const renderCompetition = () => (
    <div className="space-y-6">
      <div className="text-center mb-8">
        <Icon name="Settings" size={48} className="text-red-600 mx-auto mb-4" />
        <h2 className="text-2xl font-bold text-gray-800">Understanding Fast Food Competition</h2>
        <p className="text-gray-600">Know your competition to highlight your advantages</p>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-lg border shadow-sm">
          <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
            <Icon name="Settings" size={20} className="text-red-600 mr-2" />
            Fast Food Chains
          </h3>
          
          <div className="space-y-4">
            <div>
              <h4 className="font-medium text-gray-700 mb-2">Their Strengths:</h4>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• Extremely fast service (2-5 minutes)</li>
                <li>• Consistent quality and taste</li>
                <li>• Low prices and value deals</li>
                <li>• Multiple locations and convenience</li>
                <li>• Strong brand recognition</li>
                <li>• Standardized processes</li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-medium text-gray-700 mb-2">Their Weaknesses:</h4>
              <ul className="text-sm text-red-600 space-y-1">
                <li>• Processed, unhealthy ingredients</li>
                <li>• No cultural authenticity</li>
                <li>• Generic, mass-produced flavors</li>
                <li>• No personal connection or story</li>
                <li>• Limited healthy options</li>
                <li>• Environmental concerns</li>
              </ul>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg border shadow-sm">
          <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
            <Icon name="Utensils" size={20} className="text-green-600 mr-2" />
            Your Competitive Position
          </h3>
          
          <div className="space-y-4">
            <div className="bg-green-50 p-4 rounded-lg">
              <h4 className="font-medium text-green-800 mb-2">Speed Comparison:</h4>
              <div className="text-sm space-y-1">
                <div className="flex justify-between">
                  <span>Fast Food Chains:</span>
                  <span className="font-medium">2-5 minutes</span>
                </div>
                <div className="flex justify-between">
                  <span>Your Quick Eats:</span>
                  <span className="font-medium text-green-600">5-10 minutes</span>
                </div>
                <div className="text-xs text-green-600 mt-2">
                  ✓ Slightly longer but with significantly higher quality
                </div>
              </div>
            </div>
            
            <div className="bg-blue-50 p-4 rounded-lg">
              <h4 className="font-medium text-blue-800 mb-2">Value Proposition:</h4>
              <div className="text-sm space-y-2">
                <div>
                  <strong>Fast Food:</strong> Cheap, fast, processed
                </div>
                <div>
                  <strong>Your Service:</strong> Affordable, quick, authentic homemade food
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-yellow-50 p-6 rounded-lg border-l-4 border-yellow-500">
        <h3 className="text-lg font-semibold text-yellow-800 mb-3">Market Positioning Strategy</h3>
        <p className="text-yellow-700 mb-4">
          You're not competing on speed alone - you're creating the "better fast food" category.
        </p>
        <div className="grid md:grid-cols-3 gap-4 text-sm">
          <div className="text-center">
            <div className="font-medium text-yellow-800">Fast Food Sells:</div>
            <div className="text-yellow-600">Speed & Price</div>
          </div>
          <div className="text-center">
            <div className="font-medium text-yellow-800">You Offer:</div>
            <div className="text-yellow-600">Speed + Quality + Culture</div>
          </div>
          <div className="text-center">
            <div className="font-medium text-yellow-800">Result:</div>
            <div className="text-yellow-600">Premium Fast-Casual</div>
          </div>
        </div>
      </div>

      <div className="grid md:grid-cols-3 gap-4">
        <div className="bg-white p-4 rounded-lg border text-center">
          <h4 className="font-semibold text-gray-800 mb-2">Pricing Strategy</h4>
          <div className="space-y-1 text-sm">
            <div className="text-red-600">Fast Food: $3-7</div>
            <div className="text-green-600 font-medium">Your Range: $6-12</div>
            <div className="text-blue-600">Premium justified by quality</div>
          </div>
        </div>
        <div className="bg-white p-4 rounded-lg border text-center">
          <h4 className="font-semibold text-gray-800 mb-2">Target Customer</h4>
          <div className="space-y-1 text-sm text-gray-600">
            <div>• Health-conscious professionals</div>
            <div>• Cultural food enthusiasts</div>
            <div>• Quality-seeking families</div>
          </div>
        </div>
        <div className="bg-white p-4 rounded-lg border text-center">
          <h4 className="font-semibold text-gray-800 mb-2">Key Differentiator</h4>
          <div className="space-y-1 text-sm text-green-600 font-medium">
            <div>Homemade Quality</div>
            <div>Cultural Authenticity</div>
            <div>Personal Touch</div>
          </div>
        </div>
      </div>
    </div>
  );

  const renderAdvantages = () => (
    <div className="space-y-6">
      <div className="text-center mb-8">
        <Icon name="Star" size={48} className="text-yellow-500 mx-auto mb-4" />
        <h2 className="text-2xl font-bold text-gray-800">Your Winning Advantages</h2>
        <p className="text-gray-600">Why busy people will choose you over fast food chains</p>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        <div className="bg-gradient-to-br from-green-50 to-blue-50 p-6 rounded-xl">
          <h3 className="text-lg font-semibold text-green-800 mb-4 flex items-center">
            <Icon name="Heart" size={20} className="text-red-500 mr-2" />
            Quality Advantage
          </h3>
          <ul className="space-y-3 text-sm text-gray-700">
            <li className="flex items-start">
              <Icon name="ChevronRight" size={16} className="text-green-600 mr-2 mt-0.5" />
              <div>
                <strong>Fresh Ingredients:</strong> Use the same quality ingredients you cook with at home
              </div>
            </li>
            <li className="flex items-start">
              <Icon name="ChevronRight" size={16} className="text-green-600 mr-2 mt-0.5" />
              <div>
                <strong>No Preservatives:</strong> Made fresh daily without artificial additives
              </div>
            </li>
            <li className="flex items-start">
              <Icon name="ChevronRight" size={16} className="text-green-600 mr-2 mt-0.5" />
              <div>
                <strong>Homemade Taste:</strong> Authentic flavors that taste like family cooking
              </div>
            </li>
            <li className="flex items-start">
              <Icon name="ChevronRight" size={16} className="text-green-600 mr-2 mt-0.5" />
              <div>
                <strong>Nutritious Options:</strong> Balanced meals with real vegetables and proteins
              </div>
            </li>
          </ul>
        </div>

        <div className="bg-gradient-to-br from-purple-50 to-pink-50 p-6 rounded-xl">
          <h3 className="text-lg font-semibold text-purple-800 mb-4 flex items-center">
            <Icon name="Heritage" size={20} className="text-purple-600 mr-2" />
            Cultural Advantage
          </h3>
          <ul className="space-y-3 text-sm text-gray-700">
            <li className="flex items-start">
              <Icon name="ChevronRight" size={16} className="text-purple-600 mr-2 mt-0.5" />
              <div>
                <strong>Authentic Flavors:</strong> Real cultural dishes, not adapted versions
              </div>
            </li>
            <li className="flex items-start">
              <Icon name="ChevronRight" size={16} className="text-purple-600 mr-2 mt-0.5" />
              <div>
                <strong>Unique Options:</strong> Foods you can't get at chain restaurants
              </div>
            </li>
            <li className="flex items-start">
              <Icon name="ChevronRight" size={16} className="text-purple-600 mr-2 mt-0.5" />
              <div>
                <strong>Story & Heritage:</strong> Each dish has history and meaning
              </div>
            </li>
            <li className="flex items-start">
              <Icon name="ChevronRight" size={16} className="text-purple-600 mr-2 mt-0.5" />
              <div>
                <strong>Educational Value:</strong> Customers learn about different cultures
              </div>
            </li>
          </ul>
        </div>

        <div className="bg-gradient-to-br from-orange-50 to-yellow-50 p-6 rounded-xl">
          <h3 className="text-lg font-semibold text-orange-800 mb-4 flex items-center">
            <Icon name="Settings" size={20} className="text-orange-600 mr-2" />
            Service Advantage
          </h3>
          <ul className="space-y-3 text-sm text-gray-700">
            <li className="flex items-start">
              <Icon name="ChevronRight" size={16} className="text-orange-600 mr-2 mt-0.5" />
              <div>
                <strong>Personal Touch:</strong> Remember regular customers and their preferences
              </div>
            </li>
            <li className="flex items-start">
              <Icon name="ChevronRight" size={16} className="text-orange-600 mr-2 mt-0.5" />
              <div>
                <strong>Customization:</strong> Adjust spice levels, dietary restrictions
              </div>
            </li>
            <li className="flex items-start">
              <Icon name="ChevronRight" size={16} className="text-orange-600 mr-2 mt-0.5" />
              <div>
                <strong>Care & Attention:</strong> Each order prepared with personal care
              </div>
            </li>
            <li className="flex items-start">
              <Icon name="ChevronRight" size={16} className="text-orange-600 mr-2 mt-0.5" />
              <div>
                <strong>Flexibility:</strong> Can accommodate special requests when possible
              </div>
            </li>
          </ul>
        </div>

        <div className="bg-gradient-to-br from-blue-50 to-indigo-50 p-6 rounded-xl">
          <h3 className="text-lg font-semibold text-blue-800 mb-4 flex items-center">
            <Icon name="Community" size={20} className="text-blue-600 mr-2" />
            Community Advantage
          </h3>
          <ul className="space-y-3 text-sm text-gray-700">
            <li className="flex items-start">
              <Icon name="ChevronRight" size={16} className="text-blue-600 mr-2 mt-0.5" />
              <div>
                <strong>Local Connection:</strong> Supporting local home cooks, not big corporations
              </div>
            </li>
            <li className="flex items-start">
              <Icon name="ChevronRight" size={16} className="text-blue-600 mr-2 mt-0.5" />
              <div>
                <strong>Environmental Impact:</strong> Less packaging, lower food miles
              </div>
            </li>
            <li className="flex items-start">
              <Icon name="ChevronRight" size={16} className="text-blue-600 mr-2 mt-0.5" />
              <div>
                <strong>Economic Impact:</strong> Money stays in the local community
              </div>
            </li>
            <li className="flex items-start">
              <Icon name="ChevronRight" size={16} className="text-blue-600 mr-2 mt-0.5" />
              <div>
                <strong>Cultural Preservation:</strong> Keeping traditional recipes alive
              </div>
            </li>
          </ul>
        </div>
      </div>

      <div className="bg-gradient-to-r from-orange-500 to-red-500 text-white p-8 rounded-xl text-center">
        <h3 className="text-xl font-bold mb-4">Your Unique Selling Proposition</h3>
        <p className="text-lg mb-4">
          "Fast food with a heart - authentic homemade meals ready when you need them."
        </p>
        <div className="bg-white bg-opacity-20 p-4 rounded-lg">
          <p className="text-sm">
            While fast food chains prioritize speed and profit, you prioritize speed AND quality AND culture. 
            You offer busy people a way to eat well without sacrificing their values or health.
          </p>
        </div>
      </div>
    </div>
  );

  const renderEfficiency = () => (
    <div className="space-y-6">
      <div className="text-center mb-8">
        <Icon name="Settings" size={48} className="text-blue-600 mx-auto mb-4" />
        <h2 className="text-2xl font-bold text-gray-800">Mastering Speed & Quality</h2>
        <p className="text-gray-600">Deliver excellence at the pace modern life demands</p>
      </div>

      <div className="grid lg:grid-cols-2 gap-8">
        <div className="space-y-6">
          <div className="bg-white p-6 rounded-lg border shadow-sm">
            <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
              <Icon name="Settings" size={20} className="text-green-600 mr-2" />
              Prep Strategy
            </h3>
            <div className="space-y-3 text-sm text-gray-700">
              <div className="border-l-4 border-green-500 pl-4">
                <h4 className="font-medium text-green-800">Batch Cooking</h4>
                <p className="text-gray-600">Prepare base ingredients in large quantities during slow periods</p>
              </div>
              <div className="border-l-4 border-blue-500 pl-4">
                <h4 className="font-medium text-blue-800">Component System</h4>
                <p className="text-gray-600">Pre-cook proteins, sauces, and sides that can be quickly assembled</p>
              </div>
              <div className="border-l-4 border-purple-500 pl-4">
                <h4 className="font-medium text-purple-800">Smart Timing</h4>
                <p className="text-gray-600">Start popular items before peak hours to reduce wait times</p>
              </div>
            </div>
          </div>

          <div className="bg-white p-6 rounded-lg border shadow-sm">
            <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
              <Icon name="Recipe" size={20} className="text-orange-600 mr-2" />
              Menu Optimization
            </h3>
            <div className="space-y-3 text-sm">
              <div className="bg-orange-50 p-3 rounded-lg">
                <h4 className="font-medium text-orange-800 mb-1">Limited Menu Strategy</h4>
                <ul className="text-orange-700 space-y-1">
                  <li>• Focus on 8-12 items you can make perfectly</li>
                  <li>• Choose dishes that share common ingredients</li>
                  <li>• Offer both familiar and unique options</li>
                </ul>
              </div>
              <div className="bg-blue-50 p-3 rounded-lg">
                <h4 className="font-medium text-blue-800 mb-1">Quick-Assembly Items</h4>
                <ul className="text-blue-700 space-y-1">
                  <li>• Wraps, bowls, sandwiches with pre-cooked fillings</li>
                  <li>• Soups and stews that can simmer all day</li>
                  <li>• Salads with protein that can be added quickly</li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        <div className="space-y-6">
          <div className="bg-white p-6 rounded-lg border shadow-sm">
            <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
              <Icon name="Settings" size={20} className="text-purple-600 mr-2" />
              Workflow Optimization
            </h3>
            <div class="space-y-4">
              <div className="bg-purple-50 p-4 rounded-lg">
                <h4 className="font-medium text-purple-800 mb-2">The 5-Minute Rule</h4>
                <div className="text-sm text-purple-700 space-y-1">
                  <div><strong>0-1 min:</strong> Take order, start heating/assembly</div>
                  <div><strong>1-3 min:</strong> Prepare and plate the meal</div>
                  <div><strong>3-5 min:</strong> Final touches, package, serve</div>
                </div>
              </div>
              
              <div className="bg-green-50 p-4 rounded-lg">
                <h4 className="font-medium text-green-800 mb-2">Efficiency Tips</h4>
                <ul className="text-sm text-green-700 space-y-1">
                  <li>• Set up mise en place like a professional kitchen</li>
                  <li>• Use timers for consistency</li>
                  <li>• Have packaging ready and organized</li>
                  <li>• Keep cleaning supplies within reach</li>
                </ul>
              </div>
            </div>
          </div>

          <div className="bg-white p-6 rounded-lg border shadow-sm">
            <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
              <Icon name="Star" size={20} className="text-yellow-600 mr-2" />
              Quality Control
            </h3>
            <div className="space-y-3 text-sm">
              <div className="flex items-start space-x-3">
                <Icon name="ChevronRight" size={16} className="text-yellow-600 mt-1" />
                <div>
                  <h4 className="font-medium text-gray-800">Taste Every Batch</h4>
                  <p className="text-gray-600">Quick taste test ensures consistent seasoning</p>
                </div>
              </div>
              <div className="flex items-start space-x-3">
                <Icon name="ChevronRight" size={16} className="text-yellow-600 mt-1" />
                <div>
                  <h4 className="font-medium text-gray-800">Temperature Checks</h4>
                  <p className="text-gray-600">Use thermometer to ensure food safety</p>
                </div>
              </div>
              <div className="flex items-start space-x-3">
                <Icon name="ChevronRight" size={16} className="text-yellow-600 mt-1" />
                <div>
                  <h4 className="font-medium text-gray-800">Visual Inspection</h4>
                  <p className="text-gray-600">Each plate should look appealing and consistent</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-gradient-to-r from-blue-50 to-purple-50 p-6 rounded-lg border">
        <h3 className="text-lg font-semibold text-blue-800 mb-4">Daily Prep Schedule Template</h3>
        <div className="grid md:grid-cols-3 gap-4 text-sm">
          <div className="bg-white p-4 rounded-lg">
            <h4 className="font-medium text-blue-800 mb-2">Early Morning (6-8 AM)</h4>
            <ul className="text-blue-700 space-y-1">
              <li>• Start slow-cooking items (stews, braises)</li>
              <li>• Prep vegetables and proteins</li>
              <li>• Make sauces and marinades</li>
              <li>• Set up workstation</li>
            </ul>
          </div>
          <div className="bg-white p-4 rounded-lg">
            <h4 className="font-medium text-purple-800 mb-2">Mid-Morning (8-11 AM)</h4>
            <ul className="text-purple-700 space-y-1">
              <li>• Cook proteins that will be reheated</li>
              <li>• Prepare cold items (salads, wraps)</li>
              <li>• Portion and store components</li>
              <li>• Update daily specials</li>
            </ul>
          </div>
          <div className="bg-white p-4 rounded-lg">
            <h4 className="font-medium text-green-800 mb-2">Service Hours (11 AM - 3 PM)</h4>
            <ul className="text-green-700 space-y-1">
              <li>• Focus on assembly and service</li>
              <li>• Monitor food temperatures</li>
              <li>• Restock components as needed</li>
              <li>• Maintain clean workspace</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );

  const renderOfferings = () => (
    <div className="space-y-6">
      <div className="text-center mb-8">
        <Icon name="Recipe" size={48} className="text-green-600 mx-auto mb-4" />
        <h2 className="text-2xl font-bold text-gray-800">Perfect Quick Eats Menu Items</h2>
        <p className="text-gray-600">Choose dishes that showcase your culture while meeting quick service needs</p>
      </div>

      <div className="grid lg:grid-cols-2 gap-8">
        <div className="space-y-6">
          <div className="bg-white p-6 rounded-lg border shadow-sm">
            <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
              <Icon name="Star" size={20} className="text-yellow-500 mr-2" />
              Ideal Quick Eats Items
            </h3>
            <div className="space-y-4">
              <div className="border-l-4 border-green-500 pl-4">
                <h4 className="font-medium text-green-800">Rice & Grain Bowls</h4>
                <p className="text-sm text-gray-600">Base of rice/quinoa with protein and vegetables. Easy to customize and portion.</p>
                <div className="text-xs text-green-600 mt-1">Examples: Jollof bowl, bibimbap, burrito bowls</div>
              </div>
              
              <div className="border-l-4 border-blue-500 pl-4">
                <h4 className="font-medium text-blue-800">Wraps & Flatbreads</h4>
                <p className="text-sm text-gray-600">Portable, customizable, and can use pre-cooked fillings.</p>
                <div className="text-xs text-blue-600 mt-1">Examples: Chicken shawarma, dosa wraps, quesadillas</div>
              </div>
              
              <div className="border-l-4 border-purple-500 pl-4">
                <h4 className="font-medium text-purple-800">Soups & Stews</h4>
                <p className="text-sm text-gray-600">Can simmer all day, easy to portion, comforting and filling.</p>
                <div className="text-xs text-purple-600 mt-1">Examples: Pho, lentil dal, chicken stew</div>
              </div>
              
              <div className="border-l-4 border-orange-500 pl-4">
                <h4 className="font-medium text-orange-800">Protein & Sides</h4>
                <p className="text-sm text-gray-600">Simple combinations that highlight your cooking skills.</p>
                <div className="text-xs text-orange-600 mt-1">Examples: Grilled fish with rice, curry with bread</div>
              </div>
            </div>
          </div>

          <div className="bg-white p-6 rounded-lg border shadow-sm">
            <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
              <Icon name="Settings" size={20} className="text-red-600 mr-2" />
              Items to Avoid
            </h3>
            <div className="space-y-3 text-sm">
              <div className="bg-red-50 p-3 rounded-lg">
                <h4 className="font-medium text-red-800 mb-1">Too Complex</h4>
                <ul className="text-red-700 space-y-1">
                  <li>• Dishes requiring 30+ minutes of active cooking</li>
                  <li>• Items with too many components to assemble quickly</li>
                  <li>• Foods that don't travel or reheat well</li>
                </ul>
              </div>
              <div className="bg-yellow-50 p-3 rounded-lg">
                <h4 className="font-medium text-yellow-800 mb-1">Food Safety Concerns</h4>
                <ul className="text-yellow-700 space-y-1">
                  <li>• Raw or undercooked items (unless specially equipped)</li>
                  <li>• Foods that spoil quickly at room temperature</li>
                  <li>• Items requiring specialized storage</li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        <div className="space-y-6">
          <div className="bg-gradient-to-br from-green-50 to-blue-50 p-6 rounded-lg">
            <h3 className="text-lg font-semibold text-green-800 mb-4">Sample Menu Structure</h3>
            <div className="space-y-4 text-sm">
              <div>
                <h4 className="font-medium text-green-800 mb-2">Rice Bowls (3-4 options)</h4>
                <ul className="text-green-700 space-y-1 ml-4">
                  <li>• Traditional chicken & rice with your cultural twist</li>
                  <li>• Vegetarian option with legumes or tofu</li>
                  <li>• Spicy option for heat lovers</li>
                  <li>• Mild/kid-friendly version</li>
                </ul>
              </div>
              
              <div>
                <h4 className="font-medium text-blue-800 mb-2">Handheld Items (2-3 options)</h4>
                <ul className="text-blue-700 space-y-1 ml-4">
                  <li>• Cultural sandwich or wrap</li>
                  <li>• Stuffed flatbread or pastry</li>
                  <li>• Protein-filled pocket bread</li>
                </ul>
              </div>
              
              <div>
                <h4 className="font-medium text-purple-800 mb-2">Comfort Foods (2-3 options)</h4>
                <ul className="text-purple-700 space-y-1 ml-4">
                  <li>• Signature soup or stew</li>
                  <li>• Traditional curry with bread/rice</li>
                  <li>• Hearty salad with protein</li>
                </ul>
              </div>
              
              <div>
                <h4 className="font-medium text-orange-800 mb-2">Beverages & Sides</h4>
                <ul className="text-orange-700 space-y-1 ml-4">
                  <li>• Traditional drinks (lassi, horchata, etc.)</li>
                  <li>• Simple sides that complement mains</li>
                  <li>• Small desserts or treats</li>
                </ul>
              </div>
            </div>
          </div>

          <div className="bg-white p-6 rounded-lg border shadow-sm">
            <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
              <Icon name="Dollar" size={20} className="text-green-600 mr-2" />
              Pricing Strategy
            </h3>
            <div className="space-y-3">
              <div className="bg-green-50 p-3 rounded-lg">
                <h4 className="font-medium text-green-800 mb-2">Value Pricing Model</h4>
                <div className="text-sm text-green-700 space-y-1">
                  <div className="flex justify-between">
                    <span>Small Portion (lunch):</span>
                    <span className="font-medium">$6-8</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Regular Portion:</span>
                    <span className="font-medium">$8-12</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Large/Family Size:</span>
                    <span className="font-medium">$12-16</span>
                  </div>
                </div>
              </div>
              
              <div className="bg-blue-50 p-3 rounded-lg text-sm">
                <h4 className="font-medium text-blue-800 mb-1">Competitive Positioning</h4>
                <p className="text-blue-700">
                  Price 20-40% above fast food, but 20-40% below fast-casual chains. 
                  Justify premium with quality, authenticity, and cultural value.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  const renderOperations = () => (
    <div className="space-y-6">
      <div className="text-center mb-8">
        <Icon name="Settings" size={48} className="text-purple-600 mx-auto mb-4" />
        <h2 className="text-2xl font-bold text-gray-800">Smooth Operations</h2>
        <p className="text-gray-600">Systems and processes for consistent success</p>
      </div>

      <div className="grid lg:grid-cols-2 gap-8">
        <div className="space-y-6">
          <div className="bg-white p-6 rounded-lg border shadow-sm">
            <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
              <Icon name="Settings" size={20} className="text-blue-600 mr-2" />
              Daily Operations Checklist
            </h3>
            <div className="space-y-4">
              <div className="bg-blue-50 p-4 rounded-lg">
                <h4 className="font-medium text-blue-800 mb-2">Opening (1 hour before service)</h4>
                <ul className="text-sm text-blue-700 space-y-1">
                  <li>□ Check equipment and heating elements</li>
                  <li>□ Review today's prep and ingredients</li>
                  <li>□ Set up workstation and mise en place</li>
                  <li>□ Check Lambalia orders and timing</li>
                  <li>□ Verify payment system is working</li>
                </ul>
              </div>
              
              <div className="bg-green-50 p-4 rounded-lg">
                <h4 className="font-medium text-green-800 mb-2">During Service</h4>
                <ul className="text-sm text-green-700 space-y-1">
                  <li>□ Monitor food temperatures every hour</li>
                  <li>□ Restock components as needed</li>
                  <li>□ Clean as you go</li>
                  <li>□ Track popular items for tomorrow's prep</li>
                  <li>□ Maintain friendly customer service</li>
                </ul>
              </div>
              
              <div className="bg-purple-50 p-4 rounded-lg">
                <h4 className="font-medium text-purple-800 mb-2">Closing</h4>
                <ul className="text-sm text-purple-700 space-y-1">
                  <li>□ Clean and sanitize all surfaces</li>
                  <li>□ Store leftover food properly</li>
                  <li>□ Review sales and popular items</li>
                  <li>□ Plan tomorrow's prep list</li>
                  <li>□ Check Lambalia payment status</li>
                </ul>
              </div>
            </div>
          </div>

          <div className="bg-white p-6 rounded-lg border shadow-sm">
            <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
              <Icon name="Shield" size={20} className="text-red-600 mr-2" />
              Food Safety & Quality
            </h3>
            <div className="space-y-3 text-sm">
              <div className="border-l-4 border-red-500 pl-4">
                <h4 className="font-medium text-red-800">Temperature Control</h4>
                <p className="text-gray-600">Keep hot foods above 140°F, cold foods below 40°F</p>
              </div>
              <div className="border-l-4 border-orange-500 pl-4">
                <h4 className="font-medium text-orange-800">Storage Times</h4>
                <p className="text-gray-600">Prepared foods: max 4 hours at room temp, 2 days refrigerated</p>
              </div>
              <div className="border-l-4 border-yellow-500 pl-4">
                <h4 className="font-medium text-yellow-800">Cross-Contamination</h4>
                <p className="text-gray-600">Separate cutting boards for meat/vegetables, wash hands frequently</p>
              </div>
              <div className="border-l-4 border-green-500 pl-4">
                <h4 className="font-medium text-green-800">Labeling System</h4>
                <p className="text-gray-600">Date all prepared items, first in first out rotation</p>
              </div>
            </div>
          </div>
        </div>

        <div className="space-y-6">
          <div className="bg-white p-6 rounded-lg border shadow-sm">
            <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
              <Icon name="Community" size={20} className="text-green-600 mr-2" />
              Customer Service Excellence
            </h3>
            <div className="space-y-4">
              <div className="bg-green-50 p-4 rounded-lg">
                <h4 className="font-medium text-green-800 mb-2">The Quick Service Formula</h4>
                <div className="text-sm text-green-700 space-y-2">
                  <div><strong>Greeting (10 seconds):</strong> "Welcome! What can I make for you today?"</div>
                  <div><strong>Recommendation (20 seconds):</strong> Suggest popular or special items</div>
                  <div><strong>Customization (30 seconds):</strong> "How spicy? Any dietary restrictions?"</div>
                  <div><strong>Prep Time (5 minutes):</strong> "This will be ready in about 5 minutes"</div>
                  <div><strong>Cultural Note (during prep):</strong> Share brief story about the dish</div>
                </div>
              </div>
              
              <div className="bg-blue-50 p-4 rounded-lg">
                <h4 className="font-medium text-blue-800 mb-2">Handling Rush Periods</h4>
                <ul className="text-sm text-blue-700 space-y-1">
                  <li>• Pre-prepare popular items during slow times</li>
                  <li>• Take multiple orders before starting cooking</li>
                  <li>• Communicate wait times honestly</li>
                  <li>• Offer small samples while customers wait</li>
                  <li>• Stay calm and maintain quality standards</li>
                </ul>
              </div>
            </div>
          </div>

          <div className="bg-white p-6 rounded-lg border shadow-sm">
            <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
              <Icon name="Star" size={20} className="text-yellow-500 mr-2" />
              Building Regulars
            </h3>
            <div className="space-y-3 text-sm">
              <div className="flex items-start space-x-3">
                <Icon name="Heart" size={16} className="text-red-500 mt-1" />
                <div>
                  <h4 className="font-medium text-gray-800">Remember Names & Preferences</h4>
                  <p className="text-gray-600">Keep mental notes of regular customers' favorite orders</p>
                </div>
              </div>
              <div className="flex items-start space-x-3">
                <Icon name="Star" size={16} className="text-yellow-500 mt-1" />
                <div>
                  <h4 className="font-medium text-gray-800">Loyalty Rewards</h4>
                  <p className="text-gray-600">Offer "buy 9, get 10th free" or surprise regulars with extras</p>
                </div>
              </div>
              <div className="flex items-start space-x-3">
                <Icon name="Heritage" size={16} className="text-blue-500 mt-1" />
                <div>
                  <h4 className="font-medium text-gray-800">Cultural Education</h4>
                  <p className="text-gray-600">Share cooking tips, ingredient info, or cultural context</p>
                </div>
              </div>
              <div className="flex items-start space-x-3">
                <Icon name="Community" size={16} className="text-green-500 mt-1" />
                <div>
                  <h4 className="font-medium text-gray-800">Community Connection</h4>
                  <p className="text-gray-600">Ask about their day, remember personal details they share</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-yellow-50 p-6 rounded-lg border-l-4 border-yellow-500">
        <h3 className="text-lg font-semibold text-yellow-800 mb-3">Success Metrics to Track</h3>
        <div className="grid md:grid-cols-4 gap-4 text-sm">
          <div className="text-center">
            <div className="font-semibold text-yellow-800">Average Order Time</div>
            <div className="text-yellow-600">Target: 5-7 minutes</div>
          </div>
          <div className="text-center">
            <div className="font-semibold text-yellow-800">Customer Return Rate</div>
            <div className="text-yellow-600">Target: 40-60%</div>
          </div>
          <div className="text-center">
            <div className="font-semibold text-yellow-800">Daily Sales</div>
            <div className="text-yellow-600">Track trends & peaks</div>
          </div>
          <div className="text-center">
            <div className="font-semibold text-yellow-800">Food Cost %</div>
            <div className="text-yellow-600">Target: 25-35%</div>
          </div>
        </div>
      </div>
    </div>
  );

  const renderSuccess = () => (
    <div className="space-y-6">
      <div className="text-center mb-8">
        <Icon name="Community" size={48} className="text-green-600 mx-auto mb-4" />
        <h2 className="text-2xl font-bold text-gray-800">Building Long-Term Success</h2>
        <p className="text-gray-600">Strategies for sustainable growth in the quick eats market</p>
      </div>

      <div className="bg-gradient-to-r from-green-50 to-blue-50 p-8 rounded-xl">
        <h3 className="text-xl font-semibold text-green-800 mb-6 text-center">Growth Strategy Framework</h3>
        <div className="grid md:grid-cols-4 gap-6">
          <div className="text-center">
            <div className="bg-green-100 p-4 rounded-full w-16 h-16 mx-auto mb-4 flex items-center justify-center">
              <Icon name="Star" size={24} className="text-green-600" />
            </div>
            <h4 className="font-semibold text-green-800 mb-2">Excel</h4>
            <p className="text-sm text-green-700">Perfect your core offerings</p>
          </div>
          <div className="text-center">
            <div className="bg-blue-100 p-4 rounded-full w-16 h-16 mx-auto mb-4 flex items-center justify-center">
              <Icon name="Community" size={24} className="text-blue-600" />
            </div>
            <h4 className="font-semibold text-blue-800 mb-2">Connect</h4>
            <p className="text-sm text-blue-700">Build customer relationships</p>
          </div>
          <div className="text-center">
            <div className="bg-purple-100 p-4 rounded-full w-16 h-16 mx-auto mb-4 flex items-center justify-center">
              <Icon name="Heritage" size={24} className="text-purple-600" />
            </div>
            <h4 className="font-semibold text-purple-800 mb-2">Expand</h4>
            <p className="text-sm text-purple-700">Add complementary offerings</p>
          </div>
          <div className="text-center">
            <div className="bg-orange-100 p-4 rounded-full w-16 h-16 mx-auto mb-4 flex items-center justify-center">
              <Icon name="Settings" size={24} className="text-orange-600" />
            </div>
            <h4 className="font-semibold text-orange-800 mb-2">Scale</h4>
            <p className="text-sm text-orange-700">Optimize for growth</p>
          </div>
        </div>
      </div>

      <div className="grid lg:grid-cols-2 gap-8">
        <div className="space-y-6">
          <div className="bg-white p-6 rounded-lg border shadow-sm">
            <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
              <Icon name="Star" size={20} className="text-yellow-500 mr-2" />
              Excellence Phase (Months 1-3)
            </h3>
            <div className="space-y-3 text-sm">
              <div className="border-l-4 border-yellow-500 pl-4">
                <h4 className="font-medium text-yellow-800">Master Your Core Menu</h4>
                <ul className="text-gray-600 space-y-1">
                  <li>• Perfect 6-8 signature items</li>
                  <li>• Achieve consistent 5-7 minute service</li>
                  <li>• Maintain food cost under 35%</li>
                  <li>• Get first positive reviews</li>
                </ul>
              </div>
              <div className="border-l-4 border-green-500 pl-4">
                <h4 className="font-medium text-green-800">Build Local Reputation</h4>
                <ul className="text-gray-600 space-y-1">
                  <li>• Focus on neighborhood customers</li>
                  <li>• Encourage social media sharing</li>
                  <li>• Join local business networks</li>
                  <li>• Participate in community events</li>
                </ul>
              </div>
            </div>
          </div>

          <div className="bg-white p-6 rounded-lg border shadow-sm">
            <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
              <Icon name="Community" size={20} className="text-blue-500 mr-2" />
              Connection Phase (Months 4-6)
            </h3>
            <div className="space-y-3 text-sm">
              <div className="border-l-4 border-blue-500 pl-4">
                <h4 className="font-medium text-blue-800">Develop Regular Customers</h4>
                <ul className="text-gray-600 space-y-1">
                  <li>• Target 40% repeat customer rate</li>
                  <li>• Implement loyalty program</li>
                  <li>• Remember names and preferences</li>
                  <li>• Create weekly specials</li>
                </ul>
              </div>
              <div className="border-l-4 border-purple-500 pl-4">
                <h4 className="font-medium text-purple-800">Cultural Programming</h4>
                <ul className="text-gray-600 space-y-1">
                  <li>• Host cultural food education events</li>
                  <li>• Share cooking tips and techniques</li>
                  <li>• Collaborate with other cultural businesses</li>
                  <li>• Create social media content</li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        <div className="space-y-6">
          <div className="bg-white p-6 rounded-lg border shadow-sm">
            <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
              <Icon name="Heritage" size={20} className="text-green-500 mr-2" />
              Expansion Phase (Months 7-12)
            </h3>
            <div className="space-y-3 text-sm">
              <div className="border-l-4 border-green-500 pl-4">
                <h4 className="font-medium text-green-800">Menu Diversification</h4>
                <ul className="text-gray-600 space-y-1">
                  <li>• Add seasonal specialties</li>
                  <li>• Introduce breakfast or dinner options</li>
                  <li>• Create family meal packages</li>
                  <li>• Offer catering for small events</li>
                </ul>
              </div>
              <div className="border-l-4 border-orange-500 pl-4">
                <h4 className="font-medium text-orange-800">Service Expansion</h4>
                <ul className="text-gray-600 space-y-1">
                  <li>• Add delivery radius if possible</li>
                  <li>• Offer meal prep services</li>
                  <li>• Create take-home meal kits</li>
                  <li>• Partner with local businesses</li>
                </ul>
              </div>
            </div>
          </div>

          <div className="bg-white p-6 rounded-lg border shadow-sm">
            <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
              <Icon name="Settings" size={20} className="text-purple-500 mr-2" />
              Scale Phase (Year 2+)
            </h3>
            <div className="space-y-3 text-sm">
              <div className="border-l-4 border-purple-500 pl-4">
                <h4 className="font-medium text-purple-800">Operational Excellence</h4>
                <ul className="text-gray-600 space-y-1">
                  <li>• Streamline all processes</li>
                  <li>• Consider hiring part-time help</li>
                  <li>• Implement technology solutions</li>
                  <li>• Optimize supply chain</li>
                </ul>
              </div>
              <div className="border-l-4 border-red-500 pl-4">
                <h4 className="font-medium text-red-800">Brand Development</h4>
                <ul className="text-gray-600 space-y-1">
                  <li>• Develop signature packaging</li>
                  <li>• Create cookbook or recipe cards</li>
                  <li>• Teach cooking classes</li>
                  <li>• Consider second location</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-gradient-to-r from-purple-500 to-pink-500 text-white p-8 rounded-xl">
        <div className="text-center">
          <h3 className="text-2xl font-bold mb-4">Your Success Milestones</h3>
          <div className="grid md:grid-cols-2 gap-6 max-w-4xl mx-auto">
            <div className="bg-white bg-opacity-20 p-6 rounded-lg">
              <h4 className="font-semibold mb-3">6-Month Goals</h4>
              <ul className="text-sm space-y-1">
                <li>• 50+ orders per week</li>
                <li>• 40% repeat customers</li>
                <li>• $800+ weekly revenue</li>
                <li>• 4.5+ star rating</li>
              </ul>
            </div>
            <div className="bg-white bg-opacity-20 p-6 rounded-lg">
              <h4 className="font-semibold mb-3">12-Month Goals</h4>
              <ul className="text-sm space-y-1">
                <li>• 100+ orders per week</li>
                <li>• Local food destination status</li>
                <li>• $1,500+ weekly revenue</li>
                <li>• Recognized cultural ambassador</li>
              </ul>
            </div>
          </div>
          <div className="mt-6 bg-white bg-opacity-20 p-4 rounded-lg">
            <p className="text-sm">
              Remember: You're not just selling fast food – you're preserving culture, building community, 
              and providing busy people with a connection to authentic flavors. Success comes from staying 
              true to your heritage while meeting modern needs.
            </p>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <div className="max-w-6xl mx-auto p-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-8 rounded-xl mb-8">
        <div className="text-center">
          <h1 className="text-3xl font-bold mb-4">Quick Eats Provider Training</h1>
          <p className="text-xl text-blue-100">Authentic Fast Food Revolution</p>
          <div className="mt-4 text-sm bg-white bg-opacity-20 inline-block px-4 py-2 rounded-full">
            Bring homemade quality to the speed of modern life
          </div>
        </div>
      </div>

      {/* Navigation */}
      <div className="bg-white rounded-lg shadow-lg mb-8">
        <div className="flex flex-wrap justify-center border-b">
          {sections.map((section) => (
            <button
              key={section.id}
              onClick={() => setActiveSection(section.id)}
              className={`flex items-center space-x-2 px-4 py-3 border-b-2 transition-colors ${
                activeSection === section.id
                  ? 'border-blue-500 text-blue-600 bg-blue-50'
                  : 'border-transparent text-gray-600 hover:text-blue-600 hover:bg-gray-50'
              }`}
            >
              <Icon name={section.icon} size={16} />
              <span className="font-medium">{section.title}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Content */}
      <div className="bg-white rounded-lg shadow-lg p-8">
        {activeSection === 'introduction' && renderIntroduction()}
        {activeSection === 'competition' && renderCompetition()}
        {activeSection === 'advantages' && renderAdvantages()}
        {activeSection === 'efficiency' && renderEfficiency()}
        {activeSection === 'offerings' && renderOfferings()}
        {activeSection === 'operations' && renderOperations()}
        {activeSection === 'success' && renderSuccess()}
      </div>
    </div>
  );
};

export default QuickEatsTraining;