// Currency Exchange and Localization Service
import { useTranslation } from 'react-i18next';

class CurrencyService {
  constructor() {
    this.apiBaseUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';
    this.cache = new Map();
    this.cacheDuration = 5 * 60 * 1000; // 5 minutes
    this.supportedCurrencies = {};
    this.userCurrency = 'USD';
    this.exchangeRates = {};
    
    // Initialize
    this.initializeService();
  }

  async initializeService() {
    try {
      await this.loadSupportedCurrencies();
      await this.detectUserCurrency();
    } catch (error) {
      console.error('Currency service initialization failed:', error);
    }
  }

  /**
   * Load supported currencies from backend
   */
  async loadSupportedCurrencies() {
    try {
      const response = await fetch(`${this.apiBaseUrl}/api/currency/supported`);
      const data = await response.json();
      
      this.supportedCurrencies = data.supported_currencies;
      this.languageCurrencyMapping = data.language_currency_mapping;
      
      return this.supportedCurrencies;
    } catch (error) {
      console.error('Failed to load supported currencies:', error);
      // Fallback to basic currencies
      this.supportedCurrencies = {
        'USD': { name: 'US Dollar', symbol: '$', countries: ['US'] },
        'EUR': { name: 'Euro', symbol: '€', countries: ['DE', 'FR', 'IT', 'ES'] },
        'GBP': { name: 'British Pound', symbol: '£', countries: ['GB'] },
        'JPY': { name: 'Japanese Yen', symbol: '¥', countries: ['JP'] }
      };
    }
  }

  /**
   * Detect user's preferred currency based on language and location
   */
  async detectUserCurrency() {
    try {
      const user = this.getCurrentUser();
      const language = localStorage.getItem('i18nextLng') || 'en';
      const country = this.getUserCountry();
      
      if (user && user.id) {
        const response = await fetch(
          `${this.apiBaseUrl}/api/currency/user-preference/${user.id}?language_code=${language}&country_code=${country}`,
          {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
          }
        );
        
        if (response.ok) {
          const data = await response.json();
          this.userCurrency = data.preferred_currency;
          localStorage.setItem('userCurrency', this.userCurrency);
          return this.userCurrency;
        }
      }
      
      // Fallback to language-based detection
      this.userCurrency = this.languageCurrencyMapping?.[language] || 'USD';
      localStorage.setItem('userCurrency', this.userCurrency);
      
    } catch (error) {
      console.error('Currency detection failed:', error);
      this.userCurrency = localStorage.getItem('userCurrency') || 'USD';
    }
    
    return this.userCurrency;
  }

  /**
   * Get current user from localStorage or context
   */
  getCurrentUser() {
    try {
      const userStr = localStorage.getItem('user');
      return userStr ? JSON.parse(userStr) : null;
    } catch {
      return null;
    }
  }

  /**
   * Get user's country code (simplified implementation)
   */
  getUserCountry() {
    // Try to get from user profile
    const user = this.getCurrentUser();
    if (user && user.country_code) {
      return user.country_code;
    }
    
    // Try to get from browser
    try {
      const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
      const countryMapping = {
        'America/New_York': 'US',
        'America/Chicago': 'US',
        'America/Denver': 'US',
        'America/Los_Angeles': 'US',
        'Europe/London': 'GB',
        'Europe/Paris': 'FR',
        'Europe/Berlin': 'DE',
        'Europe/Rome': 'IT',
        'Europe/Madrid': 'ES',
        'Asia/Tokyo': 'JP',
        'Asia/Shanghai': 'CN',
        'Asia/Seoul': 'KR',
        'Asia/Kolkata': 'IN'
      };
      
      return countryMapping[timezone] || 'US';
    } catch {
      return 'US'; // Default fallback
    }
  }

  /**
   * Get exchange rate between currencies
   */
  async getExchangeRate(fromCurrency, toCurrency = null) {
    const targetCurrency = toCurrency || this.userCurrency;
    const cacheKey = `${fromCurrency}_${targetCurrency}`;
    
    // Check cache
    const cached = this.cache.get(cacheKey);
    if (cached && (Date.now() - cached.timestamp) < this.cacheDuration) {
      return cached.rate;
    }
    
    try {
      const response = await fetch(
        `${this.apiBaseUrl}/api/currency/rates/${fromCurrency}?target_currencies=${targetCurrency}`
      );
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      
      const data = await response.json();
      const rate = data.rates[targetCurrency];
      
      if (rate && !rate.error) {
        // Cache the rate
        this.cache.set(cacheKey, {
          rate: rate.rate,
          timestamp: Date.now(),
          source: rate.source
        });
        
        return rate.rate;
      } else {
        throw new Error(rate?.error || 'Rate not available');
      }
      
    } catch (error) {
      console.error(`Exchange rate fetch failed for ${fromCurrency} -> ${targetCurrency}:`, error);
      
      // Return fallback rate
      if (fromCurrency === targetCurrency) return 1.0;
      return this.getFallbackRate(fromCurrency, targetCurrency);
    }
  }

  /**
   * Get fallback exchange rate
   */
  getFallbackRate(fromCurrency, toCurrency) {
    const fallbackRates = {
      'EUR_USD': 1.08,
      'GBP_USD': 1.27,
      'JPY_USD': 0.0067,
      'CAD_USD': 0.74,
      'AUD_USD': 0.66,
      'CHF_USD': 1.10,
      'CNY_USD': 0.14,
      'INR_USD': 0.012,
      'BRL_USD': 0.20,
      'MXN_USD': 0.059
    };
    
    const key = `${fromCurrency}_${toCurrency}`;
    const reverseKey = `${toCurrency}_${fromCurrency}`;
    
    if (fallbackRates[key]) {
      return fallbackRates[key];
    } else if (fallbackRates[reverseKey]) {
      return 1 / fallbackRates[reverseKey];
    }
    
    return 1.0; // Default to 1:1 if no fallback available
  }

  /**
   * Convert currency amount
   */
  async convertCurrency(amount, fromCurrency, toCurrency = null) {
    const targetCurrency = toCurrency || this.userCurrency;
    
    if (fromCurrency === targetCurrency) {
      return {
        originalAmount: amount,
        convertedAmount: amount,
        rate: 1.0,
        fromCurrency,
        toCurrency: targetCurrency
      };
    }
    
    try {
      const response = await fetch(`${this.apiBaseUrl}/api/currency/convert`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          amount: amount,
          from_currency: fromCurrency,
          to_currency: targetCurrency
        })
      });
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      
      const data = await response.json();
      
      return {
        originalAmount: data.original_amount,
        convertedAmount: data.converted_amount,
        rate: data.exchange_rate,
        fromCurrency: data.original_currency,
        toCurrency: data.target_currency,
        rateSource: data.rate_source,
        timestamp: data.timestamp
      };
      
    } catch (error) {
      console.error('Currency conversion failed:', error);
      
      // Fallback conversion using cached or fallback rates
      const rate = await this.getExchangeRate(fromCurrency, targetCurrency);
      return {
        originalAmount: amount,
        convertedAmount: amount * rate,
        rate: rate,
        fromCurrency,
        toCurrency: targetCurrency,
        rateSource: 'fallback'
      };
    }
  }

  /**
   * Format currency amount with proper symbol and locale
   */
  formatCurrency(amount, currency = null, options = {}) {
    const targetCurrency = currency || this.userCurrency;
    const currencyInfo = this.supportedCurrencies[targetCurrency];
    
    const defaultOptions = {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
      ...options
    };
    
    try {
      // Use Intl.NumberFormat for proper localization
      const formatter = new Intl.NumberFormat(this.getLocaleForCurrency(targetCurrency), {
        style: 'currency',
        currency: targetCurrency,
        ...defaultOptions
      });
      
      return formatter.format(amount);
    } catch (error) {
      // Fallback formatting
      const symbol = currencyInfo?.symbol || targetCurrency;
      const formattedAmount = amount.toFixed(defaultOptions.maximumFractionDigits);
      return `${symbol}${formattedAmount}`;
    }
  }

  /**
   * Get appropriate locale for currency formatting
   */
  getLocaleForCurrency(currency) {
    const localeMap = {
      'USD': 'en-US',
      'EUR': 'de-DE',
      'GBP': 'en-GB',
      'JPY': 'ja-JP',
      'CAD': 'en-CA',
      'AUD': 'en-AU',
      'CHF': 'de-CH',
      'CNY': 'zh-CN',
      'INR': 'hi-IN',
      'BRL': 'pt-BR',
      'MXN': 'es-MX',
      'KRW': 'ko-KR'
    };
    
    return localeMap[currency] || 'en-US';
  }

  /**
   * Calculate commission for a transaction
   */
  async calculateCommission(amount, currency, commissionRate = 0.15) {
    try {
      const response = await fetch(`${this.apiBaseUrl}/api/currency/calculate-commission`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          amount: amount,
          currency: currency,
          commission_rate: commissionRate
        })
      });
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      
      const data = await response.json();
      return data.commission_calculation;
      
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
        rate_source: 'fallback'
      };
    }
  }

  /**
   * Set user's currency preference
   */
  async setUserCurrencyPreference(currency) {
    const user = this.getCurrentUser();
    if (!user || !user.id) {
      // Store locally for guest users
      localStorage.setItem('userCurrency', currency);
      this.userCurrency = currency;
      return true;
    }
    
    try {
      const response = await fetch(`${this.apiBaseUrl}/api/currency/user-preference/${user.id}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          currency_code: currency
        })
      });
      
      if (response.ok) {
        this.userCurrency = currency;
        localStorage.setItem('userCurrency', currency);
        
        // Trigger currency change event
        window.dispatchEvent(new CustomEvent('currencyChanged', {
          detail: { newCurrency: currency }
        }));
        
        return true;
      }
      
      return false;
      
    } catch (error) {
      console.error('Failed to set currency preference:', error);
      return false;
    }
  }

  /**
   * Get user's current currency
   */
  getUserCurrency() {
    return this.userCurrency;
  }

  /**
   * Get supported currencies list
   */
  getSupportedCurrencies() {
    return this.supportedCurrencies;
  }

  /**
   * Get currency info
   */
  getCurrencyInfo(currency) {
    return this.supportedCurrencies[currency] || {
      name: currency,
      symbol: currency,
      countries: []
    };
  }

  /**
   * Clear rate cache
   */
  clearCache() {
    this.cache.clear();
  }
}

// Create singleton instance
const currencyService = new CurrencyService();

export default currencyService;