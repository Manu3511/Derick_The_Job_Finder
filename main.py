import os
import json
from job_scraper import fetch_all_jobs
from resume_matcher import match_job
from telegram_notifier import send_telegram_alert

NOTIFIED_FILE = os.path.join(os.path.dirname(__file__), "notified_jobs.json")

def load_notified_jobs():
    if not os.path.exists(NOTIFIED_FILE):
        return []
    with open(NOTIFIED_FILE, "r") as f:
        try:
            return json.load(f)
        except Exception:
            return []

def save_notified_jobs(notified_list):
    with open(NOTIFIED_FILE, "w") as f:
        json.dump(notified_list, f, indent=4)

def run_pipeline():
    print("--- Starting Job Monitor Pipeline ---")
    
    # 1. Load already notified job IDs
    notified_jobs = load_notified_jobs()
    print(f"Loaded {len(notified_jobs)} previously notified job IDs.")
    
    # 2. Fetch all jobs
    jobs = fetch_all_jobs()
    
    # 3. Match and Notify
    new_notified_count = 0
    for job in jobs:
        job_id = job["id"]
        
        # Skip if already notified
        if job_id in notified_jobs:
            continue
            
        title = job["title"]
        company = job["company"]
        desc = job["description"]
        url = job["apply_url"]
        loc = job["location"]
        
        # Screen and Match (passing location now)
        is_match, score = match_job(title, desc, loc)
        
        if is_match:
            print(f"[Match] Found matching job in India: {title} @ {company} (Score: {score})")
            
            # Format concise Telegram alert
            telegram_msg = (
                f"🚨 <b>New Job Alert!</b>\n\n"
                f"<b>Role:</b> {title}\n"
                f"<b>Company:</b> {company}\n"
                f"<b>Location:</b> {loc}\n\n"
                f"👉 <a href='{url}'>Apply Link</a>"
            )
            
            # Send alert
            success = send_telegram_alert(telegram_msg)
            
            if success:
                notified_jobs.append(job_id)
                new_notified_count += 1
                
    # 4. Save updated notified state
    if new_notified_count > 0:
        save_notified_jobs(notified_jobs)
        print(f"Saved notified state. Sent {new_notified_count} new alerts.")
    else:
        print("No new matching jobs found this run.")
        
    print("--- Pipeline Finished ---")

if __name__ == "__main__":
    run_pipeline()
