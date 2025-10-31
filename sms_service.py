"""
SMS Service Module for Kagan Collection Management
Handles SMS sending via various providers and automated campaigns
"""
from database import db
from datetime import datetime, timedelta

class SMSService:
    """SMS service handler"""
    def __init__(self):
        self.provider = self.get_setting('sms_provider', 'none')
        self.api_key = self.get_setting('sms_api_key', '')
        self.api_secret = self.get_setting('sms_api_secret', '')
        self.sender_number = self.get_setting('sms_sender_number', '')
    
    def get_setting(self, key, default=''):
        """Get setting value from database"""
        try:
            result = db.fetchone("SELECT value FROM settings WHERE key = ?", (key,))
            return result['value'] if result else default
        except:
            return default
    
    def is_configured(self):
        """Check if SMS service is properly configured"""
        return (self.provider != 'none' and 
                self.provider != '' and 
                self.api_key != '' and 
                self.api_key is not None)
    
    def send_sms(self, phone_number, message, sms_type='manual', customer_id=None):
        """Send SMS via configured provider - requires proper API configuration"""
        # Check if SMS is properly configured
        if not self.is_configured():
            error_message = 'SMS provider not configured. Please configure SMS API settings in Settings > SMS Configuration before sending SMS.'
            self.log_sms(customer_id, phone_number, message, sms_type, 'not_configured', error_message)
            return {'success': False, 'message': error_message}
        
        # Validate that API key is set
        if not self.api_key or self.api_key == '':
            error_message = 'SMS API Key is not configured. Please set your API Key in Settings > SMS Configuration.'
            self.log_sms(customer_id, phone_number, message, sms_type, 'no_api_key', error_message)
            return {'success': False, 'message': error_message}
        
        try:
            # Send via appropriate provider
            if self.provider == 'twilio':
                result = self._send_via_twilio(phone_number, message)
            elif self.provider == 'kavenegar':
                result = self._send_via_kavenegar(phone_number, message)
            elif self.provider == 'ghasedak':
                result = self._send_via_ghasedak(phone_number, message)
            else:
                result = {'success': False, 'message': 'Unknown provider'}
            
            # Log SMS
            status = 'sent' if result['success'] else 'failed'
            error_msg = result.get('message', '') if not result['success'] else None
            self.log_sms(customer_id, phone_number, message, sms_type, status, error_msg)
            
            return result
        except Exception as e:
            self.log_sms(customer_id, phone_number, message, sms_type, 'error', str(e))
            return {'success': False, 'message': str(e)}
    
    def _send_via_twilio(self, phone_number, message):
        """Send SMS via Twilio"""
        try:
            # Import Twilio client
            # from twilio.rest import Client
            # client = Client(self.api_key, self.api_secret)
            # message = client.messages.create(
            #     body=message,
            #     from_='+1234567890',  # Your Twilio number
            #     to=phone_number
            # )
            # return {'success': True, 'sid': message.sid}
            
            # Placeholder - requires twilio package
            return {'success': False, 'message': 'Twilio integration not implemented'}
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def _send_via_kavenegar(self, phone_number, message):
        """Send SMS via Kavenegar (Iranian SMS provider)"""
        try:
            # Import Kavenegar API
            # from kavenegar import *
            # api = KavenegarAPI(self.api_key)
            # params = {
            #     'sender': '10008663',  # Your Kavenegar number
            #     'receptor': phone_number,
            #     'message': message
            # }
            # response = api.sms_send(params)
            # return {'success': True, 'messageid': response[0]['messageid']}
            
            # Placeholder - requires kavenegar package
            return {'success': False, 'message': 'Kavenegar integration not implemented'}
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def _send_via_ghasedak(self, phone_number, message):
        """Send SMS via Ghasedak (Iranian SMS provider)"""
        try:
            # Import Ghasedak API
            # import requests
            # url = "https://api.ghasedak.me/v2/sms/send/simple"
            # headers = {'apikey': self.api_key}
            # data = {
            #     'receptor': phone_number,
            #     'message': message
            # }
            # response = requests.post(url, headers=headers, json=data)
            # return {'success': response.status_code == 200}
            
            # Placeholder - requires requests package
            return {'success': False, 'message': 'Ghasedak integration not implemented'}
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def log_sms(self, customer_id, phone_number, message, sms_type, status, error_message=None):
        """Log SMS in database"""
        db.execute(
            """INSERT INTO sms_history 
               (customer_id, phone_number, message, sms_type, status, sent_date, error_message)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (customer_id, phone_number, message, sms_type, status,
             datetime.now().strftime('%Y-%m-%d %H:%M:%S'), error_message)
        )
    
    def send_survey_sms(self, customer_id):
        """Send survey SMS manually (requires user action)"""
        customer = db.fetchone("SELECT * FROM customers WHERE id = ?", (customer_id,))
        if not customer:
            return {'success': False, 'message': 'Customer not found'}
        
        message = f"""سلام {customer['name']} عزیز،
از اینکه از خدمات ما استفاده کردید متشکریم.
لطفا نظر خود را در مورد کیفیت خدمات با ما در میان بگذارید.
امتیاز شما به ما کمک می‌کند تا خدمات بهتری ارائه دهیم.
مجموعه کاگان"""
        
        return self.send_sms(customer['phone'], message, 'survey', customer_id)
    
    def send_birthday_sms(self, customer_id):
        """Send birthday greeting SMS manually (requires user action)"""
        customer = db.fetchone("SELECT * FROM customers WHERE id = ?", (customer_id,))
        if not customer:
            return {'success': False, 'message': 'Customer not found'}
        
        message = f"""سلام {customer['name']} عزیز،
تولدت مبارک! 🎉
ما در مجموعه کاگان آرزوی سالی پر از شادی و موفقیت برای شما داریم.
هدیه ویژه تولد شما آماده است، منتظر دیدار شما هستیم.
مجموعه کاگان"""
        
        return self.send_sms(customer['phone'], message, 'birthday', customer_id)
    
    def send_promotional_sms(self, customer_id, promotion_text):
        """Send promotional SMS manually (requires user action)"""
        customer = db.fetchone("SELECT * FROM customers WHERE id = ?", (customer_id,))
        if not customer:
            return {'success': False, 'message': 'Customer not found'}
        
        message = f"""سلام {customer['name']} عزیز،
{promotion_text}
مجموعه کاگان"""
        
        return self.send_sms(customer['phone'], message, 'promotional', customer_id)
    
    def send_inactive_customer_sms(self, customer_id):
        """Send SMS to inactive customers manually (requires user action)"""
        customer = db.fetchone("SELECT * FROM customers WHERE id = ?", (customer_id,))
        if not customer:
            return {'success': False, 'message': 'Customer not found'}
        
        message = f"""سلام {customer['name']} عزیز،
مدتی است که شما را در مجموعه کاگان نداشتیم و دلتنگ شما هستیم.
برای بازگشت شما تخفیف ویژه‌ای در نظر گرفته‌ایم.
منتظر دیدار شما هستیم.
مجموعه کاگان"""
        
        return self.send_sms(customer['phone'], message, 'reactivation', customer_id)
    
    def get_sms_history(self, limit=100):
        """Get SMS history"""
        return db.fetchall(
            """SELECT sh.*, c.name as customer_name
               FROM sms_history sh
               LEFT JOIN customers c ON sh.customer_id = c.id
               ORDER BY sh.sent_date DESC
               LIMIT ?""",
            (limit,)
        )

# Global SMS service instance
sms_service = SMSService()
