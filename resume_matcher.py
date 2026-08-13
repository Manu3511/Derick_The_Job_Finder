import re

# Candidate Profile Details
CANDIDATE_PROFILE = {
    "name": "Manuraj M",
    "email": "manurajmanoj8@gmail.com",
    "phone": "9207244681",
    "linkedin": "https://linkedin.com/in/manuraj--",
    "github": "https://github.com/Manu3511",
    "skills": {
        "core": ["sql", "excel", "python", "looker studio", "databricks"],
        "analytics": ["a/b testing", "funnel analysis", "cohort analysis", "statistics"],
        "automation": ["n8n", "selenium", "beautifulsoup", "fastapi", "bigquery"]
    }
}

def clean_text(text):
    if not text:
        return ""
    return text.lower()

def extract_experience(text):
    """
    Parses the text and returns the maximum required experience in years if found.
    If no experience is found, returns None.
    """
    text_lower = text.lower()
    
    # Pattern 1: "3-5 years", "3 to 5 yrs"
    range_match = re.findall(r"(\d+)\s*(?:-|to)\s*(\d+)\s*(?:years|yrs|year|yr)", text_lower)
    for min_yr, max_yr in range_match:
        return int(max_yr)
        
    # Pattern 2: "3+ years", "3+ yrs"
    plus_match = re.findall(r"(\d+)\+\s*(?:years|yrs|year|yr)", text_lower)
    for yr in plus_match:
        return int(yr)
        
    # Pattern 3: "3 years of experience", "3 yrs experience"
    exp_match = re.findall(r"(\d+)\s*(?:years|yrs|year|yr)\s*(?:of)?\s*experience", text_lower)
    for yr in exp_match:
        return int(yr)
        
    return None

def is_india_location(location):
    """
    Checks if the job location is in India.
    """
    if not location:
        return False
    loc_lower = location.lower()
    
    # Must contain an Indian city or India
    india_keywords = ["india", "bengaluru", "bangalore", "hyderabad", "pune", "mumbai", "delhi", "gurgaon", "noida", "chennai", "kolkata"]
    has_india_kw = any(kw in loc_lower for kw in india_keywords)
    if not has_india_kw:
        return False
        
    # Exclude foreign countries explicitly if they don't have "india"
    foreign_countries = ["united states", "usa", "canada", "germany", "united kingdom", "uk", "australia", "singapore"]
    for country in foreign_countries:
        if country in loc_lower and "india" not in loc_lower:
            return False
            
    return True

def match_job(title, description, location):
    """
    Analyzes job title, description, and location against candidate profile.
    Filters: India-only location, hard 0-2 years experience, title screening.
    Returns (is_match, score)
    """
    # 1. Location Filter: Strict India-only
    if not is_india_location(location):
        return False, 0

    title_clean = clean_text(title)
    desc_clean = clean_text(description)
    
    # 2. Title Filter: Strictly reject senior roles
    senior_kws = ["senior", "sr.", "lead", "manager", "head", "director", "architect", "chief", "vp", "avp"]
    for kw in senior_kws:
        pattern = r"\b" + re.escape(kw) + r"\b"
        if re.search(pattern, title_clean):
            return False, 0

    # 2b. Title Filter: Reject engineering/dev/support job functions (wrong role type for this profile)
    wrong_function_kws = [
        "engineer", "engineering", "developer", "swe", "sde",
        "programmer", "devops", "sre", "qa", "quality assurance",
        "designer", "sales", "marketing", "recruiter", "recruiting", "hr ",
        "human resources", "legal", "counsel"
    ]
    for kw in wrong_function_kws:
        pattern = r"\b" + re.escape(kw) + r"\b"
        if re.search(pattern, title_clean):
            return False, 0

    # 3. Experience Filter: Hard filter for 0-2 years
    req_exp = extract_experience(description)
    if req_exp is not None and req_exp > 2:
        return False, 0

    title_exp = extract_experience(title)
    if title_exp is not None and title_exp > 2:
        return False, 0

    # 4. Role Title Fit: must be data/business/operations analyst or similar
    valid_titles = [
        "analyst", "analytics", "mis", "reporting", "data", "business intelligence",
        "insights", "dashboard", "research analyst"
    ]
    has_valid_title = any(kw in title_clean for kw in valid_titles)
    if not has_valid_title:
        return False, 0

    # 5. Check for core technical skills
    score = 0

    # SQL (High Priority)
    if "sql" in title_clean or "sql" in desc_clean:
        score += 40

    # Excel (High Priority)
    if "excel" in desc_clean or "spreadsheet" in desc_clean or "sheets" in desc_clean:
        score += 40

    # Python (Medium Priority)
    if "python" in desc_clean or "pandas" in desc_clean:
        score += 20

    # BI / visualization tools (Medium Priority)
    if any(kw in desc_clean for kw in ["tableau", "power bi", "powerbi", "looker", "data studio"]):
        score += 20

    # Data warehousing / query tools (Medium Priority)
    if any(kw in desc_clean for kw in ["bigquery", "databricks", "snowflake"]):
        score += 20

    # Stats/analysis fundamentals (Low Priority)
    if any(kw in desc_clean for kw in ["statistics", "a/b testing", "cohort", "funnel"]):
        score += 10

    # Minimum threshold to match: lowered so a single strong skill mention (SQL/Excel/BI/warehouse) qualifies
    is_match = score >= 40

    return is_match, score

if __name__ == "__main__":
    # Tests
    print(match_job("Data Analyst", "SQL, 1-2 years experience", "Bangalore")) # True
    print(match_job("Data Analyst", "SQL, 1-2 years experience", "San Francisco, CA")) # False
