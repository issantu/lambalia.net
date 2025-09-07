# Currency Exchange and Commission Consolidation Service
import asyncio
import aiohttp
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from motor.motor_asyncio import AsyncIOMotorDatabase
import logging
from pydantic import BaseModel, Field
from decimal import Decimal, ROUND_HALF_UP
import uuid

logger = logging.getLogger(__name__)

class CurrencyRate(BaseModel):
    base_currency: str
    target_currency: str
    rate: Decimal
    timestamp: datetime
    source: str  # 'live', 'cached', 'fallback'
    expires_at: datetime

class TransactionRecord(BaseModel):
    transaction_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    transaction_type: str  # 'purchase', 'commission', 'payout', 'fee'
    amount_original: Decimal
    currency_original: str
    amount_usd: Decimal
    exchange_rate: Decimal
    commission_rate: Decimal = Decimal('0.15')  # 15% default
    lambalia_commission: Decimal
    net_amount: Decimal
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    country_code: Optional[str] = None
    payment_method: Optional[str] = None
    status: str = "pending"  # pending, completed, failed
    metadata: Dict[str, Any] = {}

class CommissionSummary(BaseModel):
    period_start: datetime
    period_end: datetime
    total_transactions: int
    total_volume_usd: Decimal
    total_commission_usd: Decimal
    by_currency: Dict[str, Dict]
    by_country: Dict[str, Dict]
    top_earners: List[Dict]

class CurrencyExchangeService:
    """Service for real-time currency exchange and commission consolidation"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.cache_duration = timedelta(minutes=5)  # 5-minute cache for exchange rates
        self.supported_currencies = {
            'USD': {'name': 'US Dollar', 'symbol': '$', 'countries': ['US']},
            'EUR': {'name': 'Euro', 'symbol': '€', 'countries': ['DE', 'FR', 'IT', 'ES', 'NL']},
            'GBP': {'name': 'British Pound', 'symbol': '£', 'countries': ['GB']},
            'JPY': {'name': 'Japanese Yen', 'symbol': '¥', 'countries': ['JP']},
            'CAD': {'name': 'Canadian Dollar', 'symbol': 'C$', 'countries': ['CA']},
            'AUD': {'name': 'Australian Dollar', 'symbol': 'A$', 'countries': ['AU']},
            'CHF': {'name': 'Swiss Franc', 'symbol': 'CHF', 'countries': ['CH']},
            'CNY': {'name': 'Chinese Yuan', 'symbol': '¥', 'countries': ['CN']},
            'INR': {'name': 'Indian Rupee', 'symbol': '₹', 'countries': ['IN']},
            'BRL': {'name': 'Brazilian Real', 'symbol': 'R$', 'countries': ['BR']},
            'MXN': {'name': 'Mexican Peso', 'symbol': '$', 'countries': ['MX']},
            'ZAR': {'name': 'South African Rand', 'symbol': 'R', 'countries': ['ZA']},
            'KRW': {'name': 'South Korean Won', 'symbol': '₩', 'countries': ['KR']},
            'SEK': {'name': 'Swedish Krona', 'symbol': 'kr', 'countries': ['SE']},
            'NOK': {'name': 'Norwegian Krone', 'symbol': 'kr', 'countries': ['NO']},
            'PLN': {'name': 'Polish Złoty', 'symbol': 'zł', 'countries': ['PL']},
            'TRY': {'name': 'Turkish Lira', 'symbol': '₺', 'countries': ['TR']},
            'SGD': {'name': 'Singapore Dollar', 'symbol': 'S$', 'countries': ['SG']},
            'HKD': {'name': 'Hong Kong Dollar', 'symbol': 'HK$', 'countries': ['HK']},
            'NZD': {'name': 'New Zealand Dollar', 'symbol': 'NZ$', 'countries': ['NZ']}
        }
        
        # Language to currency mapping for automatic detection
        self.language_currency_map = {
            'en': 'USD',  # Default to USD for English
            'es': 'USD',  # Spanish could be USD (US) or other currencies
            'fr': 'EUR',  # French -> EUR
            'de': 'EUR',  # German -> EUR
            'it': 'EUR',  # Italian -> EUR
            'pt': 'BRL',  # Portuguese -> BRL (Brazil)
            'ja': 'JPY',  # Japanese -> JPY
            'zh': 'CNY',  # Chinese -> CNY
            'ar': 'USD',  # Arabic -> USD (varies by country)
            'ru': 'USD',  # Russian -> USD (varies)
            'hi': 'INR',  # Hindi -> INR
            'ko': 'KRW'   # Korean -> KRW
        }
        
        # Exchange rate APIs (free tiers available)
        self.rate_apis = [
            {
                'name': 'ExchangeRate-API',
                'url': 'https://api.exchangerate-api.com/v4/latest/USD',
                'free_tier': True,
                'requests_per_month': 100000
            },
            {
                'name': 'Fixer.io',
                'url': 'http://data.fixer.io/api/latest',
                'free_tier': True,
                'requests_per_month': 1000
            },
            {
                'name': 'CurrencyAPI',
                'url': 'https://api.currencyapi.com/v3/latest',
                'free_tier': True,
                'requests_per_month': 300
            }
        ]
    
    async def get_exchange_rate(self, from_currency: str, to_currency: str = 'USD') -> CurrencyRate:
        """Get real-time exchange rate between currencies"""
        
        if from_currency == to_currency:
            return CurrencyRate(
                base_currency=from_currency,
                target_currency=to_currency,
                rate=Decimal('1.0'),
                timestamp=datetime.utcnow(),
                source='direct',
                expires_at=datetime.utcnow() + timedelta(hours=24)
            )
        
        # Check cache first
        cached_rate = await self._get_cached_rate(from_currency, to_currency)
        if cached_rate and cached_rate.expires_at > datetime.utcnow():
            cached_rate.source = 'cached'
            return cached_rate
        
        # Fetch live rate
        try:
            live_rate = await self._fetch_live_rate(from_currency, to_currency)
            if live_rate:
                # Cache the rate
                await self._cache_rate(live_rate)
                return live_rate
        except Exception as e:
            logger.error(f"Error fetching live exchange rate: {e}")
        
        # Fallback to last known rate or default
        fallback_rate = await self._get_fallback_rate(from_currency, to_currency)
        return fallback_rate
    
    async def _fetch_live_rate(self, from_currency: str, to_currency: str) -> Optional[CurrencyRate]:
        """Fetch live exchange rate from external APIs"""
        
        async with aiohttp.ClientSession() as session:
            # Try ExchangeRate-API first (most reliable free tier)
            try:
                async with session.get(f'https://api.exchangerate-api.com/v4/latest/{from_currency}') as response:
                    if response.status == 200:
                        data = await response.json()
                        if to_currency in data['rates']:
                            rate = Decimal(str(data['rates'][to_currency]))
                            return CurrencyRate(
                                base_currency=from_currency,
                                target_currency=to_currency,
                                rate=rate,
                                timestamp=datetime.utcnow(),
                                source='live',
                                expires_at=datetime.utcnow() + self.cache_duration
                            )
            except Exception as e:
                logger.warning(f"ExchangeRate-API failed: {e}")
            
            # Fallback to other APIs
            # Note: In production, you would cycle through APIs and handle API keys
            pass
        
        return None
    
    async def _get_cached_rate(self, from_currency: str, to_currency: str) -> Optional[CurrencyRate]:
        """Get cached exchange rate from database"""
        try:
            cache_key = f"{from_currency}_{to_currency}"
            cached = await self.db.exchange_rate_cache.find_one({"cache_key": cache_key})
            
            if cached:
                return CurrencyRate(**cached['data'])
        except Exception as e:
            logger.error(f"Error getting cached rate: {e}")
        
        return None
    
    async def _cache_rate(self, rate: CurrencyRate) -> None:
        """Cache exchange rate in database"""
        try:
            cache_key = f"{rate.base_currency}_{rate.target_currency}"
            await self.db.exchange_rate_cache.update_one(
                {"cache_key": cache_key},
                {
                    "$set": {
                        "cache_key": cache_key,
                        "data": rate.dict(),
                        "cached_at": datetime.utcnow()
                    }
                },
                upsert=True
            )
        except Exception as e:
            logger.error(f"Error caching rate: {e}")
    
    async def _get_fallback_rate(self, from_currency: str, to_currency: str) -> CurrencyRate:
        """Get fallback rate (last known rate or estimated rate)"""
        
        # Try to get last known rate from cache (even if expired)
        try:
            cache_key = f"{from_currency}_{to_currency}"
            cached = await self.db.exchange_rate_cache.find_one({"cache_key": cache_key})
            
            if cached:
                fallback_rate = CurrencyRate(**cached['data'])
                fallback_rate.source = 'fallback'
                fallback_rate.expires_at = datetime.utcnow() + timedelta(minutes=30)
                return fallback_rate
        except Exception as e:
            logger.error(f"Error getting fallback rate: {e}")
        
        # Default fallback rates (approximate)
        fallback_rates = {
            ('EUR', 'USD'): 1.08,
            ('GBP', 'USD'): 1.27,
            ('JPY', 'USD'): 0.0067,
            ('CAD', 'USD'): 0.74,
            ('AUD', 'USD'): 0.66,
            ('CHF', 'USD'): 1.10,
            ('CNY', 'USD'): 0.14,
            ('INR', 'USD'): 0.012,
            ('BRL', 'USD'): 0.20,
            ('MXN', 'USD'): 0.059
        }
        
        rate_value = fallback_rates.get((from_currency, to_currency), 1.0)
        
        return CurrencyRate(
            base_currency=from_currency,
            target_currency=to_currency,
            rate=Decimal(str(rate_value)),
            timestamp=datetime.utcnow(),
            source='fallback',
            expires_at=datetime.utcnow() + timedelta(hours=1)
        )
    
    async def convert_currency(self, amount: Decimal, from_currency: str, to_currency: str = 'USD') -> Tuple[Decimal, CurrencyRate]:
        """Convert amount between currencies"""
        
        if from_currency == to_currency:
            rate = CurrencyRate(
                base_currency=from_currency,
                target_currency=to_currency,
                rate=Decimal('1.0'),
                timestamp=datetime.utcnow(),
                source='direct',
                expires_at=datetime.utcnow() + timedelta(hours=24)
            )
            return amount, rate
        
        exchange_rate = await self.get_exchange_rate(from_currency, to_currency)
        converted_amount = (amount * exchange_rate.rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        
        return converted_amount, exchange_rate
    
    async def calculate_commission(self, amount: Decimal, currency: str, commission_rate: Decimal = Decimal('0.15')) -> Dict[str, Decimal]:
        """Calculate commission in local currency and USD"""
        
        # Convert to USD for commission calculation
        amount_usd, exchange_rate = await self.convert_currency(amount, currency, 'USD')
        
        # Calculate commission
        commission_local = (amount * commission_rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        commission_usd = (amount_usd * commission_rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        net_amount_local = amount - commission_local
        net_amount_usd = amount_usd - commission_usd
        
        return {
            'original_amount': amount,
            'original_currency': currency,
            'amount_usd': amount_usd,
            'exchange_rate': exchange_rate.rate,
            'commission_rate': commission_rate,
            'commission_local': commission_local,
            'commission_usd': commission_usd,
            'net_amount_local': net_amount_local,
            'net_amount_usd': net_amount_usd,
            'rate_source': exchange_rate.source
        }
    
    async def record_transaction(self, transaction: TransactionRecord) -> str:
        """Record transaction with currency conversion and commission calculation"""
        
        # Ensure USD conversion is calculated
        if transaction.currency_original != 'USD':
            amount_usd, exchange_rate = await self.convert_currency(
                transaction.amount_original,
                transaction.currency_original,
                'USD'
            )
            transaction.amount_usd = amount_usd
            transaction.exchange_rate = exchange_rate.rate
        else:
            transaction.amount_usd = transaction.amount_original
            transaction.exchange_rate = Decimal('1.0')
        
        # Calculate commission
        commission_calculation = await self.calculate_commission(
            transaction.amount_original,
            transaction.currency_original,
            transaction.commission_rate
        )
        
        transaction.lambalia_commission = commission_calculation['commission_usd']
        transaction.net_amount = commission_calculation['net_amount_usd']
        
        # Add metadata
        transaction.metadata.update({
            'commission_calculation': commission_calculation,
            'recorded_at': datetime.utcnow().isoformat()
        })
        
        # Store in database
        await self.db.financial_transactions.insert_one(transaction.dict())
        
        # Update commission summary cache
        await self._update_commission_summary(transaction)
        
        logger.info(f"Transaction recorded: {transaction.transaction_id} - ${transaction.amount_usd} USD")
        
        return transaction.transaction_id
    
    async def _update_commission_summary(self, transaction: TransactionRecord) -> None:
        """Update commission summary for analytics"""
        try:
            today = datetime.utcnow().date()
            
            # Update daily summary
            await self.db.commission_summaries.update_one(
                {"date": today},
                {
                    "$inc": {
                        "total_transactions": 1,
                        "total_volume_usd": float(transaction.amount_usd),
                        "total_commission_usd": float(transaction.lambalia_commission),
                        f"by_currency.{transaction.currency_original}.count": 1,
                        f"by_currency.{transaction.currency_original}.volume": float(transaction.amount_original),
                        f"by_currency.{transaction.currency_original}.commission_usd": float(transaction.lambalia_commission)
                    },
                    "$setOnInsert": {"date": today, "created_at": datetime.utcnow()}
                },
                upsert=True
            )
            
            # Update user earnings
            await self.db.user_earnings.update_one(
                {"user_id": transaction.user_id, "date": today},
                {
                    "$inc": {
                        "total_earned_local": float(transaction.net_amount),
                        "total_earned_usd": float(transaction.net_amount),
                        "transactions_count": 1
                    },
                    "$setOnInsert": {
                        "user_id": transaction.user_id,
                        "date": today,
                        "currency": transaction.currency_original,
                        "created_at": datetime.utcnow()
                    }
                },
                upsert=True
            )
            
        except Exception as e:
            logger.error(f"Error updating commission summary: {e}")
    
    async def get_commission_summary(self, start_date: datetime, end_date: datetime) -> CommissionSummary:
        """Get commission summary for a date range"""
        
        pipeline = [
            {
                "$match": {
                    "timestamp": {"$gte": start_date, "$lte": end_date}
                }
            },
            {
                "$group": {
                    "_id": None,
                    "total_transactions": {"$sum": 1},
                    "total_volume_usd": {"$sum": "$amount_usd"},
                    "total_commission_usd": {"$sum": "$lambalia_commission"},
                    "currencies": {"$addToSet": "$currency_original"},
                    "countries": {"$addToSet": "$country_code"}
                }
            }
        ]
        
        result = await self.db.financial_transactions.aggregate(pipeline).to_list(length=1)
        
        if not result:
            return CommissionSummary(
                period_start=start_date,
                period_end=end_date,
                total_transactions=0,
                total_volume_usd=Decimal('0'),
                total_commission_usd=Decimal('0'),
                by_currency={},
                by_country={},
                top_earners=[]
            )
        
        summary_data = result[0]
        
        # Get breakdown by currency
        currency_breakdown = await self._get_currency_breakdown(start_date, end_date)
        
        # Get breakdown by country
        country_breakdown = await self._get_country_breakdown(start_date, end_date)
        
        # Get top earners
        top_earners = await self._get_top_earners(start_date, end_date)
        
        return CommissionSummary(
            period_start=start_date,
            period_end=end_date,
            total_transactions=summary_data['total_transactions'],
            total_volume_usd=Decimal(str(summary_data['total_volume_usd'])),
            total_commission_usd=Decimal(str(summary_data['total_commission_usd'])),
            by_currency=currency_breakdown,
            by_country=country_breakdown,
            top_earners=top_earners
        )
    
    async def _get_currency_breakdown(self, start_date: datetime, end_date: datetime) -> Dict[str, Dict]:
        """Get transaction breakdown by currency"""
        pipeline = [
            {
                "$match": {
                    "timestamp": {"$gte": start_date, "$lte": end_date}
                }
            },
            {
                "$group": {
                    "_id": "$currency_original",
                    "transaction_count": {"$sum": 1},
                    "total_volume_local": {"$sum": "$amount_original"},
                    "total_volume_usd": {"$sum": "$amount_usd"},
                    "total_commission_usd": {"$sum": "$lambalia_commission"},
                    "avg_exchange_rate": {"$avg": "$exchange_rate"}
                }
            }
        ]
        
        results = await self.db.financial_transactions.aggregate(pipeline).to_list(length=None)
        
        breakdown = {}
        for result in results:
            currency = result['_id']
            breakdown[currency] = {
                'transaction_count': result['transaction_count'],
                'total_volume_local': float(result['total_volume_local']),
                'total_volume_usd': float(result['total_volume_usd']),
                'total_commission_usd': float(result['total_commission_usd']),
                'avg_exchange_rate': float(result['avg_exchange_rate']),
                'currency_info': self.supported_currencies.get(currency, {})
            }
        
        return breakdown
    
    async def _get_country_breakdown(self, start_date: datetime, end_date: datetime) -> Dict[str, Dict]:
        """Get transaction breakdown by country"""
        pipeline = [
            {
                "$match": {
                    "timestamp": {"$gte": start_date, "$lte": end_date},
                    "country_code": {"$ne": None}
                }
            },
            {
                "$group": {
                    "_id": "$country_code",
                    "transaction_count": {"$sum": 1},
                    "total_volume_usd": {"$sum": "$amount_usd"},
                    "total_commission_usd": {"$sum": "$lambalia_commission"},
                    "unique_users": {"$addToSet": "$user_id"}
                }
            }
        ]
        
        results = await self.db.financial_transactions.aggregate(pipeline).to_list(length=None)
        
        breakdown = {}
        for result in results:
            country = result['_id']
            breakdown[country] = {
                'transaction_count': result['transaction_count'],
                'total_volume_usd': float(result['total_volume_usd']),
                'total_commission_usd': float(result['total_commission_usd']),
                'unique_users': len(result['unique_users'])
            }
        
        return breakdown
    
    async def _get_top_earners(self, start_date: datetime, end_date: datetime, limit: int = 10) -> List[Dict]:
        """Get top earning users in the period"""
        pipeline = [
            {
                "$match": {
                    "timestamp": {"$gte": start_date, "$lte": end_date}
                }
            },
            {
                "$group": {
                    "_id": "$user_id",
                    "total_earned_usd": {"$sum": "$net_amount"},
                    "transaction_count": {"$sum": 1},
                    "currencies_used": {"$addToSet": "$currency_original"}
                }
            },
            {
                "$sort": {"total_earned_usd": -1}
            },
            {
                "$limit": limit
            }
        ]
        
        results = await self.db.financial_transactions.aggregate(pipeline).to_list(length=limit)
        
        top_earners = []
        for result in results:
            top_earners.append({
                'user_id': result['_id'],
                'total_earned_usd': float(result['total_earned_usd']),
                'transaction_count': result['transaction_count'],
                'currencies_used': result['currencies_used']
            })
        
        return top_earners
    
    def get_currency_for_language(self, language_code: str) -> str:
        """Get appropriate currency for a language"""
        return self.language_currency_map.get(language_code, 'USD')
    
    def get_currency_info(self, currency_code: str) -> Dict[str, Any]:
        """Get currency information"""
        return self.supported_currencies.get(currency_code, {
            'name': currency_code,
            'symbol': currency_code,
            'countries': []
        })
    
    async def get_user_currency_preference(self, user_id: str, language_code: str = None, country_code: str = None) -> str:
        """Get user's preferred currency based on profile and context"""
        
        # Check user's saved preference
        user_preference = await self.db.user_preferences.find_one(
            {"user_id": user_id},
            {"currency_preference": 1}
        )
        
        if user_preference and user_preference.get('currency_preference'):
            return user_preference['currency_preference']
        
        # Determine from country code
        if country_code:
            for currency, info in self.supported_currencies.items():
                if country_code in info.get('countries', []):
                    return currency
        
        # Determine from language
        if language_code:
            return self.get_currency_for_language(language_code)
        
        # Default to USD
        return 'USD'
    
    async def set_user_currency_preference(self, user_id: str, currency_code: str) -> bool:
        """Set user's currency preference"""
        if currency_code not in self.supported_currencies:
            return False
        
        try:
            await self.db.user_preferences.update_one(
                {"user_id": user_id},
                {
                    "$set": {
                        "currency_preference": currency_code,
                        "updated_at": datetime.utcnow()
                    }
                },
                upsert=True
            )
            return True
        except Exception as e:
            logger.error(f"Error setting currency preference: {e}")
            return False