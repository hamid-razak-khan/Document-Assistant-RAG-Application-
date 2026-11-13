#!/usr/bin/env python
import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner

# Add the project directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resume_backend.settings')
django.setup()

import re
from django.core.mail import send_mail
from screening.views import extract_email_from_text

def test_email_extraction():
    """Test the email extraction function with various text samples"""
    print("Testing email extraction function...")
    
    test_cases = [
        # (text, expected_email)
        ("Contact: john.doe@example.com for more info", "john.doe@example.com"),
        ("Email me at jane_smith@company.org", "jane_smith@company.org"),
        ("No email in this text", None),
        ("Multiple emails: first@test.com and second@example.org", "first@test.com"),
        ("Invalid: @invalid.com and valid: valid@domain.co.uk", "valid@domain.co.uk"),
        ("Special chars: user.name+tag@sub.domain.com", "user.name+tag@sub.domain.com"),
    ]
    
    passed = 0
    failed = 0
    
    for text, expected in test_cases:
        result = extract_email_from_text(text)
        if result == expected:
            print(f"✅ PASS: '{text}' -> {result}")
            passed += 1
        else:
            print(f"❌ FAIL: '{text}' -> Expected: {expected}, Got: {result}")
            failed += 1
    
    print(f"\nEmail Extraction Results: {passed} passed, {failed} failed")
    return failed == 0

def test_email_sending_simulation():
    """Simulate email sending without actually sending"""
    print("\nTesting email sending simulation...")
    
    # This would normally use Django's send_mail function
    # For simulation, we'll just verify the function is available
    try:
        # Check if send_mail is available
        assert callable(send_mail)
        print("✅ Django send_mail function is available")
        
        # Check if email settings are configured
        required_settings = [
            'EMAIL_BACKEND',
            'EMAIL_HOST', 
            'EMAIL_PORT',
            'EMAIL_USE_TLS',
            'EMAIL_HOST_USER',
            'EMAIL_HOST_PASSWORD',
            'DEFAULT_FROM_EMAIL'
        ]
        
        missing_settings = []
        for setting in required_settings:
            if not hasattr(settings, setting) or not getattr(settings, setting):
                missing_settings.append(setting)
        
        if missing_settings:
            print(f"❌ Missing email settings: {missing_settings}")
            return False
        else:
            print("✅ All required email settings are configured")
            print(f"   EMAIL_HOST: {settings.EMAIL_HOST}")
            print(f"   EMAIL_PORT: {settings.EMAIL_PORT}")
            print(f"   EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
            print(f"   EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
            return True
            
    except Exception as e:
        print(f"❌ Error testing email sending: {e}")
        return False

def test_regex_pattern():
    """Test the specific regex pattern used for email extraction"""
    print("\nTesting regex pattern...")
    
    # The exact pattern from the implementation
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    
    test_emails = [
        "simple@example.com",
        "user.name@domain.co.uk",
        "user+tag@sub.domain.org",
        "123@test-domain.com",
        "invalid@",  # Invalid
        "@invalid.com",  # Invalid
        "valid@domain.",  # Invalid
    ]
    
    passed = 0
    failed = 0
    
    for email in test_emails:
        matches = re.findall(email_pattern, email)
        found = matches[0] if matches else None
        
        # For invalid emails, we expect no match
        is_valid = "@" in email and "." in email and not email.startswith("@") and not email.endswith(".")
        
        if (is_valid and found == email) or (not is_valid and found is None):
            print(f"✅ PASS: '{email}' -> {found}")
            passed += 1
        else:
            print(f"❌ FAIL: '{email}' -> Expected: {'match' if is_valid else 'no match'}, Got: {found}")
            failed += 1
    
    print(f"\nRegex Pattern Results: {passed} passed, {failed} failed")
    return failed == 0

if __name__ == "__main__":
    print("=== Email Functionality Test Suite ===\n")
    
    # Run all tests
    extraction_ok = test_email_extraction()
    regex_ok = test_regex_pattern()
    sending_ok = test_email_sending_simulation()
    
    print("\n=== Test Summary ===")
    print(f"Email Extraction: {'✅ PASS' if extraction_ok else '❌ FAIL'}")
    print(f"Regex Pattern: {'✅ PASS' if regex_ok else '❌ FAIL'}")
    print(f"Email Sending Setup: {'✅ PASS' if sending_ok else '❌ FAIL'}")
    
    if extraction_ok and regex_ok and sending_ok:
        print("\n🎉 All tests passed! Email functionality should work correctly.")
        sys.exit(0)
    else:
        print("\n⚠️  Some tests failed. Please check the implementation.")
        sys.exit(1)