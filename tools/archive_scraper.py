import logging
import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import re

# Logging setup
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
# logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s') # in case if smth breaks
logger = logging.getLogger(__name__)

# SQLAlchemy setup
Base = declarative_base()

class Issue(Base):
    __tablename__ = 'issues'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    pdf_url = Column(String, nullable=False)
    detail_url = Column(String, nullable=False)
    content_html = Column(String, nullable=True)

    def __repr__(self):
        return f"<Issue(title='{self.title}', year={self.year})>"

# Database init
def init_db():
    engine = create_engine('sqlite:///issues.db')
    Base.metadata.create_all(engine)
    logger.info("Database initialized.")
    return engine

# Scraper
def scrape_issues():
    base_url = 'http://www.ginras.ru/library/papers.php?m=qt&p=0&l=30000'
    logger.info(f"Requesting main page: {base_url}")
    response = requests.get(base_url)
    response.encoding = 'windows-1251'
    soup = BeautifulSoup(response.text, 'html.parser')

    issue_spans = soup.select('span.txt')
    logger.info(f"Found {len(issue_spans)} issue blocks.")

    engine = init_db()
    Session = sessionmaker(bind=engine)
    session = Session()

    # ⚠️ Wipe existing issues
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

            # Extract year from title
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