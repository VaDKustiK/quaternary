import logging
import requests
from bs4 import BeautifulSoup
import re

from tools.models.init_db import init_db, SessionLocal
from tools.models.author import Author, Article

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

BASE_URL = "http://www.ginras.ru/library/papers.php?m=qt&p=0&l=30000"


def scrape_authors():
    logger.info(f"Requesting page: {BASE_URL}")
    response = requests.get(BASE_URL)
    response.encoding = "windows-1251"
    soup = BeautifulSoup(response.text, "html.parser")

    init_db()
    session = SessionLocal()

    # Clear old data
    session.query(Article).delete()
    session.query(Author).delete()
    logger.info("Deleted old authors & articles.")

    count_articles = 0
    count_authors = 0

    for row in soup.select("span.txt"):
        link = row.find("a", href=True)
        if not link:
            continue

        title = link.get_text(strip=True)
        url = link["href"]
        if not url.startswith("http"):
            url = "http://www.ginras.ru/" + url.lstrip("/")

        text = row.get_text(" ", strip=True)
        authors_text = text.replace(title, "").strip(" -—")

        authors = [a.strip() for a in re.split(r",|;", authors_text) if a.strip()]

        for author_name in authors:
            # Get or create author
            author = session.query(Author).filter_by(name=author_name).first()
            if not author:
                author = Author(name=author_name)
                session.add(author)
                session.flush()  # assign id
                count_authors += 1

            # Add article
            article = Article(title=title, url=url, author=author)
            session.add(article)
            count_articles += 1

    session.commit()
    logger.info(f"Saved {count_authors} authors and {count_articles} articles.")


if __name__ == "__main__":
    scrape_authors()