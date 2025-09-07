import logging
import re
import requests
from bs4 import BeautifulSoup

from tools.models.init_db import init_db, SessionLocal
from tools.models.author import Author, Article

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

BASE_URL = "http://www.ginras.ru/library/papers.php?m=qt&p=0&l=30000"

NAME_RE = re.compile(
    r"""
    (?P<surname>[А-ЯЁ][а-яё\-]+(?:\s[А-ЯЁ][а-яё\-]+)?)   # surname (maybe double)
    \s+
    (?P<initials>[А-ЯЁ]\.\s?[А-ЯЁ]\.(?:\s?[А-ЯЁ]\.)?)     # initials like A.A. or A.А.Б.
    """,
    re.VERBOSE,
)

SEP_RE = re.compile(r"\s*(?:,|и)\s+")


def parse_line(line: str):
    """
    Extract consecutive author names from the *beginning* of the line.
    Returns (authors: list[str], article_title: str).
    """
    idx = 0
    authors = []

    while True:
        m = NAME_RE.match(line, idx)
        if not m:
            break
        surname = m.group("surname").strip()
        initials = m.group("initials").replace(" ", "")
        authors.append(f"{surname} {initials}")
        idx = m.end()

        sep = SEP_RE.match(line, idx)
        if sep:
            idx = sep.end()
        else:
            break

    if not authors:
        return [], ""

    # Remaining part = supposed to be the article title
    title = line[idx:].strip(" —-–.:\u00a0 ").strip()

    # If the "title" looks like just another name, skip
    if NAME_RE.match(title):
        return authors, ""

    return authors, title


def scrape_authors():
    logger.info(f"Requesting page: {BASE_URL}")
    resp = requests.get(BASE_URL, timeout=60)
    resp.encoding = "windows-1251"
    soup = BeautifulSoup(resp.text, "html.parser")

    init_db()
    session = SessionLocal()

    # Clear old data
    session.query(Article).delete()
    session.query(Author).delete()
    logger.info("Deleted old authors & articles.")

    authors_cache = {}
    count_articles = 0
    count_authors_new = 0

    blocks = soup.select("span.txt")
    logger.info(f"Found {len(blocks)} issue blocks to scan.")

    for span in blocks:
        # --- Issue title + link ---
        link = span.find("a", href=True)
        if not link:
            continue
        issue_title = link.get_text(strip=True)
        issue_pdf_url = link.get("href", "").strip()
        if issue_pdf_url and not issue_pdf_url.startswith("http"):
            issue_pdf_url = "http://www.ginras.ru/" + issue_pdf_url.lstrip("/")

        content_div = span.find("div")
        if not content_div:
            continue

        lines = content_div.get_text("\n", strip=True).splitlines()

        for raw_line in lines:
            line = raw_line.strip()
            if not line:
                continue
            if line.lower().startswith(("содержание", "contents")):
                continue

            authors, article_title = parse_line(line)
            if not authors or not article_title:
                continue

            for name in authors:
                author_obj = authors_cache.get(name)
                if not author_obj:
                    author_obj = session.query(Author).filter_by(name=name).first()
                    if not author_obj:
                        author_obj = Author(name=name)
                        session.add(author_obj)
                        session.flush()
                        count_authors_new += 1
                    authors_cache[name] = author_obj

                # Save article with link and issue context
                session.add(Article(
                    title=f"{article_title} ({issue_title})",
                    url=issue_pdf_url,
                    author=author_obj
                ))
                count_articles += 1

    session.commit()
    logger.info(f"Saved {count_authors_new} authors and {count_articles} author-article links.")


if __name__ == "__main__":
    scrape_authors()
