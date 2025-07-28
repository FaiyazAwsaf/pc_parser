from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_verification_email(user, token):
    """Send email verification OTP to user"""
    subject = 'Verify Your Email - PC Parser'
    
    # Create HTML email content
    html_message = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #2c3e50;">Email Verification</h2>
            <p>Hello {user.first_name},</p>
            <p>Thank you for registering with PC Parser. To complete your registration, please verify your email address using the OTP below:</p>
            
            <div style="background-color: #f8f9fa; padding: 20px; border-radius: 5px; text-align: center; margin: 20px 0;">
                <h3 style="color: #2c3e50; margin: 0;">Your Verification Code</h3>
                <p style="font-size: 32px; font-weight: bold; color: #3498db; margin: 10px 0; letter-spacing: 5px;">{token}</p>
            </div>
            
            <p><strong>Important:</strong> This code will expire in 10 minutes for security reasons.</p>
            <p>If you didn't create an account with us, please ignore this email.</p>
            
            <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
            <p style="font-size: 12px; color: #666;">
                This is an automated message, please do not reply to this email.
            </p>
        </div>
    </body>
    </html>
    """
    
    # Create plain text version
    plain_message = f"""
    Email Verification - PC Parser
    
    Hello {user.first_name},
    
    Thank you for registering with PC Parser. To complete your registration, please verify your email address using the OTP below:
    
    Your Verification Code: {token}
    
    Important: This code will expire in 10 minutes for security reasons.
    
    If you didn't create an account with us, please ignore this email.
    
    This is an automated message, please do not reply to this email.
    """
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def send_welcome_email(user):
    """Send welcome email after successful verification"""
    subject = 'Welcome to PC Parser!'
    
    html_message = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #2c3e50;">Welcome to PC Parser!</h2>
            <p>Hello {user.first_name},</p>
            <p>Congratulations! Your email has been successfully verified and your account is now active.</p>
            
            <div style="background-color: #d4edda; padding: 20px; border-radius: 5px; border-left: 4px solid #28a745; margin: 20px 0;">
                <h3 style="color: #155724; margin: 0;">Account Details</h3>
                <p style="margin: 10px 0;"><strong>Email:</strong> {user.email}</p>
                <p style="margin: 10px 0;"><strong>Username:</strong> {user.username}</p>
                <p style="margin: 10px 0;"><strong>Name:</strong> {user.first_name} {user.last_name}</p>
            </div>
            
            <p>You can now log in to your account and start using PC Parser.</p>
            
            <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
            <p style="font-size: 12px; color: #666;">
                This is an automated message, please do not reply to this email.
            </p>
        </div>
    </body>
    </html>
    """
    
    plain_message = f"""
    Welcome to PC Parser!
    
    Hello {user.first_name},
    
    Congratulations! Your email has been successfully verified and your account is now active.
    
    Account Details:
    Email: {user.email}
    Username: {user.username}
    Name: {user.first_name} {user.last_name}
    
    You can now log in to your account and start using PC Parser.
    
    This is an automated message, please do not reply to this email.
    """
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending welcome email: {e}")
        return False
