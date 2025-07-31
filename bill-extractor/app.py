# import re
# import pytesseract
# from PIL import Image
# import pdfplumber
# import os

# def extract_text_from_pdf(pdf_path):
#     text = ""
#     with pdfplumber.open(pdf_path) as pdf:
#         for page in pdf.pages:
#             text += page.extract_text() or ""
#     return text

# def extract_text_from_image(image_path):
#     image = Image.open(image_path)
#     text = pytesseract.image_to_string(image)
#     return text

# def extract_bill_info(text):
#     # Regex patterns for bill amount and account number
#     amount_pattern = r'(?:Total\s*Amount|Amount\s*Due|Bill\s*Amount)\s*[:\-]?\s*(?:\$)?(\d+(?:\.\d{1,2})?)'
#     account_pattern = r'(?:Account\s*Number|A/C\s*No\.?)\s*[:\-]?\s*(\w+)'

#     amount = re.search(amount_pattern, text, re.IGNORECASE)
#     account = re.search(account_pattern, text, re.IGNORECASE)

#     return {
#         "bill_amount": amount.group(1) if amount else "Not Found",
#         "account_number": account.group(1) if account else "Not Found"
#     }

# def extract_from_document(file_path):
#     ext = os.path.splitext(file_path)[1].lower()
#     if ext in [".pdf"]:
#         text = extract_text_from_pdf(file_path)
#     elif ext in [".png", ".jpg", ".jpeg"]:
#         text = extract_text_from_image(file_path)
#     else:
#         return "Unsupported file format"

#     return extract_bill_info(text)

# # Test
# if __name__ == "__main__":
#     file_path = "sample.pdf"  # Replace with your document
#     result = extract_from_document(file_path)
#     print("Bill Amount:", result["bill_amount"])
#     print("Account Number:", result["account_number"])
import streamlit as st
import re
import pytesseract
import pdfplumber
from PIL import Image
import os

st.set_page_config(page_title="Bill Info Extractor", page_icon="📄")

st.title("📄 Bill Info Extractor")
st.write("Upload a **PDF** or **Image** file to extract Bill Amount and Account Number.")

# --- Functions ---
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def extract_text_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

def extract_bill_info(text):
    amount_pattern = r'(?:Total\s*Amount|Amount\s*Due|Bill\s*Amount)\s*[:\-]?\s*\$?(\d+(?:\.\d{1,2})?)'
    account_pattern = r'(?:Account\s*Number|A/C\s*No\.?)\s*[:\-]?\s*(\w+)'
    amount = re.search(amount_pattern, text, re.IGNORECASE)
    account = re.search(account_pattern, text, re.IGNORECASE)

    return {
        "Bill Amount": amount.group(1) if amount else "Not Found",
        "Account Number": account.group(1) if account else "Not Found"
    }

# --- File Upload ---
uploaded_file = st.file_uploader("Upload your bill document", type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file is not None:
    temp_path = os.path.join("temp_" + uploaded_file.name)
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("✅ File uploaded successfully!")

    # Show preview if image
    if uploaded_file.name.lower().endswith(("png", "jpg", "jpeg")):
        st.image(temp_path, caption="Uploaded Bill", use_column_width=True)

    # Process button
    if st.button("🔍 Extract Bill Information"):
        with st.spinner("Extracting information..."):
            text = extract_text_from_pdf(temp_path) if uploaded_file.name.endswith("pdf") else extract_text_from_image(temp_path)
            result = extract_bill_info(text)

        st.subheader("📌 Extracted Details:")
        st.write(f"**Bill Amount:** {result['Bill Amount']}")
        st.write(f"**Account Number:** {result['Account Number']}")

        os.remove(temp_path)
