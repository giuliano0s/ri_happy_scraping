# Ri Happy Web Scraper

This is a web scraping tool that collects product data from [https://www.rihappy.com.br/](https://www.rihappy.com.br/), one of Brazil’s largest toy and children’s products retailers (similar to Toys"R"Us).

The script extracts product information such as name, price, link, and categories, and stores everything into a structured CSV file (`ri_happy.csv`).

> ⚠️ Note: This scraper was built in 2023. As of 2025, the site layout may have changed, so some parts of the script might need adjustments to run properly.

## Output
The output file `ri_happy.csv` (included in the repository) contains:
- 20,000+ unique product entries
- Structured fields ready for analysis or automation
- Suitable for price tracking, product mapping, or category analysis

## How to run
1. Clone this repository
2. Install the required dependencies (`Selenium`, `pandas`, etc.)
3. Run the script to start scraping data from Ri Happy
4. The result will be saved as `ri_happy.csv`

## Example use cases
- Competitive pricing research
- E-commerce product data enrichment
- Toy market trend analysis
