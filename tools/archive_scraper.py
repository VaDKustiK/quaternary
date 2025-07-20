import logging
import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
import re

from tools.models.init_db import engine, init_db, SessionLocal
from tools.models.issue import Issue

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

def scrape_issues():
    base_url = 'http://www.ginras.ru/library/papers.php?m=qt&p=0&l=30000'
    logger.info(f"Requesting main page: {base_url}")
    response = requests.get(base_url)
    response.encoding = 'windows-1251'
    soup = BeautifulSoup(response.text, 'html.parser')

    issue_spans = soup.select('span.txt')
    logger.info(f"Found {len(issue_spans)} issue blocks.")

    init_db()
    session = SessionLocal()

    session.query(Issue).delete()
    logger.info("Deleted all previous issues.")

    for span in issue_spans:
        try:
            link = span.find('a', href=re.compile(r'\.pdf$'))
            if not link:
                logger.warning("No PDF link found in span. Skipping.")
                continue

            pdf_url = link['href'].strip()
            if not pdf_url.startswith('http'):
                pdf_url = 'http://www.ginras.ru' + pdf_url

            title = link.get_text(separator=' ', strip=True)
            match = re.search(r'(\d{4})', title)
            year = int(match.group(1)) if match else 0

            content_div = span.find('div')
            content_html = str(content_div) if content_div else None

            issue = Issue(
                title=title,
                year=year,
                pdf_url=pdf_url,
                detail_url=pdf_url,
                content_html=content_html
            )

            session.add(issue)
            logger.info(f"Saved: {title} ({year})")

        except Exception as e:
            logger.error(f"Failed to parse issue span: {e}")

    session.commit()
    logger.info("All issues scraped and saved.")

if __name__ == '__main__':
    scrape_issues()