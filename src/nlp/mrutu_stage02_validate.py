"""src/nlp/stage02_validate.py - Validate Stage.

(EDIT YOUR VERSION OF THIS FILE)

Source: Raw HTML string
Sink:   BeautifulSoup object (in memory)

Purpose

  Validates that the expected page structure is present.

Analytical Questions

- What is the top-level structure of the HTML document?
- What elements are present in the document?
- What data types are associated with each field?
- Does the data meet expectations for transformation?

Edit your Python file to:
- inspect the HTML structure for your API,
- validate the presence of required HTML elements,
- confirm the data is usable for your analysis.
"""

# ============================================================
# Section 1. Setup and Imports
# ============================================================

import logging

from bs4 import BeautifulSoup

# ============================================================
# Section 2. Define Run Validate Function
# ============================================================


def run_validate(
    html_content: str,
    LOG: logging.Logger,
) -> BeautifulSoup:
    """Inspect and validate the HTML structure for Books to Scrape.

    Args:
        html_content (str): Raw HTML downloaded in Stage 01.
        LOG (logging.Logger): Logger instance.

    Returns:
        BeautifulSoup: Validated BeautifulSoup object.
    """
    LOG.info("========================")
    LOG.info("STAGE 02: VALIDATE starting...")
    LOG.info("========================")

    # ============================================================
    # INSPECT HTML STRUCTURE
    # ============================================================

    LOG.info("HTML STRUCTURE INSPECTION:")

    soup = BeautifulSoup(html_content, "html.parser")

    LOG.info(f"Top-level type: {type(soup).__name__}")

    LOG.info(
        f"Top-level elements: "
        f"{[element.name for element in soup.find_all(recursive=False)]}"
    )

    # ============================================================
    # VALIDATE EXPECTED BOOK ELEMENTS
    # ============================================================

    first_book = soup.find("article", class_="product_pod")

    if first_book:
        title = first_book.find("h3")

        price = first_book.find("p", class_="price_color")

        availability = first_book.find("p", class_="instock availability")

        rating = first_book.find("p", class_=lambda x: x and "star-rating" in x)

    else:
        title = None
        price = None
        availability = None
        rating = None

    LOG.info("VALIDATE: Book found: %s", first_book is not None)
    LOG.info("VALIDATE: Title found: %s", title is not None)
    LOG.info("VALIDATE: Price found: %s", price is not None)
    LOG.info("VALIDATE: Rating found: %s", rating is not None)
    LOG.info("VALIDATE: Availability found: %s", availability is not None)

    missing = []

    if not first_book:
        missing.append("product_pod")

    if not title:
        missing.append("title")

    if not price:
        missing.append("price")

    if not rating:
        missing.append("rating")

    if not availability:
        missing.append("availability")

    if missing:
        raise ValueError(
            f"VALIDATE: Required elements missing: {missing}. "
            "Page structure may have changed."
        )

    # Count books discovered on the page

    books = soup.find_all("article", class_="product_pod")

    LOG.info("VALIDATE: %d books found on page.", len(books))

    LOG.info("VALIDATE: HTML structure is valid.")
    LOG.info("Sink: validated BeautifulSoup object")

    return soup
