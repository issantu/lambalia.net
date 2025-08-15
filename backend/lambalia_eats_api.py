# Lambalia Eats API Routes - Real-time Food Marketplace
from fastapi import APIRouter, HTTPException, Depends, WebSocket, WebSocketDisconnect
from typing import List, Optional, Dict, Any
import json
import uuid
from datetime import datetime, timedelta

from lambalia_eats_service import LambaliaEatsService, EatsMatchingEngine
from lambalia_eats_models import (
    FoodRequestSubmission, FoodOfferSubmission, OrderPlacementRequest,
    RealTimeUpdate, EatsStatsResponse, FoodRequest, FoodOffer, ActiveOrder,
    EatsCookProfile, EatsEaterProfile, ServiceType, RequestStatus, OfferStatus
)

class ConnectionManager:
    """WebSocket connection manager for real-time updates"""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.user_connections: Dict[str, List[str]] = {}  # user_id -> [connection_ids]
    
    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        connection_id = str(uuid.uuid4())
        self.active_connections[connection_id] = websocket
        
        if user_id not in self.user_connections:
            self.user_connections[user_id] = []
        self.user_connections[user_id].append(connection_id)
        
        return connection_id
    
    def disconnect(self, connection_id: str, user_id: str):
        if connection_id in self.active_connections:
            del self.active_connections[connection_id]
        
        if user_id in self.user_connections:
            self.user_connections[user_id] = [
                cid for cid in self.user_connections[user_id] if cid != connection_id
            ]
            if not self.user_connections[user_id]:
                del self.user_connections[user_id]
    
    async def send_to_user(self, user_id: str, message: dict):
        if user_id in self.user_connections:
            for connection_id in self.user_connections[user_id]:
                if connection_id in self.active_connections:
                    try:
                        await self.active_connections[connection_id].send_text(json.dumps(message))
                    except:
                        # Connection closed, remove it
                        self.disconnect(connection_id, user_id)
    
    async def send_to_all(self, message: dict):
        for connection in self.active_connections.values():
            try:
                await connection.send_text(json.dumps(message))
            except:
                pass  # Connection closed

# Global connection manager
manager = ConnectionManager()

def create_lambalia_eats_router(eats_service: LambaliaEatsService, get_current_user, get_current_user_optional):
    """Create Lambalia Eats API router with dependency injection"""
    
    router = APIRouter(prefix="/eats", tags=["Lambalia Eats"])
    
    # FOOD REQUESTS - "I want to eat X"
    
    @router.post("/request-food", response_model=dict)
    async def create_food_request(
        request_data: FoodRequestSubmission,
        current_user_id: str = Depends(get_current_user_optional)  # Optional for standalone users
    ):
        """Create a food request - 'I want to eat X dish'"""
        try:
            if not current_user_id:
                # For standalone users, create temporary eater profile
                current_user_id = f"temp_eater_{str(uuid.uuid4())[:8]}"
            
            food_request = await eats_service.create_food_request(request_data.dict(), current_user_id)
            
            return {
                "success": True,
                "request_id": food_request.id,
                "message": "Food request posted successfully!",
                "status": food_request.status,
                "expires_at": food_request.expires_at.isoformat(),
                "max_price": food_request.max_price,
                "service_types": food_request.preferred_service_types,
                "tracking_info": {
                    "request_id": food_request.id,
                    "status": "posted",
                    "message": "Looking for cooks who can prepare your dish..."
                }
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.get("/requests/active", response_model=List[dict])
    async def get_active_requests(
        lat: float,
        lng: float,
        radius_km: float = 20,
        current_user_id: str = Depends(get_current_user_optional)
    ):
        """Get active food requests near cook's location"""
        try:
            cook_location = {"lat": lat, "lng": lng}
            requests = await eats_service.get_active_requests(cook_location, radius_km)
            
            return requests
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    # FOOD OFFERS - "I have X ready to serve"
    
    @router.post("/offer-food", response_model=dict)
    async def create_food_offer(
        offer_data: FoodOfferSubmission,
        current_user_id: str = Depends(get_current_user_optional)
    ):
        """Create a food offer - 'I have X dish ready to serve'"""
        try:
            if not current_user_id:
                # For standalone users, create temporary cook profile
                current_user_id = f"temp_cook_{str(uuid.uuid4())[:8]}"
            
            food_offer = await eats_service.create_food_offer(offer_data.dict(), current_user_id)
            
            return {
                "success": True,
                "offer_id": food_offer.id,
                "message": "Food offer posted successfully!",
                "status": food_offer.status,
                "quantity_available": food_offer.quantity_available,
                "price_per_serving": food_offer.price_per_serving,
                "ready_at": food_offer.ready_at.isoformat(),
                "available_until": food_offer.available_until.isoformat(),
                "service_types": food_offer.available_service_types,
                "tracking_info": {
                    "offer_id": food_offer.id,
                    "status": "available",
                    "message": "Your meal is available for order!"
                }
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.get("/offers/nearby", response_model=List[dict])
    async def get_nearby_offers(
        lat: float,
        lng: float,
        radius_km: float = 15,
        cuisine: Optional[str] = None,
        max_price: Optional[float] = None,
        service_type: Optional[str] = None
    ):
        """Get nearby food offers for browsing"""
        try:
            eater_location = {"lat": lat, "lng": lng}
            offers = await eats_service.get_nearby_offers(eater_location, radius_km, cuisine)
            
            # Apply additional filters
            if max_price:
                offers = [o for o in offers if o["price_per_serving"] <= max_price]
            
            if service_type:
                offers = [o for o in offers if service_type in o["available_service_types"]]
            
            return offers
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    # ORDER MANAGEMENT
    
    @router.post("/place-order", response_model=dict)
    async def place_order(
        order_data: OrderPlacementRequest,
        current_user_id: str = Depends(get_current_user_optional)
    ):
        """Place an order (from offer or accepting a request)"""
        try:
            if not current_user_id:
                current_user_id = f"temp_user_{str(uuid.uuid4())[:8]}"
            
            order = await eats_service.place_order(order_data.dict(), current_user_id)
            
            # Send real-time notification
            await manager.send_to_user(order.cook_id, {
                "type": "new_order",
                "order_id": order.id,
                "dish_name": order.dish_name,
                "service_type": order.service_type,
                "total_amount": order.total_amount,
                "message": f"New order received: {order.dish_name}"
            })
            
            return {
                "success": True,
                "order_id": order.id,
                "tracking_code": order.tracking_code,
                "message": "Order placed successfully!",
                "order_details": {
                    "dish_name": order.dish_name,
                    "service_type": order.service_type,
                    "total_amount": order.total_amount,
                    "estimated_ready_time": order.estimated_ready_time.isoformat(),
                    "estimated_delivery_time": order.estimated_delivery_time.isoformat() if order.estimated_delivery_time else None
                },
                "tracking_info": {
                    "order_id": order.id,
                    "status": "confirmed",
                    "message": "Order confirmed! Cook is preparing your meal.",
                    "tracking_code": order.tracking_code
                }
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.put("/orders/{order_id}/status", response_model=dict)
    async def update_order_status(
        order_id: str,
        status: str,
        message: Optional[str] = None,
        lat: Optional[float] = None,
        lng: Optional[float] = None,
        current_user_id: str = Depends(get_current_user_optional)
    ):
        """Update order status (cook or delivery person)"""
        try:
            update_data = {"message": message or f"Order status updated to {status}"}
            
            if lat and lng:
                update_data["location"] = {"lat": lat, "lng": lng}
            
            result = await eats_service.update_order_status(order_id, status, update_data)
            
            # Send real-time update to eater
            order = await eats_service.db.active_orders.find_one({"id": order_id}, {"_id": 0})
            if order:
                await manager.send_to_user(order["eater_id"], {
                    "type": "order_update",
                    "order_id": order_id,
                    "status": status,
                    "message": update_data["message"],
                    "location": update_data.get("location"),
                    "timestamp": datetime.utcnow().isoformat()
                })
            
            return result
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.get("/orders/{order_id}/tracking", response_model=dict)
    async def get_order_tracking(order_id: str):
        """Get real-time order tracking information"""
        try:
            tracking_info = await eats_service.get_order_tracking(order_id)
            return {
                "success": True,
                "tracking": tracking_info
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.get("/orders/my-orders", response_model=List[dict])
    async def get_my_orders(
        status: Optional[str] = None,
        current_user_id: str = Depends(get_current_user_optional)
    ):
        """Get user's orders (as eater or cook)"""
        try:
            query = {"$or": [{"eater_id": current_user_id}, {"cook_id": current_user_id}]}
            
            if status:
                query["current_status"] = status
            
            orders = await eats_service.db.active_orders.find(query, {"_id": 0}).to_list(length=50)
            
            # Add role indicator
            for order in orders:
                order["user_role"] = "eater" if order["eater_id"] == current_user_id else "cook"
            
            return orders
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    # PROFILE MANAGEMENT
    
    @router.post("/profiles/cook", response_model=dict)
    async def create_cook_profile(
        profile_data: dict,
        current_user_id: str = Depends(get_current_user_optional)
    ):
        """Create or update cook profile for Lambalia Eats"""
        try:
            if not current_user_id:
                current_user_id = f"temp_cook_{str(uuid.uuid4())[:8]}"
            
            profile = await eats_service.create_cook_profile(profile_data, current_user_id)
            
            return {
                "success": True,
                "profile_id": profile.id,
                "message": "Cook profile created successfully!",
                "specialties": profile.specialties,
                "service_types": profile.available_service_types,
                "delivery_radius": profile.max_delivery_radius_km
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.post("/profiles/eater", response_model=dict)
    async def create_eater_profile(
        profile_data: dict,
        current_user_id: str = Depends(get_current_user_optional)
    ):
        """Create or update eater profile for Lambalia Eats"""
        try:
            profile = await eats_service.create_eater_profile(profile_data, current_user_id)
            
            return {
                "success": True,
                "profile_id": profile.id,
                "message": "Eater profile created successfully!",
                "favorite_cuisines": profile.favorite_cuisines,
                "dietary_restrictions": profile.dietary_restrictions
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    # PLATFORM STATISTICS
    
    @router.get("/stats", response_model=dict)
    async def get_platform_stats():
        """Get real-time platform statistics"""
        try:
            stats = await eats_service.get_platform_stats()
            return {
                "success": True,
                "stats": stats,
                "message": "Lambalia Eats - Connecting hungry eaters with talented home cooks!"
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    # SEARCH & DISCOVERY
    
    @router.get("/search", response_model=dict)
    async def search_food(
        query: str,
        lat: float,
        lng: float,
        search_type: str = "both",  # "offers", "requests", "both"
        radius_km: float = 20
    ):
        """Search for food offers or requests"""
        try:
            location = {"lat": lat, "lng": lng}
            results = {"offers": [], "requests": []}
            
            if search_type in ["offers", "both"]:
                offers = await eats_service.get_nearby_offers(location, radius_km)
                # Filter by search query
                offers = [o for o in offers if query.lower() in o["dish_name"].lower() or 
                         query.lower() in o["description"].lower()]
                results["offers"] = offers
            
            if search_type in ["requests", "both"]:
                requests = await eats_service.get_active_requests(location, radius_km)
                # Filter by search query
                requests = [r for r in requests if query.lower() in r["dish_name"].lower() or 
                           query.lower() in r["description"].lower()]
                results["requests"] = requests
            
            return {
                "success": True,
                "query": query,
                "results": results,
                "total_found": len(results["offers"]) + len(results["requests"])
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    # WEBSOCKET FOR REAL-TIME UPDATES
    
    @router.websocket("/ws/{user_id}")
    async def websocket_endpoint(websocket: WebSocket, user_id: str):
        """WebSocket endpoint for real-time updates"""
        connection_id = await manager.connect(websocket, user_id)
        
        try:
            # Send welcome message
            await websocket.send_text(json.dumps({
                "type": "connected",
                "message": "Connected to Lambalia Eats real-time updates",
                "user_id": user_id,
                "connection_id": connection_id
            }))
            
            while True:
                # Keep connection alive and handle incoming messages
                data = await websocket.receive_text()
                message = json.loads(data)
                
                # Handle different message types
                if message.get("type") == "ping":
                    await websocket.send_text(json.dumps({"type": "pong"}))
                elif message.get("type") == "location_update":
                    # Update user location for delivery tracking
                    # TODO: Update location in database
                    pass
                
        except WebSocketDisconnect:
            manager.disconnect(connection_id, user_id)
    
    # MOCK DATA ENDPOINTS (for standalone app demonstration)
    
    @router.get("/demo/sample-offers", response_model=List[dict])
    async def get_sample_offers():
        """Get sample food offers for demo purposes"""
        sample_offers = [
            {
                "id": str(uuid.uuid4()),
                "dish_name": "Homemade Chicken Biryani",
                "cuisine_type": "indian",
                "description": "Authentic Hyderabadi-style biryani with tender chicken and aromatic basmati rice",
                "price_per_serving": 12.99,
                "cook_name": "Priya's Kitchen",
                "cook_rating": 4.8,
                "ready_at": (datetime.utcnow().replace(minute=0, second=0) + timedelta(hours=1)).isoformat(),
                "available_service_types": ["pickup", "delivery", "dine_in"],
                "distance_km": 2.3,
                "delivery_fee": 3.99,
                "quantity_remaining": 4,
                "food_photos": ["/api/demo/biryani1.jpg"]
            },
            {
                "id": str(uuid.uuid4()),
                "dish_name": "Fresh Pasta Carbonara",
                "cuisine_type": "italian",
                "description": "Creamy carbonara with pancetta, fresh eggs, and aged parmesan",
                "price_per_serving": 14.50,
                "cook_name": "Mama Rosa's",
                "cook_rating": 4.9,
                "ready_at": (datetime.utcnow().replace(minute=30, second=0) + timedelta(minutes=45)).isoformat(),
                "available_service_types": ["pickup", "delivery"],
                "distance_km": 1.8,
                "delivery_fee": 2.99,
                "quantity_remaining": 2,
                "food_photos": ["/api/demo/carbonara1.jpg"]
            },
            {
                "id": str(uuid.uuid4()),
                "dish_name": "Korean BBQ Bulgogi Bowl",
                "cuisine_type": "korean",
                "description": "Marinated beef bulgogi with steamed rice, kimchi, and fresh vegetables",
                "price_per_serving": 13.99,
                "cook_name": "Seoul Kitchen",
                "cook_rating": 4.7,
                "ready_at": (datetime.utcnow().replace(minute=0, second=0) + timedelta(minutes=30)).isoformat(),
                "available_service_types": ["pickup", "delivery", "dine_in"],
                "distance_km": 3.1,
                "delivery_fee": 4.99,
                "quantity_remaining": 6,
                "food_photos": ["/api/demo/bulgogi1.jpg"]
            }
        ]
        
        return sample_offers
    
    @router.get("/demo/sample-requests", response_model=List[dict])
    async def get_sample_requests():
        """Get sample food requests for demo purposes"""
        sample_requests = [
            {
                "id": str(uuid.uuid4()),
                "dish_name": "Authentic Mexican Tacos",
                "cuisine_type": "mexican",
                "description": "Looking for authentic street-style tacos with fresh tortillas",
                "max_price": 15.00,
                "preferred_service_types": ["pickup", "delivery"],
                "distance_km": 1.5,
                "time_until_expires": 180,  # 3 hours
                "dietary_restrictions": [],
                "eater_name": "Food Lover"
            },
            {
                "id": str(uuid.uuid4()),
                "dish_name": "Vegan Buddha Bowl",
                "cuisine_type": "healthy",
                "description": "Nutritious vegan bowl with quinoa, fresh vegetables, and tahini dressing",
                "max_price": 12.00,
                "preferred_service_types": ["pickup"],
                "distance_km": 2.8,
                "time_until_expires": 120,  # 2 hours
                "dietary_restrictions": ["vegan", "gluten_free"],
                "eater_name": "Health Enthusiast"
            }
        ]
        
        return sample_requests
    
    return router