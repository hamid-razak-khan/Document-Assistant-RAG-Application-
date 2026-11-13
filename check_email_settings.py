import os
import sys

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Load environment variables
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), 'backend', '.env'))

# Check environment variables
print("Checking environment variables...")
print("=" * 40)

email_host_user = os.getenv('EMAIL_HOST_USER')
email_host_password = os.getenv('EMAIL_HOST_PASSWORD')

print(f"EMAIL_HOST_USER: {email_host_user}")
print(f"EMAIL_HOST_PASSWORD: {'*' * len(email_host_password) if email_host_password else 'Not set'}")

# Check if required variables are set
if email_host_user and email_host_password:
    print("✅ Email environment variables are set")
else:
    print("❌ Email environment variables are missing")
    
# Check Django settings
print("\nChecking Django settings...")
print("=" * 40)

try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resume_backend.settings')
    import django
    django.setup()
    
    from django.conf import settings
    
    print(f"EMAIL_BACKEND: {getattr(settings, 'EMAIL_BACKEND', 'Not set')}")
    print(f"EMAIL_HOST: {getattr(settings, 'EMAIL_HOST', 'Not set')}")
    print(f"EMAIL_PORT: {getattr(settings, 'EMAIL_PORT', 'Not set')}")
    print(f"EMAIL_USE_TLS: {getattr(settings, 'EMAIL_USE_TLS', 'Not set')}")
    print(f"EMAIL_HOST_USER: {getattr(settings, 'EMAIL_HOST_USER', 'Not set')}")
    print(f"DEFAULT_FROM_EMAIL: {getattr(settings, 'DEFAULT_FROM_EMAIL', 'Not set')}")
    
    # Check if all required settings are present
    required_settings = [
        'EMAIL_BACKEND',
        'EMAIL_HOST',
        'EMAIL_PORT', 
        'EMAIL_USE_TLS',
        'EMAIL_HOST_USER',
        'EMAIL_HOST_PASSWORD',
        'DEFAULT_FROM_EMAIL'
    ]
    
    missing = []
    for setting in required_settings:
        if not getattr(settings, setting, None):
            missing.append(setting)
    
    if missing:
        print(f"❌ Missing Django settings: {missing}")
    else:
        print("✅ All Django email settings are configured")
        
except Exception as e:
    print(f"❌ Error checking Django settings: {e}")