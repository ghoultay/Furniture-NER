# Furniture-NER

**Furniture-NER** is a web application designed to scrape product information from URLs and recognize named entities related to furniture using Spark NLP. The application extracts product data, processes it with Named Entity Recognition (NER), and returns a list of products.

## Features

- **Web Scraping**: Scrapes product details from a given URL.
- **Named Entity Recognition (NER)**: Identifies furniture-related entities in the scraped text using Spark NLP.
- **Custom NER Model**: A specialized NER model built with Spark NLP to detect product names, brands, and other relevant information.

### Prerequisites

- Python 3.10+
- Apache Spark
- Spark NLP
- Java 8

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/ghoultay/Furniture-NER.git
   cd Furniture-NER
