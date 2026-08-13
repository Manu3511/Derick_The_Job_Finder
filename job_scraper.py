import requests

GREENHOUSE_COMPANIES = ["coinbase", "sisense", "cockroachlabs", "assemblyai", "bitpanda", "clickhouse", "gemini", "pagerduty", "intercom", "mongodb", "slice", "mixpanel", "coursera", "udemy", "algolia", "hubspot", "circleci", "netlify", "dropbox", "n26", "okta", "epicgames", "newrelic", "grafanalabs", "sofi", "samsara", "roblox", "binance", "digit", "komodohealth", "affirm", "figma", "chime", "twilio", "scaleai", "inmobi", "medium", "duolingo", "asana", "bcg", "attentive", "druva", "highradius", "fastly", "reddit", "slintel", "calm", "calendly", "planetscale", "amplitude", "databricks", "peloton", "instacart", "remote", "gitlab", "airbnb", "careem", "launchdarkly", "phonepe", "fireblocks", "lyft", "buzzfeed", "fivetran", "cloudsek", "carta", "cloudflare", "stabilityai", "contentful", "elastic", "airtable", "discord", "consensys", "squarespace", "agoda", "webflow", "collibra", "faire", "pinterest", "riotgames", "masterclass", "postman", "brex", "datadog", "typeform", "wise", "robinhood", "pendo", "groww", "vercel", "ripple", "glance", "gusto"]
LEVER_COMPANIES = ["immutable", "pocketfm", "kraken", "anyscale", "fi", "binance", "outreach", "meesho", "highspot", "kpmg", "paytm", "epifi", "anchorage", "freshworks", "plaid", "gopuff", "ledger", "metabase", "cred", "neon", "fampay", "spotify", "clari", "ro"]

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
