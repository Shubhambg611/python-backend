#!/usr/bin/env python3
"""
Email Configuration Test Script
Tests if the SMTP email configuration is working correctly
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
import sys

# Load environment variables
load_dotenv()

# Get email configuration from .env
EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASS = os.getenv('EMAIL_PASS')
SMTP_HOST = os.getenv('SMTP_HOST')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))

def test_email_config():
    """Test email configuration by sending a test email"""

    print("=" * 60)
    print("Email Configuration Test")
    print("=" * 60)

    # Display configuration
    print(f"\n📧 Email Configuration:")
    print(f"   EMAIL_USER: {EMAIL_USER}")
    print(f"   EMAIL_PASS: {'*' * len(EMAIL_PASS) if EMAIL_PASS else 'Not Set'}")
    print(f"   SMTP_HOST: {SMTP_HOST}")
    print(f"   SMTP_PORT: {SMTP_PORT}")

    # Validate configuration
    if not all([EMAIL_USER, EMAIL_PASS, SMTP_HOST, SMTP_PORT]):
        print("\n❌ ERROR: Missing email configuration!")
        print("   Please check your .env file")
        return False

    # Ask for test email recipient
    print(f"\n📬 Test email will be sent from: {EMAIL_USER}")
    recipient = input("Enter recipient email address (or press Enter to send to yourself): ").strip()

    if not recipient:
        recipient = EMAIL_USER
        print(f"   Using sender email as recipient: {recipient}")

    print(f"\n🔄 Attempting to send test email...")

    try:
        # Create test message
        message = MIMEMultipart('alternative')
        message['Subject'] = 'Convis Labs - Email Configuration Test'
        message['From'] = EMAIL_USER
        message['To'] = recipient

        # HTML body
        html_body = """
        <div style="font-family: Arial, sans-serif; color: #333; padding: 20px;">
            <h2 style="color: #4CAF50;">✅ Email Configuration Test Successful!</h2>
            <p>Hello,</p>
            <p>This is a test email from your Convis Labs Python backend.</p>
            <p>If you're receiving this email, your SMTP configuration is working correctly!</p>
            <hr style="border: 1px solid #eee; margin: 20px 0;">
            <p style="font-size: 12px; color: #666;">
                <strong>Configuration Details:</strong><br>
                SMTP Host: {smtp_host}<br>
                SMTP Port: {smtp_port}<br>
                From: {email_user}
            </p>
            <p style="font-size: 12px; color: #999;">
                This is an automated test email from Convis Labs Backend.
            </p>
        </div>
        """.format(
            smtp_host=SMTP_HOST,
            smtp_port=SMTP_PORT,
            email_user=EMAIL_USER
        )

        html_part = MIMEText(html_body, 'html')
        message.attach(html_part)

        # Connect to SMTP server
        print(f"   ↳ Connecting to {SMTP_HOST}:{SMTP_PORT}...")
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as server:
            print(f"   ↳ Starting TLS encryption...")
            server.starttls()

            print(f"   ↳ Logging in as {EMAIL_USER}...")
            server.login(EMAIL_USER, EMAIL_PASS)

            print(f"   ↳ Sending email to {recipient}...")
            server.send_message(message)

        print(f"\n✅ SUCCESS! Test email sent successfully!")
        print(f"   📧 Check your inbox at: {recipient}")
        print(f"\n💡 Your email configuration is working correctly!")
        return True

    except smtplib.SMTPAuthenticationError as e:
        print(f"\n❌ AUTHENTICATION FAILED!")
        print(f"   Error: {str(e)}")
        print(f"\n🔧 Troubleshooting:")
        print(f"   1. Verify EMAIL_USER is correct: {EMAIL_USER}")
        print(f"   2. Verify EMAIL_PASS is correct (check for typos)")
        print(f"   3. Check if your email provider requires app-specific passwords")
        print(f"   4. Ensure your account allows SMTP access")
        return False

    except smtplib.SMTPConnectError as e:
        print(f"\n❌ CONNECTION FAILED!")
        print(f"   Error: {str(e)}")
        print(f"\n🔧 Troubleshooting:")
        print(f"   1. Verify SMTP_HOST is correct: {SMTP_HOST}")
        print(f"   2. Verify SMTP_PORT is correct: {SMTP_PORT}")
        print(f"   3. Check your internet connection")
        print(f"   4. Check if firewall is blocking the connection")
        return False

    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print(f"\n🔧 Troubleshooting:")
        print(f"   1. Check all email configuration values in .env")
        print(f"   2. Ensure SMTP_HOST doesn't have http:// or trailing /")
        print(f"   3. Try using port 465 (SSL) or 587 (TLS)")
        print(f"   4. Contact your email provider for SMTP settings")
        return False

if __name__ == "__main__":
    print("\n")
    success = test_email_config()
    print("\n" + "=" * 60 + "\n")

    if success:
        sys.exit(0)
    else:
        sys.exit(1)
