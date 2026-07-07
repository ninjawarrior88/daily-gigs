import requests
import json
import os
import re
import xml.etree.ElementTree as ET
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
KEYWORDS = ["python", "javascript", "web developer", "freelance", "remote", "content writer", "virtual assistant", "data entry", "full stack", "react", "node", "design", "marketing", "writing", "customer support", "admin"]


def clean_html(text):
    return re.sub(r'<[^>]+>', '', text).strip() if text else ""


def matches_keywords(text):
    text_lower = text.lower()
    for kw in KEYWORDS:
        if kw.lower() in text_lower:
            return True
    return False


def fetch_weworkremotely():
    try:
        resp = requests.get("https://weworkremotely.com/remote-jobs.rss", timeout=20)
        jobs = []
        root = ET.fromstring(resp.content)
        for item in root.findall(".//item"):
            title = item.findtext("title", "")
            desc = clean_html(item.findtext("description", ""))
            url = item.findtext("link", "")
            date = item.findtext("pubDate", "")
            company = ""
            dc = item.find("{http://purl.org/dc/elements/1.1/}creator")
            if dc is not None:
                company = dc.text or ""
            if not matches_keywords(f"{title} {desc} {company}"):
                continue
            jobs.append({
                "title": title.strip(),
                "company": company.strip(),
                "location": "Remote",
                "url": url.strip(),
                "description": desc[:500],
                "date": date.strip(),
                "source": "WeWorkRemotely"
            })
        return jobs
    except Exception as e:
        print(f"  WeWorkRemotely error: {e}")
        return []


def fetch_remoteok():
    try:
        resp = requests.get("https://remoteok.com/api", timeout=20, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        if resp.status_code != 200:
            return []
        data = resp.json()
        jobs = []
        for item in data[1:]:
            title = item.get("position", "") or ""
            desc = clean_html(item.get("description", "") or "")
            company = item.get("company", "") or ""
            slug = item.get("slug", "")
            date = item.get("date", "") or ""
            if not matches_keywords(f"{title} {desc} {company}"):
                continue
            jobs.append({
                "title": title.strip(),
                "company": company.strip(),
                "location": "Remote",
                "url": f"https://remoteok.com/remote-jobs/{slug}" if slug else "",
                "description": desc[:500],
                "date": date,
                "source": "RemoteOK"
            })
        return jobs
    except Exception as e:
        print(f"  RemoteOK error: {e}")
        return []


def fetch_remotive():
    try:
        resp = requests.get("https://remotive.com/api/remote-jobs", timeout=20, headers={
            "User-Agent": "Mozilla/5.0"
        })
        if resp.status_code != 200:
            return []
        data = resp.json()
        jobs = []
        for item in data.get("jobs", []):
            title = item.get("title", "") or ""
            desc = clean_html(item.get("description", "") or "")
            company = item.get("company_name", "") or ""
            url = item.get("url", "") or ""
            date = item.get("publication_date", "") or ""
            salary = item.get("salary", "") or ""
            tags = item.get("tags", []) or []
            job_type = item.get("job_type", "") or ""
            location = item.get("candidate_required_location", "Remote") or "Remote"
            if not matches_keywords(f"{title} {desc} {company} {' '.join(tags)} {job_type}"):
                continue
            desc_text = f"[{salary}] {desc[:400]}" if salary else desc[:500]
            jobs.append({
                "title": title.strip(),
                "company": company.strip(),
                "location": location.strip(),
                "url": url.strip(),
                "description": desc_text,
                "date": date.strip(),
                "source": "Remotive"
            })
        return jobs
    except Exception as e:
        print(f"  Remotive error: {e}")
        return []


def main():
    print(f"Scraping freelance jobs - {datetime.now().isoformat()}")

    all_jobs = []

    print("Fetching WeWorkRemotely...")
    all_jobs.extend(fetch_weworkremotely())

    print("Fetching RemoteOK...")
    all_jobs.extend(fetch_remoteok())

    print("Fetching Remotive...")
    all_jobs.extend(fetch_remotive())

    all_jobs.sort(key=lambda j: j.get("date", ""), reverse=True)

    os.makedirs(DATA_DIR, exist_ok=True)
    filepath = os.path.join(DATA_DIR, "jobs.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(all_jobs, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(all_jobs)} jobs to {filepath}")

    print(f"Saved {len(all_jobs)} jobs to {filepath}")
    print("Done.")


if __name__ == "__main__":
    main()
