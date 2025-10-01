import smtplib

from playwright.sync_api import sync_playwright
import sqlite3
from email.mime.text import MIMEText

def send_email(new_jobs):
    if not new_jobs:
        print("No new jobs found today")
        return
    body = "New job alerts:\n\n"
    for job in new_jobs:
        body += f"{job['title']} | {job['company']}\n{job['url']}\n\n"

    msg = MIMEText(body)
    msg['subject'] = "Daily job Alert"
    msg['from'] = ""
    msg['to'] = ""

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login()
        smtp.send_message(msg)
    print("Email sent successfully")

def create_connection(db_file="jobs.db"):
    return sqlite3.connect(db_file)

def create_table(conn):
    sql_create_jobs_table = """
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        company TEXT NOT NULL,
        posted TEXT,
        url TEXT UNIQUE,
        description TEXT
    );
"""
    conn.execute(sql_create_jobs_table)
    conn.commit()

def insert_job(conn, job):
    sql_insert = """
        INSERT OR IGNORE INTO jobs (title, company, posted, url, description) 
    VALUES (?, ?, ?, ?, ?)
    """
    cursor = conn.execute(sql_insert, (job['title'], job['company'], job['posted'], job['url'], job['description']))
    conn.commit()
    return cursor.rowcount

def run():

    conn = create_connection()
    create_table(conn)

    counter = 1
    new_jobs = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.naukri.com", wait_until="domcontentloaded")

        print("Successfully opened naukri.com")

        # Fill role/skill input
        page.wait_for_selector('input[placeholder="Enter skills / designations / companies"]')
        page.fill('input[placeholder="Enter skills / designations / companies"]', 'machine learning')

        # Click experience dropdown and select 2 years
        page.click('input#expereinceDD')
        page.click('li >> text="2 years"')

        # Fill location
        page.fill('input[placeholder="Enter location"]', 'Bengaluru')

        # Press Enter to submit
        page.press('input[placeholder="Enter location"]', 'Enter')

        print("Search submitted. Waiting to inspect results.")
        # page.wait_for_timeout(10000)  # Wait for 10 seconds to observe the result

        page.wait_for_selector('button#filter-sort')

        page.click('button#filter-sort')

        page.wait_for_selector('a[data-id="filter-sort-f"]')

        page.click('a[data-id="filter-sort-f"]')

        print("Sorted jobs be date")

        # page.wait_for_timeout(10000)

        #pagination loop

        while True:
            page.wait_for_selector('div.cust-job-tuple')

            stop_scraping = False

            job_cards = page.query_selector_all('div.cust-job-tuple')

            for job in job_cards:
                try:
                    title_element = job.query_selector('h2 a.title')
                    if title_element is None:
                        print("Skipping job: missing title element")
                        continue
                    title = title_element.inner_text().strip()
                    company = job.query_selector('a.comp-name').inner_text().strip()
                    posted = job.query_selector('.job-post-day').inner_text().strip().lower()

                    print(f"{title} | {company} | ({posted})")
                    url = title_element.get_attribute('href')
                    if not url:
                        print(f"Skipping job '{title}' due to missing URL")
                        continue

                    job_page = browser.new_page()
                    job_page.goto(url, wait_until='domcontentloaded')

                    job_page.wait_for_selector('section.styles_job-desc-container__txpYf')
                    description_section = job_page.query_selector('section.styles_job-desc-container__txpYf')
                    description = description_section.inner_text().strip()

                    job_page.close()

                    job_to_add = {"title": title, "company": company, "posted": posted, "url": url, "description":description}
                    if insert_job(conn, job_to_add):
                        new_jobs.append(job_to_add)

                    if "1 day" in posted or "1 week" in posted or "2 weeks" in posted or "month" in posted or "30" in posted:
                        stop_scraping = True
                        break
                except Exception as e:
                    print("Failed to extract job posting: ", e)

            if stop_scraping:
                print("\nReached jobs older than 1 week. Stopped scraping.")
                break

            try:
                next_button = page.query_selector('a[title="Next"]') or page.query_selector('a >> text="Next"')
                if next_button and next_button.is_enabled():
                    next_button.click()
                    page.wait_for_timeout(2000)
                else:
                    print("No more pages found")
                    break
            except Exception as e:
                print("Error clicking next: ", e)
                break

        print("\nDone scraping. ")
        send_email(new_jobs)
        page.wait_for_timeout(50000)

if __name__ == '__main__':
    run()
