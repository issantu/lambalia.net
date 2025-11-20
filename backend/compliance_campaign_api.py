"""
Compliance and Campaign API Endpoints
User types, state compliance, document verification, campaigns, and promo codes
"""
from fastapi import APIRouter, HTTPException, Depends, File, UploadFile, Form
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List, Optional, Dict, Any, Callable
from datetime import datetime, timedelta
import uuid
import string
import random
import os
from pathlib import Path

from user_types_models import (
    UserType, StateCategory, UserTypeProfile, UserTypeChangeRequest,
    UserTypeResponse, UniversalDisclaimer
)
from compliance_models import (
    ChefTier, ComplianceStatus, DocumentType as ComplianceDocumentType,
    ChefCompliance, ComplianceDocument, ChefComplianceRequest,
    ChefComplianceResponse, ChefDashboardStats, AdminReviewQueue
)
from campaign_models import (
    CampaignType, CampaignStatus, PromoCodeStatus, Campaign, PromoCode,
    PromoCodeRedemption, CampaignRequest, CampaignResponse, PromoCodeResponse,
    PromoCodeValidationRequest, PromoCodeValidationResponse, CampaignStatsResponse
)
from state_compliance_service import state_compliance_service
from remaining_states_data import REMAINING_STATES


def create_compliance_campaign_router(
    db: AsyncIOMotorDatabase,
    get_current_user: Callable,
    get_current_user_optional: Callable = None
):
    """Create router for compliance and campaign endpoints"""
    
    router = APIRouter()
    
    # ==================== STATE COMPLIANCE ENDPOINTS ====================
    
    @router.get("/compliance/states")
    async def get_all_states():
        """Get list of all 50 states with categories"""
        states = state_compliance_service.get_all_states()
        
        # Add remaining states data
        for state_code, state_data in REMAINING_STATES.items():
            if not any(s['code'] == state_code for s in states):
                states.append({
                    "code": state_code,
                    "name": state_data["state_name"],
                    "category": state_data["category"]
                })
        
        return {
            "states": sorted(states, key=lambda x: x['name']),
            "categories": {
                "food_freedom": "Minimal regulation - No permits needed",
                "permissive": "Cottage food friendly - Easy permits",
                "moderate": "Permits required - Reasonable requirements",
                "restrictive": "Commercial kitchen required"
            }
        }
    
    @router.get("/compliance/states/{state_code}")
    async def get_state_requirements(state_code: str, user_type: str = "home_chef"):
        """Get requirements for specific state and user type"""
        
        # Get from main service
        state_info = state_compliance_service.get_state_info(state_code.upper())
        
        # If not found, check remaining states
        if not state_info:
            state_info = REMAINING_STATES.get(state_code.upper())
        
        if not state_info:
            raise HTTPException(status_code=404, detail="State not found")
        
        requirements = state_compliance_service.get_requirements_for_user_type(
            state_code.upper(),
            UserType(user_type)
        )
        
        return {
            "state_code": state_code.upper(),
            "state_name": state_info.get("state_name"),
            "category": state_info.get("category"),
            "user_type": user_type,
            "requirements": requirements,
            "is_food_freedom": state_compliance_service.is_food_freedom_state(state_code.upper())
        }
    
    @router.get("/compliance/disclaimer")
    async def get_universal_disclaimer():
        """Get universal platform disclaimer"""
        disclaimer = UniversalDisclaimer()
        return disclaimer.dict()
    
    # ==================== USER TYPE ENDPOINTS ====================
    
    @router.get("/user/types")
    async def get_my_user_types(current_user_id: str = Depends(get_current_user)):
        """Get current user's types and compliance status"""
        
        profile = await db.user_type_profiles.find_one({"user_id": current_user_id})
        if not profile:
            raise HTTPException(status_code=404, detail="User type profile not found")
        
        # Get requirements for each type
        requirements = {}
        for user_type in profile['user_types']:
            req = state_compliance_service.get_requirements_for_user_type(
                profile['state_code'],
                UserType(user_type)
            )
            requirements[user_type] = req.get('requirements', {}).get('permits', [])
        
        return UserTypeResponse(
            user_id=profile['user_id'],
            user_types=profile['user_types'],
            primary_type=profile['primary_type'],
            state_code=profile['state_code'],
            state_name=profile['state_name'],
            state_category=profile['state_category'],
            can_sell_packaged_foods=profile.get('can_sell_packaged_foods', False),
            can_serve_meals=profile.get('can_serve_meals', False),
            can_create_content=profile.get('can_create_content', True),
            can_review=profile.get('can_review', True),
            requirements=requirements,
            compliance_status=profile.get('compliance_status', {}),
            warnings=[]
        )
    
    @router.post("/user/types/change")
    async def change_user_types(
        request: UserTypeChangeRequest,
        current_user_id: str = Depends(get_current_user)
    ):
        """Add or remove user types"""
        
        profile = await db.user_type_profiles.find_one({"user_id": current_user_id})
        if not profile:
            raise HTTPException(status_code=404, detail="User type profile not found")
        
        current_types = set(profile['user_types'])
        
        # Add new types
        for user_type in request.add_types:
            current_types.add(user_type.value)
        
        # Remove types
        for user_type in request.remove_types:
            current_types.discard(user_type.value)
        
        # Update capabilities
        updated_profile = {
            "user_types": list(current_types),
            "primary_type": request.new_primary_type.value if request.new_primary_type else profile['primary_type'],
            "can_sell_packaged_foods": "home_chef" in current_types,
            "can_serve_meals": "home_restaurant" in current_types,
            "can_create_content": "recipe_creator" in current_types,
            "can_review": "food_reviewer" in current_types or "food_enthusiast" in current_types,
            "updated_at": datetime.utcnow()
        }
        
        await db.user_type_profiles.update_one(
            {"user_id": current_user_id},
            {"$set": updated_profile}
        )
        
        # If adding home_chef or home_restaurant, create compliance profile
        if ("home_chef" in request.add_types or "home_restaurant" in request.add_types):
            existing_compliance = await db.chef_compliance.find_one({"user_id": current_user_id})
            if not existing_compliance:
                state_info = state_compliance_service.get_state_info(profile['state_code'])
                chef_compliance = ChefCompliance(
                    chef_id=current_user_id,
                    user_id=current_user_id,
                    state_code=profile['state_code'],
                    state_name=state_info.get('state_name', profile['state_code']),
                    zip_code=profile.get('zip_code', ''),
                    tier=ChefTier.PENDING,
                    compliance_status=ComplianceStatus.PENDING_REVIEW
                )
                await db.chef_compliance.insert_one(chef_compliance.dict())
        
        return {
            "success": True,
            "message": "User types updated successfully",
            "user_types": list(current_types)
        }
    
    # ==================== CHEF COMPLIANCE ENDPOINTS ====================
    
    @router.get("/chef/compliance")
    async def get_chef_compliance(current_user_id: str = Depends(get_current_user)):
        """Get chef compliance profile"""
        
        compliance = await db.chef_compliance.find_one({"user_id": current_user_id})
        if not compliance:
            raise HTTPException(status_code=404, detail="Chef compliance profile not found")
        
        # Get uploaded documents
        documents = await db.compliance_documents.find({"user_id": current_user_id}).to_list(None)
        
        documents_required = []
        documents_uploaded = []
        documents_verified = []
        
        # Determine required documents based on state
        state_reqs = state_compliance_service.get_requirements_for_user_type(
            compliance['state_code'],
            UserType.HOME_CHEF
        )
        
        if state_reqs.get('requirements', {}).get('permits'):
            documents_required.extend(['cottage_permit', 'food_handler_cert'])
        
        for doc in documents:
            documents_uploaded.append(doc['document_type'])
            if doc.get('verified'):
                documents_verified.append(doc['document_type'])
        
        # Calculate warnings
        warnings = []
        expiring_soon = []
        if compliance.get('next_expiration_date'):
            days_until_expiry = (compliance['next_expiration_date'] - datetime.utcnow().date()).days
            if days_until_expiry < 30:
                warnings.append(f"Documents expiring in {days_until_expiry} days")
        
        badges = []
        if compliance['tier'] == ChefTier.FULLY_CERTIFIED:
            badges.extend(["Certified Chef", "Insured", "Verified"])
        elif compliance['tier'] == ChefTier.CERTIFIED_NO_INSURANCE:
            badges.extend(["Certified Chef"])
        
        state_info = state_compliance_service.get_state_info(compliance['state_code'])
        sales_limit = state_info.get('sales_cap') if state_info else None
        sales_remaining = None
        if sales_limit:
            sales_remaining = sales_limit - compliance.get('annual_sales', 0)
        
        return ChefComplianceResponse(
            chef_id=compliance['chef_id'],
            user_id=compliance['user_id'],
            state_code=compliance['state_code'],
            state_name=compliance['state_name'],
            tier=compliance['tier'],
            daily_order_limit=compliance.get('daily_order_limit'),
            compliance_status=compliance['compliance_status'],
            badges=badges,
            documents_required=documents_required,
            documents_uploaded=documents_uploaded,
            documents_verified=documents_verified,
            annual_sales=compliance.get('annual_sales', 0),
            sales_limit=sales_limit,
            sales_remaining=sales_remaining,
            expiring_soon=expiring_soon,
            warnings=warnings,
            created_at=compliance['created_at'],
            updated_at=compliance['updated_at']
        )
    
    @router.post("/chef/compliance/documents/upload")
    async def upload_compliance_document(
        document_type: str = Form(...),
        document_number: Optional[str] = Form(None),
        issued_date: Optional[str] = Form(None),
        expiry_date: Optional[str] = Form(None),
        file: UploadFile = File(...),
        current_user_id: str = Depends(get_current_user)
    ):
        """Upload compliance document"""
        
        # Check file size (max 10MB)
        file_content = await file.read()
        if len(file_content) > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File too large (max 10MB)")
        
        # Create uploads directory if it doesn't exist
        upload_dir = Path("/app/uploads/compliance")
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate unique filename
        file_extension = Path(file.filename).suffix
        unique_filename = f"{current_user_id}_{document_type}_{uuid.uuid4()}{file_extension}"
        file_path = upload_dir / unique_filename
        
        # Save file
        with open(file_path, "wb") as f:
            f.write(file_content)
        
        # Create document record
        document = ComplianceDocument(
            chef_id=current_user_id,
            user_id=current_user_id,
            document_type=ComplianceDocumentType(document_type),
            filename=file.filename,
            file_path=str(file_path),
            file_size=len(file_content),
            content_type=file.content_type,
            document_number=document_number,
            issued_date=datetime.fromisoformat(issued_date).date() if issued_date else None,
            expiry_date=datetime.fromisoformat(expiry_date).date() if expiry_date else None,
            status="pending"
        )
        
        await db.compliance_documents.insert_one(document.dict())
        
        # Update chef compliance with document reference
        update_fields = {}
        if document_type == "food_handler_cert":
            update_fields['food_handler_cert_id'] = document.id
        elif document_type == "cottage_permit":
            update_fields['cottage_permit_id'] = document.id
        elif document_type == "insurance":
            update_fields['insurance_id'] = document.id
        
        if update_fields:
            await db.chef_compliance.update_one(
                {"user_id": current_user_id},
                {"$set": {**update_fields, "updated_at": datetime.utcnow()}}
            )
        
        return {
            "success": True,
            "message": "Document uploaded successfully",
            "document_id": document.id,
            "status": "pending_review"
        }
    
    # ==================== CAMPAIGN ENDPOINTS ====================
    
    @router.post("/campaigns", response_model=CampaignResponse)
    async def create_campaign(
        campaign_req: CampaignRequest,
        current_user_id: str = Depends(get_current_user)
    ):
        """Create new promotional campaign (admin only)"""
        
        # Check if user is admin
        user = await db.users.find_one({"id": current_user_id})
        if not user or not user.get('is_admin'):
            raise HTTPException(status_code=403, detail="Admin access required")
        
        campaign = Campaign(
            campaign_name=campaign_req.campaign_name,
            campaign_type=campaign_req.campaign_type,
            description=campaign_req.description,
            discount_type=campaign_req.discount_type,
            discount_value=campaign_req.discount_value,
            total_quota=campaign_req.total_quota,
            codes_remaining=campaign_req.total_quota,
            target_cities=campaign_req.target_cities,
            target_states=campaign_req.target_states,
            valid_zip_codes=campaign_req.valid_zip_codes,
            start_date=campaign_req.start_date,
            end_date=campaign_req.end_date,
            participating_chef_ids=campaign_req.participating_chef_ids,
            all_chefs_eligible=campaign_req.all_chefs_eligible,
            minimum_order_amount=campaign_req.minimum_order_amount,
            new_users_only=campaign_req.new_users_only,
            status=CampaignStatus.ACTIVE,
            created_by=current_user_id
        )
        
        await db.campaigns.insert_one(campaign.dict())
        
        return CampaignResponse(
            id=campaign.id,
            campaign_name=campaign.campaign_name,
            campaign_type=campaign.campaign_type,
            description=campaign.description,
            discount_type=campaign.discount_type,
            discount_value=campaign.discount_value,
            total_quota=campaign.total_quota,
            codes_generated=0,
            codes_redeemed=0,
            codes_remaining=campaign.total_quota,
            status=campaign.status,
            start_date=campaign.start_date,
            end_date=campaign.end_date,
            valid_zip_codes=campaign.valid_zip_codes,
            conversion_rate=0.0,
            total_orders=0,
            total_revenue=0.0,
            created_at=campaign.created_at
        )
    
    @router.post("/campaigns/{campaign_id}/generate-code")
    async def generate_promo_code(
        campaign_id: str,
        current_user_id: str = Depends(get_current_user)
    ):
        """Generate promo code for user (auto-called on registration)"""
        
        campaign = await db.campaigns.find_one({"id": campaign_id})
        if not campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")
        
        # Check if campaign is active
        if campaign['status'] != CampaignStatus.ACTIVE:
            raise HTTPException(status_code=400, detail="Campaign is not active")
        
        # Check if user already has a code for this campaign
        existing_code = await db.promo_codes.find_one({
            "campaign_id": campaign_id,
            "user_id": current_user_id
        })
        if existing_code:
            return {
                "success": True,
                "code": existing_code['code'],
                "message": "Code already generated for this campaign"
            }
        
        # Check if quota is available
        if campaign['codes_generated'] >= campaign['total_quota']:
            raise HTTPException(status_code=400, detail="Campaign quota reached")
        
        # Get user profile for zip code validation
        user_profile = await db.user_type_profiles.find_one({"user_id": current_user_id})
        user_zip = user_profile.get('zip_code', '') if user_profile else ''
        
        # Validate zip code
        if campaign.get('valid_zip_codes') and user_zip not in campaign['valid_zip_codes']:
            raise HTTPException(status_code=400, detail="Not eligible for this campaign (location)")
        
        # Generate unique code: LMB150-XXXXXX
        code_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        code = f"LMB{campaign['total_quota']}-{code_suffix}"
        
        # Create promo code
        promo_code = PromoCode(
            code=code,
            campaign_id=campaign_id,
            user_id=current_user_id,
            user_email=user_profile.get('email') if user_profile else None,
            user_zip_code=user_zip,
            expires_at=campaign['end_date']
        )
        
        await db.promo_codes.insert_one(promo_code.dict())
        
        # Update campaign stats
        await db.campaigns.update_one(
            {"id": campaign_id},
            {
                "$inc": {"codes_generated": 1},
                "$set": {"codes_remaining": campaign['total_quota'] - campaign['codes_generated'] - 1}
            }
        )
        
        return {
            "success": True,
            "code": code,
            "campaign_name": campaign['campaign_name'],
            "expires_at": campaign['end_date'],
            "message": "Promo code generated successfully"
        }
    
    @router.get("/user/promo-codes")
    async def get_my_promo_codes(current_user_id: str = Depends(get_current_user)):
        """Get user's promo codes"""
        
        codes = await db.promo_codes.find({"user_id": current_user_id}).to_list(None)
        
        result = []
        for code_data in codes:
            campaign = await db.campaigns.find_one({"id": code_data['campaign_id']})
            if campaign:
                discount_desc = "Free meal" if campaign['discount_value'] == 0 else f"${campaign['discount_value']} off"
                
                result.append(PromoCodeResponse(
                    code=code_data['code'],
                    campaign_name=campaign['campaign_name'],
                    discount_description=discount_desc,
                    valid_until=code_data['expires_at'],
                    status=PromoCodeStatus(code_data['status']),
                    redemptions_remaining=code_data['max_redemptions'] - code_data['redemptions_count'],
                    instructions="Present this code at checkout to redeem your discount.",
                    participating_chefs=[]
                ))
        
        return {"promo_codes": result}
    
    @router.post("/checkout/validate-promo-code", response_model=PromoCodeValidationResponse)
    async def validate_promo_code(
        request: PromoCodeValidationRequest,
        current_user_id: str = Depends(get_current_user)
    ):
        """Validate promo code at checkout"""
        
        # Find promo code
        promo_code = await db.promo_codes.find_one({"code": request.code})
        if not promo_code:
            return PromoCodeValidationResponse(
                valid=False,
                code=request.code,
                discount_amount=0,
                final_amount=request.cart_total,
                message="Invalid promo code",
                errors=["Code not found"]
            )
        
        # Check if code belongs to user
        if promo_code['user_id'] != current_user_id:
            return PromoCodeValidationResponse(
                valid=False,
                code=request.code,
                discount_amount=0,
                final_amount=request.cart_total,
                message="Invalid promo code",
                errors=["Code does not belong to you"]
            )
        
        # Check if code is already redeemed
        if promo_code['status'] != PromoCodeStatus.ACTIVE:
            return PromoCodeValidationResponse(
                valid=False,
                code=request.code,
                discount_amount=0,
                final_amount=request.cart_total,
                message="Code already used",
                errors=["Code has already been redeemed"]
            )
        
        # Check if code is expired
        if promo_code.get('expires_at') and promo_code['expires_at'] < datetime.utcnow():
            return PromoCodeValidationResponse(
                valid=False,
                code=request.code,
                discount_amount=0,
                final_amount=request.cart_total,
                message="Code expired",
                errors=["Code has expired"]
            )
        
        # Get campaign
        campaign = await db.campaigns.find_one({"id": promo_code['campaign_id']})
        if not campaign:
            return PromoCodeValidationResponse(
                valid=False,
                code=request.code,
                discount_amount=0,
                final_amount=request.cart_total,
                message="Campaign not found",
                errors=["Associated campaign not found"]
            )
        
        # Check zip code
        if campaign.get('valid_zip_codes') and request.user_zip_code not in campaign['valid_zip_codes']:
            return PromoCodeValidationResponse(
                valid=False,
                code=request.code,
                discount_amount=0,
                final_amount=request.cart_total,
                message="Not valid in your location",
                errors=["Code not valid for your zip code"]
            )
        
        # Calculate discount
        if campaign['discount_type'] == "free":
            discount_amount = request.cart_total
        elif campaign['discount_type'] == "fixed_amount":
            discount_amount = min(campaign['discount_value'], request.cart_total)
        elif campaign['discount_type'] == "percentage":
            discount_amount = (campaign['discount_value'] / 100) * request.cart_total
        else:
            discount_amount = 0
        
        # Apply maximum discount if set
        if campaign.get('maximum_discount_amount'):
            discount_amount = min(discount_amount, campaign['maximum_discount_amount'])
        
        final_amount = max(0, request.cart_total - discount_amount)
        
        return PromoCodeValidationResponse(
            valid=True,
            code=request.code,
            discount_amount=discount_amount,
            final_amount=final_amount,
            message=f"Code applied successfully! You save ${discount_amount:.2f}",
            errors=[]
        )
    
    @router.get("/campaigns/{campaign_id}/stats", response_model=CampaignStatsResponse)
    async def get_campaign_stats(campaign_id: str):
        """Get real-time campaign statistics"""
        
        campaign = await db.campaigns.find_one({"id": campaign_id})
        if not campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")
        
        # Calculate days remaining
        days_remaining = (campaign['end_date'] - datetime.utcnow()).days
        
        # Calculate progress
        progress_percentage = (campaign['codes_generated'] / campaign['total_quota']) * 100 if campaign['total_quota'] > 0 else 0
        
        # Calculate redemption rate
        redemption_rate = (campaign['codes_redeemed'] / campaign['codes_generated']) * 100 if campaign['codes_generated'] > 0 else 0
        
        return CampaignStatsResponse(
            campaign_id=campaign['id'],
            campaign_name=campaign['campaign_name'],
            status=CampaignStatus(campaign['status']),
            total_quota=campaign['total_quota'],
            codes_generated=campaign['codes_generated'],
            codes_redeemed=campaign['codes_redeemed'],
            codes_remaining=campaign['codes_remaining'],
            progress_percentage=progress_percentage,
            days_remaining=max(0, days_remaining),
            start_date=campaign['start_date'],
            end_date=campaign['end_date'],
            redemption_rate=redemption_rate,
            average_order_value=campaign.get('average_order_value', 0),
            total_revenue=campaign.get('total_revenue', 0)
        )
    
    return router
