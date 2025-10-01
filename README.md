# 🧑‍💻 Naukri Job Alerts Automation

Automated script to search jobs on [Naukri.com](https://www.naukri.com), scrape job listings, store them in an SQLite database, and send **daily email alerts** for new postings.  

This project combines **web automation (Playwright)**, **data persistence (SQLite)**, and **notifications (SMTP email)** to create a real-world job tracking solution.

Many features are yet to be built but it's a good starting point
---

## ✨ Features
- 🔍 Automates search for jobs (role, experience, location).  
- 📑 Extracts job title, company, posting date, link, and description.  
- 📦 Stores jobs in an SQLite database (avoids duplicates).  
- 🆕 Detects new jobs and only emails fresh postings.  
- 📧 Sends an email alert with job details directly to your inbox.  
- ⏳ Stops scraping once jobs older than a week are reached.  

---

## 🛠️ Tech Stack
- **[Playwright](https://playwright.dev/python/)** → For browser automation and scraping.  
- **SQLite** → Lightweight database for storing job posts.  
- **smtplib** → For sending email notifications.  
- **Python 3.9+**  

---

## ⚡ Setup & Usage

### 1️⃣ Clone the repo
```bash
git clone https://github.com/yourusername/naukri-job-alerts.git
cd naukri-job-alerts
```

2️⃣ Install dependencies
```
pip install playwright sqlite3 smtplib
```

Initialize Playwright:
```
playwright install
```

3️⃣ Configure email

Edit the script and set your Gmail credentials:
```
msg['from'] = "your_email@gmail.com"
msg['to'] = "receiver_email@gmail.com"
smtp.login("your_email@gmail.com", "your_app_password")
```

⚠️ Use a Gmail App Password instead of your real password for security.

4️⃣ Run the script
```
python naukri_job_alerts.py
```

📊 Example Output

Email you receive:

```
New job alerts:

Machine Learning Engineer | ABC Tech
https://www.naukri.com/job-listings-ml-engineer-abc

Data Scientist | XYZ Pvt Ltd
https://www.naukri.com/job-listings-data-scientist-xyz
```

🚀 Future Improvements

*Add config file / CLI arguments (role, location, experience).

*Support HTML email formatting.

*Run script daily using cron (Linux/Mac) or Task Scheduler (Windows).

*Add logging for debugging and monitoring.

Looking forward for contributors

📜 License

MIT License
