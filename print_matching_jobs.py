from job_scraper import fetch_all_jobs
from resume_matcher import match_job
import os

HTML_PATH = os.path.join(os.path.dirname(__file__), "jobs_found.html")

def build_html_dashboard(matches):
    rows = ""
    for m in matches:
        rows += f"""
        <tr>
            <td><strong>{m['company']}</strong></td>
            <td>{m['title']}</td>
            <td><span class="badge">{m['location']}</span></td>
            <td><span class="score">{m['score']}%</span></td>
            <td><a href="{m['url']}" target="_blank" class="btn">Apply Now</a></td>
        </tr>
        """
        
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Active Job Matches (0-2 Yrs, India)</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                background-color: #f4f6f8;
                color: #333;
                margin: 0;
                padding: 20px;
            }}
            .container {{
                max-width: 1000px;
                margin: 0 auto;
                background: white;
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            }}
            h1 {{
                margin-top: 0;
                color: #111;
                border-bottom: 2px solid #eaeaea;
                padding-bottom: 15px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}
            th, td {{
                padding: 14px 16px;
                text-align: left;
                border-bottom: 1px solid #eaeaea;
            }}
            th {{
                background-color: #f7f9fa;
                font-weight: 600;
            }}
            .badge {{
                background-color: #e3f2fd;
                color: #0d47a1;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 12px;
            }}
            .score {{
                font-weight: bold;
                color: #2e7d32;
            }}
            .btn {{
                display: inline-block;
                background-color: #1a73e8;
                color: white;
                padding: 8px 16px;
                text-decoration: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: 500;
            }}
            .btn:hover {{
                background-color: #1557b0;
            }}
            .footer {{
                margin-top: 30px;
                font-size: 12px;
                color: #666;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎯 Active Job Matches (India, 0-2 Yrs)</h1>
            <p>Found <strong>{len(matches)}</strong> matching roles across monitored career pages.</p>
            
            <table>
                <thead>
                    <tr>
                        <th>Company</th>
                        <th>Position</th>
                        <th>Location</th>
                        <th>Match Score</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    {rows if rows else '<tr><td colspan="5" style="text-align:center;">No new jobs found matching criteria.</td></tr>'}
                </tbody>
            </table>
            
            <div class="footer">
                Last updated automatically.
            </div>
        </div>
    </body>
    </html>
    """
    
    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"[Dashboard] Local HTML dashboard created/updated at: {HTML_PATH}")

def run():
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
        
    build_html_dashboard(matches)

if __name__ == "__main__":
    run()
