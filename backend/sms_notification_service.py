# SMS Notification Service for Lambalia - Twilio Integration
import os
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime
from twilio.rest import Client
from twilio.base.exceptions import TwilioException
from dotenv import load_dotenv

load_dotenv()

class SMSNotificationService:
    """
    Comprehensive SMS notification service for user trust and engagement
    Handles registration, account changes, transactions, and post-service notifications
    """
    
    def __init__(self):
        self.account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        self.auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
        self.twilio_phone = os.environ.get('TWILIO_PHONE_NUMBER')
        self.helpdesk_number = os.environ.get('HELPDESK_PHONE', '+1-800-LAMBALIA')
        
        # Initialize Twilio client
        if self.account_sid and self.auth_token:
            self.client = Client(self.account_sid, self.auth_token)
            self.enabled = True
            logging.info("SMS notification service initialized successfully")
        else:
            self.client = None
            self.enabled = False
            logging.warning("SMS notification service disabled - Twilio credentials not found")
        
        # SMS templates
        self.templates = {
            'registration': """
🎉 Welcome to Lambalia!

Your account has been successfully created. You can now:
• Share traditional recipes
• Earn from cooking consultations  
• Join our global food community

If you did not create this account, contact our helpdesk at {helpdesk}.

Happy cooking! 👨‍🍳
            """.strip(),
            
            'account_change': """
🔔 Lambalia Account Alert

Your account information has been updated:
{change_details}

Time: {timestamp}

If you did not initiate this change, contact our helpdesk at {helpdesk} immediately.

Stay secure! 🔒
            """.strip(),
            
            'money_in': """
💰 Money Received - Lambalia

Amount: ${amount}
From: {transaction_type}
Reference: {reference}
New Balance: ${balance}

If you did not expect this transaction, contact our helpdesk at {helpdesk}.

Thank you for using Lambalia! 🍽️
            """.strip(),
            
            'money_out': """
💳 Payment Processed - Lambalia

Amount: ${amount}
To: {recipient}
Reference: {reference}
Remaining Balance: ${balance}

If you did not initiate this payment, contact our helpdesk at {helpdesk} immediately.

Transaction secure ✅
            """.strip(),
            
            'service_rating': """
⭐ Rate Your Experience - Lambalia

Hi {user_name}! How was your recent {service_type} experience?

Rate us: {rating_link}

💡 Show appreciation with a tip:
Reply with:
• A: $2 tip
• B: $5 tip  
• C: $10 tip
• D: Custom amount

Your feedback helps our community grow! 🌟
            """.strip()
        }
    
    async def send_registration_sms(self, phone_number: str, user_name: str) -> Dict[str, Any]:
        """Send welcome SMS after successful registration"""
        try:
            if not self.enabled:
                return {"success": False, "error": "SMS service disabled"}
            
            message = self.templates['registration'].format(
                helpdesk=self.helpdesk_number
            )
            
            result = await self._send_sms(phone_number, message)
            
            if result['success']:
                logging.info(f"Registration SMS sent to {phone_number} for user {user_name}")
            
            return result
            
        except Exception as e:
            logging.error(f"Failed to send registration SMS: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def send_account_change_sms(self, phone_number: str, change_details: str) -> Dict[str, Any]:
        """Send SMS notification for account changes"""
        try:
            if not self.enabled:
                return {"success": False, "error": "SMS service disabled"}
            
            message = self.templates['account_change'].format(
                change_details=change_details,
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"),
                helpdesk=self.helpdesk_number
            )
            
            result = await self._send_sms(phone_number, message)
            
            if result['success']:
                logging.info(f"Account change SMS sent to {phone_number}: {change_details}")
            
            return result
            
        except Exception as e:
            logging.error(f"Failed to send account change SMS: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def send_money_in_sms(self, phone_number: str, amount: float, 
                               transaction_type: str, reference: str, 
                               balance: float) -> Dict[str, Any]:
        """Send SMS notification for incoming money"""
        try:
            if not self.enabled:
                return {"success": False, "error": "SMS service disabled"}
            
            message = self.templates['money_in'].format(
                amount=f"{amount:.2f}",
                transaction_type=transaction_type,
                reference=reference,
                balance=f"{balance:.2f}",
                helpdesk=self.helpdesk_number
            )
            
            result = await self._send_sms(phone_number, message)
            
            if result['success']:
                logging.info(f"Money in SMS sent to {phone_number}: ${amount:.2f}")
            
            return result
            
        except Exception as e:
            logging.error(f"Failed to send money in SMS: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def send_money_out_sms(self, phone_number: str, amount: float, 
                                recipient: str, reference: str, 
                                balance: float) -> Dict[str, Any]:
        """Send SMS notification for outgoing money"""
        try:
            if not self.enabled:
                return {"success": False, "error": "SMS service disabled"}
            
            message = self.templates['money_out'].format(
                amount=f"{amount:.2f}",
                recipient=recipient,
                reference=reference,
                balance=f"{balance:.2f}",
                helpdesk=self.helpdesk_number
            )
            
            result = await self._send_sms(phone_number, message)
            
            if result['success']:
                logging.info(f"Money out SMS sent to {phone_number}: ${amount:.2f}")
            
            return result
            
        except Exception as e:
            logging.error(f"Failed to send money out SMS: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def send_service_rating_sms(self, phone_number: str, user_name: str, 
                                     service_type: str, rating_link: str) -> Dict[str, Any]:
        """Send post-service rating and tip request SMS"""
        try:
            if not self.enabled:
                return {"success": False, "error": "SMS service disabled"}
            
            message = self.templates['service_rating'].format(
                user_name=user_name,
                service_type=service_type,
                rating_link=rating_link
            )
            
            result = await self._send_sms(phone_number, message)
            
            if result['success']:
                logging.info(f"Service rating SMS sent to {phone_number} for {service_type}")
            
            return result
            
        except Exception as e:
            logging.error(f"Failed to send service rating SMS: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def _send_sms(self, phone_number: str, message: str) -> Dict[str, Any]:
        """Internal method to send SMS via Twilio"""
        try:
            if not self.client:
                return {"success": False, "error": "Twilio client not initialized"}
            
            # Ensure phone number is in E.164 format
            if not phone_number.startswith('+'):
                # Assume US number if no country code
                phone_number = f"+1{phone_number}"
            
            message_instance = self.client.messages.create(
                body=message,
                from_=self.twilio_phone,
                to=phone_number
            )
            
            return {
                "success": True,
                "message_sid": message_instance.sid,
                "status": message_instance.status,
                "phone_number": phone_number
            }
            
        except TwilioException as e:
            logging.error(f"Twilio error sending SMS to {phone_number}: {str(e)}")
            return {"success": False, "error": f"Twilio error: {str(e)}"}
        except Exception as e:
            logging.error(f"Unexpected error sending SMS to {phone_number}: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def format_phone_number(self, phone: str, default_country_code: str = "+1") -> str:
        """Format phone number to E.164 format"""
        # Remove all non-digit characters
        digits = ''.join(filter(str.isdigit, phone))
        
        # If it's a US number without country code, add +1
        if len(digits) == 10:
            return f"{default_country_code}{digits}"
        elif len(digits) == 11 and digits.startswith('1'):
            return f"+{digits}"
        else:
            # Assume it already has country code
            return f"+{digits}"
    
    def get_service_status(self) -> Dict[str, Any]:
        """Get SMS service status and configuration"""
        return {
            "enabled": self.enabled,
            "twilio_configured": bool(self.account_sid and self.auth_token),
            "phone_number": self.twilio_phone,
            "helpdesk_number": self.helpdesk_number,
            "templates_loaded": len(self.templates)
        }

# Global SMS service instance
sms_service = None

async def get_sms_service() -> SMSNotificationService:
    """Get or create SMS service instance"""
    global sms_service
    if sms_service is None:
        sms_service = SMSNotificationService()
    return sms_service