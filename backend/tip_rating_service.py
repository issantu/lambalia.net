# Tip and Rating Service for Lambalia - Post-Service Experience
import os
import uuid
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from enum import Enum

# Rating and Tip Models
class ServiceType(str, Enum):
    COOKING_CONSULTATION = "cooking_consultation"
    HOME_RESTAURANT = "home_restaurant"
    RECIPE_SHARING = "recipe_sharing"
    COOKING_CLASS = "cooking_class"
    DAILY_MEAL = "daily_meal"
    SPECIALTY_ORDER = "specialty_order"

class TipAmount(str, Enum):
    SMALL = "2.00"
    MEDIUM = "5.00"
    LARGE = "10.00"
    CUSTOM = "custom"

class RatingRequest(BaseModel):
    service_id: str
    user_id: str
    provider_id: str
    service_type: ServiceType
    rating: int  # 1-5 stars
    comment: Optional[str] = None
    tip_amount: Optional[float] = None
    payment_method_id: Optional[str] = None

class TipRequest(BaseModel):
    service_id: str
    user_id: str
    provider_id: str
    amount: float
    payment_method_id: str

class ServiceRating(BaseModel):
    id: str
    service_id: str
    user_id: str
    provider_id: str
    service_type: ServiceType
    rating: int
    comment: Optional[str]
    tip_amount: float
    tip_processed: bool
    created_at: datetime
    processed_at: Optional[datetime]

class TipRatingService:
    """
    Service for handling post-service ratings and tips
    Integrates with payment processing and earnings tracking
    """
    
    def __init__(self):
        self.mongo_url = os.environ.get('MONGO_URL')
        self.db_name = os.environ.get('DB_NAME')
        
        if not self.mongo_url or not self.db_name:
            raise ValueError("MONGO_URL and DB_NAME must be set in environment")
        
        self.client = AsyncIOMotorClient(self.mongo_url)
        self.db = self.client[self.db_name]
        
        # Collections
        self.ratings_collection = self.db.service_ratings
        self.tips_collection = self.db.tips
        self.earnings_collection = self.db.earnings
        self.services_collection = self.db.completed_services
        
        logging.info("Tip and Rating service initialized")
    
    async def create_service_completion_record(self, service_data: Dict[str, Any]) -> str:
        """Create a record when a service is completed"""
        try:
            service_record = {
                "id": str(uuid.uuid4()),
                "service_type": service_data.get("service_type"),
                "user_id": service_data.get("user_id"),
                "provider_id": service_data.get("provider_id"),
                "service_details": service_data.get("details", {}),
                "amount_paid": service_data.get("amount", 0.0),
                "payment_method_id": service_data.get("payment_method_id"),
                "completed_at": datetime.utcnow(),
                "rating_sent": False,
                "rating_received": False
            }
            
            await self.services_collection.insert_one(service_record)
            
            # Schedule rating request (will be sent via SMS)
            await self._schedule_rating_request(service_record)
            
            return service_record["id"]
            
        except Exception as e:
            logging.error(f"Failed to create service completion record: {str(e)}")
            raise
    
    async def submit_rating_and_tip(self, rating_request: RatingRequest) -> Dict[str, Any]:
        """Process user rating and optional tip"""
        try:
            # Validate rating
            if not 1 <= rating_request.rating <= 5:
                raise ValueError("Rating must be between 1 and 5")
            
            # Create rating record
            rating_record = {
                "id": str(uuid.uuid4()),
                "service_id": rating_request.service_id,
                "user_id": rating_request.user_id,
                "provider_id": rating_request.provider_id,
                "service_type": rating_request.service_type,
                "rating": rating_request.rating,
                "comment": rating_request.comment,
                "tip_amount": rating_request.tip_amount or 0.0,
                "tip_processed": False,
                "created_at": datetime.utcnow(),
                "processed_at": None
            }
            
            # Insert rating
            await self.ratings_collection.insert_one(rating_record)
            
            # Process tip if provided
            tip_result = None
            if rating_request.tip_amount and rating_request.tip_amount > 0:
                tip_result = await self._process_tip(
                    rating_request.service_id,
                    rating_request.user_id,
                    rating_request.provider_id,
                    rating_request.tip_amount,
                    rating_request.payment_method_id
                )
            
            # Update service completion record
            await self.services_collection.update_one(
                {"id": rating_request.service_id},
                {"$set": {"rating_received": True}}
            )
            
            # Update provider rating statistics
            await self._update_provider_rating_stats(
                rating_request.provider_id,
                rating_request.rating,
                rating_request.tip_amount or 0.0
            )
            
            return {
                "success": True,
                "rating_id": rating_record["id"],
                "tip_processed": tip_result is not None and tip_result.get("success", False),
                "tip_amount": rating_request.tip_amount or 0.0
            }
            
        except Exception as e:
            logging.error(f"Failed to process rating and tip: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def _process_tip(self, service_id: str, user_id: str, provider_id: str, 
                          amount: float, payment_method_id: str) -> Dict[str, Any]:
        """Process tip payment from user to provider"""
        try:
            # Create tip record
            tip_record = {
                "id": str(uuid.uuid4()),
                "service_id": service_id,
                "user_id": user_id,
                "provider_id": provider_id,
                "amount": amount,
                "payment_method_id": payment_method_id,
                "status": "pending",
                "created_at": datetime.utcnow(),
                "processed_at": None
            }
            
            # Insert tip record
            await self.tips_collection.insert_one(tip_record)
            
            # Process payment (mock for now - integrate with actual payment service)
            payment_result = await self._process_tip_payment(
                user_id, provider_id, amount, payment_method_id
            )
            
            if payment_result["success"]:
                # Update tip status
                await self.tips_collection.update_one(
                    {"id": tip_record["id"]},
                    {
                        "$set": {
                            "status": "completed",
                            "processed_at": datetime.utcnow(),
                            "transaction_id": payment_result["transaction_id"]
                        }
                    }
                )
                
                # Add to provider's tip earnings
                await self._add_tip_earning(provider_id, amount, tip_record["id"])
                
                return {"success": True, "tip_id": tip_record["id"]}
            else:
                # Update tip status to failed
                await self.tips_collection.update_one(
                    {"id": tip_record["id"]},
                    {"$set": {"status": "failed", "error": payment_result["error"]}}
                )
                
                return {"success": False, "error": payment_result["error"]}
            
        except Exception as e:
            logging.error(f"Failed to process tip: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def _process_tip_payment(self, user_id: str, provider_id: str, 
                                  amount: float, payment_method_id: str) -> Dict[str, Any]:
        """Process actual tip payment (integrate with payment service)"""
        try:
            # Mock payment processing - replace with actual payment service
            # This would integrate with Stripe, PayPal, etc.
            
            transaction_id = f"tip_{uuid.uuid4().hex[:12]}"
            
            # Simulate payment processing
            return {
                "success": True,
                "transaction_id": transaction_id,
                "amount": amount,
                "processed_at": datetime.utcnow()
            }
            
        except Exception as e:
            logging.error(f"Payment processing failed: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def _add_tip_earning(self, provider_id: str, amount: float, tip_id: str):
        """Add tip to provider's earnings (separate from regular earnings)"""
        try:
            earning_record = {
                "id": str(uuid.uuid4()),
                "provider_id": provider_id,
                "type": "tip",
                "amount": amount,
                "tip_id": tip_id,
                "tax_category": "tips",
                "created_at": datetime.utcnow(),
                "date": datetime.utcnow().date().isoformat()
            }
            
            await self.earnings_collection.insert_one(earning_record)
            
        except Exception as e:
            logging.error(f"Failed to add tip earning: {str(e)}")
    
    async def _update_provider_rating_stats(self, provider_id: str, rating: int, tip_amount: float):
        """Update provider's overall rating statistics"""
        try:
            # This would update provider profile with new rating stats
            # Implementation depends on your user/provider data structure
            pass
            
        except Exception as e:
            logging.error(f"Failed to update provider rating stats: {str(e)}")
    
    async def _schedule_rating_request(self, service_record: Dict[str, Any]):
        """Schedule rating request to be sent after service completion"""
        try:
            # Mark that rating SMS should be sent
            # This could be processed by a background job or trigger SMS immediately
            
            # For now, we'll create a scheduled task record
            scheduled_task = {
                "id": str(uuid.uuid4()),
                "task_type": "send_rating_sms",
                "service_id": service_record["id"],
                "user_id": service_record["user_id"],
                "provider_id": service_record["provider_id"],
                "service_type": service_record["service_type"],
                "scheduled_at": datetime.utcnow() + timedelta(hours=1),  # Send 1 hour after completion
                "status": "pending",
                "created_at": datetime.utcnow()
            }
            
            await self.db.scheduled_tasks.insert_one(scheduled_task)
            
        except Exception as e:
            logging.error(f"Failed to schedule rating request: {str(e)}")
    
    async def get_provider_earnings_summary(self, provider_id: str, 
                                          start_date: Optional[datetime] = None,
                                          end_date: Optional[datetime] = None) -> Dict[str, Any]:
        """Get provider's earnings summary with regular and tip separation"""
        try:
            # Default to current month if no dates provided
            if not start_date:
                start_date = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            if not end_date:
                end_date = datetime.utcnow()
            
            # Query earnings
            earnings_cursor = self.earnings_collection.find({
                "provider_id": provider_id,
                "created_at": {"$gte": start_date, "$lte": end_date}
            })
            
            earnings = await earnings_cursor.to_list(length=None)
            
            # Separate regular earnings from tips
            regular_earnings = [e for e in earnings if e.get("type") != "tip"]
            tip_earnings = [e for e in earnings if e.get("type") == "tip"]
            
            regular_total = sum(e["amount"] for e in regular_earnings)
            tips_total = sum(e["amount"] for e in tip_earnings)
            
            return {
                "provider_id": provider_id,
                "period": {
                    "start_date": start_date.isoformat(),
                    "end_date": end_date.isoformat()
                },
                "regular_earnings": {
                    "total": regular_total,
                    "count": len(regular_earnings),
                    "tax_category": "regular_income"
                },
                "tips": {
                    "total": tips_total,
                    "count": len(tip_earnings),
                    "tax_category": "tips"
                },
                "total_earnings": regular_total + tips_total,
                "breakdown": {
                    "regular": regular_earnings,
                    "tips": tip_earnings
                }
            }
            
        except Exception as e:
            logging.error(f"Failed to get earnings summary: {str(e)}")
            return {"error": str(e)}
    
    async def get_pending_rating_requests(self) -> List[Dict[str, Any]]:
        """Get services that need rating requests sent"""
        try:
            # Find completed services that haven't had rating SMS sent
            cursor = self.services_collection.find({
                "rating_sent": False,
                "completed_at": {"$lte": datetime.utcnow() - timedelta(hours=1)}
            })
            
            return await cursor.to_list(length=100)
            
        except Exception as e:
            logging.error(f"Failed to get pending rating requests: {str(e)}")
            return []

# Global tip rating service instance
tip_rating_service = None

async def get_tip_rating_service() -> TipRatingService:
    """Get or create tip rating service instance"""
    global tip_rating_service
    if tip_rating_service is None:
        tip_rating_service = TipRatingService()
    return tip_rating_service