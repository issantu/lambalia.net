// Price Display Component with Automatic Currency Conversion
import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { usePrice, useCommission } from '../hooks/useCurrency';

const PriceDisplay = ({ 
  amount, 
  currency, 
  showCommission = false, 
  commissionRate = 0.15,
  showConversionToggle = true,
  className = '',
  size = 'normal' // 'small', 'normal', 'large'
}) => {
  const { t } = useTranslation();
  const {
    convertedPrice,
    formattedPrice,
    formattedBasePrice,
    conversionRate,
    isConverting,
    showConversion,
    baseCurrency,
    targetCurrency
  } = usePrice(amount, currency);
  
  const { calculateCommission, isCalculating } = useCommission();
  const [showOriginal, setShowOriginal] = useState(false);
  const [commissionInfo, setCommissionInfo] = useState(null);

  // Calculate commission on mount if needed
  React.useEffect(() => {
    if (showCommission && amount && currency) {
      calculateCommission(amount, currency, commissionRate).then(setCommissionInfo);
    }
  }, [showCommission, amount, currency, commissionRate, calculateCommission]);

  // Size classes
  const sizeClasses = {
    small: {
      price: 'text-sm',
      originalPrice: 'text-xs',
      commission: 'text-xs',
      button: 'text-xs px-2 py-1'
    },
    normal: {
      price: 'text-lg font-semibold',
      originalPrice: 'text-sm',
      commission: 'text-sm',
      button: 'text-xs px-2 py-1'
    },
    large: {
      price: 'text-2xl font-bold',
      originalPrice: 'text-base',
      commission: 'text-base',
      button: 'text-sm px-3 py-1'
    }
  };

  const classes = sizeClasses[size];

  if (isConverting) {
    return (
      <div className={`flex items-center space-x-2 ${className}`}>
        <div className="animate-pulse bg-gray-200 h-6 w-20 rounded"></div>
        <div className="text-xs text-gray-500">{t('currency.converting', 'Converting...')}</div>
      </div>
    );
  }

  const togglePriceDisplay = () => {
    setShowOriginal(!showOriginal);
  };

  const displayPrice = showOriginal ? formattedBasePrice : formattedPrice;
  const displayCurrency = showOriginal ? baseCurrency : targetCurrency;

  return (
    <div className={`price-display ${className}`}>
      {/* Main Price */}
      <div className="flex items-center space-x-2">
        <span className={`text-gray-900 ${classes.price}`}>
          {displayPrice}
        </span>
        
        {/* Conversion Toggle Button */}
        {showConversion && showConversionToggle && (
          <button
            onClick={togglePriceDisplay}
            className={`bg-gray-100 hover:bg-gray-200 text-gray-600 rounded-md transition-colors duration-150 ${classes.button}`}
            title={showOriginal ? 
              t('currency.showConverted', 'Show in your currency') : 
              t('currency.showOriginal', 'Show original price')
            }
          >
            {showOriginal ? targetCurrency : baseCurrency}
          </button>
        )}
      </div>

      {/* Secondary Price (Original/Converted) */}
      {showConversion && !showOriginal && (
        <div className={`text-gray-500 mt-1 ${classes.originalPrice}`}>
          {t('currency.originalPrice', 'Originally')}: {formattedBasePrice}
          <span className="ml-2 text-xs bg-blue-100 text-blue-800 px-1 py-0.5 rounded">
            1 {baseCurrency} = {conversionRate.toFixed(4)} {targetCurrency}
          </span>
        </div>
      )}

      {/* Commission Information */}
      {showCommission && commissionInfo && (
        <div className={`mt-2 p-3 bg-yellow-50 border border-yellow-200 rounded-md ${classes.commission}`}>
          {isCalculating ? (
            <div className="flex items-center space-x-2">
              <div className="animate-spin h-4 w-4 border-2 border-yellow-500 border-t-transparent rounded-full"></div>
              <span>{t('currency.calculatingCommission', 'Calculating commission...')}</span>
            </div>
          ) : (
            <div className="space-y-1">
              <div className="flex justify-between items-center">
                <span className="text-yellow-800 font-medium">
                  {t('currency.lambaliaCommission', 'Lambalia Commission')} ({(commissionRate * 100).toFixed(1)}%)
                </span>
                <span className="text-yellow-900 font-semibold">
                  -{commissionInfo.commission_local?.toFixed(2)} {currency}
                </span>
              </div>
              
              <div className="flex justify-between items-center">
                <span className="text-yellow-800">
                  {t('currency.youReceive', 'You receive')}
                </span>
                <span className="text-green-700 font-semibold">
                  {commissionInfo.net_amount_local?.toFixed(2)} {currency}
                </span>
              </div>
              
              {commissionInfo.amount_usd && currency !== 'USD' && (
                <div className="pt-2 border-t border-yellow-300">
                  <div className="text-xs text-yellow-700">
                    {t('currency.usdEquivalent', 'USD equivalent')}: 
                    <span className="ml-1">
                      ~${commissionInfo.amount_usd?.toFixed(2)} USD
                    </span>
                    <span className="ml-1 text-yellow-600">
                      (Commission: ${commissionInfo.commission_usd?.toFixed(2)})
                    </span>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      )}

      {/* Rate Source Indicator */}
      {showConversion && (
        <div className="mt-1 text-xs text-gray-400">
          {t('currency.rateSource', 'Exchange rate')}: {
            conversionRate === 1 ? t('currency.direct', 'Direct') : t('currency.live', 'Live')
          }
        </div>
      )}
    </div>
  );
};

// Simplified Price Component for inline use
export const SimplePrice = ({ amount, currency, className = '' }) => {
  const { formattedPrice, isConverting } = usePrice(amount, currency);
  
  if (isConverting) {
    return <span className={`animate-pulse ${className}`}>...</span>;
  }
  
  return <span className={className}>{formattedPrice}</span>;
};

// Commission-only display component
export const CommissionDisplay = ({ amount, currency, commissionRate = 0.15, className = '' }) => {
  const { calculateCommission } = useCommission();
  const [commissionInfo, setCommissionInfo] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  React.useEffect(() => {
    if (amount && currency) {
      setIsLoading(true);
      calculateCommission(amount, currency, commissionRate)
        .then(setCommissionInfo)
        .finally(() => setIsLoading(false));
    }
  }, [amount, currency, commissionRate, calculateCommission]);

  if (isLoading) {
    return (
      <div className={`animate-pulse ${className}`}>
        <div className="h-4 bg-gray-200 rounded w-24"></div>
      </div>
    );
  }

  if (!commissionInfo) return null;

  return (
    <div className={`commission-display ${className}`}>
      <div className="flex justify-between text-sm">
        <span className="text-gray-600">Platform Fee ({(commissionRate * 100).toFixed(1)}%)</span>
        <span className="text-red-600">-{commissionInfo.commission_local?.toFixed(2)} {currency}</span>
      </div>
      <div className="flex justify-between text-sm font-semibold">
        <span className="text-gray-800">You receive</span>
        <span className="text-green-600">{commissionInfo.net_amount_local?.toFixed(2)} {currency}</span>
      </div>
    </div>
  );
};

export default PriceDisplay;