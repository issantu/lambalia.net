# Lambalia Transaction Verification System
# GPS Tracking + Barcode Verification + Payment Hold/Release System

import asyncio
import qrcode
import io
import base64
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any, Tuple
from motor.motor_asyncio import AsyncIOMotorDatabase
import logging
from pydantic import BaseModel, Field
import uuid
from enum import Enum
import json
import math

class TransactionType(str, Enum):
    HOME_RESTAURANT = "home_restaurant"
    LAMBALIA_EATS = "lambalia_eats"
    QUICK_PICKUP = "quick_pickup"
    DELIVERY = "delivery"

class TransactionStatus(str, Enum):
    PENDING = "pending"
    FUNDS_HELD = "funds_held"
    IN_PROGRESS = "in_progress"
    CUSTOMER_ARRIVED = "customer_arrived"
    SERVICE_STARTED = "service_started"
    SERVICE_COMPLETED = "service_completed"
    PAYMENT_RELEASED = "payment_released"
    CANCELLED = "cancelled"
    DISPUTED = "disputed"

class ServiceType(str, Enum):
    TABLE_SETTING = "table_setting"
    AMBIANCE_CREATION = "ambiance_creation"
    HOSTING_WELCOME = "hosting_welcome"
    MEAL_PRESENTATION = "meal_presentation"
    CLEANUP_SERVICE = "cleanup_service"
    FAREWELL_SERVICE = "farewell_service"

class MealComponent(str, Enum):
    APPETIZER = "appetizer"
    ENTREE = "entree"
    MAIN_COURSE = "main_course"
    DESSERT = "dessert"
    BEVERAGE = "beverage"
    SIDE_DISH = "side_dish"

class GPSLocation(BaseModel):
    """GPS coordinates for location tracking"""
    latitude: float
    longitude: float
    accuracy: float = 10.0  # meters
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class PricingJustification(BaseModel):
    """User's explanation for their pricing"""
    meal_complexity: str  # Simple, Moderate, Complex, Gourmet
    ingredient_quality: str  # Basic, Premium, Organic, Exotic
    preparation_time: int  # minutes
    cultural_authenticity: str  # Traditional, Fusion, Modern
    presentation_level: str  # Casual, Elegant, Fine Dining
    unique_value_proposition: str  # What makes this special
    competitive_analysis: Optional[str] = None  # How it compares to local options
    justification_text: str  # Detailed explanation

class ServiceFeeStructure(BaseModel):
    """Regulated service fees by Lambalia"""
    table_setting_fee: float = 2.50
    ambiance_creation_fee: float = 3.00
    hosting_welcome_fee: float = 2.00
    meal_presentation_fee: float = 1.50
    cleanup_service_fee: float = 4.00
    farewell_service_fee: float = 1.00
    
    # Dynamic pricing based on meal value
    percentage_based_service: float = 0.08  # 8% of meal price
    minimum_service_fee: float = 5.00
    maximum_service_fee: float = 25.00

class CompleteMealPackage(BaseModel):
    """Structure for complete meal offerings"""
    appetizer: Dict[str, Any]
    main_course: Dict[str, Any]
    dessert: Dict[str, Any]
    beverage: Dict[str, Any]
    
    # Pricing
    individual_total: float  # Sum of individual components
    package_price: float  # Discounted package price
    savings_amount: float  # How much customer saves
    savings_percentage: float  # Savings as percentage

class TransactionVerification(BaseModel):
    """Complete transaction with verification system"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    transaction_type: TransactionType
    
    # Parties involved
    customer_id: str
    vendor_id: str
    home_restaurant_id: Optional[str] = None
    
    # Location and verification
    restaurant_location: GPSLocation
    customer_location: Optional[GPSLocation] = None
    verification_barcode: str = Field(default_factory=lambda: str(uuid.uuid4()))
    
    # Meal and pricing
    meal_package: CompleteMealPackage
    pricing_justification: PricingJustification
    service_fees: ServiceFeeStructure
    
    # Payment details
    meal_cost: float
    service_cost: float
    total_amount: float
    amount_held: float = 0.0
    
    # Status tracking
    status: TransactionStatus = TransactionStatus.PENDING
    customer_arrived_at: Optional[datetime] = None
    service_started_at: Optional[datetime] = None
    service_completed_at: Optional[datetime] = None
    payment_released_at: Optional[datetime] = None
    
    # Verification scans
    entry_scan_time: Optional[datetime] = None
    exit_scan_time: Optional[datetime] = None
    
    # Created timestamp
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class TransactionVerificationService:
    """Service for managing GPS + Barcode verification transactions"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.logger = logging.getLogger(__name__)
        
        # Competitive pricing analysis data
        self.local_restaurant_benchmarks = {
            "casual_dining": {"avg_price": 15.50, "service_fee": 2.00},
            "mid_scale": {"avg_price": 28.00, "service_fee": 4.50},
            "upscale": {"avg_price": 45.00, "service_fee": 8.00},
            "fine_dining": {"avg_price": 75.00, "service_fee": 12.00}
        }
    
    async def create_complete_meal_package(self, meal_components: Dict[str, Any], vendor_id: str) -> CompleteMealPackage:
        """Create a complete meal package with entrée, main, dessert, and drink"""
        
        # Ensure all required components are present
        required_components = [MealComponent.ENTREE, MealComponent.MAIN_COURSE, 
                             MealComponent.DESSERT, MealComponent.BEVERAGE]
        
        for component in required_components:
            if component not in meal_components:
                raise ValueError(f"Complete meal package requires {component}")
        
        # Calculate individual pricing
        individual_total = sum(item.get('price', 0) for item in meal_components.values())
        
        # Apply package discount (encourage complete meals)
        package_discount = 0.15  # 15% discount for complete package
        package_price = individual_total * (1 - package_discount)
        savings_amount = individual_total - package_price
        savings_percentage = (savings_amount / individual_total) * 100
        
        return CompleteMealPackage(
            appetizer=meal_components.get(MealComponent.ENTREE, {}),
            main_course=meal_components[MealComponent.MAIN_COURSE],
            dessert=meal_components[MealComponent.DESSERT],
            beverage=meal_components[MealComponent.BEVERAGE],
            individual_total=individual_total,
            package_price=package_price,
            savings_amount=savings_amount,
            savings_percentage=savings_percentage
        )
    
    async def validate_pricing_justification(self, justification: PricingJustification, meal_price: float) -> Dict[str, Any]:
        """Validate if pricing is competitive and justified"""
        
        # Determine restaurant category based on justification
        category = "casual_dining"
        if justification.presentation_level == "Fine Dining":
            category = "fine_dining"
        elif justification.presentation_level == "Elegant":
            category = "upscale"
        elif justification.ingredient_quality in ["Premium", "Organic", "Exotic"]:
            category = "mid_scale"
        
        benchmark = self.local_restaurant_benchmarks[category]
        
        # Calculate competitive analysis
        price_difference = meal_price - benchmark["avg_price"]
        price_percentage = (price_difference / benchmark["avg_price"]) * 100
        
        is_competitive = price_difference <= 5.00  # Within $5 of local average
        
        recommendations = []
        if not is_competitive:
            recommendations.append("Consider reducing price to be more competitive with local restaurants")
        
        if justification.preparation_time > 120:  # Over 2 hours
            recommendations.append("Highlight extended preparation time as premium value")
        
        if justification.cultural_authenticity == "Traditional":
            recommendations.append("Emphasize authentic cultural experience as unique selling point")
        
        return {
            "is_competitive": is_competitive,
            "local_benchmark": benchmark["avg_price"],
            "price_difference": price_difference,
            "price_percentage": price_percentage,
            "category": category,
            "recommendations": recommendations,
            "competitiveness_score": max(0, 100 - abs(price_percentage))
        }
    
    async def calculate_service_fees(self, meal_price: float, services_selected: List[ServiceType]) -> ServiceFeeStructure:
        """Calculate regulated service fees"""
        
        base_fees = ServiceFeeStructure()
        total_service_fee = 0.0
        
        # Add selected service fees
        service_fee_map = {
            ServiceType.TABLE_SETTING: base_fees.table_setting_fee,
            ServiceType.AMBIANCE_CREATION: base_fees.ambiance_creation_fee,
            ServiceType.HOSTING_WELCOME: base_fees.hosting_welcome_fee,
            ServiceType.MEAL_PRESENTATION: base_fees.meal_presentation_fee,
            ServiceType.CLEANUP_SERVICE: base_fees.cleanup_service_fee,
            ServiceType.FAREWELL_SERVICE: base_fees.farewell_service_fee
        }
        
        for service in services_selected:
            total_service_fee += service_fee_map.get(service, 0.0)
        
        # Add percentage-based service fee
        percentage_fee = meal_price * base_fees.percentage_based_service
        total_service_fee += percentage_fee
        
        # Apply min/max limits
        total_service_fee = max(base_fees.minimum_service_fee, 
                              min(base_fees.maximum_service_fee, total_service_fee))
        
        return ServiceFeeStructure(
            table_setting_fee=base_fees.table_setting_fee if ServiceType.TABLE_SETTING in services_selected else 0,
            ambiance_creation_fee=base_fees.ambiance_creation_fee if ServiceType.AMBIANCE_CREATION in services_selected else 0,
            hosting_welcome_fee=base_fees.hosting_welcome_fee if ServiceType.HOSTING_WELCOME in services_selected else 0,
            meal_presentation_fee=base_fees.meal_presentation_fee if ServiceType.MEAL_PRESENTATION in services_selected else 0,
            cleanup_service_fee=base_fees.cleanup_service_fee if ServiceType.CLEANUP_SERVICE in services_selected else 0,
            farewell_service_fee=base_fees.farewell_service_fee if ServiceType.FAREWELL_SERVICE in services_selected else 0,
            percentage_based_service=percentage_fee,
            minimum_service_fee=base_fees.minimum_service_fee,
            maximum_service_fee=base_fees.maximum_service_fee
        )
    
    async def create_transaction(self, transaction_data: Dict[str, Any]) -> TransactionVerification:
        """Create a new transaction with complete verification system"""
        
        # Create complete meal package
        meal_package = await self.create_complete_meal_package(
            transaction_data["meal_components"], 
            transaction_data["vendor_id"]
        )
        
        # Validate pricing justification
        pricing_validation = await self.validate_pricing_justification(
            PricingJustification(**transaction_data["pricing_justification"]),
            meal_package.package_price
        )
        
        if not pricing_validation["is_competitive"]:
            self.logger.warning(f"Non-competitive pricing detected: {pricing_validation['recommendations']}")
        
        # Calculate service fees
        service_fees = await self.calculate_service_fees(
            meal_package.package_price,
            transaction_data.get("services_selected", [])
        )
        
        # Create transaction
        transaction = TransactionVerification(
            transaction_type=TransactionType(transaction_data["transaction_type"]),
            customer_id=transaction_data["customer_id"],
            vendor_id=transaction_data["vendor_id"],
            home_restaurant_id=transaction_data.get("home_restaurant_id"),
            restaurant_location=GPSLocation(**transaction_data["restaurant_location"]),
            meal_package=meal_package,
            pricing_justification=PricingJustification(**transaction_data["pricing_justification"]),
            service_fees=service_fees,
            meal_cost=meal_package.package_price,
            service_cost=sum([
                service_fees.table_setting_fee, service_fees.ambiance_creation_fee,
                service_fees.hosting_welcome_fee, service_fees.meal_presentation_fee,
                service_fees.cleanup_service_fee, service_fees.farewell_service_fee,
                service_fees.percentage_based_service
            ]),
            total_amount=meal_package.package_price + sum([
                service_fees.table_setting_fee, service_fees.ambiance_creation_fee,
                service_fees.hosting_welcome_fee, service_fees.meal_presentation_fee,
                service_fees.cleanup_service_fee, service_fees.farewell_service_fee,
                service_fees.percentage_based_service
            ])
        )
        
        # Store in database
        await self.db.transaction_verifications.insert_one(transaction.dict())
        
        return transaction
    
    async def hold_customer_funds(self, transaction_id: str, customer_id: str) -> Dict[str, Any]:
        """Put a hold on customer's account for the transaction amount"""
        
        transaction = await self.db.transaction_verifications.find_one({"id": transaction_id})
        if not transaction:
            raise ValueError("Transaction not found")
        
        # Check customer balance
        customer = await self.db.users.find_one({"id": customer_id})
        if not customer:
            raise ValueError("Customer not found")
        
        customer_balance = customer.get("account_balance", 0.0)
        transaction_amount = transaction["total_amount"]
        
        if customer_balance < transaction_amount:
            # Insufficient funds - notify both parties
            await self._notify_insufficient_funds(transaction_id, customer_id, transaction["vendor_id"])
            return {
                "success": False,
                "error": "insufficient_funds",
                "required": transaction_amount,
                "available": customer_balance,
                "shortfall": transaction_amount - customer_balance
            }
        
        # Create hold on funds
        await self.db.users.update_one(
            {"id": customer_id},
            {
                "$inc": {"account_balance": -transaction_amount, "held_balance": transaction_amount},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        
        # Update transaction status
        await self.db.transaction_verifications.update_one(
            {"id": transaction_id},
            {
                "$set": {
                    "status": TransactionStatus.FUNDS_HELD,
                    "amount_held": transaction_amount,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        return {
            "success": True,
            "amount_held": transaction_amount,
            "remaining_balance": customer_balance - transaction_amount
        }
    
    async def generate_customer_barcode(self, customer_id: str, transaction_id: str) -> str:
        """Generate QR code barcode for customer verification"""
        
        # Create QR code data
        qr_data = {
            "customer_id": customer_id,
            "transaction_id": transaction_id,
            "timestamp": datetime.utcnow().isoformat(),
            "type": "customer_verification"
        }
        
        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(json.dumps(qr_data))
        qr.make(fit=True)
        
        # Convert to base64 image
        img = qr.make_image(fill_color="black", back_color="white")
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='PNG')
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        
        return f"data:image/png;base64,{img_base64}"
    
    async def verify_customer_arrival(self, transaction_id: str, customer_location: GPSLocation, scan_data: Dict[str, Any]) -> Dict[str, Any]:
        """Verify customer arrival using GPS + barcode scan"""
        
        transaction = await self.db.transaction_verifications.find_one({"id": transaction_id})
        if not transaction:
            raise ValueError("Transaction not found")
        
        # Verify GPS proximity (within 50 meters)
        restaurant_loc = GPSLocation(**transaction["restaurant_location"])
        distance = self._calculate_distance(customer_location, restaurant_loc)
        
        is_nearby = distance <= 50.0  # 50 meters radius
        
        # Verify barcode scan
        barcode_valid = scan_data.get("transaction_id") == transaction_id
        
        if is_nearby and barcode_valid:
            # Update transaction status
            await self.db.transaction_verifications.update_one(
                {"id": transaction_id},
                {
                    "$set": {
                        "status": TransactionStatus.CUSTOMER_ARRIVED,
                        "customer_location": customer_location.dict(),
                        "customer_arrived_at": datetime.utcnow(),
                        "entry_scan_time": datetime.utcnow(),
                        "updated_at": datetime.utcnow()
                    }
                }
            )
            
            return {
                "success": True,
                "message": "Customer arrival verified",
                "distance_to_restaurant": distance
            }
        
        return {
            "success": False,
            "error": "verification_failed",
            "gps_verified": is_nearby,
            "barcode_verified": barcode_valid,
            "distance_to_restaurant": distance
        }
    
    async def complete_service_and_release_payment(self, transaction_id: str, exit_scan_data: Dict[str, Any]) -> Dict[str, Any]:
        """Complete service and release payment to vendor"""
        
        transaction = await self.db.transaction_verifications.find_one({"id": transaction_id})
        if not transaction:
            raise ValueError("Transaction not found")
        
        # Verify exit scan
        barcode_valid = exit_scan_data.get("transaction_id") == transaction_id
        
        if not barcode_valid:
            return {"success": False, "error": "invalid_exit_scan"}
        
        # Release payment to vendor
        vendor_id = transaction["vendor_id"]
        amount_to_release = transaction["amount_held"]
        
        # Calculate Lambalia commission (15%)
        commission_rate = 0.15
        lambalia_commission = amount_to_release * commission_rate
        vendor_earnings = amount_to_release - lambalia_commission
        
        # Update vendor balance
        await self.db.users.update_one(
            {"id": vendor_id},
            {
                "$inc": {"total_earnings": vendor_earnings, "account_balance": vendor_earnings},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        
        # Update customer held balance
        customer_id = transaction["customer_id"]
        await self.db.users.update_one(
            {"id": customer_id},
            {
                "$inc": {"held_balance": -amount_to_release},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        
        # Update transaction status
        await self.db.transaction_verifications.update_one(
            {"id": transaction_id},
            {
                "$set": {
                    "status": TransactionStatus.PAYMENT_RELEASED,
                    "service_completed_at": datetime.utcnow(),
                    "exit_scan_time": datetime.utcnow(),
                    "payment_released_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        return {
            "success": True,
            "vendor_earnings": vendor_earnings,
            "lambalia_commission": lambalia_commission,
            "transaction_completed": True
        }
    
    def _calculate_distance(self, loc1: GPSLocation, loc2: GPSLocation) -> float:
        """Calculate distance between two GPS coordinates in meters"""
        
        # Haversine formula
        R = 6371000  # Earth's radius in meters
        
        lat1_rad = math.radians(loc1.latitude)
        lat2_rad = math.radians(loc2.latitude)
        delta_lat = math.radians(loc2.latitude - loc1.latitude)
        delta_lon = math.radians(loc2.longitude - loc1.longitude)
        
        a = (math.sin(delta_lat / 2) ** 2 + 
             math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return R * c
    
    async def _notify_insufficient_funds(self, transaction_id: str, customer_id: str, vendor_id: str):
        """Notify both parties about insufficient funds"""
        
        # In production, this would send push notifications, emails, SMS
        notification_data = {
            "transaction_id": transaction_id,
            "customer_id": customer_id,
            "vendor_id": vendor_id,
            "message": "Transaction cancelled due to insufficient funds",
            "timestamp": datetime.utcnow()
        }
        
        # Store notification
        await self.db.notifications.insert_one(notification_data)
        
        self.logger.info(f"Insufficient funds notification sent for transaction {transaction_id}")
    
    async def create_restaurant_sign_order(self, vendor_id: str, restaurant_info: Dict[str, Any]) -> Dict[str, Any]:
        """Create order for physical restaurant identification sign"""
        
        # Generate restaurant barcode
        restaurant_qr_data = {
            "restaurant_id": restaurant_info["restaurant_id"],
            "vendor_id": vendor_id,
            "type": "restaurant_identification",
            "created": datetime.utcnow().isoformat()
        }
        
        # Generate QR code for the sign
        qr = qrcode.QRCode(version=2, box_size=15, border=8)
        qr.add_data(json.dumps(restaurant_qr_data))
        qr.make(fit=True)
        
        # Convert to base64 for preview
        img = qr.make_image(fill_color="black", back_color="white")
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='PNG')
        qr_preview = base64.b64encode(img_buffer.getvalue()).decode()
        
        # Create sign order
        sign_order = {
            "id": str(uuid.uuid4()),
            "vendor_id": vendor_id,
            "restaurant_info": restaurant_info,
            "qr_code_data": restaurant_qr_data,
            "qr_code_preview": f"data:image/png;base64,{qr_preview}",
            "sign_specifications": {
                "size": "12\" x 18\"",
                "material": "Weather-resistant aluminum composite",
                "finish": "UV-protected lamination",
                "mounting": "Pre-drilled holes for easy installation"
            },
            "pricing": {
                "sign_cost": 45.00,
                "shipping": 8.50,
                "total": 53.50
            },
            "status": "pending_payment",
            "created_at": datetime.utcnow()
        }
        
        await self.db.restaurant_sign_orders.insert_one(sign_order)
        
        return {
            "success": True,
            "order_id": sign_order["id"],
            "qr_preview": sign_order["qr_code_preview"],
            "specifications": sign_order["sign_specifications"],
            "total_cost": sign_order["pricing"]["total"],
            "estimated_delivery": "5-7 business days"
        }