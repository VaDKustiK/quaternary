# Bulletin of the Commission for Study of the Quaternary (BCSQ)

**Live Website:** [https://quaternary.ru/](https://quaternary.ru/)
**Repository:** `https://github.com/VaDKustiK/quaternary`
**Branch:** `dev`

Это английская версия README. Вы можете прочитать русскую версию [здесь](README.md)

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

* Seamless internationalization with Russian source templates and English translations.

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

5. **Update PDF files**:
   To replace an existing PDF:

   1. Go to `./static/pdf`.
   2. Place the updated PDF file in that folder.
   3. Copy the filename of the PDF that needs to be replaced, for example `terms_of_use_quaternary.pdf`.
   4. Delete the outdated PDF.
   5. Rename the new PDF so it uses the same filename as the old one.

   If you prefer to update it from the page itself, go to `./templates/`, find the page where the PDF is linked, and change the filename there as needed.

6. **Localization (Babel)**:
   The translation workflow is one-way: Russian text is the source, and English is maintained as the translated output.

   Translation files are stored under `translations/`, with English strings in `translations/en/LC_MESSAGES/messages.po`.

   When you add or change translated text, follow this sequence:

   1. Edit the Russian text in the templates.
   2. Extract and refresh translation messages:

      ```bash
      pybabel extract -F babel.cfg -o messages.pot .
      pybabel update -i messages.pot -d translations
      ```

   3. Add the new English translations in `translations/en/LC_MESSAGES/messages.po`.
   4. Compile the translation catalog:

      ```bash
      pybabel compile -d translations
      ```

   Repeat this flow whenever template text changes so the English version stays in sync with the Russian source.

7. **Hosting**:
   The live version is hosted at [quaternary.ru](https://quaternary.ru/).

---

## License

This project and website are part of the **Bulletin of the Commission for Study of the Quaternary (RAS)** digital modernization initiative.
© Geological Institute RAS, 2025. All rights reserved.