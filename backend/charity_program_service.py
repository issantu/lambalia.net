# Charity Program Service - Social Impact & Premium Membership Management
import math
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple, Any
from motor.motor_asyncio import AsyncIOMotorDatabase
import logging

from charity_program_models import (
    CharityProgram, CharityActivity, CharityVerificationCommittee, PremiumMembership,
    CommunityImpactMetrics, LocalPartnerOrganization, CharityType, VerificationStatus,
    PremiumTier, ImpactMetricType
)

class CharityImpactCalculator:
    """Service for calculating impact scores from charity activities"""
    
    @staticmethod
    def calculate_activity_impact_score(activity: CharityActivity) -> float:
        """Calculate impact score for a charity activity"""
        base_score = 10.0  # Base points for any charity activity
        
        # Food donation scoring
        if activity.food_donated_lbs:
            base_score += activity.food_donated_lbs * 2.0  # 2 points per pound
        
        # Meals provided scoring
        if activity.meals_provided:
            base_score += activity.meals_provided * 5.0  # 5 points per meal
        
        # People helped scoring
        if activity.people_helped:
            base_score += activity.people_helped * 3.0  # 3 points per person
        
        # Volunteer hours scoring
        if activity.volunteer_hours:
            base_score += activity.volunteer_hours * 8.0  # 8 points per hour
        
        # Activity type multipliers
        type_multipliers = {
            CharityType.FOOD_BANK: 1.2,
            CharityType.HOMELESS_SHELTER: 1.3,
            CharityType.COMMUNITY_KITCHEN: 1.1,
            CharityType.SENIORS_CENTER: 1.1,
            CharityType.SCHOOL_PROGRAM: 1.2,
            CharityType.EMERGENCY_RELIEF: 1.5,
            CharityType.LOCAL_CHARITY: 1.0
        }
        
        multiplier = type_multipliers.get(activity.activity_type, 1.0)
        final_score = base_score * multiplier * activity.bonus_multiplier
        
        return round(final_score, 2)
    
    @staticmethod
    def calculate_tier_requirements() -> Dict[PremiumTier, Dict[str, float]]:
        """Calculate requirements for each premium tier"""
        return {
            PremiumTier.COMMUNITY_HELPER: {
                "monthly_impact_required": 30.0,
                "monthly_activities_required": 2,
                "minimum_food_lbs": 5.0
            },
            PremiumTier.GARDEN_SUPPORTER: {
                "monthly_impact_required": 60.0,
                "monthly_activities_required": 3,
                "minimum_food_lbs": 15.0
            },
            PremiumTier.LOCAL_CHAMPION: {
                "monthly_impact_required": 120.0,
                "monthly_activities_required": 5,
                "minimum_food_lbs": 30.0
            }
        }
    
    @staticmethod
    def determine_recognition_level(total_impact: float, activities_count: int) -> str:
        """Determine community recognition level"""
        if total_impact >= 500 and activities_count >= 20:
            return "Local Hero"
        elif total_impact >= 200 and activities_count >= 10:
            return "Community Champion"
        elif total_impact >= 50 and activities_count >= 5:
            return "Rising Helper"
        else:
            return "New Volunteer"

class CharityProgramService:
    """Main service for managing charity programs and premium memberships"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.impact_calculator = CharityImpactCalculator()
        self.logger = logging.getLogger(__name__)
    
    async def register_charity_program(self, program_data: Dict[str, Any], user_id: str) -> CharityProgram:
        """Register user for charity program"""
        
        # Check if user already has a program
        existing_program = await self.db.charity_programs.find_one({"user_id": user_id}, {"_id": 0})
        if existing_program:
            raise ValueError("User already registered for charity program")
        
        # Calculate next review date (30 days from now)
        next_review = datetime.utcnow() + timedelta(days=30)
        
        program = CharityProgram(
            user_id=user_id,
            **program_data,
            next_review_date=next_review
        )
        
        await self.db.charity_programs.insert_one(program.dict())
        
        # Create initial premium membership
        await self._create_initial_premium_membership(user_id, program.id)
        
        self.logger.info(f"User {user_id} registered for charity program")
        return program
    
    async def submit_charity_activity(self, activity_data: Dict[str, Any], user_id: str) -> CharityActivity:
        """Submit a charity activity for verification"""
        
        # Get user's charity program
        program = await self.db.charity_programs.find_one({"user_id": user_id}, {"_id": 0})
        if not program:
            raise ValueError("User not registered for charity program")
        
        # Parse activity date
        activity_dict = activity_data.copy()
        activity_dict['activity_date'] = datetime.fromisoformat(activity_data['activity_date'].replace('Z', '+00:00'))
        
        activity = CharityActivity(
            user_id=user_id,
            charity_program_id=program["id"],
            **activity_dict
        )
        
        # Calculate impact score
        activity.calculated_impact_score = self.impact_calculator.calculate_activity_impact_score(activity)
        
        await self.db.charity_activities.insert_one(activity.dict())
        
        # Update program's last activity date
        await self.db.charity_programs.update_one(
            {"user_id": user_id},
            {"$set": {"last_activity_date": datetime.utcnow()}}
        )
        
        # Queue for committee review
        await self._queue_for_committee_review(activity.id)
        
        self.logger.info(f"Charity activity submitted by user {user_id}: {activity.id}")
        return activity
    
    async def verify_charity_activity(self, activity_id: str, committee_member_id: str, 
                                    approved: bool, notes: Optional[str] = None,
                                    bonus_multiplier: float = 1.0) -> CharityActivity:
        """Verify charity activity (committee member action)"""
        
        activity = await self.db.charity_activities.find_one({"id": activity_id}, {"_id": 0})
        if not activity:
            raise ValueError("Charity activity not found")
        
        # Update verification status
        new_status = VerificationStatus.APPROVED if approved else VerificationStatus.REJECTED
        verification_data = {
            "verification_status": new_status,
            "verification_notes": notes,
            "verified_by": committee_member_id,
            "verified_at": datetime.utcnow(),
            "bonus_multiplier": bonus_multiplier
        }
        
        # Recalculate impact score with bonus
        if approved and bonus_multiplier != 1.0:
            base_activity = CharityActivity(**activity)
            base_activity.bonus_multiplier = bonus_multiplier
            verification_data["calculated_impact_score"] = self.impact_calculator.calculate_activity_impact_score(base_activity)
        
        await self.db.charity_activities.update_one(
            {"id": activity_id},
            {"$set": verification_data}
        )
        
        # If approved, update user's impact scores and check tier eligibility
        if approved:
            await self._update_user_impact_scores(activity["user_id"], verification_data.get("calculated_impact_score", activity["calculated_impact_score"]))
            await self._check_tier_eligibility(activity["user_id"])
        
        # Update committee member stats
        await self.db.charity_committee.update_one(
            {"user_id": committee_member_id},
            {"$inc": {"reviews_completed": 1, "current_month_reviews": 1}}
        )
        
        return await self.db.charity_activities.find_one({"id": activity_id}, {"_id": 0})
    
    async def upgrade_premium_membership(self, upgrade_data: Dict[str, Any], user_id: str) -> PremiumMembership:
        """Upgrade or modify premium membership"""
        
        tier_requirements = self.impact_calculator.calculate_tier_requirements()
        requested_tier = PremiumTier(upgrade_data["tier"])
        
        # Check if user qualifies through charity work
        if upgrade_data.get("payment_method") == "charity_work":
            user_stats = await self._get_user_charity_stats(user_id)
            requirements = tier_requirements[requested_tier]
            
            if (user_stats["monthly_impact"] < requirements["monthly_impact_required"] or
                user_stats["monthly_activities"] < requirements["monthly_activities_required"]):
                raise ValueError(f"Insufficient charity activity for {requested_tier.value}. Need {requirements['monthly_impact_required']} impact points and {requirements['monthly_activities_required']} activities per month.")
        
        # Get or create premium membership
        membership = await self.db.premium_memberships.find_one({"user_id": user_id}, {"_id": 0})
        
        if membership:
            # Update existing membership
            await self.db.premium_memberships.update_one(
                {"user_id": user_id},
                {
                    "$set": {
                        "tier": requested_tier,
                        "earned_through": upgrade_data.get("payment_method", "charity_work"),
                        "monthly_payment": upgrade_data.get("monthly_payment_amount", 0.0),
                        "updated_at": datetime.utcnow(),
                        "current_period_end": datetime.utcnow() + timedelta(days=30)
                    }
                }
            )
        else:
            # Create new membership
            membership = PremiumMembership(
                user_id=user_id,
                tier=requested_tier,
                earned_through=upgrade_data.get("payment_method", "charity_work"),
                monthly_payment=upgrade_data.get("monthly_payment_amount", 0.0)
            )
            await self.db.premium_memberships.insert_one(membership.dict())
        
        return await self.db.premium_memberships.find_one({"user_id": user_id}, {"_id": 0})
    
    async def get_user_charity_dashboard(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive charity dashboard for user"""
        
        # Get program info
        program = await self.db.charity_programs.find_one({"user_id": user_id}, {"_id": 0})
        if not program:
            return {"error": "User not registered for charity program"}
        
        # Get user activities
        activities = await self.db.charity_activities.find(
            {"user_id": user_id}, {"_id": 0}
        ).sort("activity_date", -1).to_list(length=50)
        
        # Calculate stats
        stats = await self._get_user_charity_stats(user_id)
        
        # Get premium membership
        membership = await self.db.premium_memberships.find_one({"user_id": user_id}, {"_id": 0})
        
        # Get community ranking
        ranking = await self._get_user_community_ranking(user_id)
        
        # Get next tier requirements
        next_tier_info = await self._get_next_tier_requirements(user_id, stats)
        
        return {
            "program_info": program,
            "membership_info": membership,
            "statistics": stats,
            "community_ranking": ranking,
            "recent_activities": activities[:10],
            "next_tier_requirements": next_tier_info,
            "available_charities": await self._get_local_partner_organizations(program.get("preferred_locations", [])),
            "recognition_badges": await self._calculate_recognition_badges(user_id, stats)
        }
    
    async def get_community_impact_metrics(self) -> Dict[str, Any]:
        """Get platform-wide community impact metrics"""
        
        try:
            # Aggregate metrics from all users
            pipeline = [
                {
                    "$match": {"verification_status": VerificationStatus.APPROVED}
                },
                {
                    "$group": {
                        "_id": None,
                        "total_food_donated": {"$sum": {"$ifNull": ["$food_donated_lbs", 0]}},
                        "total_meals_provided": {"$sum": {"$ifNull": ["$meals_provided", 0]}},
                        "total_people_helped": {"$sum": {"$ifNull": ["$people_helped", 0]}},
                        "total_volunteer_hours": {"$sum": {"$ifNull": ["$volunteer_hours", 0]}},
                        "total_activities": {"$sum": 1},
                        "total_impact_score": {"$sum": {"$ifNull": ["$calculated_impact_score", 0]}}
                    }
                }
            ]
            
            aggregate_result = await self.db.charity_activities.aggregate(pipeline).to_list(length=1)
            metrics = aggregate_result[0] if aggregate_result else {
                "total_food_donated": 0.0,
                "total_meals_provided": 0,
                "total_people_helped": 0,
                "total_volunteer_hours": 0.0,
                "total_activities": 0,
                "total_impact_score": 0.0
            }
            
            # Get additional stats
            active_participants = await self.db.charity_programs.count_documents({"is_active": True})
            premium_via_charity = await self.db.premium_memberships.count_documents({"earned_through": {"$in": ["charity_work", "both"]}})
            
            # Get top contributors (limit to prevent errors)
            top_contributors = await self._get_top_community_contributors(limit=5)
            
            return {
                "total_food_donated_lbs": float(metrics.get("total_food_donated", 0.0)),
                "total_meals_provided": int(metrics.get("total_meals_provided", 0)),
                "total_people_helped": int(metrics.get("total_people_helped", 0)),
                "total_volunteer_hours": float(metrics.get("total_volunteer_hours", 0.0)),
                "total_activities": int(metrics.get("total_activities", 0)),
                "total_impact_score": float(metrics.get("total_impact_score", 0.0)),
                "active_participants": active_participants,
                "premium_members_via_charity": premium_via_charity,
                "top_contributors": top_contributors,
                "estimated_food_waste_diverted": float(metrics.get("total_food_donated", 0.0)),
                "estimated_environmental_impact": {
                    "co2_saved_lbs": float(metrics.get("total_food_donated", 0.0)) * 2.5,  # Rough estimate
                    "water_saved_gallons": float(metrics.get("total_food_donated", 0.0)) * 10,
                    "economic_value_created": float(metrics.get("total_meals_provided", 0)) * 3.50  # Average meal value
                }
            }
        except Exception as e:
            self.logger.error(f"Error getting community impact metrics: {str(e)}")
            # Return safe default values
            return {
                "total_food_donated_lbs": 0.0,
                "total_meals_provided": 0,
                "total_people_helped": 0,
                "total_volunteer_hours": 0.0,
                "total_activities": 0,
                "total_impact_score": 0.0,
                "active_participants": 0,
                "premium_members_via_charity": 0,
                "top_contributors": [],
                "estimated_food_waste_diverted": 0.0,
                "estimated_environmental_impact": {
                    "co2_saved_lbs": 0.0,
                    "water_saved_gallons": 0.0,
                    "economic_value_created": 0.0
                }
            }
    
    async def get_premium_membership_benefits(self, user_id: str) -> Dict[str, Any]:
        """Get detailed premium membership benefits for user"""
        
        membership = await self.db.premium_memberships.find_one({"user_id": user_id}, {"_id": 0})
        if not membership:
            return {"error": "No premium membership found"}
        
        tier = PremiumTier(membership["tier"])
        
        # Define benefits by tier
        tier_benefits = {
            PremiumTier.COMMUNITY_HELPER: {
                "commission_reduction": 0.01,  # 15% -> 14%
                "monthly_cost": 0.0,
                "charity_hours_required": 4,
                "benefits": [
                    {"name": "1% Commission Reduction", "description": "Pay 14% instead of 15% on all sales"},
                    {"name": "Community Helper Badge", "description": "Show your commitment to helping others"},
                    {"name": "Priority Customer Support", "description": "Get help faster when you need it"},
                    {"name": "Monthly Impact Report", "description": "See how your charity work makes a difference"}
                ]
            },
            PremiumTier.GARDEN_SUPPORTER: {
                "commission_reduction": 0.02,  # 15% -> 13%
                "monthly_cost": 4.99,
                "charity_alternative_hours": 8,
                "benefits": [
                    {"name": "2% Commission Reduction", "description": "Pay 13% instead of 15% on all sales"},
                    {"name": "Featured Product Listings", "description": "Your products appear first in search results"},
                    {"name": "Advanced Analytics Dashboard", "description": "Detailed insights into your sales and customers"},
                    {"name": "Garden Supporter Badge", "description": "Premium recognition in community"},
                    {"name": "Charity Alternative", "description": "Earn membership through 8 hours monthly charity work"},
                    {"name": "Seasonal Harvest Calendar", "description": "Early access to seasonal demand forecasting"}
                ]
            },
            PremiumTier.LOCAL_CHAMPION: {
                "commission_reduction": 0.03,  # 15% -> 12%
                "monthly_cost": 9.99,
                "charity_alternative_hours": 12,
                "benefits": [
                    {"name": "3% Commission Reduction", "description": "Pay 12% instead of 15% on all sales"},
                    {"name": "Premium Product Placement", "description": "Top position in all relevant searches"},
                    {"name": "Local Champion Badge", "description": "Highest community recognition level"},
                    {"name": "Exclusive Community Events", "description": "Access to local champion networking events"},
                    {"name": "Advanced Marketing Tools", "description": "Professional marketing materials and support"},
                    {"name": "Charity Alternative", "description": "Earn membership through 12 hours monthly charity work"},
                    {"name": "Direct Customer Messaging", "description": "Communicate directly with customers"},
                    {"name": "Revenue Optimization Consulting", "description": "Monthly 1-on-1 strategy sessions"}
                ]
            }
        }
        
        current_benefits = tier_benefits[tier]
        
        # Calculate savings
        user_stats = await self._get_user_charity_stats(user_id)
        monthly_sales = user_stats.get("estimated_monthly_sales", 0.0)
        monthly_savings = monthly_sales * current_benefits["commission_reduction"]
        
        return {
            "current_tier": tier.value,
            "tier_name": tier.value.replace("_", " ").title(),
            "monthly_cost": current_benefits["monthly_cost"],
            "earned_through": membership.get("earned_through", "charity_work"),
            "benefits": current_benefits["benefits"],
            "commission_rate": 15 - (current_benefits["commission_reduction"] * 100),
            "monthly_savings": monthly_savings,
            "annual_savings": monthly_savings * 12,
            "charity_hours_required": current_benefits.get("charity_hours_required") or current_benefits.get("charity_alternative_hours"),
            "current_impact_score": user_stats.get("monthly_impact", 0.0),
            "recognition_level": membership.get("community_impact_level", "Rising Helper"),
            "badges": membership.get("recognition_badges", [])
        }
    
    # Private helper methods
    
    async def _create_initial_premium_membership(self, user_id: str, program_id: str):
        """Create initial Community Helper membership for new charity participants"""
        membership = PremiumMembership(
            user_id=user_id,
            tier=PremiumTier.COMMUNITY_HELPER,
            earned_through="charity_work",
            monthly_payment=0.0
        )
        await self.db.premium_memberships.insert_one(membership.dict())
    
    async def _queue_for_committee_review(self, activity_id: str):
        """Queue activity for committee review (simplified - in production would use task queue)"""
        # For now, just log that it needs review
        self.logger.info(f"Activity {activity_id} queued for committee review")
    
    async def _update_user_impact_scores(self, user_id: str, impact_score: float):
        """Update user's impact scores in charity program"""
        await self.db.charity_programs.update_one(
            {"user_id": user_id},
            {
                "$inc": {
                    "total_impact_score": impact_score,
                    "current_month_impact": impact_score
                },
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
    
    async def _check_tier_eligibility(self, user_id: str):
        """Check if user is eligible for tier upgrade"""
        stats = await self._get_user_charity_stats(user_id)
        tier_requirements = self.impact_calculator.calculate_tier_requirements()
        
        # Check eligibility for each tier (highest first)
        for tier in [PremiumTier.LOCAL_CHAMPION, PremiumTier.GARDEN_SUPPORTER, PremiumTier.COMMUNITY_HELPER]:
            requirements = tier_requirements[tier]
            if (stats["monthly_impact"] >= requirements["monthly_impact_required"] and
                stats["monthly_activities"] >= requirements["monthly_activities_required"]):
                
                # Auto-upgrade if earned through charity
                current_membership = await self.db.premium_memberships.find_one({"user_id": user_id}, {"_id": 0})
                if (current_membership and 
                    current_membership.get("earned_through") == "charity_work" and
                    PremiumTier(current_membership["tier"]).value != tier.value):
                    
                    await self.db.premium_memberships.update_one(
                        {"user_id": user_id},
                        {
                            "$set": {
                                "tier": tier,
                                "updated_at": datetime.utcnow()
                            }
                        }
                    )
                    self.logger.info(f"Auto-upgraded user {user_id} to {tier.value}")
                break
    
    async def _get_user_charity_stats(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive charity statistics for user"""
        
        # Get current month activities
        current_month_start = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        pipeline = [
            {
                "$match": {
                    "user_id": user_id,
                    "verification_status": VerificationStatus.APPROVED,
                    "activity_date": {"$gte": current_month_start}
                }
            },
            {
                "$group": {
                    "_id": None,
                    "monthly_impact": {"$sum": "$calculated_impact_score"},
                    "monthly_activities": {"$sum": 1},
                    "monthly_food_donated": {"$sum": "$food_donated_lbs"},
                    "monthly_meals_provided": {"$sum": "$meals_provided"},
                    "monthly_people_helped": {"$sum": "$people_helped"},
                    "monthly_volunteer_hours": {"$sum": "$volunteer_hours"}
                }
            }
        ]
        
        monthly_stats = await self.db.charity_activities.aggregate(pipeline).to_list(length=1)
        monthly = monthly_stats[0] if monthly_stats else {}
        
        # Get all-time stats
        all_time_pipeline = [
            {
                "$match": {
                    "user_id": user_id,
                    "verification_status": VerificationStatus.APPROVED
                }
            },
            {
                "$group": {
                    "_id": None,
                    "total_impact": {"$sum": "$calculated_impact_score"},
                    "total_activities": {"$sum": 1},
                    "total_food_donated": {"$sum": "$food_donated_lbs"},
                    "total_meals_provided": {"$sum": "$meals_provided"},
                    "total_people_helped": {"$sum": "$people_helped"},
                    "total_volunteer_hours": {"$sum": "$volunteer_hours"}
                }
            }
        ]
        
        total_stats = await self.db.charity_activities.aggregate(all_time_pipeline).to_list(length=1)
        total = total_stats[0] if total_stats else {}
        
        return {
            "monthly_impact": monthly.get("monthly_impact", 0.0),
            "monthly_activities": monthly.get("monthly_activities", 0),
            "monthly_food_donated": monthly.get("monthly_food_donated", 0.0),
            "monthly_meals_provided": monthly.get("monthly_meals_provided", 0),
            "monthly_people_helped": monthly.get("monthly_people_helped", 0),
            "monthly_volunteer_hours": monthly.get("monthly_volunteer_hours", 0.0),
            "total_impact": total.get("total_impact", 0.0),
            "total_activities": total.get("total_activities", 0),
            "total_food_donated": total.get("total_food_donated", 0.0),
            "total_meals_provided": total.get("total_meals_provided", 0),
            "total_people_helped": total.get("total_people_helped", 0),
            "total_volunteer_hours": total.get("total_volunteer_hours", 0.0),
            "estimated_monthly_sales": 150.0  # Mock value - would calculate from actual sales
        }
    
    async def _get_user_community_ranking(self, user_id: str) -> Dict[str, Any]:
        """Get user's ranking in community"""
        
        # Get total impact for user
        user_stats = await self._get_user_charity_stats(user_id)
        user_impact = user_stats["total_impact"]
        
        # Count users with higher impact
        higher_impact_users = await self.db.charity_programs.count_documents({
            "total_impact_score": {"$gt": user_impact}
        })
        
        rank = higher_impact_users + 1
        
        # Get total participants
        total_participants = await self.db.charity_programs.count_documents({"is_active": True})
        
        # Calculate percentile
        percentile = ((total_participants - rank + 1) / total_participants) * 100 if total_participants > 0 else 0
        
        return {
            "rank": rank,
            "total_participants": total_participants,
            "percentile": round(percentile, 1),
            "recognition_level": self.impact_calculator.determine_recognition_level(
                user_impact, user_stats["total_activities"]
            )
        }
    
    async def _get_next_tier_requirements(self, user_id: str, current_stats: Dict) -> Dict[str, Any]:
        """Calculate requirements for next tier"""
        
        membership = await self.db.premium_memberships.find_one({"user_id": user_id}, {"_id": 0})
        if not membership:
            return {}
        
        current_tier = PremiumTier(membership["tier"])
        tier_requirements = self.impact_calculator.calculate_tier_requirements()
        
        # Determine next tier
        tier_order = [PremiumTier.COMMUNITY_HELPER, PremiumTier.GARDEN_SUPPORTER, PremiumTier.LOCAL_CHAMPION]
        current_index = tier_order.index(current_tier)
        
        if current_index >= len(tier_order) - 1:
            return {"message": "You've reached the highest tier!"}
        
        next_tier = tier_order[current_index + 1]
        requirements = tier_requirements[next_tier]
        
        return {
            "next_tier": next_tier.value,
            "requirements": requirements,
            "progress": {
                "monthly_impact": {
                    "current": current_stats["monthly_impact"],
                    "required": requirements["monthly_impact_required"],
                    "percentage": min(100, (current_stats["monthly_impact"] / requirements["monthly_impact_required"]) * 100)
                },
                "monthly_activities": {
                    "current": current_stats["monthly_activities"],
                    "required": requirements["monthly_activities_required"],
                    "percentage": min(100, (current_stats["monthly_activities"] / requirements["monthly_activities_required"]) * 100)
                }
            }
        }
    
    async def _get_local_partner_organizations(self, preferred_locations: List[str]) -> List[Dict]:
        """Get local partner organizations based on user's preferred locations"""
        
        # For now, return mock data - in production would query actual partner database
        return [
            {
                "name": "Downtown Food Bank",
                "type": "food_bank",
                "address": "123 Main St, Downtown",
                "contact": "foodbank@downtown.org",
                "services": ["Food distribution", "Emergency meals"],
                "operating_hours": "Mon-Fri 9AM-5PM"
            },
            {
                "name": "Community Shelter",
                "type": "homeless_shelter",
                "address": "456 Oak Ave, Midtown",
                "contact": "(555) 123-4567",
                "services": ["Shelter", "Meals", "Social services"],
                "operating_hours": "24/7"
            }
        ]
    
    async def _calculate_recognition_badges(self, user_id: str, stats: Dict) -> List[str]:
        """Calculate recognition badges earned by user"""
        
        badges = []
        
        # Food donation badges
        if stats["total_food_donated"] >= 100:
            badges.append("Century Donor (100+ lbs donated)")
        elif stats["total_food_donated"] >= 50:
            badges.append("Major Donor (50+ lbs donated)")
        elif stats["total_food_donated"] >= 10:
            badges.append("Food Saver (10+ lbs donated)")
        
        # Meal provision badges
        if stats["total_meals_provided"] >= 200:
            badges.append("Meal Hero (200+ meals provided)")
        elif stats["total_meals_provided"] >= 50:
            badges.append("Meal Provider (50+ meals provided)")
        
        # Volunteer hours badges
        if stats["total_volunteer_hours"] >= 100:
            badges.append("Volunteer Champion (100+ hours)")
        elif stats["total_volunteer_hours"] >= 20:
            badges.append("Dedicated Volunteer (20+ hours)")
        
        # Impact score badges
        if stats["total_impact"] >= 1000:
            badges.append("Community Legend (1000+ impact score)")
        elif stats["total_impact"] >= 500:
            badges.append("Community Star (500+ impact score)")
        elif stats["total_impact"] >= 100:
            badges.append("Rising Star (100+ impact score)")
        
        return badges
    
    async def _get_top_community_contributors(self, limit: int = 10) -> List[Dict]:
        """Get top community contributors"""
        
        pipeline = [
            {
                "$match": {"is_active": True}
            },
            {
                "$sort": {"total_impact_score": -1}
            },
            {
                "$limit": limit
            },
            {
                "$lookup": {
                    "from": "users",
                    "localField": "user_id",
                    "foreignField": "id",
                    "as": "user_info"
                }
            },
            {
                "$project": {
                    "user_id": 1,
                    "total_impact_score": 1,
                    "username": {"$arrayElemAt": ["$user_info.username", 0]},
                    "full_name": {"$arrayElemAt": ["$user_info.full_name", 0]}
                }
            }
        ]
        
        contributors = await self.db.charity_programs.aggregate(pipeline).to_list(length=limit)
        return contributors