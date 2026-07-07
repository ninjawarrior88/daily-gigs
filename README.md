# RemoteGigs — Automated Remote Job Aggregator

A self-updating remote freelance job board that earns money through affiliate commissions.

## How it works (fully automated)

1. **GitHub Actions** runs `scrape.py` every day at 6 AM UTC (free)
2. **scrape.py** fetches 150-200+ freelance jobs from 3 sources
3. **Jobs are saved** as `data/jobs.json` and committed to the repo
4. **GitHub Pages** serves the site (free, fast, global CDN)
5. **Affiliate links** earn commissions when visitors sign up on freelancing platforms

## Setup (5 minutes, zero cost)

### Step 1: Create a GitHub repository

1. Go to https://github.com/new
2. Repository name: `daily-gigs` (or anything you like)
3. Keep it **Public** (required for free GitHub Pages)
4. Click "Create repository"

### Step 2: Push the code

Open **Command Prompt** (cmd) or **PowerShell** and run:

```bash
cd C:\Users\Dell\Documents\project1\daily_gigs
git init
git add .
git commit -m "initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/daily-gigs.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

### Step 3: Enable GitHub Pages

1. Go to your repo on GitHub
2. Click **Settings** → **Pages**
3. Under "Source", select **GitHub Actions**
4. Done.

### Step 4: Run the scraper manually (first time)

1. Go to your repo → **Actions** tab
2. Click **Scrape Jobs and Deploy** workflow
3. Click **Run workflow** → **Run workflow**
4. Wait ~2 minutes for it to complete
5. After that, visit `https://YOUR_USERNAME.github.io/daily-gigs`

The site will now auto-update every day at 6 AM UTC.

## Monetization

The site earns through:
- **Affiliate links** to Upwork, Fiverr, Freelancer, Toptal, PeoplePerHour
- **Tool recommendations** (Namecheap, NordVPN, etc.)
- **Email list** (collect subscribers for future monetization)
- **AdSense** ready (add your AdSense code later)

## Custom domain (optional)

1. Buy a domain (Namecheap ~$10/year)
2. In your repo Settings → Pages, enter your custom domain
3. Add a CNAME record pointing to `YOUR_USERNAME.github.io`

## File structure

```
daily-gigs/
├── index.html          # Homepage (job listings)
├── about.html          # About page
├── tools.html          # Tools & recommendations page
├── style.css           # Styles
├── script.js           # Frontend logic
├── scrape.py           # Python scraper (runs via GitHub Actions)
├── requirements.txt    # Python dependencies
├── _config.yml         # GitHub Pages config
├── .github/workflows/
│   └── scrape-and-deploy.yml  # Auto-scrape + deploy
└── data/               # Auto-generated job data
```

## No maintenance needed

- ✅ Scraping runs automatically
- ✅ Site updates automatically
- ✅ Affiliate links are always active
- ✅ No hosting costs
- ✅ No server to manage

Just share the link and let it earn.
