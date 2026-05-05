# 📄 AI Document Scanner & Data Extractor (Gemini API)

A powerful Python application built with Streamlit that uses Google's Gemini AI to extract structured data (Company Name, Attention, Delivery Address, Invoice Number, custom quantity) from photos, scans, and PDFs of invoices or packing slips.

## 🌐 Live Demo
You can access the hosted version of this app without any installation here:
**[👉 Access the AI Document Scanner](https://data-extractor-app.streamlit.app/)**

## 🚀 Features

- **Intelligent Extraction:** Uses Google's gemini-3.1-flash-lite-preview model to handle messy, rotated, or low-contrast photos with human-level accuracy.
- **Smart Data Formatting:**
  - Automatically extracts only the last 4 digits of invoice numbers.
  - Intelligently strips postcodes and country names from addresses.
  - Specifically captures "Attention" fields.
  - Only count quantity from specific invoice slip.
  - Can process multiple invoice slips in one photo.
- **Multi-Document Support:** Process multiple documents/invoices from a single uploaded file.
- **Data Export:** Download your extracted data directly as a CSV file for use in Excel or other tools.

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/mkchoong88/data_extractor.git
cd data_extractor
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Get a Gemini API Key
To use this application, you need a free API key from [Google AI Studio](https://aistudio.google.com/). 

## 🚦 How to Run

1. Start the Streamlit application:
   ```bash
   streamlit run app.py --server.port 8501
   ```
2. Open your browser to `http://localhost:8501`.
3. Paste your **Gemini API Key** into the sidebar.
4. Upload your documents and click **Process Documents**.

## 📁 Project Structure

- `app.py`: The main Streamlit web interface.
- `gemini_extractor.py`: Integration with the Google Generative AI SDK for data extraction.
- `requirements.txt`: List of necessary Python libraries.

## ⚖️ License
MIT License - feel free to use and modify for your own projects!
