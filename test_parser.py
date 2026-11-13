import re
from typing import List, Dict, Any

def parse_llm_response(response_text: str) -> Dict[str, Any]:
    """
    Parse the LLM response text according to the specified format.
    """
    # Initialize default values
    result = {
        "summary": "",
        "matching_skills": [],
        "missing_skills": [],
        "rating": 0,
    }
    
    # Split the response into sections
    sections = response_text.split('\n\n')
    
    for section in sections:
        section = section.strip()
        if section.startswith('Summary:'):
            result["summary"] = section.replace('Summary:', '', 1).strip()
        elif section.startswith('Extracted Resume Skills:'):
            # Skip this section as we don't need to return it
            pass
        elif section.startswith('JD Required Skills:'):
            # Skip this section as we don't need to return it
            pass
        elif section.startswith('Matching Skills:'):
            skills_text = section.replace('Matching Skills:', '', 1).strip()
            if skills_text and skills_text != "None identified":
                # Split by newlines and clean up
                skills = [skill.strip().lstrip('•- ').strip() for skill in skills_text.split('\n') if skill.strip()]
                result["matching_skills"] = [skill for skill in skills if skill]
        elif section.startswith('Missing Skills:'):
            skills_text = section.replace('Missing Skills:', '', 1).strip()
            if skills_text and skills_text != "None identified":
                # Split by newlines and clean up
                skills = [skill.strip().lstrip('•- ').strip() for skill in skills_text.split('\n') if skill.strip()]
                result["missing_skills"] = [skill for skill in skills if skill]
        elif section.startswith('Keyword Score:'):
            # Extract scores from the section
            keyword_match = re.search(r'Keyword Score:\s*(\d+)', section)
            semantic_match = re.search(r'Semantic Score:\s*(\d+)', section)
            final_match = re.search(r'Final Score:\s*(\d+)', section)
            
            if keyword_match:
                # We'll use the final score as the rating
                if final_match:
                    result["rating"] = int(final_match.group(1))
    
    return result

# Test the parser with a sample response
sample_response = """Summary:
This candidate has strong Python and Django experience with relevant cloud skills. They match most of the required technical skills and have practical experience with the core technologies mentioned in the job description.

Extracted Resume Skills:
Python, Django, REST API, AWS, Docker, PostgreSQL, Git, MySQL, Flask, JavaScript

JD Required Skills:
Python, Django, REST API, AWS, Docker, PostgreSQL, Git

Matching Skills:
• Python
• Django
• REST API
• AWS
• Docker
• PostgreSQL
• Git

Missing Skills:
• React
• Kubernetes
• CI/CD
• Machine Learning

Keyword Score: 85/100
Semantic Score: 78/100
Final Score: 80/100"""

parsed = parse_llm_response(sample_response)
print("Parsed result:")
print(parsed)