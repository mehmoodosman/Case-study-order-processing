import os
import streamlit as st
import PyPDF2
import io
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Sales Order Extractor", page_icon="📜", layout="wide")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

EXTRACTION_PROMPT = """You are a data extraction specialist. Extract the following information from the provided sales order document and email content.

Extract EXACTLY these fields in the format shown below. If a field is not found, write "Not found".

Expected output format:
Buyer:
• buyer_company_name: [extracted value]
• buyer_person_name: [extracted value]
• buyer_email_address: [extracted value]

Order:
• order_number: [extracted value]
• order_date: [extracted value]
• delivery_address_street: [extracted value]
• delivery_address_city: [extracted value]
• delivery_address_postal_code: [extracted value]

Product: (repeat for each product)
• position: [extracted value]
• article_code: [extracted value]
• quantity: [extracted value]

---
DOCUMENT CONTENT:
{pdf_content}

---
EMAIL CONTENT:
{email_content}

---
Extract the data now in the exact format specified above:"""


def extract_pdf_text(pdf_file) -> str:
    """Extract text from uploaded PDF file."""
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file.read()))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text.strip()


def call_claude_opus(api_key: str, pdf_content: str, email_content: str) -> str:
    """Call Claude Opus 4.5 via OpenRouter API."""
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    
    prompt = EXTRACTION_PROMPT.format(
        pdf_content=pdf_content or "No PDF content provided",
        email_content=email_content or "No email content provided"
    )
    
    response = client.chat.completions.create(
        model="anthropic/claude-opus-4",
        messages=[{"role": "user", "content": prompt}],
    )
    
    return response.choices[0].message.content


def main():
    st.title("📜 Sales Order Data Extractor")
    st.markdown("Extract structured data from sales order PDFs and emails using Claude Opus 4.5")
    
    if not OPENROUTER_API_KEY:
        st.error("OPENROUTER_API_KEY not found in .env file")
        return
    
    # Main content area
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📄 PDF Document")
        pdf_file = st.file_uploader("Upload Sales Order PDF", type=["pdf"])
        pdf_content = ""
        if pdf_file:
            try:
                pdf_content = extract_pdf_text(pdf_file)
                with st.expander("Preview extracted PDF text"):
                    st.text(pdf_content[:2000] + "..." if len(pdf_content) > 2000 else pdf_content)
            except Exception as e:
                st.error(f"Error reading PDF: {e}")
    
    with col2:
        st.subheader("📧 Sales Email")
        email_content = st.text_area(
            "Paste sales email content",
            height=300,
            placeholder="Paste the sales email content here..."
        )
    
    st.divider()
    
    # Extract button
    if st.button("🔍 Extract Data", type="primary", use_container_width=True):
        if not pdf_content and not email_content:
            st.error("Please provide at least a PDF document or email content")
            return
        
        with st.spinner("Extracting data with Claude Opus 4.5..."):
            try:
                result = call_claude_opus(OPENROUTER_API_KEY, pdf_content, email_content)
                st.subheader("📋 Extracted Data")
                st.markdown(result)
                
                # Copy button
                st.download_button(
                    label="📥 Download Results",
                    data=result,
                    file_name="extracted_data.txt",
                    mime="text/plain"
                )
            except Exception as e:
                st.error(f"Error calling API: {e}")


if __name__ == "__main__":
    main()
