import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

GREENHOUSE_COMPANIES = ["n26", "highradius", "postman", "fastly", "figma", "glance", "mongodb", "groww", "robinhood", "affirm", "inmobi", "stripe", "phonepe", "gitlab", "sofi", "agoda", "twilio", "coinbase", "chime", "careem", "slice", "bcg", "cloudflare", "hubspot"]
LEVER_COMPANIES = ["pocketfm", "cred", "fi", "freshworks", "plaid", "kpmg", "kraken", "atlassian", "epifi", "fampay", "meesho", "paytm"]

def get_greenhouse_jobs(company):
    """
    Fetches and normalizes jobs from Greenhouse API.
    """
    url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs?content=true"
    jobs = []
    try:
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            return jobs
            
        data = response.json()
        for job in data.get("jobs", []):
            location_name = job.get("location", {}).get("name", "")
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
    except Exception:
        pass
    return jobs

def get_lever_jobs(company):
    """
    Fetches and normalizes jobs from Lever API.
    """
    url = f"https://api.lever.co/v0/postings/{company}?mode=json"
    jobs = []
    try:
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
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
    except Exception:
        pass
    return jobs

def fetch_all_jobs():
    """
    Scrapes all companies in parallel using a ThreadPoolExecutor.
    Converts execution from sequential (taking minutes) to parallel (taking 3-5 seconds).
    """
    all_jobs = []
    print(f"[Scraper] Scraping {len(GREENHOUSE_COMPANIES)} Greenhouse and {len(LEVER_COMPANIES)} Lever boards concurrently...")
    
    with ThreadPoolExecutor(max_workers=40) as executor:
        # Submit Greenhouse tasks
        gh_futures = {executor.submit(get_greenhouse_jobs, c): c for c in GREENHOUSE_COMPANIES}
        # Submit Lever tasks
        lev_futures = {executor.submit(get_lever_jobs, c): c for c in LEVER_COMPANIES}
        
        for future in as_completed(gh_futures):
            res = future.result()
            if res:
                all_jobs.extend(res)
                
        for future in as_completed(lev_futures):
            res = future.result()
            if res:
                all_jobs.extend(res)
                
    print(f"[Scraper] Scraping complete. Total postings fetched: {len(all_jobs)}")
    return all_jobs

if __name__ == "__main__":
    import time
    start = time.time()
    jobs = fetch_all_jobs()
    print(f"Time taken: {time.time() - start:.2f} seconds")
