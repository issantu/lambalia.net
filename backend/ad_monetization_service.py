# Enhanced Ad System & Monetization Service
import asyncio
import random
import math
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple, Any
from motor.motor_asyncio import AsyncIOMotorDatabase
import logging

from ad_monetization_models import (
    Advertisement, UserEngagementProfile, PremiumSubscription, AdImpression,
    SurgePricing, RevenueAnalytics, AdType, AdPlacement, UserEngagementLevel,
    PremiumTier, AdStatus
)

class EngagementAnalysisService:
    """Service for analyzing user engagement and optimizing ad frequency"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
    
    async def calculate_user_engagement_level(self, user_id: str) -> UserEngagementProfile:
        """Calculate comprehensive user engagement profile"""
        
        # Get user activity data from last 30 days
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        
        # Aggregate activity metrics
        snippets_count = await self.db.snippets.count_documents({
            "author_id": user_id,
            "created_at": {"$gte": thirty_days_ago}
        })
        
        cooking_offers_count = await self.db.cooking_offers.count_documents({
            "cook_id": user_id,
            "created_at": {"$gte": thirty_days_ago}
        })
        
        eating_requests_count = await self.db.eating_requests.count_documents({
            "eater_id": user_id,
            "created_at": {"$gte": thirty_days_ago}
        })
        
        appointments_count = await self.db.cooking_appointments.count_documents({
            "$or": [{"cook_id": user_id}, {"eater_id": user_id}],
            "created_at": {"$gte": thirty_days_ago}
        })
        
        # Get existing engagement profile or create new one
        existing_profile = await self.db.user_engagement_profiles.find_one({"user_id": user_id}, {"_id": 0})
        
        # Calculate engagement metrics
        total_activity_score = (
            snippets_count * 2 +           # Creating content is valuable
            cooking_offers_count * 5 +      # Offering cooking services is highly valuable
            eating_requests_count * 3 +     # Requesting food shows engagement
            appointments_count * 8          # Completed transactions are most valuable
        )
        
        # Determine engagement level
        if total_activity_score >= 50:
            engagement_level = UserEngagementLevel.POWER_USER
            optimal_ads_per_day = 12
        elif total_activity_score >= 25:
            engagement_level = UserEngagementLevel.HIGH
            optimal_ads_per_day = 8
        elif total_activity_score >= 10:
            engagement_level = UserEngagementLevel.MEDIUM
            optimal_ads_per_day = 5
        else:
            engagement_level = UserEngagementLevel.LOW
            optimal_ads_per_day = 3
        
        # Calculate premium eligibility score
        premium_score = min(total_activity_score / 100, 1.0)
        
        # Calculate social interaction score (simplified)
        social_score = min((snippets_count + cooking_offers_count) / 20, 1.0)
        
        # Calculate ad fatigue score
        ads_shown_recently = existing_profile.get('ads_viewed_today', 0) if existing_profile else 0
        ad_fatigue = min(ads_shown_recently / optimal_ads_per_day, 1.0)
        
        profile = UserEngagementProfile(
            user_id=user_id,
            total_sessions=max(total_activity_score // 3, 1),  # Estimated
            snippets_created=snippets_count,
            cooking_offers_created=cooking_offers_count,
            eating_requests_created=eating_requests_count,
            appointments_booked=appointments_count,
            social_interaction_score=social_score,
            engagement_level=engagement_level,
            optimal_ads_per_day=optimal_ads_per_day,
            premium_eligibility_score=premium_score,
            ad_fatigue_score=ad_fatigue,
            ads_viewed_today=ads_shown_recently
        )
        
        # Update database
        await self.db.user_engagement_profiles.update_one(
            {"user_id": user_id},
            {"$set": profile.dict()},
            upsert=True
        )
        
        return profile
    
    async def should_show_ad_to_user(self, user_id: str) -> Tuple[bool, str]:
        """Determine if user should see an ad based on engagement and fatigue"""
        
        profile = await self.calculate_user_engagement_level(user_id)
        
        # Check if user is premium (no ads for premium users)
        premium_subscription = await self.db.premium_subscriptions.find_one({
            "user_id": user_id,
            "is_active": True
        }, {"_id": 0})
        
        if premium_subscription and premium_subscription.get('features', {}).get('ad_free_experience', False):
            return False, "Premium user - ad-free experience"
        
        # Check daily ad limit
        if profile.ads_viewed_today >= profile.optimal_ads_per_day:
            return False, "Daily ad limit reached"
        
        # Check ad fatigue
        if profile.ad_fatigue_score > 0.8:
            return False, "High ad fatigue score"
        
        # Check time since last ad
        if profile.last_ad_shown:
            time_since_last = datetime.utcnow() - profile.last_ad_shown
            if time_since_last.total_seconds() < 300:  # 5 minutes minimum
                return False, "Too soon since last ad"
        
        return True, f"Eligible for ads - engagement level: {profile.engagement_level}"

class AdPlacementService:
    """Service for intelligent ad placement and targeting"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.engagement_service = EngagementAnalysisService(db)
    
    async def get_targeted_ad(self, user_id: str, placement: AdPlacement, 
                            context: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """Get best targeted ad for user and placement"""
        
        # Check if user should see ads
        should_show, reason = await self.engagement_service.should_show_ad_to_user(user_id)
        if not should_show:
            logging.info(f"Not showing ad to user {user_id}: {reason}")
            return None
        
        # Get user profile for targeting
        user = await self.db.users.find_one({"id": user_id}, {"_id": 0})
        if not user:
            return None
        
        # Build targeting query
        query = {
            "status": AdStatus.ACTIVE,
            "start_date": {"$lte": datetime.utcnow()},
            "$or": [
                {"end_date": None},
                {"end_date": {"$gte": datetime.utcnow()}}
            ],
            "placement_types": placement.value,
            "spent_amount": {"$lt": "$total_budget"}  # Budget not exhausted
        }
        
        # Add targeting filters based on user profile
        if context and context.get('cuisine_type'):
            query["$or"] = [
                {"target_cuisines": {"$in": [context['cuisine_type']]}},
                {"target_cuisines": {"$size": 0}}  # No specific targeting
            ]
        
        # Get potential ads
        ads_cursor = self.db.advertisements.find(query, {"_id": 0}).limit(10)
        ads = await ads_cursor.to_list(length=10)
        
        if not ads:
            return None
        
        # Score ads for this user
        scored_ads = []
        for ad in ads:
            score = await self._calculate_ad_relevance_score(ad, user, context)
            scored_ads.append((ad, score))
        
        # Sort by score and select best ad
        scored_ads.sort(key=lambda x: x[1], reverse=True)
        selected_ad = scored_ads[0][0]
        
        # Record impression
        await self._record_ad_impression(selected_ad['id'], user_id, placement, context)
        
        return {
            "ad_id": selected_ad['id'],
            "ad_type": selected_ad['ad_type'],
            "title": selected_ad['title'],
            "description": selected_ad['description'],
            "creative_url": selected_ad['creative_url'],
            "click_url": selected_ad['click_url'],
            "placement": placement.value,
            "position": context.get('position', 1) if context else 1,
            "targeting_score": scored_ads[0][1]
        }
    
    async def _calculate_ad_relevance_score(self, ad: Dict, user: Dict, context: Dict = None) -> float:
        """Calculate how relevant an ad is for a specific user"""
        score = 0.5  # Base score
        
        # Demographic targeting
        user_age = user.get('age', 30)
        if f"age_{user_age//10*10}_{user_age//10*10+9}" in ad.get('target_demographics', []):
            score += 0.2
        
        # Location targeting
        user_country = user.get('country', 'US')
        if user_country in ad.get('target_locations', []) or not ad.get('target_locations'):
            score += 0.15
        
        # Cuisine interest matching
        if context and context.get('cuisine_type'):
            if context['cuisine_type'] in ad.get('target_cuisines', []):
                score += 0.25
        
        # Dietary preferences
        user_dietary = user.get('dietary_preferences', [])
        ad_dietary = ad.get('target_dietary', [])
        if any(diet in ad_dietary for diet in user_dietary):
            score += 0.2
        
        # Ad performance boost
        ctr = ad.get('click_through_rate', 0)
        if ctr > 2.0:  # High-performing ad
            score += 0.1
        elif ctr > 1.0:
            score += 0.05
        
        # Frequency capping - reduce score if user has seen this ad recently
        # This would require additional tracking, simplified for now
        
        return min(score, 1.0)
    
    async def _record_ad_impression(self, ad_id: str, user_id: str, placement: AdPlacement, context: Dict = None):
        """Record ad impression for analytics"""
        
        # Get user engagement level
        engagement_profile = await self.db.user_engagement_profiles.find_one({"user_id": user_id}, {"_id": 0})
        engagement_level = engagement_profile.get('engagement_level', UserEngagementLevel.LOW) if engagement_profile else UserEngagementLevel.LOW
        
        # Check if user is premium
        is_premium = await self.db.premium_subscriptions.find_one({
            "user_id": user_id,
            "is_active": True
        }) is not None
        
        # Create impression record
        impression = AdImpression(
            ad_id=ad_id,
            user_id=user_id,
            placement=placement,
            page_context=context.get('page_context', 'unknown') if context else 'unknown',
            position_in_content=context.get('position', 1) if context else 1,
            user_engagement_level=UserEngagementLevel(engagement_level),
            is_premium_user=is_premium,
            user_location=context.get('user_location') if context else None,
            device_type=context.get('device_type', 'web') if context else 'web'
        )
        
        await self.db.ad_impressions.insert_one(impression.dict())
        
        # Update ad performance metrics
        await self.db.advertisements.update_one(
            {"id": ad_id},
            {"$inc": {"total_impressions": 1}}
        )
        
        # Update user's daily ad count
        await self.db.user_engagement_profiles.update_one(
            {"user_id": user_id},
            {
                "$inc": {"ads_viewed_today": 1, "ads_viewed_this_week": 1},
                "$set": {"last_ad_shown": datetime.utcnow()}
            },
            upsert=True
        )
    
    async def record_ad_click(self, ad_id: str, user_id: str) -> Dict[str, Any]:
        """Record ad click and calculate revenue"""
        
        # Get ad details
        ad = await self.db.advertisements.find_one({"id": ad_id}, {"_id": 0})
        if not ad:
            return {"success": False, "error": "Ad not found"}
        
        # Calculate revenue
        click_revenue = ad.get('cost_per_click', 0.50)
        
        # Update ad metrics
        await self.db.advertisements.update_one(
            {"id": ad_id},
            {
                "$inc": {
                    "total_clicks": 1,
                    "spent_amount": click_revenue
                }
            }
        )
        
        # Update impression record if exists
        await self.db.ad_impressions.update_one(
            {"ad_id": ad_id, "user_id": user_id, "was_clicked": False},
            {
                "$set": {
                    "was_clicked": True,
                    "click_timestamp": datetime.utcnow(),
                    "revenue_generated": click_revenue
                }
            }
        )
        
        # Update user engagement
        await self.db.user_engagement_profiles.update_one(
            {"user_id": user_id},
            {"$inc": {"ads_clicked_today": 1}}
        )
        
        return {
            "success": True,
            "revenue_generated": click_revenue,
            "click_url": ad.get('click_url')
        }

class PremiumMembershipService:
    """Service for managing premium subscriptions"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
    
    async def upgrade_to_premium(self, user_id: str, tier: PremiumTier, billing_cycle: str = "monthly") -> Dict[str, Any]:
        """Upgrade user to premium tier"""
        
        # Define tier pricing and features
        tier_config = {
            PremiumTier.COOK_PLUS: {
                "monthly_price": 4.99,
                "features": {
                    "ad_free_experience": True,
                    "unlimited_cooking_offers": True,
                    "enhanced_profile": True,
                    "priority_customer_support": True,
                    "advanced_analytics": True
                }
            },
            PremiumTier.FOODIE_PRO: {
                "monthly_price": 7.99,
                "features": {
                    "ad_free_experience": True,
                    "priority_booking": True,
                    "premium_recipe_access": True,
                    "custom_dietary_filters": True,
                    "bulk_translation": True,
                    "priority_customer_support": True
                }
            },
            PremiumTier.CULINARY_VIP: {
                "monthly_price": 12.99,
                "features": {
                    "ad_free_experience": True,
                    "priority_customer_support": True,
                    "advanced_analytics": True,
                    "premium_recipe_access": True,
                    "priority_booking": True,
                    "enhanced_profile": True,
                    "unlimited_cooking_offers": True,
                    "video_calling": True,
                    "custom_dietary_filters": True,
                    "bulk_translation": True
                }
            }
        }
        
        config = tier_config.get(tier)
        if not config:
            return {"success": False, "error": "Invalid premium tier"}
        
        # Calculate pricing
        monthly_price = config["monthly_price"]
        annual_discount = 0.17 if billing_cycle == "annual" else 0.0  # 17% discount for annual
        actual_price = monthly_price * (1 - annual_discount)
        
        # Calculate next billing date
        if billing_cycle == "annual":
            next_billing = datetime.utcnow() + timedelta(days=365)
        else:
            next_billing = datetime.utcnow() + timedelta(days=30)
        
        # Create or update subscription
        subscription = PremiumSubscription(
            user_id=user_id,
            tier=tier,
            monthly_price=monthly_price,
            annual_discount=annual_discount,
            billing_cycle=billing_cycle,
            next_billing_date=next_billing,
            last_payment_date=datetime.utcnow(),
            features=config["features"],
            is_active=True,
            started_at=datetime.utcnow(),
            expires_at=next_billing
        )
        
        await self.db.premium_subscriptions.update_one(
            {"user_id": user_id},
            {"$set": subscription.dict()},
            upsert=True
        )
        
        return {
            "success": True,
            "tier": tier.value,
            "monthly_price": monthly_price,
            "actual_price": actual_price,
            "billing_cycle": billing_cycle,
            "next_billing_date": next_billing.isoformat(),
            "features_unlocked": list(config["features"].keys())
        }
    
    async def get_premium_benefits_summary(self, user_id: str) -> Dict[str, Any]:
        """Get summary of premium benefits for user"""
        
        subscription = await self.db.premium_subscriptions.find_one({
            "user_id": user_id,
            "is_active": True
        }, {"_id": 0})
        
        if not subscription:
            return {
                "is_premium": False,
                "recommended_tier": await self._recommend_premium_tier(user_id)
            }
        
        # Calculate savings (estimated)
        days_since_premium = (datetime.utcnow() - subscription['started_at']).days
        estimated_ad_revenue_avoided = days_since_premium * 0.15  # $0.15 per day in ads
        estimated_commission_savings = 0  # Could calculate based on transaction history
        
        return {
            "is_premium": True,
            "tier": subscription['tier'],
            "features": subscription['features'],
            "next_billing_date": subscription['next_billing_date'],
            "total_savings_estimated": estimated_ad_revenue_avoided + estimated_commission_savings,
            "days_as_premium": days_since_premium
        }
    
    async def _recommend_premium_tier(self, user_id: str) -> Dict[str, Any]:
        """Recommend appropriate premium tier based on user activity"""
        
        # Get user engagement profile
        engagement = await self.db.user_engagement_profiles.find_one({"user_id": user_id}, {"_id": 0})
        
        if not engagement:
            return {
                "recommended_tier": PremiumTier.COOK_PLUS.value,
                "reason": "Start with basic premium features"
            }
        
        cooking_offers = engagement.get('cooking_offers_created', 0)
        eating_requests = engagement.get('eating_requests_created', 0)
        appointments = engagement.get('appointments_booked', 0)
        
        if cooking_offers >= 5 or appointments >= 10:
            return {
                "recommended_tier": PremiumTier.CULINARY_VIP.value,
                "reason": "High activity - full premium experience recommended"
            }
        elif eating_requests >= 3 or appointments >= 3:
            return {
                "recommended_tier": PremiumTier.FOODIE_PRO.value,
                "reason": "Active food lover - enhanced discovery features"
            }
        else:
            return {
                "recommended_tier": PremiumTier.COOK_PLUS.value,
                "reason": "Getting started - basic premium features"
            }

class SurgePricingService:
    """Service for dynamic surge pricing based on demand"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
    
    async def analyze_and_apply_surge_pricing(self) -> List[Dict[str, Any]]:
        """Analyze demand patterns and apply surge pricing where appropriate"""
        
        current_time = datetime.utcnow()
        surge_results = []
        
        # Analyze cooking offers demand
        cooking_demand = await self._analyze_cooking_offers_demand()
        if cooking_demand['should_surge']:
            surge_config = SurgePricing(
                applies_to="cooking_offers",
                category=cooking_demand.get('peak_category'),
                demand_threshold=cooking_demand['demand_ratio'],
                surge_commission_rate=0.18,  # Up from 15% to 18%
                surge_multiplier=1.3,
                is_active=True,
                activated_at=current_time,
                duration_minutes=120  # 2 hours
            )
            
            await self.db.surge_pricing.insert_one(surge_config.dict())
            surge_results.append({
                "type": "cooking_offers",
                "category": cooking_demand.get('peak_category'),
                "surge_multiplier": 1.3,
                "duration_minutes": 120
            })
        
        # Analyze messaging demand (could be expanded)
        messaging_demand = await self._analyze_messaging_demand()
        if messaging_demand['should_surge']:
            surge_config = SurgePricing(
                applies_to="messaging",
                surge_commission_rate=0.20,  # Up from base rate
                surge_multiplier=1.5,
                is_active=True,
                activated_at=current_time,
                duration_minutes=90
            )
            
            await self.db.surge_pricing.insert_one(surge_config.dict())
            surge_results.append({
                "type": "messaging",
                "surge_multiplier": 1.5,
                "duration_minutes": 90
            })
        
        return surge_results
    
    async def _analyze_cooking_offers_demand(self) -> Dict[str, Any]:
        """Analyze demand for cooking offers"""
        
        # Get recent activity (last 2 hours)
        two_hours_ago = datetime.utcnow() - timedelta(hours=2)
        
        # Count active offers vs requests
        active_offers = await self.db.cooking_offers.count_documents({
            "status": "active",
            "cooking_date": {"$gte": datetime.utcnow()}
        })
        
        recent_requests = await self.db.eating_requests.count_documents({
            "created_at": {"$gte": two_hours_ago},
            "status": "active"
        })
        
        recent_bookings = await self.db.cooking_appointments.count_documents({
            "created_at": {"$gte": two_hours_ago}
        })
        
        # Calculate demand ratio
        total_demand = recent_requests + recent_bookings
        demand_ratio = total_demand / max(active_offers, 1)
        
        # Find peak category
        categories_pipeline = [
            {"$match": {"created_at": {"$gte": two_hours_ago}}},
            {"$group": {"_id": "$category", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 1}
        ]
        
        peak_category_result = await self.db.eating_requests.aggregate(categories_pipeline).to_list(length=1)
        peak_category = peak_category_result[0]['_id'] if peak_category_result else None
        
        return {
            "should_surge": demand_ratio >= 1.5 and total_demand >= 3,
            "demand_ratio": demand_ratio,
            "peak_category": peak_category,
            "active_offers": active_offers,
            "recent_requests": recent_requests,
            "recent_bookings": recent_bookings
        }
    
    async def _analyze_messaging_demand(self) -> Dict[str, Any]:
        """Analyze messaging service demand (placeholder)"""
        
        # This could analyze messaging session creation rates
        # For now, return no surge needed
        return {"should_surge": False}
    
    async def get_current_surge_multiplier(self, service_type: str, category: str = None) -> float:
        """Get current surge multiplier for a service"""
        
        active_surge = await self.db.surge_pricing.find_one({
            "applies_to": service_type,
            "is_active": True,
            "$or": [
                {"category": category},
                {"category": None}
            ],
            "activated_at": {"$gte": datetime.utcnow() - timedelta(hours=8)}
        }, {"_id": 0})
        
        if active_surge:
            # Check if surge should still be active
            activated_at = active_surge['activated_at']
            duration = timedelta(minutes=active_surge['duration_minutes'])
            
            if datetime.utcnow() <= activated_at + duration:
                return active_surge['surge_multiplier']
            else:
                # Deactivate expired surge
                await self.db.surge_pricing.update_one(
                    {"id": active_surge['id']},
                    {"$set": {"is_active": False, "deactivated_at": datetime.utcnow()}}
                )
        
        return 1.0  # No surge

class RevenueAnalyticsService:
    """Service for revenue analytics and reporting"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
    
    async def generate_daily_revenue_report(self, date: datetime = None) -> Dict[str, Any]:
        """Generate comprehensive daily revenue report"""
        
        if not date:
            date = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        
        next_day = date + timedelta(days=1)
        
        # Ad Revenue
        ad_revenue_pipeline = [
            {"$match": {"timestamp": {"$gte": date, "$lt": next_day}}},
            {"$group": {
                "_id": None,
                "total_impressions": {"$sum": 1},
                "total_clicks": {"$sum": {"$cond": ["$was_clicked", 1, 0]}},
                "total_revenue": {"$sum": "$revenue_generated"}
            }}
        ]
        
        ad_results = await self.db.ad_impressions.aggregate(ad_revenue_pipeline).to_list(length=1)
        ad_data = ad_results[0] if ad_results else {
            "total_impressions": 0, "total_clicks": 0, "total_revenue": 0
        }
        
        # Marketplace Revenue (cooking offers, bookings)
        booking_revenue_pipeline = [
            {"$match": {"created_at": {"$gte": date, "$lt": next_day}}},
            {"$group": {
                "_id": None,
                "total_commission": {"$sum": "$platform_commission_amount"},
                "total_bookings": {"$sum": 1}
            }}
        ]
        
        booking_results = await self.db.cooking_appointments.aggregate(booking_revenue_pipeline).to_list(length=1)
        booking_data = booking_results[0] if booking_results else {
            "total_commission": 0, "total_bookings": 0
        }
        
        # Premium Subscription Revenue
        premium_revenue = await self._calculate_daily_premium_revenue(date)
        
        # Calculate totals
        total_revenue = (
            ad_data['total_revenue'] +
            booking_data['total_commission'] +
            premium_revenue['daily_revenue']
        )
        
        # Active users for the day
        active_users = await self.db.user_engagement_profiles.count_documents({
            "last_updated": {"$gte": date, "$lt": next_day}
        })
        
        # Premium users count
        premium_users = await self.db.premium_subscriptions.count_documents({
            "is_active": True
        })
        
        # Revenue per user
        rpu = total_revenue / max(active_users, 1)
        
        report = {
            "date": date.isoformat(),
            "total_revenue": round(total_revenue, 2),
            "ad_revenue": round(ad_data['total_revenue'], 2),
            "marketplace_revenue": round(booking_data['total_commission'], 2),
            "premium_revenue": round(premium_revenue['daily_revenue'], 2),
            "ad_impressions": ad_data['total_impressions'],
            "ad_clicks": ad_data['total_clicks'],
            "ad_ctr": round((ad_data['total_clicks'] / max(ad_data['total_impressions'], 1)) * 100, 2),
            "bookings_completed": booking_data['total_bookings'],
            "active_users": active_users,
            "premium_users": premium_users,
            "revenue_per_user": round(rpu, 2),
            "premium_conversion_rate": round((premium_users / max(active_users, 1)) * 100, 2)
        }
        
        # Save analytics to database
        analytics_record = RevenueAnalytics(
            date=date,
            period_type="daily",
            ad_impressions=ad_data['total_impressions'],
            ad_clicks=ad_data['total_clicks'],
            ad_revenue=ad_data['total_revenue'],
            cooking_offers_revenue=booking_data['total_commission'],
            premium_subscription_revenue=premium_revenue['daily_revenue'],
            platform_commission_total=booking_data['total_commission'],
            active_users=active_users,
            premium_users=premium_users,
            revenue_per_user=rpu,
            total_revenue=total_revenue
        )
        
        await self.db.revenue_analytics.update_one(
            {"date": date, "period_type": "daily"},
            {"$set": analytics_record.dict()},
            upsert=True
        )
        
        return report
    
    async def _calculate_daily_premium_revenue(self, date: datetime) -> Dict[str, float]:
        """Calculate daily premium subscription revenue"""
        
        # This is a simplified calculation
        # In practice, you'd need to track actual billing events
        
        active_subscriptions = await self.db.premium_subscriptions.find({
            "is_active": True,
            "started_at": {"$lte": date}
        }, {"_id": 0}).to_list(length=1000)
        
        daily_revenue = 0
        for sub in active_subscriptions:
            monthly_price = sub.get('monthly_price', 0)
            # Distribute monthly revenue across 30 days
            daily_revenue += monthly_price / 30
        
        return {"daily_revenue": daily_revenue}
    
    async def get_revenue_trends(self, days: int = 30) -> Dict[str, Any]:
        """Get revenue trends over specified period"""
        
        end_date = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        start_date = end_date - timedelta(days=days)
        
        # Get daily analytics records
        analytics = await self.db.revenue_analytics.find({
            "date": {"$gte": start_date, "$lt": end_date},
            "period_type": "daily"
        }, {"_id": 0}).sort("date", 1).to_list(length=days)
        
        if not analytics:
            return {"message": "No analytics data available"}
        
        # Calculate trends
        total_revenue_trend = [record['total_revenue'] for record in analytics]
        ad_revenue_trend = [record['ad_revenue'] for record in analytics]
        marketplace_revenue_trend = [record['cooking_offers_revenue'] for record in analytics]
        
        # Calculate growth rates
        current_week_revenue = sum(total_revenue_trend[-7:]) if len(total_revenue_trend) >= 7 else 0
        previous_week_revenue = sum(total_revenue_trend[-14:-7]) if len(total_revenue_trend) >= 14 else 0
        
        week_over_week_growth = 0
        if previous_week_revenue > 0:
            week_over_week_growth = ((current_week_revenue - previous_week_revenue) / previous_week_revenue) * 100
        
        return {
            "period_days": days,
            "total_revenue": sum(total_revenue_trend),
            "average_daily_revenue": sum(total_revenue_trend) / len(total_revenue_trend),
            "week_over_week_growth": round(week_over_week_growth, 2),
            "revenue_breakdown": {
                "ad_revenue": sum(ad_revenue_trend),
                "marketplace_revenue": sum(marketplace_revenue_trend),
                "premium_revenue": sum([r.get('premium_subscription_revenue', 0) for r in analytics])
            },
            "daily_trends": [
                {
                    "date": record['date'].isoformat() if isinstance(record['date'], datetime) else record['date'],
                    "total_revenue": record['total_revenue'],
                    "ad_revenue": record['ad_revenue'],
                    "marketplace_revenue": record['cooking_offers_revenue']
                }
                for record in analytics
            ]
        }