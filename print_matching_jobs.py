from job_scraper import fetch_all_jobs
from resume_matcher import match_job

print("Fetching and filtering matching jobs for printing (India Only)...")
jobs = fetch_all_jobs()
matches = []

for job in jobs:
    title = job["title"]
    company = job["company"]
    desc = job["description"]
    url = job["apply_url"]
    loc = job["location"]
    
    is_match, score = match_job(title, desc, loc)
    if is_match:
        matches.append({
            "title": title,
            "company": company,
            "location": loc,
            "url": url,
            "score": score
        })

print(f"\nFound {len(matches)} matching jobs in India:")
for m in matches:
    print(f"- {m['title']} @ {m['company']} ({m['location']}): {m['url']}")
