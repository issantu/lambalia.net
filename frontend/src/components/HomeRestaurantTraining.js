// Home Restaurant Host Training Guide
import React, { useState } from 'react';
import { Icon, AnimatedIcon } from './ProfessionalIcons';

const HomeRestaurantTraining = () => {
  const [activeSection, setActiveSection] = useState('introduction');

  const sections = [
    { id: 'introduction', title: 'Your Unique Advantage', icon: 'Heart' },
    { id: 'competition', title: 'Know Your Competition', icon: 'Restaurant' },
    { id: 'advantages', title: 'Why You Win', icon: 'Star' },
    { id: 'success-tips', title: 'Success Strategies', icon: 'Settings' },
    { id: 'experience', title: 'Creating Magic', icon: 'Heritage' },
    { id: 'pricing', title: 'Value Pricing', icon: 'Dollar' },
    { id: 'community', title: 'Building Community', icon: 'Community' }
  ];

  const renderIntroduction = () => (
    <div className="space-y-6">
      <div className="text-center">
        <AnimatedIcon name="Heart" size={64} className="text-red-500 mx-auto mb-4" />
        <h2 className="text-3xl font-bold text-gray-800 mb-4">Welcome, Home Restaurant Host!</h2>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          You're not just another restaurant. You're a cultural ambassador, a storyteller, and a bridge between authentic heritage and hungry hearts.
        </p>
      </div>

      <div className="bg-gradient-to-r from-orange-50 to-red-50 p-8 rounded-xl border-l-4 border-orange-500">
        <h3 className="text-xl font-semibold text-orange-800 mb-4">Your Core Advantage</h3>
        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <h4 className="font-medium text-gray-800 mb-2">🏠 What You Are:</h4>
            <ul className="text-gray-600 space-y-1 text-sm">
              <li>• A passionate home cook sharing family recipes</li>
              <li>• Someone who cooks for love, not just profit</li>
              <li>• A keeper of cultural traditions and stories</li>
              <li>• A community connector and cultural bridge</li>
              <li>• An authentic voice in your cuisine</li>
            </ul>
          </div>
          <div>
            <h4 className="font-medium text-gray-800 mb-2">🏢 What Restaurants Are:</h4>
            <ul className="text-gray-600 space-y-1 text-sm">
              <li>• Commercial businesses focused on profit</li>
              <li>• Standardized recipes and processes</li>
              <li>• Impersonal, transactional experiences</li>
              <li>• Limited cultural storytelling</li>
              <li>• Generic atmosphere and service</li>
            </ul>
          </div>
        </div>
      </div>

      <div className="bg-green-50 p-6 rounded-lg">
        <h3 className="text-lg font-semibold text-green-800 mb-3">Your Mission Statement</h3>
        <p className="text-green-700 italic text-lg text-center">
          "I share the dishes I love with my family, bringing authentic flavors and stories to my community. 
          Every meal is a cultural exchange, every guest becomes family."
        </p>
      </div>
    </div>
  );

  const renderCompetition = () => (
    <div className="space-y-6">
      <div className="text-center mb-8">
        <Icon name="Restaurant" size={48} className="text-blue-600 mx-auto mb-4" />
        <h2 className="text-2xl font-bold text-gray-800">Understanding Your Competition</h2>
        <p className="text-gray-600">Know what you're up against to leverage your advantages</p>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-lg border shadow-sm">
          <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
            <Icon name="Restaurant" size={20} className="text-red-600 mr-2" />
            Local Restaurants
          </h3>
          
          <div className="space-y-4">
            <div>
              <h4 className="font-medium text-gray-700 mb-2">Their Strengths:</h4>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• Consistent food quality and presentation</li>
                <li>• Professional service and atmosphere</li>
                <li>• Established reputation and reviews</li>
                <li>• Marketing budgets and visibility</li>
                <li>• Multiple staff for faster service</li>
                <li>• Licensed bar and extensive menu</li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-medium text-gray-700 mb-2">Their Weaknesses:</h4>
              <ul className="text-sm text-red-600 space-y-1">
                <li>• Generic, commercialized recipes</li>
                <li>• Impersonal, transactional experience</li>
                <li>• Higher overhead costs = higher prices</li>
                <li>• No cultural storytelling or personal connection</li>
                <li>• Limited authenticity for ethnic cuisines</li>
                <li>• Profit-driven rather than passion-driven</li>
              </ul>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg border shadow-sm">
          <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
            <Icon name="Heritage" size={20} className="text-green-600 mr-2" />
            Your Competitive Analysis
          </h3>
          
          <div className="space-y-4">
            <div className="bg-green-50 p-4 rounded-lg">
              <h4 className="font-medium text-green-800 mb-2">Price Comparison:</h4>
              <div className="text-sm space-y-1">
                <div className="flex justify-between">
                  <span>Local Restaurant:</span>
                  <span className="font-medium">$18-35 per person</span>
                </div>
                <div className="flex justify-between">
                  <span>Your Home Restaurant:</span>
                  <span className="font-medium text-green-600">$12-25 per person</span>
                </div>
                <div className="text-xs text-green-600 mt-2">
                  ✓ 20-40% lower cost with higher authenticity
                </div>
              </div>
            </div>
            
            <div className="bg-blue-50 p-4 rounded-lg">
              <h4 className="font-medium text-blue-800 mb-2">Experience Comparison:</h4>
              <div className="text-sm space-y-2">
                <div>
                  <strong>Restaurant:</strong> Standard service, limited interaction
                </div>
                <div>
                  <strong>Your Home:</strong> Personal stories, cultural education, family atmosphere
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-yellow-50 p-6 rounded-lg border-l-4 border-yellow-500">
        <h3 className="text-lg font-semibold text-yellow-800 mb-3">Strategic Positioning</h3>
        <p className="text-yellow-700 mb-4">
          You're not competing on their terms - you're creating an entirely different category of dining experience.
        </p>
        <div className="grid md:grid-cols-3 gap-4 text-sm">
          <div className="text-center">
            <div className="font-medium text-yellow-800">Restaurants Sell:</div>
            <div className="text-yellow-600">Food & Service</div>
          </div>
          <div className="text-center">
            <div className="font-medium text-yellow-800">You Offer:</div>
            <div className="text-yellow-600">Culture & Connection</div>
          </div>
          <div className="text-center">
            <div className="font-medium text-yellow-800">Result:</div>
            <div className="text-yellow-600">Unforgettable Experience</div>
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
        <p className="text-gray-600">Why food enthusiasts will choose you over restaurants</p>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        <div className="bg-gradient-to-br from-green-50 to-blue-50 p-6 rounded-xl">
          <h3 className="text-lg font-semibold text-green-800 mb-4 flex items-center">
            <Icon name="Heart" size={20} className="text-red-500 mr-2" />
            Authenticity Advantage
          </h3>
          <ul className="space-y-3 text-sm text-gray-700">
            <li className="flex items-start">
              <Icon name="ChevronRight" size={16} className="text-green-600 mr-2 mt-0.5" />
              <div>
                <strong>Family Recipes:</strong> These are dishes you actually cook for your loved ones, not commercialized versions
              </div>
            </li>
            <li className="flex items-start">
              <Icon name="ChevronRight" size={16} className="text-green-600 mr-2 mt-0.5" />
              <div>
                <strong>Cultural Stories:</strong> Share the history, traditions, and memories behind each dish
              </div>
            </li>
            <li className="flex items-start">
              <Icon name="ChevronRight" size={16} className="text-green-600 mr-2 mt-0.5" />
              <div>
                <strong>Personal Touch:</strong> Adjust seasoning based on guest preferences and dietary needs
              </div>
            </li>
            <li className="flex items-start">
              <Icon name="ChevronRight" size={16} className="text-green-600 mr-2 mt-0.5" />
              <div>
                <strong>Heritage Connection:</strong> Connect diaspora communities with authentic homeland flavors
              </div>
            </li>
          </ul>
        </div>

        <div className="bg-gradient-to-br from-purple-50 to-pink-50 p-6 rounded-xl">
          <h3 className="text-lg font-semibold text-purple-800 mb-4 flex items-center">
            <Icon name="Community" size={20} className="text-purple-600 mr-2" />
            Experience Advantage
          </h3>
          <ul className="space-y-3 text-sm text-gray-700">
            <li className="flex items-start">
              <Icon name="ChevronRight" size={16} className="text-purple-600 mr-2 mt-0.5" />
              <div>
                <strong>Home Atmosphere:</strong> Intimate, warm, family-like dining environment
              </div>
            </li>
            <li className="flex items-start">
              <Icon name="ChevronRight" size={16} className="text-purple-600 mr-2 mt-0.5" />
              <div>
                <strong>Personal Connection:</strong> Guests feel like they're dining with friends, not customers
              </div>
            </li>
            <li className="flex items-start">
              <Icon name="ChevronRight" size={16} className="text-purple-600 mr-2 mt-0.5" />
              <div>
                <strong>Cultural Education:</strong> Learn about ingredients, techniques, and traditions
              </div>
            </li>
            <li className="flex items-start">
              <Icon name="ChevronRight" size={16} className="text-purple-600 mr-2 mt-0.5" />
              <div>
                <strong>Customization:</strong> Adapt dishes to dietary restrictions with care and creativity
              </div>
            </li>
          </ul>
        </div>

        <div className="bg-gradient-to-br from-orange-50 to-yellow-50 p-6 rounded-xl">
          <h3 className="text-lg font-semibold text-orange-800 mb-4 flex items-center">
            <Icon name="Dollar" size={20} className="text-green-600 mr-2" />
            Value Advantage
          </h3>
          <ul className="space-y-3 text-sm text-gray-700">
            <li className="flex items-start">
              <Icon name="ChevronRight" size={16} className="text-orange-600 mr-2 mt-0.5" />
              <div>
                <strong>Better Pricing:</strong> Lower overhead means better value for authentic experience
              </div>
            </li>
            <li className="flex items-start">
              <Icon name="ChevronRight" size={16} className="text-orange-600 mr-2 mt-0.5" />
              <div>
                <strong>Generous Portions:</strong> Cook with love, serve with abundance like family meals
              </div>
            </li>
            <li className="flex items-start">
              <Icon name="ChevronRight" size={16} className="text-orange-600 mr-2 mt-0.5" />
              <div>
                <strong>Complete Experience:</strong> Food + culture + stories + personal connection
              </div>
            </li>
            <li className="flex items-start">
              <Icon name="ChevronRight" size={16} className="text-orange-600 mr-2 mt-0.5" />
              <div>
                <strong>No Hidden Fees:</strong> Transparent pricing through Lambalia's verification system
              </div>
            </li>
          </ul>
        </div>

        <div className="bg-gradient-to-br from-blue-50 to-indigo-50 p-6 rounded-xl">
          <h3 className="text-lg font-semibold text-blue-800 mb-4 flex items-center">
            <Icon name="Heritage" size={20} className="text-blue-600 mr-2" />
            Uniqueness Advantage
          </h3>
          <ul className="space-y-3 text-sm text-gray-700">
            <li className="flex items-start">
              <Icon name="ChevronRight" size={16} className="text-blue-600 mr-2 mt-0.5" />
              <div>
                <strong>One-of-a-Kind Menu:</strong> Dishes restaurants don't offer or can't make authentically
              </div>
            </li>
            <li className="flex items-start">
              <Icon name="ChevronRight" size={16} className="text-blue-600 mr-2 mt-0.5" />
              <div>
                <strong>Seasonal Flexibility:</strong> Change menu based on fresh ingredients and family favorites
              </div>
            </li>
            <li className="flex items-start">
              <Icon name="ChevronRight" size={16} className="text-blue-600 mr-2 mt-0.5" />
              <div>
                <strong>Limited Availability:</strong> Exclusivity creates desire and premium positioning
              </div>
            </li>
            <li className="flex items-start">
              <Icon name="ChevronRight" size={16} className="text-blue-600 mr-2 mt-0.5" />
              <div>
                <strong>Memory Making:</strong> Guests remember experiences, not just meals
              </div>
            </li>
          </ul>
        </div>
      </div>

      <div className="bg-gradient-to-r from-green-500 to-blue-500 text-white p-8 rounded-xl text-center">
        <h3 className="text-xl font-bold mb-4">Your Secret Weapon</h3>
        <p className="text-lg mb-4">
          "You cook with love, not for profit. Guests can taste the difference."
        </p>
        <div className="bg-white bg-opacity-20 p-4 rounded-lg">
          <p className="text-sm">
            While restaurants focus on maximizing profit per table, you focus on sharing your heritage and creating connections. 
            This fundamental difference in motivation creates an authenticity that money can't buy.
          </p>
        </div>
      </div>
    </div>
  );

  const renderSuccessTips = () => (
    <div className="space-y-6">
      <div className="text-center mb-8">
        <Icon name="Settings" size={48} className="text-purple-600 mx-auto mb-4" />
        <h2 className="text-2xl font-bold text-gray-800">Success Strategies</h2>
        <p className="text-gray-600">Practical tips to outshine local restaurants</p>
      </div>

      <div className="grid lg:grid-cols-2 gap-8">
        <div className="space-y-6">
          <div className="bg-white p-6 rounded-lg border shadow-sm">
            <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
              <Icon name="ChefHat" size={20} className="text-orange-600 mr-2" />
              Master Your Signature Dishes
            </h3>
            <div className="space-y-3 text-sm text-gray-700">
              <div className="flex items-start">
                <span className="bg-orange-100 text-orange-800 text-xs font-medium px-2 py-1 rounded mr-3 mt-0.5">TIP</span>
                <div>Perfect 3-5 dishes rather than offering a huge menu. Master what you love cooking most.</div>
              </div>
              <div className="flex items-start">
                <span className="bg-orange-100 text-orange-800 text-xs font-medium px-2 py-1 rounded mr-3 mt-0.5">TIP</span>
                <div>Practice the complete meal experience: timing, presentation, and storytelling.</div>
              </div>
              <div className="flex items-start">
                <span className="bg-orange-100 text-orange-800 text-xs font-medium px-2 py-1 rounded mr-3 mt-0.5">TIP</span>
                <div>Document family recipes exactly as you make them - consistency builds reputation.</div>
              </div>
            </div>
          </div>

          <div className="bg-white p-6 rounded-lg border shadow-sm">
            <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
              <Icon name="Heart" size={20} className="text-red-600 mr-2" />
              Create Emotional Connection
            </h3>
            <div className="space-y-3 text-sm text-gray-700">
              <div className="flex items-start">
                <span className="bg-red-100 text-red-800 text-xs font-medium px-2 py-1 rounded mr-3 mt-0.5">STORY</span>
                <div>Share the story behind each dish - who taught you, special occasions, family memories.</div>
              </div>
              <div className="flex items-start">
                <span className="bg-red-100 text-red-800 text-xs font-medium px-2 py-1 rounded mr-3 mt-0.5">WELCOME</span>
                <div>Greet guests like family - learn their names, remember their preferences.</div>
              </div>
              <div className="flex items-start">
                <span className="bg-red-100 text-red-800 text-xs font-medium px-2 py-1 rounded mr-3 mt-0.5">SHARE</span>
                <div>Eat with your guests when appropriate - show that you love your own cooking.</div>
              </div>
            </div>
          </div>

          <div className="bg-white p-6 rounded-lg border shadow-sm">
            <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
              <Icon name="Settings" size={20} className="text-blue-600 mr-2" />
              Optimize Your Space
            </h3>
            <div className="space-y-3 text-sm text-gray-700">
              <div className="flex items-start">
                <span className="bg-blue-100 text-blue-800 text-xs font-medium px-2 py-1 rounded mr-3 mt-0.5">AMBIANCE</span>
                <div>Create warm lighting, play background music from your culture, add personal touches.</div>
              </div>
              <div className="flex items-start">
                <span className="bg-blue-100 text-blue-800 text-xs font-medium px-2 py-1 rounded mr-3 mt-0.5">COMFORT</span>
                <div>Ensure comfortable seating, good temperature, and clean, welcoming environment.</div>
              </div>
              <div className="flex items-start">
                <span className="bg-blue-100 text-blue-800 text-xs font-medium px-2 py-1 rounded mr-3 mt-0.5">CULTURAL</span>
                <div>Display cultural artifacts, family photos, or heritage items that tell your story.</div>
              </div>
            </div>
          </div>
        </div>

        <div className="space-y-6">
          <div className="bg-white p-6 rounded-lg border shadow-sm">
            <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
              <Icon name="Star" size={20} className="text-yellow-600 mr-2" />
              Exceed Expectations
            </h3>
            <div className="space-y-3 text-sm text-gray-700">
              <div className="flex items-start">
                <span className="bg-yellow-100 text-yellow-800 text-xs font-medium px-2 py-1 rounded mr-3 mt-0.5">SURPRISE</span>
                <div>Offer a small appetizer or dessert "on the house" - generosity wins hearts.</div>
              </div>
              <div className="flex items-start">
                <span className="bg-yellow-100 text-yellow-800 text-xs font-medium px-2 py-1 rounded mr-3 mt-0.5">TEACH</span>
                <div>Show guests how to eat traditional dishes properly or share cooking tips.</div>
              </div>
              <div className="flex items-start">
                <span className="bg-yellow-100 text-yellow-800 text-xs font-medium px-2 py-1 rounded mr-3 mt-0.5">REMEMBER</span>
                <div>Follow up with guests - ask how they liked it, share recipe cards if requested.</div>
              </div>
            </div>
          </div>

          <div className="bg-white p-6 rounded-lg border shadow-sm">
            <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
              <Icon name="Community" size={20} className="text-green-600 mr-2" />
              Build Community
            </h3>
            <div className="space-y-3 text-sm text-gray-700">
              <div className="flex items-start">
                <span className="bg-green-100 text-green-800 text-xs font-medium px-2 py-1 rounded mr-3 mt-0.5">CONNECT</span>
                <div>Introduce guests to each other - create a community dining experience.</div>
              </div>
              <div className="flex items-start">
                <span className="bg-green-100 text-green-800 text-xs font-medium px-2 py-1 rounded mr-3 mt-0.5">REGULAR</span>
                <div>Offer regular themed nights - "Moroccan Mondays" or "Filipino Fridays".</div>
              </div>
              <div className="flex items-start">
                <span className="bg-green-100 text-green-800 text-xs font-medium px-2 py-1 rounded mr-3 mt-0.5">CULTURE</span>
                <div>Host cultural events - teach cooking classes, celebrate holidays, share traditions.</div>
              </div>
            </div>
          </div>

          <div className="bg-gradient-to-r from-purple-50 to-pink-50 p-6 rounded-lg border">
            <h3 className="text-lg font-semibold text-purple-800 mb-4">Success Metrics to Track</h3>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <div className="font-medium text-purple-700">Guest Satisfaction</div>
                <div className="text-purple-600">• Repeat customers</div>
                <div className="text-purple-600">• Personal referrals</div>
                <div className="text-purple-600">• Social media mentions</div>
              </div>
              <div>
                <div className="font-medium text-purple-700">Cultural Impact</div>
                <div className="text-purple-600">• Stories shared</div>
                <div className="text-purple-600">• Recipe requests</div>
                <div className="text-purple-600">• Cultural questions asked</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  const renderExperience = () => (
    <div className="space-y-6">
      <div className="text-center mb-8">
        <Icon name="Heritage" size={48} className="text-indigo-600 mx-auto mb-4" />
        <h2 className="text-2xl font-bold text-gray-800">Creating Magical Experiences</h2>
        <p className="text-gray-600">Turn meals into memories that last a lifetime</p>
      </div>

      <div className="bg-gradient-to-r from-indigo-50 to-purple-50 p-8 rounded-xl">
        <h3 className="text-xl font-semibold text-indigo-800 mb-6 text-center">The Perfect Home Restaurant Experience</h3>
        
        <div className="grid md:grid-cols-3 gap-6">
          <div className="text-center">
            <div className="bg-indigo-100 p-4 rounded-full w-16 h-16 mx-auto mb-4 flex items-center justify-center">
              <Icon name="Heart" size={24} className="text-indigo-600" />
            </div>
            <h4 className="font-semibold text-indigo-800 mb-2">Before Arrival</h4>
            <ul className="text-sm text-indigo-700 space-y-1">
              <li>• Confirm dietary restrictions</li>
              <li>• Share cultural context</li>
              <li>• Set expectations warmly</li>
              <li>• Prepare special touches</li>
            </ul>
          </div>
          
          <div className="text-center">
            <div className="bg-indigo-100 p-4 rounded-full w-16 h-16 mx-auto mb-4 flex items-center justify-center">
              <Icon name="ChefHat" size={24} className="text-indigo-600" />
            </div>
            <h4 className="font-semibold text-indigo-800 mb-2">During Experience</h4>
            <ul className="text-sm text-indigo-700 space-y-1">
              <li>• Personal welcome & stories</li>
              <li>• Explain each dish's history</li>
              <li>• Engage in cultural exchange</li>
              <li>• Share cooking techniques</li>
            </ul>
          </div>
          
          <div className="text-center">
            <div className="bg-indigo-100 p-4 rounded-full w-16 h-16 mx-auto mb-4 flex items-center justify-center">
              <Icon name="Community" size={24} className="text-indigo-600" />
            </div>
            <h4 className="font-semibold text-indigo-800 mb-2">After Dining</h4>
            <ul className="text-sm text-indigo-700 space-y-1">
              <li>• Share recipe highlights</li>
              <li>• Connect with community</li>
              <li>• Invite return visits</li>
              <li>• Create lasting bonds</li>
            </ul>
          </div>
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-lg border shadow-sm">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Storytelling Framework</h3>
          <div className="space-y-4">
            <div className="border-l-4 border-green-500 pl-4">
              <h4 className="font-medium text-green-800">Dish Origin Story</h4>
              <p className="text-sm text-gray-600">"This recipe came from my grandmother in Lagos. She taught me when I was 12..."</p>
            </div>
            <div className="border-l-4 border-blue-500 pl-4">
              <h4 className="font-medium text-blue-800">Cultural Context</h4>
              <p className="text-sm text-gray-600">"In our culture, we eat this during celebrations because it represents..."</p>
            </div>
            <div className="border-l-4 border-purple-500 pl-4">
              <h4 className="font-medium text-purple-800">Personal Connection</h4>
              <p className="text-sm text-gray-600">"I make this for my family every Sunday. My kids request it for their birthdays..."</p>
            </div>
            <div className="border-l-4 border-orange-500 pl-4">
              <h4 className="font-medium text-orange-800">Cooking Secrets</h4>
              <p className="text-sm text-gray-600">"The secret ingredient is patience - we let it simmer for 3 hours, just like..."</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg border shadow-sm">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Experience Enhancements</h3>
          <div className="space-y-3">
            <div className="flex items-start space-x-3">
              <Icon name="Star" size={16} className="text-yellow-500 mt-1" />
              <div>
                <h4 className="font-medium text-gray-800">Cultural Music</h4>
                <p className="text-sm text-gray-600">Play traditional music from your heritage during meals</p>
              </div>
            </div>
            <div className="flex items-start space-x-3">
              <Icon name="Heritage" size={16} className="text-blue-500 mt-1" />
              <div>
                <h4 className="font-medium text-gray-800">Traditional Table Setting</h4>
                <p className="text-sm text-gray-600">Use authentic serving dishes, utensils, or presentation styles</p>
              </div>
            </div>
            <div className="flex items-start space-x-3">
              <Icon name="Recipe" size={16} className="text-green-500 mt-1" />
              <div>
                <h4 className="font-medium text-gray-800">Recipe Cards</h4>
                <p className="text-sm text-gray-600">Offer simplified versions of recipes for guests to take home</p>
              </div>
            </div>
            <div className="flex items-start space-x-3">
              <Icon name="Community" size={16} className="text-purple-500 mt-1" />
              <div>
                <h4 className="font-medium text-gray-800">Cultural Artifacts</h4>
                <p className="text-sm text-gray-600">Display photos, items, or decorations from your homeland</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-yellow-50 p-6 rounded-lg border-l-4 border-yellow-500">
        <h3 className="text-lg font-semibold text-yellow-800 mb-3">The Magic Formula</h3>
        <div className="grid md:grid-cols-4 gap-4 text-center">
          <div>
            <div className="text-2xl font-bold text-yellow-600">Authenticity</div>
            <div className="text-sm text-yellow-700">Real recipes, real stories</div>
          </div>
          <div>
            <div className="text-xl text-yellow-600">+</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-yellow-600">Connection</div>
            <div className="text-sm text-yellow-700">Personal bonds, cultural exchange</div>
          </div>
          <div>
            <div className="text-xl text-yellow-600">=</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-yellow-600">Magic</div>
            <div className="text-sm text-yellow-700">Unforgettable experiences</div>
          </div>
        </div>
      </div>
    </div>
  );

  const renderPricing = () => (
    <div className="space-y-6">
      <div className="text-center mb-8">
        <Icon name="Dollar" size={48} className="text-green-600 mx-auto mb-4" />
        <h2 className="text-2xl font-bold text-gray-800">Value-Based Pricing Strategy</h2>
        <p className="text-gray-600">Price for value, not just cost - show why you're worth every penny</p>
      </div>

      <div className="grid lg:grid-cols-2 gap-8">
        <div className="space-y-6">
          <div className="bg-green-50 p-6 rounded-lg border">
            <h3 className="text-lg font-semibold text-green-800 mb-4">Pricing Philosophy</h3>
            <div className="space-y-3 text-sm text-gray-700">
              <div className="flex items-start">
                <Icon name="Heart" size={16} className="text-red-500 mr-2 mt-1" />
                <div>
                  <strong>Price for the Experience:</strong> You're not just selling food - you're selling culture, stories, and connection
                </div>
              </div>
              <div className="flex items-start">
                <Icon name="Star" size={16} className="text-yellow-500 mr-2 mt-1" />
                <div>
                  <strong>Value Your Authenticity:</strong> Authentic cultural experiences command premium prices
                </div>
              </div>
              <div className="flex items-start">
                <Icon name="Community" size={16} className="text-blue-500 mr-2 mt-1" />
                <div>
                  <strong>Fair to Everyone:</strong> Profitable for you, valuable for guests, competitive with restaurants
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white p-6 rounded-lg border shadow-sm">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Pricing Framework</h3>
            <div className="space-y-4">
              <div className="bg-gray-50 p-4 rounded-lg">
                <h4 className="font-medium text-gray-800 mb-2">Base Meal Cost</h4>
                <div className="text-sm space-y-1">
                  <div className="flex justify-between">
                    <span>Ingredients & Preparation:</span>
                    <span className="font-medium">$8-12</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Your Time & Skill:</span>
                    <span className="font-medium">$6-10</span>
                  </div>
                  <div className="flex justify-between border-t pt-1">
                    <span className="font-medium">Base Price:</span>
                    <span className="font-semibold">$14-22</span>
                  </div>
                </div>
              </div>
              
              <div className="bg-blue-50 p-4 rounded-lg">
                <h4 className="font-medium text-blue-800 mb-2">Experience Premium</h4>
                <div className="text-sm space-y-1">
                  <div className="flex justify-between">
                    <span>Cultural Storytelling:</span>
                    <span className="font-medium">$3-5</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Personal Attention:</span>
                    <span className="font-medium">$2-4</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Home Atmosphere:</span>
                    <span className="font-medium">$2-3</span>
                  </div>
                  <div className="flex justify-between border-t pt-1">
                    <span className="font-medium">Experience Value:</span>
                    <span className="font-semibold">$7-12</span>
                  </div>
                </div>
              </div>
              
              <div className="bg-green-50 p-4 rounded-lg">
                <h4 className="font-medium text-green-800 mb-2">Final Pricing</h4>
                <div className="text-sm space-y-1">
                  <div className="flex justify-between">
                    <span>Total Value:</span>
                    <span className="font-medium">$21-34</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Competitive Adjustment:</span>
                    <span className="font-medium">-$3 to -$8</span>
                  </div>
                  <div className="flex justify-between border-t pt-1">
                    <span className="font-semibold text-green-800">Recommended Price:</span>
                    <span className="font-bold text-green-600">$18-28</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="space-y-6">
          <div className="bg-white p-6 rounded-lg border shadow-sm">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Competitive Positioning</h3>
            <div className="space-y-4">
              <div className="comparison-item">
                <h4 className="font-medium text-gray-800 mb-2">vs. Casual Restaurants ($12-18)</h4>
                <div className="bg-gray-50 p-3 rounded text-sm">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <div className="font-medium text-red-600">They Offer:</div>
                      <div className="text-gray-600">Standard food, basic service</div>
                    </div>
                    <div>
                      <div className="font-medium text-green-600">You Offer:</div>
                      <div className="text-gray-600">Authentic experience + culture</div>
                    </div>
                  </div>
                  <div className="mt-2 p-2 bg-green-100 rounded text-green-800 text-xs">
                    <strong>Your Price: $18-22</strong> - Premium justified by unique experience
                  </div>
                </div>
              </div>
              
              <div className="comparison-item">
                <h4 className="font-medium text-gray-800 mb-2">vs. Mid-Range Restaurants ($20-30)</h4>
                <div className="bg-gray-50 p-3 rounded text-sm">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <div className="font-medium text-red-600">They Offer:</div>
                      <div className="text-gray-600">Better food, professional service</div>
                    </div>
                    <div>
                      <div className="font-medium text-green-600">You Offer:</div>
                      <div className="text-gray-600">Personal connection + authenticity</div>
                    </div>
                  </div>
                  <div className="mt-2 p-2 bg-blue-100 rounded text-blue-800 text-xs">
                    <strong>Your Price: $22-26</strong> - Competitive with added cultural value
                  </div>
                </div>
              </div>
              
              <div className="comparison-item">
                <h4 className="font-medium text-gray-800 mb-2">vs. Upscale Restaurants ($35+)</h4>
                <div className="bg-gray-50 p-3 rounded text-sm">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <div className="font-medium text-red-600">They Offer:</div>
                      <div className="text-gray-600">Fancy atmosphere, high prices</div>
                    </div>
                    <div>
                      <div className="font-medium text-green-600">You Offer:</div>
                      <div className="text-gray-600">Intimate setting + real stories</div>
                    </div>
                  </div>
                  <div className="mt-2 p-2 bg-purple-100 rounded text-purple-800 text-xs">
                    <strong>Your Price: $25-28</strong> - Exceptional value for unique experience
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-yellow-50 p-6 rounded-lg border-l-4 border-yellow-500">
            <h3 className="text-lg font-semibold text-yellow-800 mb-4">Pricing Justification Template</h3>
            <div className="text-sm text-yellow-700 space-y-2">
              <p><strong>"Why $25 per person?"</strong></p>
              <ul className="list-disc list-inside space-y-1 ml-4">
                <li>Premium ingredients sourced authentically ($8)</li>
                <li>3 hours of preparation and cooking ($10)</li>
                <li>Cultural storytelling and education ($4)</li>
                <li>Intimate home dining experience ($3)</li>
              </ul>
              <p className="mt-3 font-medium">
                "You're not just buying dinner - you're experiencing my heritage, learning my family's history, and becoming part of our cultural story."
              </p>
            </div>
          </div>

          <div className="bg-red-50 p-6 rounded-lg border-l-4 border-red-500">
            <h3 className="text-lg font-semibold text-red-800 mb-3">Pricing Don'ts</h3>
            <div className="text-sm text-red-700 space-y-2">
              <div className="flex items-start">
                <Icon name="Settings" size={16} className="text-red-600 mr-2 mt-0.5" />
                <div><strong>Don't undersell yourself</strong> - Cheap prices signal low quality</div>
              </div>
              <div className="flex items-start">
                <Icon name="Settings" size={16} className="text-red-600 mr-2 mt-0.5" />
                <div><strong>Don't copy restaurant prices</strong> - You offer something different</div>
              </div>
              <div className="flex items-start">
                <Icon name="Settings" size={16} className="text-red-600 mr-2 mt-0.5" />
                <div><strong>Don't forget your costs</strong> - Include time, ingredients, and overhead</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  const renderCommunity = () => (
    <div className="space-y-6">
      <div className="text-center mb-8">
        <Icon name="Community" size={48} className="text-purple-600 mx-auto mb-4" />
        <h2 className="text-2xl font-bold text-gray-800">Building Your Food Community</h2>
        <p className="text-gray-600">Create lasting relationships that go beyond single meals</p>
      </div>

      <div className="bg-gradient-to-r from-purple-50 to-pink-50 p-8 rounded-xl">
        <h3 className="text-xl font-semibold text-purple-800 mb-6 text-center">Community Building Strategy</h3>
        <div className="grid md:grid-cols-3 gap-6">
          <div className="text-center">
            <div className="bg-purple-100 p-4 rounded-full w-16 h-16 mx-auto mb-4 flex items-center justify-center">
              <Icon name="Heart" size={24} className="text-purple-600" />
            </div>
            <h4 className="font-semibold text-purple-800 mb-2">Connect</h4>
            <p className="text-sm text-purple-700">Build personal relationships with every guest</p>
          </div>
          <div className="text-center">
            <div className="bg-purple-100 p-4 rounded-full w-16 h-16 mx-auto mb-4 flex items-center justify-center">
              <Icon name="Heritage" size={24} className="text-purple-600" />
            </div>
            <h4 className="font-semibold text-purple-800 mb-2">Share</h4>
            <p className="text-sm text-purple-700">Share culture, stories, and authentic experiences</p>
          </div>
          <div className="text-center">
            <div className="bg-purple-100 p-4 rounded-full w-16 h-16 mx-auto mb-4 flex items-center justify-center">
              <Icon name="Community" size={24} className="text-purple-600" />
            </div>
            <h4 className="font-semibold text-purple-800 mb-2">Grow</h4>
            <p className="text-sm text-purple-700">Expand through referrals and repeat visits</p>
          </div>
        </div>
      </div>

      <div className="grid lg:grid-cols-2 gap-8">
        <div className="space-y-6">
          <div className="bg-white p-6 rounded-lg border shadow-sm">
            <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
              <Icon name="Star" size={20} className="text-yellow-500 mr-2" />
              Creating Regular Guests
            </h3>
            <div className="space-y-3">
              <div className="border-l-4 border-blue-500 pl-4">
                <h4 className="font-medium text-blue-800">Remember Personal Details</h4>
                <p className="text-sm text-gray-600">Names, food preferences, special occasions, family details</p>
              </div>
              <div className="border-l-4 border-green-500 pl-4">
                <h4 className="font-medium text-green-800">Seasonal Menus</h4>
                <p className="text-sm text-gray-600">Change offerings to give repeat customers new experiences</p>
              </div>
              <div className="border-l-4 border-purple-500 pl-4">
                <h4 className="font-medium text-purple-800">Special Invitations</h4>
                <p className="text-sm text-gray-600">Invite favorite guests to try new dishes or special events</p>
              </div>
              <div className="border-l-4 border-orange-500 pl-4">
                <h4 className="font-medium text-orange-800">Cultural Calendar</h4>
                <p className="text-sm text-gray-600">Celebrate holidays and traditions from your heritage</p>
              </div>
            </div>
          </div>

          <div className="bg-white p-6 rounded-lg border shadow-sm">
            <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
              <Icon name="Message" size={20} className="text-blue-500 mr-2" />
              Word-of-Mouth Marketing
            </h3>
            <div className="space-y-3 text-sm">
              <div className="bg-green-50 p-3 rounded-lg">
                <h4 className="font-medium text-green-800 mb-1">Encourage Sharing</h4>
                <ul className="text-green-700 space-y-1">
                  <li>• Ask guests to share photos of their experience</li>
                  <li>• Provide beautiful plating for social media</li>
                  <li>• Share your cultural story - people love authenticity</li>
                </ul>
              </div>
              <div className="bg-blue-50 p-3 rounded-lg">
                <h4 className="font-medium text-blue-800 mb-1">Referral Rewards</h4>
                <ul className="text-blue-700 space-y-1">
                  <li>• Offer small gifts for bringing new guests</li>
                  <li>• Create "friend and family" discount nights</li>
                  <li>• Thank referrers publicly (with permission)</li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        <div className="space-y-6">
          <div className="bg-white p-6 rounded-lg border shadow-sm">
            <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
              <Icon name="Heritage" size={20} className="text-indigo-500 mr-2" />
              Cultural Events & Themes
            </h3>
            <div className="space-y-4">
              <div className="bg-indigo-50 p-4 rounded-lg">
                <h4 className="font-medium text-indigo-800 mb-2">Monthly Theme Ideas</h4>
                <div className="grid grid-cols-2 gap-2 text-sm text-indigo-700">
                  <div>• Regional specialties</div>
                  <div>• Holiday traditions</div>
                  <div>• Family recipe stories</div>
                  <div>• Seasonal ingredients</div>
                  <div>• Cooking techniques</div>
                  <div>• Cultural celebrations</div>
                </div>
              </div>
              <div className="bg-yellow-50 p-4 rounded-lg">
                <h4 className="font-medium text-yellow-800 mb-2">Special Events</h4>
                <ul className="text-sm text-yellow-700 space-y-1">
                  <li>• Cooking classes for small groups</li>
                  <li>• Cultural holiday celebrations</li>
                  <li>• "Meet the Chef" storytelling nights</li>
                  <li>• Ingredient sourcing trips (virtual or real)</li>
                </ul>
              </div>
            </div>
          </div>

          <div className="bg-white p-6 rounded-lg border shadow-sm">
            <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
              <Icon name="Settings" size={20} className="text-gray-600 mr-2" />
              Long-term Success Metrics
            </h3>
            <div className="grid grid-cols-2 gap-4">
              <div className="text-center p-3 bg-green-50 rounded-lg">
                <div className="text-2xl font-bold text-green-600">70%</div>
                <div className="text-sm text-green-700">Repeat Customers</div>
              </div>
              <div className="text-center p-3 bg-blue-50 rounded-lg">
                <div className="text-2xl font-bold text-blue-600">4.8</div>
                <div className="text-sm text-blue-700">Average Rating</div>
              </div>
              <div className="text-center p-3 bg-purple-50 rounded-lg">
                <div className="text-2xl font-bold text-purple-600">85%</div>
                <div className="text-sm text-purple-700">Referral Rate</div>
              </div>
              <div className="text-center p-3 bg-orange-50 rounded-lg">
                <div className="text-2xl font-bold text-orange-600">$180</div>
                <div className="text-sm text-orange-700">Monthly Earnings</div>
              </div>
            </div>
            <p className="text-xs text-gray-500 mt-3 text-center">
              Average successful Home Restaurant host metrics after 6 months
            </p>
          </div>
        </div>
      </div>

      <div className="bg-gradient-to-r from-green-500 to-blue-500 text-white p-8 rounded-xl">
        <div className="text-center">
          <h3 className="text-2xl font-bold mb-4">Your Success Formula</h3>
          <div className="max-w-2xl mx-auto">
            <p className="text-lg mb-6">
              Authentic Food + Personal Stories + Cultural Connection + Community Building = Sustainable Success
            </p>
            <div className="bg-white bg-opacity-20 p-6 rounded-lg">
              <h4 className="font-semibold mb-3">Remember: You're Not Just Competing with Restaurants</h4>
              <p className="text-sm">
                You're creating a new category of dining experience that restaurants can't replicate. 
                Focus on what makes you unique: your heritage, your story, your genuine love for sharing culture through food.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <div className="max-w-6xl mx-auto p-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-orange-600 to-red-600 text-white p-8 rounded-xl mb-8">
        <div className="text-center">
          <h1 className="text-3xl font-bold mb-4">Home Restaurant Host Training</h1>
          <p className="text-xl text-orange-100">Transform Your Kitchen Into a Cultural Bridge</p>
          <div className="mt-4 text-sm bg-white bg-opacity-20 inline-block px-4 py-2 rounded-full">
            Master the art of authentic hospitality and cultural sharing
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
                  ? 'border-orange-500 text-orange-600 bg-orange-50'
                  : 'border-transparent text-gray-600 hover:text-orange-600 hover:bg-gray-50'
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
        {activeSection === 'success-tips' && renderSuccessTips()}
        {activeSection === 'experience' && renderExperience()}
        {activeSection === 'pricing' && renderPricing()}
        {activeSection === 'community' && renderCommunity()}
      </div>
    </div>
  );
};

export default HomeRestaurantTraining;