# Sales Order Data Extractor

A Streamlit application that extracts structured data from sales order PDFs and emails using Claude Opus 4.5 via OpenRouter API.

## Features

- Upload sales order PDFs for text extraction
- Paste sales email content
- Extract structured buyer, order, and product information using AI
- Download extracted data as text file

## Setup

1. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your OpenRouter API key:
```
OPENROUTER_API_KEY=your_api_key_here
```

4. Run the app:
```bash
streamlit run app.py
```

## Extracted Data Format

The app extracts the following fields:

**Buyer:**
- buyer_company_name
- buyer_person_name
- buyer_email_address

**Order:**
- order_number
- order_date
- delivery_address_street
- delivery_address_city
- delivery_address_postal_code

**Product (for each item):**
- position
- article_code
- quantity
