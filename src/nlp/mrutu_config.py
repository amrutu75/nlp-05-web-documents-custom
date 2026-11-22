"""src/nlp/config.py - Module Configuration.

Purpose

  Orchestrate an EVTL pipeline to scrape book data from a web page, validate the HTML structure, extract book titles, prices, and ratings using BeautifulSoup, transform the data into a structured format, and load the results into a CSV file for analysis.

Analytical Questions:

Which rating appears most often?
What is the average price by rating?
Which books are the most expensive?

Edit your Python file to change:
- PAGE_URL (source of the HTML web page document),
- customize your output file name.
"""

from pathlib import Path

# ============================================================
# API CONFIGURATION
# ============================================================

# TODO: In your custom app, change the URL to work with a different page.
PAGE_URL: str = "https://books.toscrape.com/"
# Designed specifically for practicing web scraping.

# Let them know who we are (and that we're doing educational web mining).
HTTP_REQUEST_HEADERS: dict = {
    "User-Agent": "Mozilla/5.0 (educational-use; web-mining-course)"
}

# ============================================================
# PATH CONFIGURATION
# ============================================================

ROOT_PATH: Path = Path.cwd()
DATA_PATH: Path = ROOT_PATH / "data"
RAW_PATH: Path = DATA_PATH / "raw"
PROCESSED_PATH: Path = DATA_PATH / "processed"

# TODO: In your custom app, change the output file names from case_
# to something that represents YOUR custom project.
RAW_HTML_PATH: Path = RAW_PATH / "mrutu_raw.html"
PROCESSED_CSV_PATH: Path = PROCESSED_PATH / "mrutu_processed.csv"
