import requests

companies = [
    "razorpay", "paytm", "zepto", "zeptonow", "ather", "atherenergy", "meesho", 
    "jupiter", "navi", "swiggy", "zomato", "urbancompany", "licious", "dunzo", 
    "rupeek", "khatabook", "coinswitch", "upstox", "fi", "fimoney", "uni", "unicards", 
    "onecard", "indmoney", "jar", "fampay", "leadsquared", "shadowfax", "ninjacart", 
    "ola", "olaelectric", "bharatpe", "postpe", "slice", "cred", "groww", "phonepe", 
    "inmobi", "wazirx", "unacademy", "byjus", "dream11", "pharmeasy", "cultfit", 
    "curefit", "lenskart", "nykaa", "spinny", "caratlane", "mamaearth", 
    "delhivery", "pocketfm", "atlassian", "salesforce"
]

print("--- Testing Greenhouse Board APIs ---")
active_greenhouse = []
for company in companies:
    url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            jobs_count = len(data.get("jobs", []))
            print(f"[Greenhouse] {company}: SUCCESS ({jobs_count} jobs found)")
            active_greenhouse.append(company)
    except Exception as e:
        pass

print("\n--- Testing Lever Postings APIs ---")
active_lever = []
for company in companies:
    url = f"https://api.lever.co/v0/postings/{company}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            jobs_count = len(data)
            print(f"[Lever] {company}: SUCCESS ({jobs_count} jobs found)")
            active_lever.append(company)
    except Exception as e:
        pass

print("\n--- Active Summary ---")
print(f"Greenhouse: {active_greenhouse}")
print(f"Lever: {active_lever}")
