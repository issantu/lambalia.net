// Currency Management Hooks
import { useState, useEffect, useCallback } from 'react';
import { useTranslation } from 'react-i18next';
import currencyService from '../services/currencyService';

/**
 * Hook for currency conversion and formatting
 */
export const useCurrency = () => {
  const { i18n } = useTranslation();
  const [userCurrency, setUserCurrency] = useState('USD');
  const [supportedCurrencies, setSupportedCurrencies] = useState({});
  const [isLoading, setIsLoading] = useState(true);
  const [exchangeRates, setExchangeRates] = useState({});

  // Initialize currency service
  useEffect(() => {
    const initializeCurrency = async () => {
      setIsLoading(true);
      
      try {
        // Load supported currencies
        const currencies = await currencyService.loadSupportedCurrencies();
        setSupportedCurrencies(currencies);
        
        // Detect user currency
        const detectedCurrency = await currencyService.detectUserCurrency();
        setUserCurrency(detectedCurrency);
        
      } catch (error) {
        console.error('Currency initialization failed:', error);
        setUserCurrency('USD'); // Fallback
      } finally {
        setIsLoading(false);
      }
    };

    initializeCurrency();
  }, []);

  // Listen for currency changes
  useEffect(() => {
    const handleCurrencyChange = (event) => {
      setUserCurrency(event.detail.newCurrency);
      // Clear exchange rates cache when currency changes
      setExchangeRates({});
    };

    window.addEventListener('currencyChanged', handleCurrencyChange);
    
    return () => {
      window.removeEventListener('currencyChanged', handleCurrencyChange);
    };
  }, []);

  // Update currency when language changes
  useEffect(() => {
    if (!isLoading && i18n.language) {
      const currencyForLanguage = currencyService.languageCurrencyMapping?.[i18n.language];
      if (currencyForLanguage && currencyForLanguage !== userCurrency) {
        // Only auto-change if user hasn't manually set a preference
        const hasManualPreference = localStorage.getItem('userCurrencyManual');
        if (!hasManualPreference) {
          currencyService.setUserCurrencyPreference(currencyForLanguage);
        }
      }
    }
  }, [i18n.language, userCurrency, isLoading]);

  // Convert currency
  const convertCurrency = useCallback(async (amount, fromCurrency, toCurrency = null) => {
    const targetCurrency = toCurrency || userCurrency;
    
    try {
      const result = await currencyService.convertCurrency(amount, fromCurrency, targetCurrency);
      
      // Cache the exchange rate
      setExchangeRates(prev => ({
        ...prev,
        [`${fromCurrency}_${targetCurrency}`]: result.rate
      }));
      
      return result;
    } catch (error) {
      console.error('Currency conversion failed:', error);
      return {
        originalAmount: amount,
        convertedAmount: amount,
        rate: 1.0,
        fromCurrency,
        toCurrency: targetCurrency,
        error: error.message
      };
    }
  }, [userCurrency]);

  // Format currency amount
  const formatCurrency = useCallback((amount, currency = null, options = {}) => {
    const targetCurrency = currency || userCurrency;
    return currencyService.formatCurrency(amount, targetCurrency, options);
  }, [userCurrency]);

  // Set user currency preference
  const setCurrency = useCallback(async (currency) => {
    const success = await currencyService.setUserCurrencyPreference(currency);
    if (success) {
      localStorage.setItem('userCurrencyManual', 'true');
      setUserCurrency(currency);
    }
    return success;
  }, []);

  // Get exchange rate
  const getExchangeRate = useCallback(async (fromCurrency, toCurrency = null) => {
    const targetCurrency = toCurrency || userCurrency;
    const cacheKey = `${fromCurrency}_${targetCurrency}`;
    
    // Check cache first
    if (exchangeRates[cacheKey]) {
      return exchangeRates[cacheKey];
    }
    
    try {
      const rate = await currencyService.getExchangeRate(fromCurrency, targetCurrency);
      
      setExchangeRates(prev => ({
        ...prev,
        [cacheKey]: rate
      }));
      
      return rate;
    } catch (error) {
      console.error('Failed to get exchange rate:', error);
      return 1.0; // Fallback
    }
  }, [userCurrency, exchangeRates]);

  return {
    userCurrency,
    supportedCurrencies,
    isLoading,
    convertCurrency,
    formatCurrency,
    setCurrency,
    getExchangeRate,
    exchangeRates
  };
};

/**
 * Hook for commission calculations
 */
export const useCommission = () => {
  const { userCurrency } = useCurrency();
  const [isCalculating, setIsCalculating] = useState(false);

  const calculateCommission = useCallback(async (amount, currency, commissionRate = 0.15) => {
    setIsCalculating(true);
    
    try {
      const result = await currencyService.calculateCommission(amount, currency, commissionRate);
      return result;
    } catch (error) {
      console.error('Commission calculation failed:', error);
      
      // Fallback calculation
      const commissionLocal = amount * commissionRate;
      const netAmount = amount - commissionLocal;
      
      return {
        original_amount: amount,
        original_currency: currency,
        commission_rate: commissionRate,
        commission_local: commissionLocal,
        net_amount_local: netAmount,
        error: error.message
      };
    } finally {
      setIsCalculating(false);
    }
  }, []);

  return {
    calculateCommission,
    isCalculating,
    userCurrency
  };
};

/**
 * Hook for real-time price display with currency conversion
 */
export const usePrice = (baseAmount, baseCurrency) => {
  const { userCurrency, convertCurrency, formatCurrency, isLoading } = useCurrency();
  const [convertedPrice, setConvertedPrice] = useState(null);
  const [conversionRate, setConversionRate] = useState(1);
  const [isConverting, setIsConverting] = useState(false);

  useEffect(() => {
    const convertPrice = async () => {
      if (!baseAmount || !baseCurrency || isLoading) return;
      
      setIsConverting(true);
      
      try {
        const result = await convertCurrency(baseAmount, baseCurrency, userCurrency);
        setConvertedPrice(result.convertedAmount);
        setConversionRate(result.rate);
      } catch (error) {
        console.error('Price conversion failed:', error);
        setConvertedPrice(baseAmount);
        setConversionRate(1);
      } finally {
        setIsConverting(false);
      }
    };

    convertPrice();
  }, [baseAmount, baseCurrency, userCurrency, convertCurrency, isLoading]);

  const formattedPrice = convertedPrice !== null 
    ? formatCurrency(convertedPrice, userCurrency)
    : formatCurrency(baseAmount, baseCurrency);

  const formattedBasePrice = formatCurrency(baseAmount, baseCurrency);

  return {
    convertedPrice,
    formattedPrice,
    formattedBasePrice,
    conversionRate,
    isConverting,
    showConversion: baseCurrency !== userCurrency && convertedPrice !== null,
    baseCurrency,
    targetCurrency: userCurrency
  };
};

/**
 * Hook for currency selector component
 */
export const useCurrencySelector = () => {
  const { userCurrency, supportedCurrencies, setCurrency, isLoading } = useCurrency();
  const [isOpen, setIsOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');

  const filteredCurrencies = Object.entries(supportedCurrencies).filter(([code, info]) => {
    if (!searchTerm) return true;
    const search = searchTerm.toLowerCase();
    return (
      code.toLowerCase().includes(search) ||
      info.name.toLowerCase().includes(search) ||
      info.countries.some(country => country.toLowerCase().includes(search))
    );
  });

  const selectCurrency = useCallback(async (currencyCode) => {
    const success = await setCurrency(currencyCode);
    if (success) {
      setIsOpen(false);
      setSearchTerm('');
    }
    return success;
  }, [setCurrency]);

  return {
    userCurrency,
    supportedCurrencies,
    filteredCurrencies,
    isOpen,
    setIsOpen,
    searchTerm,
    setSearchTerm,
    selectCurrency,
    isLoading
  };
};