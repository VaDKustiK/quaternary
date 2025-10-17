# Bulletin of the Commission for Study of the Quaternary (BCSQ)

**Live Website:** [https://quaternary.ru/](https://quaternary.ru/)
**Repository:** `https://github.com/VaDKustiK/quaternary`
**Branch:** `dev`

---

## Overview

The **Quaternary Journal Web Portal** is a modern web application built for the *Bulletin of the Commission for Study of the Quaternary* — an academic journal of the **Russian Academy of Sciences (RAS)**.
It serves as a digital platform for publishing and accessing scientific issues, editorial board information, author submissions, and licensing documentation.

The project aims to provide a clean, multilingual, and accessible interface for both readers and contributors of the *Bulletin of the Commission for Study of the Quaternary*.

---

## Main Features

### Journal Archive

* Dynamic archive of all journal issues grouped by year.
* Each issue links directly to its PDF publication.
* Accordion layout for easy navigation.

### Author Directory

* Automatically scraped and updated author database.
* Each author page lists only their own published works (linked to issue PDFs).
* Powered by the `author_scraper.py` script using BeautifulSoup and SQLAlchemy.

### Editorial Board

* Complete list of editors and institutions.
* Presented in a card-based layout with sidebar navigation.

### License Agreement & Terms of Use

* Interactive PDF viewer embedded directly on the page.
* Downloadable version available for offline reference.

### Manuscript Submission

* Dedicated “Submit” page with email-based submission system.
* Instructions for authors on manuscript preparation.

### Multilingual Support (Flask-Babel)

* Seamless internationalization with English and Russian translations.

### Responsive Design

* Built with **Bootstrap 5**, ensuring accessibility and consistency across devices.

---

## Technology Stack

| Layer            | Technology                                       |
| ---------------- | ------------------------------------------------ |
| **Backend**      | Flask (Python)                                   |
| **Frontend**     | HTML5, CSS3, Bootstrap 5, Jinja2                 |
| **Database**     | SQLite (local), SQLAlchemy ORM                   |
| **Localization** | Flask-Babel                                      |
| **Scraping**     | Requests, BeautifulSoup4                         |
| **Hosting**      | [https://quaternary.ru/](https://quaternary.ru/) |

---

## How It Works

1. **Backend**:
   Flask serves as the main framework handling routing, rendering templates, and localization.

2. **Database Initialization**:
   The `tools/models/` directory defines ORM models for `Author`, `Article`, and related entities.

3. **Data Scraping**:
   `author_scraper.py` and `archive_scraper.py` scripts fetch the list of authors and publications directly from the GIN RAS website using BeautifulSoup.

   ```bash
   python -m tools.author_scraper # or tools.archive_scraper
   ```

4. **Templates**:
   The Jinja2 templates use a base layout (`base.html`) and structured sidebar includes for consistent design across all pages.

5. **Localization (Babel)**:
   Translation files (`messages.po`, `messages.mo`) are stored under `translations/`.
   Use:

   ```bash
   flask babel extract -F babel.cfg -o messages.pot .
   flask babel update -i messages.pot -d translations
   flask babel compile -d translations
   ```

6. **Hosting**:
   The live version is hosted at [quaternary.ru](https://quaternary.ru/).

---

## License

This project and website are part of the **Bulletin of the Commission for Study of the Quaternary (RAS)** digital modernization initiative.
© Geological Institute RAS, 2025. All rights reserved.