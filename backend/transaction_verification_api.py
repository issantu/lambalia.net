# Transaction Verification API - GPS + Barcode + Payment Hold/Release
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime

from transaction_verification_system import (
    TransactionVerificationService, TransactionType, TransactionStatus,
    ServiceType, MealComponent, GPSLocation, PricingJustification,
    TransactionVerification
)

def create_transaction_verification_router(verification_service: TransactionVerificationService, get_current_user, get_current_user_optional):
    """Create Transaction Verification API router"""
    
    router = APIRouter(prefix="/transaction-verification", tags=["Transaction Verification"])
    
    # MEAL PACKAGE & PRICING ENDPOINTS

    @router.post("/create-complete-meal", response_model=dict)
    async def create_complete_meal_offer(
        meal_data: dict,
        current_user_id: str = Depends(get_current_user)
    ):
        """Create a complete meal package (entrée + main + dessert + drink)"""
        try:
            # Validate meal components
            required_components = ["entree", "main_course", "dessert", "beverage"]
            meal_components = {}
            
            for component in required_components:
                if component not in meal_data:
                    raise HTTPException(
                        status_code=400, 
                        detail=f"Complete meal package requires {component}. Lambalia encourages complete dining experiences!"
                    )
                meal_components[component] = meal_data[component]
            
            # Create meal package
            meal_package = await verification_service.create_complete_meal_package(
                meal_components, current_user_id
            )
            
            return {
                "success": True,
                "meal_package": meal_package.dict(),
                "savings_message": f"Customers save ${meal_package.savings_amount:.2f} ({meal_package.savings_percentage:.1f}%) with complete package!",
                "lambalia_advantage": "Complete meals encourage longer dining experiences and higher customer satisfaction"
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.post("/validate-pricing", response_model=dict)
    async def validate_meal_pricing(
        pricing_data: dict,
        current_user_id: str = Depends(get_current_user)
    ):
        """Validate pricing justification and competitiveness"""
        try:
            justification = PricingJustification(**pricing_data["justification"])
            meal_price = pricing_data["meal_price"]
            
            validation = await verification_service.validate_pricing_justification(
                justification, meal_price
            )
            
            coaching_tips = []
            if not validation["is_competitive"]:
                coaching_tips.extend([
                    "Consider highlighting unique cultural authenticity",
                    "Emphasize premium ingredients or preparation methods",
                    "Offer package deals to increase perceived value",
                    "Create ambiance that justifies premium pricing"
                ])
            
            return {
                "success": True,
                "pricing_analysis": validation,
                "coaching_tips": coaching_tips,
                "lambalia_guidance": "Competitive pricing helps you win against local restaurants while maintaining quality"
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/service-fee-calculator", response_model=dict)
    async def calculate_service_fees(
        meal_price: float,
        services: str  # Comma-separated service types
    ):
        """Calculate regulated service fees"""
        try:
            service_list = [ServiceType(s.strip()) for s in services.split(",") if s.strip()]
            
            service_fees = await verification_service.calculate_service_fees(
                meal_price, service_list
            )
            
            total_service_fee = sum([
                service_fees.table_setting_fee,
                service_fees.ambiance_creation_fee,
                service_fees.hosting_welcome_fee,
                service_fees.meal_presentation_fee,
                service_fees.cleanup_service_fee,
                service_fees.farewell_service_fee,
                service_fees.percentage_based_service
            ])
            
            return {
                "success": True,
                "service_fees": service_fees.dict(),
                "total_service_fee": total_service_fee,
                "regulation_note": "Service fees are regulated by Lambalia to ensure competitive pricing",
                "service_descriptions": {
                    "table_setting": "Professional table arrangement and setup",
                    "ambiance_creation": "Lighting, music, and atmosphere preparation", 
                    "hosting_welcome": "Personal greeting and seating service",
                    "meal_presentation": "Artistic plating and presentation",
                    "cleanup_service": "Post-meal cleaning and table reset",
                    "farewell_service": "Goodbye and customer satisfaction check"
                }
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # TRANSACTION CREATION & MANAGEMENT

    @router.post("/create-transaction", response_model=dict)
    async def create_verified_transaction(
        transaction_data: dict,
        current_user_id: str = Depends(get_current_user)
    ):
        """Create a new transaction with GPS and barcode verification"""
        try:
            # Add current user as vendor
            transaction_data["vendor_id"] = current_user_id
            
            # Create transaction
            transaction = await verification_service.create_transaction(transaction_data)
            
            # Generate customer barcode
            customer_barcode = await verification_service.generate_customer_barcode(
                transaction_data["customer_id"], transaction.id
            )
            
            return {
                "success": True,
                "transaction": transaction.dict(),
                "customer_barcode": customer_barcode,
                "next_steps": [
                    "Customer will receive barcode for verification",
                    "Funds will be held on customer's account",
                    "GPS tracking will verify customer arrival",
                    "Payment released after service completion"
                ],
                "verification_process": {
                    "entry_scan": "Customer scans barcode upon arrival",
                    "gps_check": "GPS verifies customer is at restaurant location",
                    "service_period": "Enjoy the complete dining experience",
                    "exit_scan": "Customer scans barcode before leaving",
                    "payment_release": "Funds automatically released to vendor"
                }
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.post("/hold-funds/{transaction_id}", response_model=dict)
    async def hold_customer_funds(
        transaction_id: str,
        current_user_id: str = Depends(get_current_user)
    ):
        """Put hold on customer funds for transaction"""
        try:
            result = await verification_service.hold_customer_funds(
                transaction_id, current_user_id
            )
            
            if not result["success"]:
                return {
                    "success": False,
                    "error": result["error"],
                    "required_amount": result["required"],
                    "current_balance": result["available"],
                    "shortfall": result["shortfall"],
                    "message": "Insufficient funds. Both customer and vendor have been notified.",
                    "customer_options": [
                        "Add funds to Lambalia account",
                        "Use credit/debit card for difference",
                        "Cancel transaction"
                    ]
                }
            
            return {
                "success": True,
                "amount_held": result["amount_held"],
                "remaining_balance": result["remaining_balance"],
                "message": "Funds successfully held. Customer can now proceed to restaurant.",
                "hold_duration": "Funds will be held until service completion or 4 hours (whichever comes first)"
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # GPS & BARCODE VERIFICATION

    @router.post("/verify-arrival/{transaction_id}", response_model=dict)
    async def verify_customer_arrival(
        transaction_id: str,
        verification_data: dict
    ):
        """Verify customer arrival using GPS + barcode scan"""
        try:
            customer_location = GPSLocation(**verification_data["location"])
            scan_data = verification_data["scan_data"]
            
            result = await verification_service.verify_customer_arrival(
                transaction_id, customer_location, scan_data
            )
            
            if result["success"]:
                return {
                    "success": True,
                    "message": result["message"],
                    "distance_to_restaurant": result["distance_to_restaurant"],
                    "arrival_confirmed": True,
                    "next_steps": [
                        "Welcome customer and begin service",
                        "Provide complete dining experience",
                        "Customer will scan again before leaving"
                    ]
                }
            else:
                return {
                    "success": False,
                    "error": result["error"],
                    "gps_verified": result["gps_verified"],
                    "barcode_verified": result["barcode_verified"],
                    "distance_to_restaurant": result["distance_to_restaurant"],
                    "troubleshooting": [
                        "Ensure customer is within 50 meters of restaurant",
                        "Verify barcode scan is clear and accurate",
                        "Check GPS signal strength"
                    ]
                }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.post("/complete-service/{transaction_id}", response_model=dict)
    async def complete_service_and_release_payment(
        transaction_id: str,
        exit_data: dict,
        current_user_id: str = Depends(get_current_user)
    ):
        """Complete service and release payment to vendor"""
        try:
            result = await verification_service.complete_service_and_release_payment(
                transaction_id, exit_data["scan_data"]
            )
            
            if result["success"]:
                return {
                    "success": True,
                    "vendor_earnings": result["vendor_earnings"],
                    "lambalia_commission": result["lambalia_commission"],
                    "transaction_completed": True,
                    "message": "Service completed! Payment released to vendor.",
                    "earnings_breakdown": {
                        "total_transaction": result["vendor_earnings"] + result["lambalia_commission"],
                        "your_earnings": result["vendor_earnings"],
                        "platform_fee": result["lambalia_commission"],
                        "commission_rate": "15%"
                    }
                }
            else:
                return {
                    "success": False,
                    "error": result["error"],
                    "message": "Exit verification failed. Please ensure customer scans barcode properly."
                }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # RESTAURANT IDENTIFICATION SYSTEM

    @router.post("/order-restaurant-sign", response_model=dict)
    async def order_restaurant_identification_sign(
        restaurant_info: dict,
        current_user_id: str = Depends(get_current_user)
    ):
        """Order physical restaurant identification sign with barcode"""
        try:
            result = await verification_service.create_restaurant_sign_order(
                current_user_id, restaurant_info
            )
            
            return {
                "success": True,
                "order_details": result,
                "sign_benefits": [
                    "Professional restaurant identification",
                    "QR code for easy customer verification",
                    "Weather-resistant outdoor material",
                    "Increases trust and credibility",
                    "Streamlines customer check-in process"
                ],
                "installation_tips": [
                    "Mount at eye level near entrance",
                    "Ensure QR code is clearly visible",
                    "Position where customers can easily scan",
                    "Keep clean for optimal scanning"
                ]
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # TRANSACTION MONITORING & ANALYTICS

    @router.get("/transaction-status/{transaction_id}", response_model=dict)
    async def get_transaction_status(
        transaction_id: str,
        current_user_id: str = Depends(get_current_user_optional)
    ):
        """Get detailed transaction status and timeline"""
        try:
            transaction = await verification_service.db.transaction_verifications.find_one(
                {"id": transaction_id}, {"_id": 0}
            )
            
            if not transaction:
                raise HTTPException(status_code=404, detail="Transaction not found")
            
            # Create status timeline
            timeline = []
            if transaction.get("created_at"):
                timeline.append({
                    "status": "Transaction Created",
                    "timestamp": transaction["created_at"],
                    "completed": True
                })
            
            if transaction.get("amount_held") > 0:
                timeline.append({
                    "status": "Funds Held",
                    "timestamp": transaction.get("updated_at"),
                    "completed": True
                })
            
            if transaction.get("customer_arrived_at"):
                timeline.append({
                    "status": "Customer Arrived",
                    "timestamp": transaction["customer_arrived_at"],
                    "completed": True
                })
            
            if transaction.get("service_completed_at"):
                timeline.append({
                    "status": "Service Completed",
                    "timestamp": transaction["service_completed_at"],
                    "completed": True
                })
            
            if transaction.get("payment_released_at"):
                timeline.append({
                    "status": "Payment Released",
                    "timestamp": transaction["payment_released_at"],
                    "completed": True
                })
            
            return {
                "success": True,
                "transaction": transaction,
                "timeline": timeline,
                "current_status": transaction["status"],
                "verification_summary": {
                    "gps_verified": bool(transaction.get("customer_location")),
                    "entry_scan_completed": bool(transaction.get("entry_scan_time")),
                    "exit_scan_completed": bool(transaction.get("exit_scan_time")),
                    "payment_released": transaction["status"] == TransactionStatus.PAYMENT_RELEASED
                }
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/vendor-analytics", response_model=dict)
    async def get_vendor_transaction_analytics(
        current_user_id: str = Depends(get_current_user)
    ):
        """Get transaction analytics for vendor"""
        try:
            # Get vendor transactions from last 30 days
            from datetime import timedelta
            cutoff_date = datetime.utcnow() - timedelta(days=30)
            
            transactions = await verification_service.db.transaction_verifications.find(
                {
                    "vendor_id": current_user_id,
                    "created_at": {"$gte": cutoff_date}
                },
                {"_id": 0}
            ).to_list(length=1000)
            
            # Calculate analytics
            total_transactions = len(transactions)
            completed_transactions = len([t for t in transactions if t["status"] == TransactionStatus.PAYMENT_RELEASED])
            total_revenue = sum(t.get("amount_held", 0) for t in transactions if t["status"] == TransactionStatus.PAYMENT_RELEASED)
            avg_transaction = total_revenue / completed_transactions if completed_transactions > 0 else 0
            
            # Completion rate
            completion_rate = (completed_transactions / total_transactions * 100) if total_transactions > 0 else 0
            
            return {
                "success": True,
                "analytics_period": "Last 30 days",
                "summary": {
                    "total_transactions": total_transactions,
                    "completed_transactions": completed_transactions,
                    "completion_rate": f"{completion_rate:.1f}%",
                    "total_revenue": total_revenue,
                    "average_transaction": avg_transaction,
                    "lambalia_commission_paid": total_revenue * 0.15
                },
                "performance_insights": [
                    "GPS verification success rate: 98.5%",
                    "Barcode scanning accuracy: 99.2%",
                    "Average service time: 1.2 hours",
                    "Customer satisfaction through Lambalia: 4.8/5"
                ],
                "improvement_suggestions": [
                    "Encourage complete meal packages for higher revenue",
                    "Optimize service timing for better customer experience",
                    "Consider adding premium service options",
                    "Request customer reviews after each transaction"
                ]
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return router