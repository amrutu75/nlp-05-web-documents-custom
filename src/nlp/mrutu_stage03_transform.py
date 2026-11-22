"""src/nlp/stage03_transform.py.

(EDIT YOUR VERSION OF THIS FILE)

Source: validated BeautifulSoup object
Sink: Pandas DataFrame

NOTE: We use Pandas here to contrast with Polars (from Module 4).
You may use Polars or another library if you prefer:
the pipeline pattern is identical; only the DataFrame API differs.

Pandas vs. Polars:
- Pandas is widely used and has a larger ecosystem.
- Polars is faster, more memory efficient, handles larger datasets,
  and is better suited for production pipelines and complex
  transformations.

Purpose

  Transform validated BeautifulSoup object into a structured format.

Analytical Questions

- Which fields are needed from the HTML data?
- How can records be normalized into tabular form?
- What derived fields would support analysis?

How to find the fields you want to extract from the web page:

  1. Open the web page in your browser.
  2. Right-click anywhere on the page and select "View Page Source".
  3. Use Ctrl+F to search for text you can see on the page,
     e.g. the paper title or "Abstract:".
  4. Find the HTML tag and class that wraps it, e.g.:
       <h1 class="title mathjax"><span class="descriptor">Title:</span>
  5. Use soup.find("h1", class_="title") to locate the associated tag.
  6. Use .get_text(strip=True) to extract the visible text from inside the tag.
  7. If the tag contains a descriptor prefix like "Title:" or "Authors:",
     use .replace("Title:", "").strip() to remove it.
  8. If the tag is not found, soup.find() returns None which is not a string.
     To avoid errors, use a conditional expression to return "unknown" as a safe fallback:
       value = tag.get_text(strip=True) if tag else "unknown"

Apply this process for each field you want to extract for analysis.
The same approach works for any web page.

Example: For the arXiv page at https://arxiv.org/abs/2602.20021,
we can extract the following fields using BeautifulSoup:

- title from <h1 class="title"> (string)
- authors from <div class="authors"> (string)
- abstract from <blockquote class="abstract"> (string)
- primary subject from <div class="subheader"> (string)
- submission date from <div class="dateline"> (string)
- arXiv ID from canonical link in the <head> section (string)

we can calculate derived fields like:
- abstract word count (integer)
- author count (integer)

IMPORTANT: Getting information from a web page is not as simple as it looks.
Web pages are designed for human consumption, not for data extraction.
The HTML structure can be complex and inconsistent, and may require careful inspection and handling to extract the desired information.
The title and abstract are wrapped in tags with descriptor text ("Title:", "Abstract:") that must be removed to get clean values.
The authors are listed as multiple <a> tags inside a <div>, so we must extract each author separately and join them with commas to avoid double-comma issues.
The arXiv ID is not directly visible on the page but can be extracted from the canonical link in the HTML head.
This stage requires careful inspection of the HTML structure and thoughtful handling of edge cases to ensure we extract clean, structured data for analysis.

Use all your resources, creativity, and problem-solving skills to navigate the complexities of web data extraction and transformation.

Edit your Python file to change:
- extract the fields needed for your analysis,
- normalize records into a consistent structure,
- create any derived fields required.
"""
# ============================================================
# Section 1. Setup and Imports
# ============================================================

import logging

import bs4
import pandas as pd

# ============================================================
# Section 2. Define Run Transform Function
# ============================================================


def run_transform(
    soup: bs4.BeautifulSoup,
    LOG: logging.Logger,
) -> pd.DataFrame:
    """Transform Books to Scrape HTML into a structured DataFrame.

    Args:
        soup (BeautifulSoup): Validated BeautifulSoup object.
        LOG (logging.Logger): Logger instance.

    Returns:
        pd.DataFrame: Dataset containing book information.
    """
    LOG.info("========================")
    LOG.info("STAGE 03: TRANSFORM starting...")
    LOG.info("========================")

    LOG.info("Extracting book metadata from HTML")

    LOG.info(
        "Fields to extract:"
        "\n- Book Title"
        "\n- Price"
        "\n- Rating"
        "\n- Availability"
        "\n- Generate Analytical Visuals"
        "n- Word Cloud of Book Titles"
        "n- Rating Distribution Chart"
    )

    # ============================================================
    # STAGE 03a: Find All Books
    # ============================================================

    books = soup.find_all("article", class_="product_pod")

    LOG.info(f"Found {len(books)} books")

    records = []

    # ============================================================
    # STAGE 03b: Extract Data for Each Book
    # ============================================================

    for book in books:
        # --------------------------------------------------------
        # TITLE
        # --------------------------------------------------------

        title_tag: bs4.Tag | None = book.find("h3")

        if title_tag:
            link_tag = title_tag.find("a")
            title = link_tag.get("title", "unknown") if link_tag else "unknown"
        else:
            title = "unknown"

        # --------------------------------------------------------
        # PRICE
        # --------------------------------------------------------

        price_tag: bs4.Tag | None = book.find("p", class_="price_color")

        price_text = price_tag.get_text(strip=True) if price_tag else "£0.00"

        price = float(price_text.replace("£", "").replace("Â", ""))

        # --------------------------------------------------------
        # RATING
        # --------------------------------------------------------

        rating_tag: bs4.Tag | None = book.find(
            "p", class_=lambda x: x and "star-rating" in x
        )

        rating = "unknown"

        if rating_tag:
            rating_classes = rating_tag.get("class", [])

            for cls in rating_classes:
                if cls != "star-rating":
                    rating = cls

        # --------------------------------------------------------
        # AVAILABILITY
        # --------------------------------------------------------

        availability_tag: bs4.Tag | None = book.find("p", class_="instock availability")

        availability = (
            availability_tag.get_text(strip=True) if availability_tag else "unknown"
        )

        # --------------------------------------------------------
        # BUILD RECORD
        # --------------------------------------------------------

        record = {
            "title": title,
            "price": price,
            "rating": rating,
            "availability": availability,
        }

        records.append(record)

    # ============================================================
    # STAGE 03c: Create DataFrame
    # ============================================================

    df = pd.DataFrame(records)

    LOG.info(f"Created DataFrame with {len(df)} rows and {len(df.columns)} columns")

    LOG.info(f"Columns: {list(df.columns)}")

    # ============================================================
    # STAGE 03d: Derived Fields For Analysis
    # ============================================================

    rating_counts = df["rating"].value_counts()

    LOG.info("Rating Distribution:")
    LOG.info(f"\n{rating_counts}")

    average_price_by_rating = df.groupby("rating")["price"].mean().round(2)

    LOG.info("Average Price by Rating:")
    LOG.info(f"\n{average_price_by_rating}")

    most_expensive_books = df.sort_values(by="price", ascending=False).head(5)

    LOG.info("Top 5 Most Expensive Books:")
    LOG.info(f"\n{most_expensive_books[['title', 'price']]}")

    LOG.info("Sink: Pandas DataFrame created")

    import matplotlib.pyplot as plt
    from wordcloud import WordCloud

    LOG.info("========================")
    LOG.info("STAGE 03e: Generate Word Cloud")
    LOG.info("========================")

    title_text = " ".join(df["title"].astype(str))

    wordcloud = WordCloud(width=1200, height=600, background_color="white").generate(
        title_text
    )

    plt.figure(figsize=(12, 6))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title("Most Common Words in Book Titles")

    plt.savefig("data/processed/book_title_wordcloud.png", bbox_inches="tight")

    plt.close()

    LOG.info("Word cloud saved.")

    LOG.info("========================")
    LOG.info("STAGE 03f: Generate Rating Distribution")
    LOG.info("========================")

    rating_order = ["One", "Two", "Three", "Four", "Five"]

    rating_counts = df["rating"].value_counts().reindex(rating_order, fill_value=0)

    plt.figure(figsize=(8, 5))

    rating_counts.plot(kind="bar", color="steelblue")

    plt.title("Book Rating Distribution")
    plt.xlabel("Rating")
    plt.ylabel("Number of Books")

    plt.tight_layout()

    plt.savefig("data/processed/rating_distribution.png", bbox_inches="tight")

    plt.close()

    LOG.info("Rating distribution chart saved.")
    LOG.info("Transformation complete.")

    return df
