# Glassdoor job scraper # todo

This project web scrapes the popular job listing site "Glassdoor" for information from job listings

- Functions without any authentication e.g. user sign-ins/ API tokens and keys. Users simply modifies a config file to provide:
  - A 'base url' to scrape from, based on desired job role and country.
  - A 'target job size' i.e. number of individual job listings to scrape from.
- Script scrapes:
  - Job link, role, company and job description from glassdoor job listing results.
- Information collected are accessible to users in the form of an output csv.
- Script has been tested and verified to be working as expected for a job with:
  - A target job size of < 2000 individual listings,
  - Multiple pages > 10 pages of job listing links.

## Extracted data # todo

![](https://github.com/kelvinxuande/glassdoor-scraper/blob/master/docs/def-3.jpg)

## Purpose # todo

1. A means of collecting unstructured data of job descriptions provided in job listings.
   - Data collected can then be analysed and visualised to generate useful insights
2. With some technical knowledge and [familiarity on how it works](https://github.com/kelvinxuande/glassdoor-scraper/blob/master/docs/README.md#how-it-works), developers can:
   - Modify the script to work for other job listing sites with similar layouts.
   - Incorporate this script into their own data science pipelines and workflows

## Prerequisites

## Usage

1.
2.

## Future work
