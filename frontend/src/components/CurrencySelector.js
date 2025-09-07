// Currency Selector Component
import React, { useState, useRef, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { useCurrencySelector } from '../hooks/useCurrency';

const CurrencySelector = ({ className = '', showLabel = true }) => {
  const { t } = useTranslation();
  const {
    userCurrency,
    filteredCurrencies,
    isOpen,
    setIsOpen,
    searchTerm,
    setSearchTerm,
    selectCurrency,
    isLoading
  } = useCurrencySelector();
  
  const dropdownRef = useRef(null);
  const searchInputRef = useRef(null);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false);
        setSearchTerm('');
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [setIsOpen, setSearchTerm]);

  // Focus search input when dropdown opens
  useEffect(() => {
    if (isOpen && searchInputRef.current) {
      setTimeout(() => {
        searchInputRef.current.focus();
      }, 100);
    }
  }, [isOpen]);

  const handleCurrencySelect = async (currencyCode) => {
    const success = await selectCurrency(currencyCode);
    if (!success) {
      // Show error message
      console.error('Failed to set currency preference');
    }
  };

  const currentCurrencyInfo = filteredCurrencies.find(([code]) => code === userCurrency)?.[1] || 
    { name: userCurrency, symbol: userCurrency };

  if (isLoading) {
    return (
      <div className={`flex items-center space-x-2 ${className}`}>
        <div className="animate-pulse bg-gray-200 h-6 w-16 rounded"></div>
        {showLabel && <div className="animate-pulse bg-gray-200 h-4 w-20 rounded"></div>}
      </div>
    );
  }

  return (
    <div ref={dropdownRef} className={`relative inline-block text-left ${className}`}>
      {showLabel && (
        <label className="block text-sm font-medium text-gray-700 mb-1">
          {t('currency.label', 'Currency')}
        </label>
      )}
      
      <div>
        <button
          type="button"
          onClick={() => setIsOpen(!isOpen)}
          className="inline-flex justify-center items-center w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
          aria-expanded={isOpen}
          aria-haspopup="true"
        >
          <span className="flex items-center space-x-2">
            <span className="text-lg">{currentCurrencyInfo.symbol}</span>
            <span className="font-medium">{userCurrency}</span>
            <span className="text-xs text-gray-500 hidden sm:inline truncate max-w-20">
              {currentCurrencyInfo.name}
            </span>
          </span>
          <svg
            className={`ml-2 h-4 w-4 transform transition-transform duration-200 ${isOpen ? 'rotate-180' : ''}`}
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 20 20"
            fill="currentColor"
          >
            <path
              fillRule="evenodd"
              d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
              clipRule="evenodd"
            />
          </svg>
        </button>

        {isOpen && (
          <div className="absolute right-0 mt-2 w-72 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 z-50">
            <div className="p-3 border-b border-gray-100">
              <input
                ref={searchInputRef}
                type="text"
                placeholder={t('currency.search', 'Search currencies...')}
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
              />
            </div>
            
            <div className="max-h-60 overflow-y-auto py-1">
              {filteredCurrencies.length > 0 ? (
                filteredCurrencies.map(([code, info]) => (
                  <button
                    key={code}
                    onClick={() => handleCurrencySelect(code)}
                    className={`${
                      code === userCurrency
                        ? 'bg-indigo-100 text-indigo-900'
                        : 'text-gray-900 hover:bg-gray-100'
                    } group flex items-center justify-between w-full px-4 py-3 text-sm transition-colors duration-150`}
                  >
                    <div className="flex items-center space-x-3">
                      <span className="text-lg font-medium">{info.symbol}</span>
                      <div className="flex flex-col items-start">
                        <span className="font-medium">{code}</span>
                        <span className="text-xs text-gray-500 truncate max-w-32">
                          {info.name}
                        </span>
                      </div>
                    </div>
                    
                    <div className="flex items-center space-x-2">
                      {info.countries && info.countries.length > 0 && (
                        <div className="flex space-x-1">
                          {info.countries.slice(0, 3).map(country => (
                            <span key={country} className="text-xs bg-gray-100 px-1 py-0.5 rounded">
                              {country}
                            </span>
                          ))}
                          {info.countries.length > 3 && (
                            <span className="text-xs text-gray-400">+{info.countries.length - 3}</span>
                          )}
                        </div>
                      )}
                      
                      {code === userCurrency && (
                        <svg className="h-4 w-4 text-indigo-600" fill="currentColor" viewBox="0 0 20 20">
                          <path
                            fillRule="evenodd"
                            d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                            clipRule="evenodd"
                          />
                        </svg>
                      )}
                    </div>
                  </button>
                ))
              ) : (
                <div className="px-4 py-3 text-sm text-gray-500 text-center">
                  {t('currency.noResults', 'No currencies found')}
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default CurrencySelector;