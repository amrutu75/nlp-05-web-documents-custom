# Web Mining and Applied NLP Project Report

Web Mining and Applied NLP | Project 05 | Report

Agnes Mrutu | November 2026| Report for nlp-05-web-documents-custom

## Document and source URL
https://books.toscrape.com/
.

## Tools and Methods

The project uses:

- Python for pipeline orchestration and processing.
- Requests for retrieving HTML documents.
- BeautifulSoup for parsing and inspecting HTML.
- HTML selectors for locating document content.
- Validation checks for confirming required elements.
- Pandas for structured data transformation.
- CSV for persistent output.
- Logging for execution records.
- Ruff, ty, and pytest for code verification.
- Zensical and GitHub Pages for published documentation.
- WordCloud for generating text-based visual insights

## Analytical Questions for extraction
The pipeline preserves the original HTML and produces a structured CSV dataset containing extracted metadata.
For the actual assignment, data is retrived from Booktore website (https://books.toscrape.com/). The website (source document) containes information such as:

Book title
Price
Rating
Availability
Analytical Questions:

Which rating appears most often? What is the average price by rating? Which books are the most expensive?



## Data Transformation

Extracted book metadata from HTML 20 books were found on the page with created Dataframe with 20 rows and 4 columns.


## Interpretation

Books found: 20
Field extracted:
- Book Title
- Price
- Rating
- Availability
- Generated Analytical Visualization

![Word Cloud](data/processed/book_title_wordcloud.png)
![Word Cloud](data/processed/rating_distribution.png)



### Project Data Insights

This project demonstrated how to build an EVTL (Extract, Validate, Transform, Load) pipeline to collect and analyze book information from the Books to Scrape website. The pipeline successfully extracted book titles, prices, ratings, and availability from HTML pages using BeautifulSoup and transformed the data into a structured dataset for analysis.

The rating distribution analysis revealed which rating categories were most common among the books listed on the website, providing insight into the overall quality distribution of the catalog. By comparing prices across ratings, it was possible to explore whether highly rated books tended to be priced differently than lower-rated books.

A Word Cloud generated from book titles highlighted frequently occurring words and themes, making it easier to identify common topics and patterns within the collection. This visualization provided a quick overview of recurring keywords that would be difficult to recognize from tabular data alone.

Overall, the addition of visualizations improved data interpretation by presenting trends and patterns in a clear and intuitive manner. The project illustrated how web scraping, data transformation, and visualization can work together to convert unstructured web content into meaningful analytical insights.
