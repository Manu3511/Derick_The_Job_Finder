import requests
import re
import os
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

# Expanded list of 250+ target startups, unicorns, fintechs, MNCs, and tech companies in India and globally
COMPANIES_TO_TEST = [
    # Fintech & Payments
    "phonepe", "slice", "groww", "paytm", "cred", "fampay", "fi", "epifi", "razorpay", 
    "jupiter", "navi", "upstox", "coinswitch", "wazirx", "uni", "unicards", "onecard", 
    "indmoney", "jar", "leadsquared", "bharatpe", "postpe", "dhan", "zerodha", "smallcase", 
    "scripbox", "cleartax", "kuvera", "zestmoney", "earlysalary", "mpokket", "kreditbee", 
    "moneyview", "rupeek", "lendingkart", "flexiloans", "progcap", "dripcapital", "cashfree", 
    "pinelabs", "mswipe", "signzy", "m2p", "niyo", "scapia", "salt", "multipl", "dezerv", 
    "liquiloans", "wintwealth", "fatakpay", "moneytap", "cashe", "payu", "simpl", "lazypay",
    
    # E-commerce, Logtech, Consumer Tech
    "zepto", "zeptonow", "blinkit", "swiggy", "zomato", "meesho", "flipkart", "amazon", 
    "myntra", "nykaa", "ajio", "tata1mg", "pharmeasy", "netmeds", "bigbasket", "dunzo", 
    "dealshare", "citymall", "glowroad", "fashinza", "mamaearth", "sugarcosmetics", 
    "wowskinscience", "plumgoodness", "mcaffeine", "boat", "noise", "boult", "portronics", 
    "spinny", "cars24", "ola", "olaelectric", "ather", "atherenergy", "rapido", "yulu", 
    "bounce", "chalo", "locus", "shadowfax", "delhivery", "xpressbees", "ecomexpress", 
    "elasticrun", "ninjacart", "waycool", "dehaat", "cropin", "letsretail", "wakefit",
    
    # SaaS, Enterprise, Analytics, AI
    "druva", "postman", "browserstack", "chargebee", "freshworks", "zoho", "highradius", 
    "innovaccer", "darwinbox", "amagi", "fractal", "fractalanalytics", "musigma", "capillary", 
    "clevertap", "webengage", "moengage", "gupshup", "yellowai", "haptik", "sprinklr", 
    "whatfix", "bizongo", "inframarket", "ofbusiness", "moglix", "zetwerk", "inmobi", 
    "glance", "hasura", "verloop", "verloopio", "leadhq", "leadsquared", "vymo", "hubilo",
    
    # EdTech, Media, Content, Gaming
    "unacademy", "byjus", "upgrad", "simplilearn", "eruditus", "classplus", "physicswallah", 
    "vedantu", "pratilipi", "kukufm", "sharechat", "moj", "dailyhunt", "zupee", "winzo", 
    "nazara", "pocketfm", "halaplay", "mpl", "dream11", "games24x7", "mobilepremierleague",
    
    # Global Tech, MNCs, Consulting (hiring in BLR)
    "atlassian", "salesforce", "uber", "grab", "gojek", "bolt", "careem", "stripe", 
    "adoyen", "revolut", "wise", "n26", "klarna", "affirm", "chime", "robinhood", 
    "sofi", "plaid", "coinbase", "kraken", "intuit", "adobe", "paypal", "walmart", 
    "expedia", "booking", "agoda", "oyo", "redbus", "makemytrip", "yatra", "easemytrip", 
    "goibibo", "canva", "notion", "figma", "slack", "zoom", "hubspot", "datadog", 
    "snowflake", "confluent", "mongodb", "elastic", "hashicorp", "gitlab", "github", 
    "twilio", "sendgrid", "crowdstrike", "cloudflare", "fastly", "akamai", "ey",
    "deloitte", "pwc", "kpmg", "mckinsey", "bcg", "bain", "accenture", "cognizant",

    # Additional global SaaS / dev tools / infra (commonly on Greenhouse or Lever)
    "discord", "airtable", "asana", "dropbox", "doordash", "instacart", "reddit",
    "pinterest", "databricks", "scaleai", "rippling", "deel", "remote", "brex", "ramp",
    "gusto", "webflow", "vercel", "netlify", "linear", "retool", "airbyte", "temporal",
    "pagerduty", "okta", "auth0", "segment", "amplitude", "mixpanel", "zapier", "miro",
    "loom", "calendly", "typeform", "intercom", "zendesk", "docker", "circleci",
    "sentry", "launchdarkly", "contentful", "algolia", "redis", "grafanalabs",
    "newrelic", "splunk", "digitalocean", "linode", "render", "supabase", "airbnb",
    "lyft", "spotify", "shopify", "squarespace", "monday", "asanahq", "1password",
    "carta", "benchling", "samsara", "attentive", "faire", "gopuff", "getir",

    # Additional India-focused
    "urbancompany", "cardekho", "licious", "rebelfoods", "udaan", "lenskart",
    "pharmeasy", "innovaccer", "chargebee", "browserstack", "darwinbox", "hasura",
    "clevertap", "capillary", "moglix", "zetwerk", "razorpay", "cure_fit", "curefit",
    "acko", "digit", "policybazaar", "paisabazaar", "coverfox", "khatabook", "vedantu",
    "unacademy", "physicswallah", "meesho", "urbanclap"
]

SCRAPER_PATH = os.path.join(os.path.dirname(__file__), "job_scraper.py")

def check_greenhouse(company):
    url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs"
    try:
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            return company
    except Exception:
        pass
    return None

def check_lever(company):
    url = f"https://api.lever.co/v0/postings/{company}"
    try:
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            return company
    except Exception:
        pass
    return None

def discover_and_update():
    print(f"Testing {len(COMPANIES_TO_TEST)} companies in parallel for Greenhouse/Lever...")
    
    unique_companies = list(set(COMPANIES_TO_TEST))
    active_greenhouse = []
    active_lever = []
    
    with ThreadPoolExecutor(max_workers=60) as executor:
        gh_futures = {executor.submit(check_greenhouse, c): c for c in unique_companies}
        lev_futures = {executor.submit(check_lever, c): c for c in unique_companies}
        
        for future in as_completed(gh_futures):
            res = future.result()
            if res:
                active_greenhouse.append(res)
                
        for future in as_completed(lev_futures):
            res = future.result()
            if res:
                active_lever.append(res)
                
    print(f"\nDiscovered {len(active_greenhouse)} Greenhouse boards and {len(active_lever)} Lever boards.")
    
    # Update job_scraper.py
    if not os.path.exists(SCRAPER_PATH):
        print(f"Error: {SCRAPER_PATH} not found.")
        return
        
    with open(SCRAPER_PATH, "r") as f:
        content = f.read()
        
    # Replace GREENHOUSE_COMPANIES list
    gh_repr = json.dumps(active_greenhouse)
    content = re.sub(r'GREENHOUSE_COMPANIES\s*=\s*\[.*?\]', f'GREENHOUSE_COMPANIES = {gh_repr}', content)
    
    # Replace LEVER_COMPANIES list
    lev_repr = json.dumps(active_lever)
    content = re.sub(r'LEVER_COMPANIES\s*=\s*\[.*?\]', f'LEVER_COMPANIES = {lev_repr}', content)
    
    with open(SCRAPER_PATH, "w") as f:
        f.write(content)
        
    print("\nSuccessfully updated job_scraper.py with the active lists!")
    print(f"Greenhouse: {active_greenhouse}")
    print(f"Lever: {active_lever}")

if __name__ == "__main__":
    discover_and_update()
