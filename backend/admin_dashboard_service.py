# Comprehensive Admin Dashboard Service
import asyncio
from datetime import datetime, timedelta, date
from typing import Dict, List, Optional, Any
from motor.motor_asyncio import AsyncIOMotorDatabase
import logging
from pydantic import BaseModel, Field
from collections import defaultdict
import calendar

logger = logging.getLogger(__name__)

class DashboardMetrics(BaseModel):
    period: str  # daily, weekly, monthly, yearly
    start_date: datetime
    end_date: datetime
    
    # Transaction Metrics
    total_transactions: int = 0
    transaction_volume_usd: float = 0.0
    commission_earned_usd: float = 0.0
    
    # User Metrics
    total_users: int = 0
    new_users: int = 0
    active_users: int = 0
    
    # Platform Performance
    total_orders: int = 0
    total_offers: int = 0
    total_demands: int = 0
    completion_rate: float = 0.0
    
    # Revenue Breakdown
    revenue_by_service: Dict[str, float] = {}
    revenue_by_currency: Dict[str, float] = {}
    revenue_by_country: Dict[str, float] = {}
    
    # Growth Metrics
    growth_rate: float = 0.0
    previous_period_volume: float = 0.0
    
    # Top Performers
    top_earners: List[Dict] = []
    top_services: List[Dict] = []
    top_countries: List[Dict] = []

class DashboardChartData(BaseModel):
    labels: List[str] = []
    datasets: List[Dict[str, Any]] = []

class AdminDashboardService:
    """Service for comprehensive admin dashboard analytics"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        
    async def get_dashboard_overview(self, period: str = 'daily', custom_start: datetime = None, custom_end: datetime = None) -> DashboardMetrics:
        """Get comprehensive dashboard overview for specified period"""
        
        # Calculate date range
        start_date, end_date = self._get_date_range(period, custom_start, custom_end)
        
        # Get all metrics in parallel for performance
        tasks = [
            self._get_transaction_metrics(start_date, end_date),
            self._get_user_metrics(start_date, end_date),
            self._get_platform_performance(start_date, end_date),
            self._get_revenue_breakdown(start_date, end_date),
            self._get_growth_metrics(start_date, end_date, period),
            self._get_top_performers(start_date, end_date)
        ]
        
        results = await asyncio.gather(*tasks)
        
        # Combine all metrics
        metrics = DashboardMetrics(
            period=period,
            start_date=start_date,
            end_date=end_date,
            **results[0],  # transaction_metrics
            **results[1],  # user_metrics
            **results[2],  # platform_performance
            **results[3],  # revenue_breakdown
            **results[4],  # growth_metrics
            **results[5]   # top_performers
        )
        
        return metrics
    
    def _get_date_range(self, period: str, custom_start: datetime = None, custom_end: datetime = None) -> tuple[datetime, datetime]:
        """Calculate start and end dates for the specified period"""
        
        now = datetime.utcnow()
        
        if custom_start and custom_end:
            return custom_start, custom_end
        
        if period == 'daily':
            start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = start_date + timedelta(days=1) - timedelta(microseconds=1)
        elif period == 'weekly':
            days_since_monday = now.weekday()
            start_date = (now - timedelta(days=days_since_monday)).replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = start_date + timedelta(days=7) - timedelta(microseconds=1)
        elif period == 'monthly':
            start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            if now.month == 12:
                end_date = datetime(now.year + 1, 1, 1) - timedelta(microseconds=1)
            else:
                end_date = datetime(now.year, now.month + 1, 1) - timedelta(microseconds=1)
        elif period == 'yearly':
            start_date = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            end_date = datetime(now.year + 1, 1, 1) - timedelta(microseconds=1)
        else:
            # Default to daily
            start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = start_date + timedelta(days=1) - timedelta(microseconds=1)
        
        return start_date, end_date
    
    async def _get_transaction_metrics(self, start_date: datetime, end_date: datetime) -> Dict:
        """Get transaction-related metrics"""
        
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
                    "total_commission_usd": {"$sum": "$lambalia_commission"}
                }
            }
        ]
        
        try:
            result = await self.db.financial_transactions.aggregate(pipeline).to_list(length=1)
            
            if result:
                return {
                    "total_transactions": result[0]["total_transactions"],
                    "transaction_volume_usd": float(result[0]["total_volume_usd"]),
                    "commission_earned_usd": float(result[0]["total_commission_usd"])
                }
        except Exception as e:
            logger.error(f"Error getting transaction metrics: {e}")
        
        return {
            "total_transactions": 0,
            "transaction_volume_usd": 0.0,
            "commission_earned_usd": 0.0
        }
    
    async def _get_user_metrics(self, start_date: datetime, end_date: datetime) -> Dict:
        """Get user-related metrics"""
        
        try:
            # Total users (all time)
            total_users = await self.db.users.count_documents({})
            
            # New users in period
            new_users = await self.db.users.count_documents({
                "created_at": {"$gte": start_date, "$lte": end_date}
            })
            
            # Active users (users who made transactions in period)
            active_users_pipeline = [
                {
                    "$match": {
                        "timestamp": {"$gte": start_date, "$lte": end_date}
                    }
                },
                {
                    "$group": {
                        "_id": "$user_id"
                    }
                },
                {
                    "$count": "active_users"
                }
            ]
            
            active_result = await self.db.financial_transactions.aggregate(active_users_pipeline).to_list(length=1)
            active_users = active_result[0]["active_users"] if active_result else 0
            
            return {
                "total_users": total_users,
                "new_users": new_users,
                "active_users": active_users
            }
            
        except Exception as e:
            logger.error(f"Error getting user metrics: {e}")
            return {
                "total_users": 0,
                "new_users": 0,
                "active_users": 0
            }
    
    async def _get_platform_performance(self, start_date: datetime, end_date: datetime) -> Dict:
        """Get platform performance metrics"""
        
        try:
            # Get orders from Lambalia Eats
            total_orders = await self.db.food_orders.count_documents({
                "created_at": {"$gte": start_date, "$lte": end_date}
            })
            
            # Get offers from LOD marketplace
            total_offers = await self.db.market_items.count_documents({
                "item_type": "offer",
                "created_at": {"$gte": start_date, "$lte": end_date}
            })
            
            # Get demands from LOD marketplace
            total_demands = await self.db.market_items.count_documents({
                "item_type": "demand",
                "created_at": {"$gte": start_date, "$lte": end_date}
            })
            
            # Calculate completion rate (completed vs total orders)
            completed_orders = await self.db.food_orders.count_documents({
                "created_at": {"$gte": start_date, "$lte": end_date},
                "status": "completed"
            })
            
            completion_rate = (completed_orders / total_orders * 100) if total_orders > 0 else 0.0
            
            return {
                "total_orders": total_orders,
                "total_offers": total_offers,
                "total_demands": total_demands,
                "completion_rate": completion_rate
            }
            
        except Exception as e:
            logger.error(f"Error getting platform performance: {e}")
            return {
                "total_orders": 0,
                "total_offers": 0,
                "total_demands": 0,
                "completion_rate": 0.0
            }
    
    async def _get_revenue_breakdown(self, start_date: datetime, end_date: datetime) -> Dict:
        """Get revenue breakdown by service, currency, and country"""
        
        try:
            # Revenue by service type (transaction_type)
            service_pipeline = [
                {
                    "$match": {
                        "timestamp": {"$gte": start_date, "$lte": end_date}
                    }
                },
                {
                    "$group": {
                        "_id": "$transaction_type",
                        "revenue": {"$sum": "$lambalia_commission"}
                    }
                }
            ]
            
            service_results = await self.db.financial_transactions.aggregate(service_pipeline).to_list(length=None)
            revenue_by_service = {result["_id"]: float(result["revenue"]) for result in service_results}
            
            # Revenue by currency
            currency_pipeline = [
                {
                    "$match": {
                        "timestamp": {"$gte": start_date, "$lte": end_date}
                    }
                },
                {
                    "$group": {
                        "_id": "$currency_original",
                        "revenue": {"$sum": "$lambalia_commission"}
                    }
                }
            ]
            
            currency_results = await self.db.financial_transactions.aggregate(currency_pipeline).to_list(length=None)
            revenue_by_currency = {result["_id"]: float(result["revenue"]) for result in currency_results}
            
            # Revenue by country
            country_pipeline = [
                {
                    "$match": {
                        "timestamp": {"$gte": start_date, "$lte": end_date},
                        "country_code": {"$ne": None}
                    }
                },
                {
                    "$group": {
                        "_id": "$country_code",
                        "revenue": {"$sum": "$lambalia_commission"}
                    }
                }
            ]
            
            country_results = await self.db.financial_transactions.aggregate(country_pipeline).to_list(length=None)
            revenue_by_country = {result["_id"]: float(result["revenue"]) for result in country_results}
            
            return {
                "revenue_by_service": revenue_by_service,
                "revenue_by_currency": revenue_by_currency,
                "revenue_by_country": revenue_by_country
            }
            
        except Exception as e:
            logger.error(f"Error getting revenue breakdown: {e}")
            return {
                "revenue_by_service": {},
                "revenue_by_currency": {},
                "revenue_by_country": {}
            }
    
    async def _get_growth_metrics(self, start_date: datetime, end_date: datetime, period: str) -> Dict:
        """Calculate growth metrics compared to previous period"""
        
        try:
            # Calculate previous period dates
            period_duration = end_date - start_date
            prev_start = start_date - period_duration
            prev_end = start_date - timedelta(microseconds=1)
            
            # Current period volume
            current_pipeline = [
                {
                    "$match": {
                        "timestamp": {"$gte": start_date, "$lte": end_date}
                    }
                },
                {
                    "$group": {
                        "_id": None,
                        "volume": {"$sum": "$amount_usd"}
                    }
                }
            ]
            
            # Previous period volume
            prev_pipeline = [
                {
                    "$match": {
                        "timestamp": {"$gte": prev_start, "$lte": prev_end}
                    }
                },
                {
                    "$group": {
                        "_id": None,
                        "volume": {"$sum": "$amount_usd"}
                    }
                }
            ]
            
            current_result = await self.db.financial_transactions.aggregate(current_pipeline).to_list(length=1)
            prev_result = await self.db.financial_transactions.aggregate(prev_pipeline).to_list(length=1)
            
            current_volume = float(current_result[0]["volume"]) if current_result else 0.0
            previous_volume = float(prev_result[0]["volume"]) if prev_result else 0.0
            
            # Calculate growth rate
            growth_rate = 0.0
            if previous_volume > 0:
                growth_rate = ((current_volume - previous_volume) / previous_volume) * 100
            
            return {
                "growth_rate": growth_rate,
                "previous_period_volume": previous_volume
            }
            
        except Exception as e:
            logger.error(f"Error calculating growth metrics: {e}")
            return {
                "growth_rate": 0.0,
                "previous_period_volume": 0.0
            }
    
    async def _get_top_performers(self, start_date: datetime, end_date: datetime) -> Dict:
        """Get top performing users, services, and countries"""
        
        try:
            # Top earners
            earners_pipeline = [
                {
                    "$match": {
                        "timestamp": {"$gte": start_date, "$lte": end_date}
                    }
                },
                {
                    "$group": {
                        "_id": "$user_id",
                        "total_earned": {"$sum": "$net_amount"},
                        "transaction_count": {"$sum": 1},
                        "total_volume": {"$sum": "$amount_usd"}
                    }
                },
                {
                    "$sort": {"total_earned": -1}
                },
                {
                    "$limit": 10
                }
            ]
            
            earners_result = await self.db.financial_transactions.aggregate(earners_pipeline).to_list(length=10)
            top_earners = [
                {
                    "user_id": result["_id"],
                    "total_earned_usd": float(result["total_earned"]),
                    "transaction_count": result["transaction_count"],
                    "total_volume_usd": float(result["total_volume"])
                }
                for result in earners_result
            ]
            
            # Top services
            services_pipeline = [
                {
                    "$match": {
                        "timestamp": {"$gte": start_date, "$lte": end_date}
                    }
                },
                {
                    "$group": {
                        "_id": "$transaction_type",
                        "transaction_count": {"$sum": 1},
                        "total_volume": {"$sum": "$amount_usd"},
                        "total_commission": {"$sum": "$lambalia_commission"}
                    }
                },
                {
                    "$sort": {"total_volume": -1}
                }
            ]
            
            services_result = await self.db.financial_transactions.aggregate(services_pipeline).to_list(length=None)
            top_services = [
                {
                    "service": result["_id"],
                    "transaction_count": result["transaction_count"],
                    "total_volume_usd": float(result["total_volume"]),
                    "total_commission_usd": float(result["total_commission"])
                }
                for result in services_result
            ]
            
            # Top countries
            countries_pipeline = [
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
                        "total_volume": {"$sum": "$amount_usd"},
                        "unique_users": {"$addToSet": "$user_id"}
                    }
                },
                {
                    "$sort": {"total_volume": -1}
                },
                {
                    "$limit": 10
                }
            ]
            
            countries_result = await self.db.financial_transactions.aggregate(countries_pipeline).to_list(length=10)
            top_countries = [
                {
                    "country": result["_id"],
                    "transaction_count": result["transaction_count"],
                    "total_volume_usd": float(result["total_volume"]),
                    "unique_users": len(result["unique_users"])
                }
                for result in countries_result
            ]
            
            return {
                "top_earners": top_earners,
                "top_services": top_services,
                "top_countries": top_countries
            }
            
        except Exception as e:
            logger.error(f"Error getting top performers: {e}")
            return {
                "top_earners": [],
                "top_services": [],
                "top_countries": []
            }
    
    async def get_chart_data(self, metric: str, period: str = 'daily', days_back: int = 30) -> DashboardChartData:
        """Get chart data for various metrics"""
        
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days_back)
        
        if period == 'daily':
            date_format = "%Y-%m-%d"
            group_format = {"$dateToString": {"format": "%Y-%m-%d", "date": "$timestamp"}}
        elif period == 'weekly':
            date_format = "%Y-W%U"
            group_format = {"$dateToString": {"format": "%Y-W%U", "date": "$timestamp"}}
        elif period == 'monthly':
            date_format = "%Y-%m"
            group_format = {"$dateToString": {"format": "%Y-%m", "date": "$timestamp"}}
        else:
            date_format = "%Y-%m-%d"
            group_format = {"$dateToString": {"format": "%Y-%m-%d", "date": "$timestamp"}}
        
        pipeline = [
            {
                "$match": {
                    "timestamp": {"$gte": start_date, "$lte": end_date}
                }
            },
            {
                "$group": {
                    "_id": group_format,
                    "transaction_count": {"$sum": 1},
                    "total_volume": {"$sum": "$amount_usd"},
                    "total_commission": {"$sum": "$lambalia_commission"}
                }
            },
            {
                "$sort": {"_id": 1}
            }
        ]
        
        try:
            results = await self.db.financial_transactions.aggregate(pipeline).to_list(length=None)
            
            labels = [result["_id"] for result in results]
            
            if metric == 'transactions':
                data = [result["transaction_count"] for result in results]
                label = "Transactions"
            elif metric == 'volume':
                data = [float(result["total_volume"]) for result in results]
                label = "Volume (USD)"
            elif metric == 'commission':
                data = [float(result["total_commission"]) for result in results]
                label = "Commission (USD)"
            else:
                data = [result["transaction_count"] for result in results]
                label = "Transactions"
            
            chart_data = DashboardChartData(
                labels=labels,
                datasets=[
                    {
                        "label": label,
                        "data": data,
                        "borderColor": "#3B82F6",
                        "backgroundColor": "rgba(59, 130, 246, 0.1)",
                        "fill": True
                    }
                ]
            )
            
            return chart_data
            
        except Exception as e:
            logger.error(f"Error getting chart data: {e}")
            return DashboardChartData()
    
    async def get_real_time_stats(self) -> Dict:
        """Get real-time platform statistics"""
        
        try:
            now = datetime.utcnow()
            today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            
            # Today's transactions
            today_transactions = await self.db.financial_transactions.count_documents({
                "timestamp": {"$gte": today_start}
            })
            
            # Today's revenue
            today_revenue_pipeline = [
                {
                    "$match": {
                        "timestamp": {"$gte": today_start}
                    }
                },
                {
                    "$group": {
                        "_id": None,
                        "revenue": {"$sum": "$lambalia_commission"}
                    }
                }
            ]
            
            revenue_result = await self.db.financial_transactions.aggregate(today_revenue_pipeline).to_list(length=1)
            today_revenue = float(revenue_result[0]["revenue"]) if revenue_result else 0.0
            
            # Active users (last 24 hours)
            yesterday = now - timedelta(days=1)
            active_users = await self.db.financial_transactions.distinct("user_id", {
                "timestamp": {"$gte": yesterday}
            })
            
            # Pending transactions
            pending_transactions = await self.db.financial_transactions.count_documents({
                "status": "pending"
            })
            
            return {
                "today_transactions": today_transactions,
                "today_revenue_usd": today_revenue,
                "active_users_24h": len(active_users),
                "pending_transactions": pending_transactions,
                "last_updated": now.isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting real-time stats: {e}")
            return {
                "today_transactions": 0,
                "today_revenue_usd": 0.0,
                "active_users_24h": 0,
                "pending_transactions": 0,
                "last_updated": datetime.utcnow().isoformat()
            }