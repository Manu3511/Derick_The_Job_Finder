import requests

GREENHOUSE_COMPANIES = ["highradius", "hubspot", "grafanalabs", "lyft", "instacart", "elastic", "stripe", "digit", "druva", "webflow", "brex", "postman", "twilio", "newrelic", "chime", "robinhood", "airbnb", "carta", "fastly", "n26", "careem", "intercom", "pagerduty", "samsara", "sofi", "gitlab", "agoda", "launchdarkly", "glance", "coinbase", "okta", "figma", "reddit", "scaleai", "dropbox", "slice", "mixpanel", "gusto", "amplitude", "circleci", "squarespace", "datadog", "phonepe", "groww", "netlify", "algolia", "asana", "affirm", "bcg", "attentive", "discord", "remote", "databricks", "contentful", "cloudflare", "inmobi", "airtable", "mongodb", "vercel", "pinterest", "calendly", "typeform"]
LEVER_COMPANIES = ["cred", "meesho", "paytm", "gopuff", "fampay", "fi", "plaid", "pocketfm", "epifi", "kpmg", "spotify", "freshworks", "kraken"]

def get_greenhouse_jobs(company):
    """
    Fetches and normalizes jobs from Greenhouse API.
    """
    url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs?content=true"
    jobs = []
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"[Scraper] Failed to fetch {company} from Greenhouse (Status: {response.status_code})")
            return jobs
            
        data = response.json()
        for job in data.get("jobs", []):
            location_name = job.get("location", {}).get("name", "")
            # Filter for Bengaluru / Bangalore / Remote
            location_lower = location_name.lower()
            if "bengaluru" in location_lower or "bangalore" in location_lower or "remote" in location_lower or "india" in location_lower:
                jobs.append({
                    "id": f"gh_{company}_{job.get('id')}",
                    "title": job.get("title", ""),
                    "company": company.upper(),
                    "description": job.get("content", ""),
                    "apply_url": job.get("absolute_url", ""),
                    "location": location_name
                })
    except Exception as e:
        print(f"[Scraper] Error fetching Greenhouse jobs for {company}: {str(e)}")
    return jobs

def get_lever_jobs(company):
    """
    Fetches and normalizes jobs from Lever API.
    """
    url = f"https://api.lever.co/v0/postings/{company}?mode=json"
    jobs = []
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"[Scraper] Failed to fetch {company} from Lever (Status: {response.status_code})")
            return jobs
            
        data = response.json()
        for job in data:
            location_name = job.get("categories", {}).get("location", "")
            location_lower = location_name.lower()
            if "bengaluru" in location_lower or "bangalore" in location_lower or "remote" in location_lower or "india" in location_lower:
                desc = job.get("descriptionPlain", "") + "\n" + job.get("additionalPlain", "")
                jobs.append({
                    "id": f"lev_{company}_{job.get('id')}",
                    "title": job.get("text", ""),
                    "company": company.upper(),
                    "description": desc,
                    "apply_url": job.get("hostedUrl", ""),
                    "location": location_name
                })
    except Exception as e:
        print(f"[Scraper] Error fetching Lever jobs for {company}: {str(e)}")
    return jobs

def fetch_all_jobs():
    """
    Orchestrates scraping of all target companies.
    """
    all_jobs = []
    
    # Fetch Greenhouse
    for company in GREENHOUSE_COMPANIES:
        print(f"[Scraper] Scraping Greenhouse board: {company}...")
        jobs = get_greenhouse_jobs(company)
        print(f"[Scraper] Found {len(jobs)} matches for {company}.")
        all_jobs.extend(jobs)
        
    # Fetch Lever
    for company in LEVER_COMPANIES:
        print(f"[Scraper] Scraping Lever board: {company}...")
        jobs = get_lever_jobs(company)
        print(f"[Scraper] Found {len(jobs)} matches for {company}.")
        all_jobs.extend(jobs)
        
    return all_jobs

if __name__ == "__main__":
    jobs = fetch_all_jobs()
    print(f"\nTotal collected jobs: {len(jobs)}")
    if jobs:
        print(f"Sample Job: {jobs[0]['title']} @ {jobs[0]['company']} ({jobs[0]['location']})")
