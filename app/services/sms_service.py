from typing import Optional
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class SMSService:
    """Service for sending SMS messages"""
    
    @staticmethod
    def send_otp(mobile: str, otp: str) -> bool:
        """
        Send OTP via SMS
        
        Args:
            mobile: Mobile number
            otp: OTP code
            
        Returns:
            bool: True if SMS sent successfully
        """
        try:
            # In development mode, just log the OTP
            if settings.DEBUG:
                logger.info(f"[DEV MODE] OTP for {mobile}: {otp}")
                print(f"\n{'='*50}")
                print(f"OTP for {mobile}: {otp}")
                print(f"{'='*50}\n")
                return True
            
            # Production: Use Twilio or other SMS service
            if settings.TWILIO_ACCOUNT_SID and settings.TWILIO_AUTH_TOKEN:
                from twilio.rest import Client
                
                client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                
                message = client.messages.create(
                    body=f"Your B2B Marketplace verification code is: {otp}. Valid for {settings.OTP_EXPIRY_MINUTES} minutes.",
                    from_=settings.TWILIO_PHONE_NUMBER,
                    to=mobile
                )
                
                logger.info(f"SMS sent to {mobile}: {message.sid}")
                return True
            else:
                logger.warning("Twilio credentials not configured. OTP not sent.")
                return False
                
        except Exception as e:
            logger.error(f"Failed to send SMS to {mobile}: {str(e)}")
            return False
    
    @staticmethod
    def send_welcome_sms(mobile: str, name: str) -> bool:
        """
        Send welcome SMS to new buyer
        
        Args:
            mobile: Mobile number
            name: Buyer name
            
        Returns:
            bool: True if SMS sent successfully
        """
        try:
            if settings.DEBUG:
                logger.info(f"[DEV MODE] Welcome SMS for {name} ({mobile})")
                return True
            
            if settings.TWILIO_ACCOUNT_SID and settings.TWILIO_AUTH_TOKEN:
                from twilio.rest import Client
                
                client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                
                message = client.messages.create(
                    body=f"Welcome to B2B Marketplace, {name}! Your account has been verified successfully.",
                    from_=settings.TWILIO_PHONE_NUMBER,
                    to=mobile
                )
                
                logger.info(f"Welcome SMS sent to {mobile}: {message.sid}")
                return True
            else:
                return False
                
        except Exception as e:
            logger.error(f"Failed to send welcome SMS to {mobile}: {str(e)}")
            return False
