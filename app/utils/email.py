import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config.settings import settings
import logging

logger = logging.getLogger(__name__)

async def send_otp_email_with_retry(email: str, otp: str, retries: int = 3, delay: int = 3000):
    """
    Send OTP email with retry logic

    Args:
        email: Recipient email address
        otp: The OTP code to send
        retries: Number of retry attempts (default: 3)
        delay: Delay between retries in milliseconds (default: 3000)
    """
    delay_seconds = delay / 1000  # Convert milliseconds to seconds

    for attempt in range(1, retries + 1):
        try:
            # Create message
            message = MIMEMultipart('alternative')
            message['Subject'] = 'Welcome to Convis Labs ! Verify Your Email'
            message['From'] = settings.email_user
            message['To'] = email

            # HTML body
            html_body = f"""
            <div style="font-family: Arial, sans-serif; color: #333;">
                <p>Dear User,</p>
                <p>Thank you for registering with Convis Labs. We are excited to have you on board and look forward to providing you with the best AI-driven solutions to enhance your experience.</p>
                <p>To complete your registration, please verify your email by entering the OTP provided below</p>
                <h3>Your OTP: <strong>{otp}</strong></h3>
                <p>If you didn't register, please ignore this email.</p>
                <p>Best regards,<br>Convis Labs Team</p>
            </div>
            """

            html_part = MIMEText(html_body, 'html')
            message.attach(html_part)

            # Connect to SMTP server
            with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
                server.starttls()
                server.login(settings.email_user, settings.email_pass)
                server.send_message(message)

            logger.info(f"OTP email sent successfully to {email} on attempt {attempt}")
            return  # Success, exit the function

        except Exception as error:
            logger.error(f"Attempt {attempt} failed to send email to {email}: {str(error)}")

            # If we've exhausted all retries, raise the error
            if attempt == retries:
                raise Exception('Failed to send OTP after multiple attempts.')

            # Wait for the specified delay before retrying
            time.sleep(delay_seconds)
