# Payment Service with Stripe Integration
import stripe
import os
from typing import Dict, Optional
from datetime import datetime, timedelta
import json
import logging

# Set Stripe API key
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY', 'sk_test_...')  # Use test key for development

logger = logging.getLogger(__name__)

class PaymentService:
    def __init__(self):
        self.platform_commission_rate = 0.15  # 15% platform fee
        
    async def create_payment_intent(
        self, 
        booking_id: str,
        amount: float,
        currency: str = "usd",
        vendor_id: str = None
    ) -> Dict:
        """Create a Stripe Payment Intent for the booking"""
        try:
            # Calculate amounts
            total_amount_cents = int(amount * 100)  # Stripe uses cents
            platform_commission_cents = int(amount * self.platform_commission_rate * 100)
            vendor_payout_cents = total_amount_cents - platform_commission_cents
            
            # Create Payment Intent with automatic payment methods
            intent = stripe.PaymentIntent.create(
                amount=total_amount_cents,
                currency=currency,
                automatic_payment_methods={
                    'enabled': True,
                },
                metadata={
                    'booking_id': booking_id,
                    'vendor_id': vendor_id or '',
                    'platform_commission': platform_commission_cents,
                    'vendor_payout': vendor_payout_cents,
                    'type': 'home_restaurant_booking'
                },
                # Hold funds until booking completion (optional)
                capture_method='automatic',  # Can be 'manual' for escrow
                description=f'Lambalia Home Restaurant Booking #{booking_id[:8]}'
            )
            
            return {
                'client_secret': intent.client_secret,
                'payment_intent_id': intent.id,
                'amount': amount,
                'platform_commission': amount * self.platform_commission_rate,
                'vendor_payout': amount * (1 - self.platform_commission_rate),
                'status': 'requires_payment_method'
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error creating payment intent: {str(e)}")
            raise Exception(f"Payment processing error: {str(e)}")
        except Exception as e:
            logger.error(f"Error creating payment intent: {str(e)}")
            raise Exception(f"Payment system error: {str(e)}")
    
    async def confirm_payment(self, payment_intent_id: str) -> Dict:
        """Confirm a payment intent"""
        try:
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            
            if intent.status == 'succeeded':
                return {
                    'status': 'succeeded',
                    'amount': intent.amount / 100,
                    'booking_id': intent.metadata.get('booking_id'),
                    'vendor_id': intent.metadata.get('vendor_id'),
                    'platform_commission': int(intent.metadata.get('platform_commission', 0)) / 100,
                    'vendor_payout': int(intent.metadata.get('vendor_payout', 0)) / 100
                }
            
            return {
                'status': intent.status,
                'amount': intent.amount / 100,
                'booking_id': intent.metadata.get('booking_id')
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error confirming payment: {str(e)}")
            raise Exception(f"Payment confirmation error: {str(e)}")
    
    async def create_refund(
        self, 
        payment_intent_id: str, 
        amount: Optional[float] = None,
        reason: str = "requested_by_customer"
    ) -> Dict:
        """Create a refund for a payment"""
        try:
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            
            if intent.charges.data:
                charge_id = intent.charges.data[0].id
                
                refund_data = {
                    'charge': charge_id,
                    'reason': reason
                }
                
                if amount:
                    refund_data['amount'] = int(amount * 100)
                
                refund = stripe.Refund.create(**refund_data)
                
                return {
                    'refund_id': refund.id,
                    'amount': refund.amount / 100,
                    'status': refund.status,
                    'reason': refund.reason
                }
            
            raise Exception("No charges found for this payment")
            
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error creating refund: {str(e)}")
            raise Exception(f"Refund processing error: {str(e)}")
    
    async def create_vendor_account(self, vendor_info: Dict) -> Dict:
        """Create a Stripe Express account for vendor payouts"""
        try:
            account = stripe.Account.create(
                type='express',
                country=vendor_info.get('country', 'US'),
                email=vendor_info.get('email'),
                capabilities={
                    'card_payments': {'requested': True},
                    'transfers': {'requested': True},
                },
                business_type='individual',
                individual={
                    'first_name': vendor_info.get('first_name'),
                    'last_name': vendor_info.get('last_name'),
                    'email': vendor_info.get('email'),
                    'phone': vendor_info.get('phone'),
                    'address': {
                        'line1': vendor_info.get('address'),
                        'city': vendor_info.get('city'),
                        'state': vendor_info.get('state'),
                        'postal_code': vendor_info.get('postal_code'),
                        'country': vendor_info.get('country', 'US'),
                    }
                }
            )
            
            return {
                'account_id': account.id,
                'status': 'created',
                'onboarding_required': True
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error creating vendor account: {str(e)}")
            raise Exception(f"Vendor account creation error: {str(e)}")
    
    async def create_onboarding_link(self, account_id: str, return_url: str, refresh_url: str) -> Dict:
        """Create onboarding link for vendor Stripe account"""
        try:
            account_link = stripe.AccountLink.create(
                account=account_id,
                return_url=return_url,
                refresh_url=refresh_url,
                type='account_onboarding',
            )
            
            return {
                'onboarding_url': account_link.url,
                'expires_at': account_link.expires_at
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error creating onboarding link: {str(e)}")
            raise Exception(f"Onboarding link error: {str(e)}")
    
    async def transfer_to_vendor(
        self, 
        vendor_account_id: str, 
        amount: float, 
        booking_id: str
    ) -> Dict:
        """Transfer payment to vendor after booking completion"""
        try:
            transfer = stripe.Transfer.create(
                amount=int(amount * 100),
                currency='usd',
                destination=vendor_account_id,
                metadata={
                    'booking_id': booking_id,
                    'type': 'vendor_payout'
                }
            )
            
            return {
                'transfer_id': transfer.id,
                'amount': transfer.amount / 100,
                'status': 'transferred',
                'destination_account': vendor_account_id
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error transferring to vendor: {str(e)}")
            raise Exception(f"Vendor payout error: {str(e)}")
    
    async def get_account_status(self, account_id: str) -> Dict:
        """Get vendor account status and capabilities"""
        try:
            account = stripe.Account.retrieve(account_id)
            
            return {
                'account_id': account.id,
                'charges_enabled': account.charges_enabled,
                'payouts_enabled': account.payouts_enabled,
                'details_submitted': account.details_submitted,
                'requirements': account.requirements.currently_due if account.requirements else [],
                'verification_status': 'verified' if account.details_submitted else 'pending'
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error getting account status: {str(e)}")
            raise Exception(f"Account status error: {str(e)}")
    
    async def handle_webhook(self, payload: str, signature: str) -> Dict:
        """Handle Stripe webhooks for payment events"""
        webhook_secret = os.environ.get('STRIPE_WEBHOOK_SECRET')
        
        try:
            event = stripe.Webhook.construct_event(
                payload, signature, webhook_secret
            )
            
            # Handle different event types
            if event['type'] == 'payment_intent.succeeded':
                payment_intent = event['data']['object']
                booking_id = payment_intent['metadata'].get('booking_id')
                
                return {
                    'event_type': 'payment_succeeded',
                    'booking_id': booking_id,
                    'payment_intent_id': payment_intent['id'],
                    'amount': payment_intent['amount'] / 100
                }
            
            elif event['type'] == 'payment_intent.payment_failed':
                payment_intent = event['data']['object']
                booking_id = payment_intent['metadata'].get('booking_id')
                
                return {
                    'event_type': 'payment_failed',
                    'booking_id': booking_id,
                    'payment_intent_id': payment_intent['id'],
                    'error': payment_intent.get('last_payment_error', {}).get('message', 'Unknown error')
                }
            
            elif event['type'] == 'account.updated':
                account = event['data']['object']
                
                return {
                    'event_type': 'account_updated',
                    'account_id': account['id'],
                    'charges_enabled': account['charges_enabled'],
                    'payouts_enabled': account['payouts_enabled']
                }
            
            return {'event_type': event['type'], 'processed': True}
            
        except ValueError as e:
            logger.error(f"Invalid webhook payload: {str(e)}")
            raise Exception("Invalid webhook payload")
        except stripe.error.SignatureVerificationError as e:
            logger.error(f"Webhook signature verification failed: {str(e)}")
            raise Exception("Webhook signature verification failed")

# Pricing Engine
class PricingEngine:
    def __init__(self):
        self.base_multipliers = {
            'monday': 0.8,
            'tuesday': 0.8,
            'wednesday': 0.85,
            'thursday': 0.9,
            'friday': 1.2,
            'saturday': 1.3,
            'sunday': 1.1
        }
        
        self.demand_multipliers = {
            'low': 0.9,
            'medium': 1.0,
            'high': 1.15,
            'very_high': 1.3
        }
    
    def calculate_dynamic_price(
        self, 
        base_price: float, 
        booking_date: datetime,
        demand_level: str = 'medium',
        vendor_rating: float = 4.0,
        location_premium: float = 1.0
    ) -> Dict[str, float]:
        """Calculate dynamic pricing based on various factors"""
        
        day_of_week = booking_date.strftime('%A').lower()
        day_multiplier = self.base_multipliers.get(day_of_week, 1.0)
        demand_multiplier = self.demand_multipliers.get(demand_level, 1.0)
        
        # Rating bonus (higher rated vendors can charge more)
        rating_multiplier = 0.8 + (vendor_rating / 5.0) * 0.4  # 0.8 to 1.2 range
        
        # Calculate final price
        dynamic_price = base_price * day_multiplier * demand_multiplier * rating_multiplier * location_premium
        
        # Apply platform commission
        platform_commission = dynamic_price * 0.15
        vendor_payout = dynamic_price * 0.85
        
        return {
            'base_price': base_price,
            'dynamic_price': round(dynamic_price, 2),
            'day_multiplier': day_multiplier,
            'demand_multiplier': demand_multiplier,
            'rating_multiplier': rating_multiplier,
            'platform_commission': round(platform_commission, 2),
            'vendor_payout': round(vendor_payout, 2)
        }

# Initialize services
payment_service = PaymentService()
pricing_engine = PricingEngine()