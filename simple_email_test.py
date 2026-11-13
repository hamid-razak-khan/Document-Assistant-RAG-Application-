import re

def extract_email_from_text(text):
    """
    Extract the first email address from text using regex.
    """
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    matches = re.findall(email_pattern, text)
    return matches[0] if matches else None

# Test the function with sample resume texts
sample_resumes = [
    "John Doe\nSoftware Engineer\nEmail: john.doe@example.com\nPhone: 123-456-7890",
    "Jane Smith\nData Scientist\nContact: jane.smith@company.org\nExperience in Python and ML",
    "Robert Brown\nResume without email\nExperience in various technologies",
    "Multiple contacts:\nPrimary: primary@test.com\nSecondary: secondary@example.org",
]

print("Testing email extraction with sample resume texts:")
print("=" * 50)

for i, resume_text in enumerate(sample_resumes, 1):
    email = extract_email_from_text(resume_text)
    print(f"Resume {i}:")
    print(f"Text: {resume_text[:50]}{'...' if len(resume_text) > 50 else ''}")
    print(f"Extracted Email: {email}")
    print("-" * 30)

# Test the regex pattern directly
print("\nTesting regex pattern with various email formats:")
print("=" * 50)

test_emails = [
    "simple@example.com",
    "user.name@domain.co.uk", 
    "user+tag@sub.domain.org",
    "123@test-domain.com",
    "invalid@",  # Invalid
    "@invalid.com",  # Invalid
]

email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

for email in test_emails:
    matches = re.findall(email_pattern, email)
    found = matches[0] if matches else None
    print(f"'{email}' -> {found}")