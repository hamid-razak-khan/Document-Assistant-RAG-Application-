import re

def extract_email_from_text(text):
    """
    Extract the first email address from text using regex.
    """
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    matches = re.findall(email_pattern, text)
    return matches[0] if matches else None

# Test the function
test_texts = [
    "John Doe, Email: john.doe@example.com, Phone: 123-456-7890",
    "Contact me at jane.smith@company.org for more information",
    "No email here, just some random text",
    "Multiple emails: first@test.com and second@example.org",
    "Invalid email: @invalid.com and valid email: valid@domain.co.uk"
]

for i, text in enumerate(test_texts, 1):
    email = extract_email_from_text(text)
    print(f"Test {i}: '{text}' -> Email: {email}")