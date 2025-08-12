# Tyre Web Scraper

## Description

A scraper that scrapes tyre data from National.co.uk using BeautifulSoup, stores them on Replit's key-value pair database and exports the database to a CSV file or multiple.

## Features

Automatic and manual options. Scrape from list of tyre inputs on database or enter inputs manually. Search with or without postcodes. Option to export CSV or not. Database designed to enable additional features, such as look-up by tyre id capability (scalability). Self-documented (maintainability).

## Database

Key-value pair, document model using the following structure to increase readability, scalability and efficiency:



```
product : {
  "225-50-16": {
        '2255016CTW1H': [
                      'national.co.uk', 'Continental Tyres',
                      'ContiWinterContact TS 830 P', '225/50 R16 92H', '', '£264.99'
                  ],
        '2255016MN9Y': [
                      'national.co.uk', 'Michelin Tyres', 'Michelin Pilot Sport',
                      '225/50 R16 92Y', '', '£402.99'
                  ]
  }
}
```

For more efficiency I considered the following, but concluded it would reduce readability, scalability and future features:


```
product : {
  "225-50-16": {
    "site" : ["national.co.uk", etc.],
    "Brand": ["Michelin", "Avon", etc.]
  }
```

I could have added a relational structure to reduce redundancy and increase efficiency. But this would create greater complexity and reduce readability. Perhaps, it would be worth it and I would like to try and add it in the future. This would require programmatically enumerating repeat site, brand, size and pattern data into separate dictionaries with unique index/integer keys, imitating SQL relational databases. Then instead of repeating strings throughout the database, I would input the corresponding indices/integers much like foreign keys.

## Time-Management

7 1/2 hours.

## Challenges

No major challenges. Had to review some old builds of mine and research the CSV module somewhat. Minimal AI Assistance.

## Working example here:

https://replit.com/@DoulosIYXY/WebScraper?v=1
