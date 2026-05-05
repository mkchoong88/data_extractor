import streamlit as st
import pandas as pd
import google.generativeai as genai
from gemini_extractor import process_document_gemini

st.set_page_config(page_title="Document Scanner & Extractor", layout="wide")

with st.sidebar:
    st.header("⚙️ Configuration")
    engine = "Gemini API"
    
    api_key = ""
    selected_model = "gemini-3.1-flash-lite-preview"
    
    if engine == "Gemini API":
        api_key = st.text_input("Gemini API Key", type="password")
        st.markdown("[Get your free API key here](https://aistudio.google.com/)")
        
        if api_key:
            try:
                genai.configure(api_key=api_key)
                models = [m.name.replace('models/', '') for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                good_models = [m for m in models if 'flash' in m or 'pro' in m or 'vision' in m]
                
                if good_models:
                    try:
                        idx = good_models.index(selected_model)
                    except ValueError:
                        idx = 0
                    selected_model = st.selectbox("Select Gemini Model", good_models, index=idx)
                elif models:
                    try:
                        idx = models.index(selected_model)
                    except ValueError:
                        idx = 0
                    selected_model = st.selectbox("Select Gemini Model", models, index=idx)
                else:
                    st.warning("No compatible models found for this API key.")
            except Exception as e:
                st.error(f"Could not load models. Check API key. Error: {e}")
    else:
        st.warning("Offline OCR requires Tesseract to be installed. It may struggle with multi-column layouts and messy photos.")

st.title("📄 Document Scanner & Data Extractor")
st.markdown("Upload **JPEG, PNG, or PDF** files to extract text and specific information into a tabular format.")

uploaded_files = st.file_uploader("Upload Documents", type=["pdf", "png", "jpg", "jpeg"], accept_multiple_files=True)

if uploaded_files:
    if st.button("Process Documents"):
        with st.spinner("Extracting text and analyzing..."):
            results = []
            for file in uploaded_files:
                try:
                    file_bytes = file.read()

                    if not api_key:
                        st.error("Please enter a Gemini API Key in the sidebar.")
                        continue
                    parsed_invoices, raw_text = process_document_gemini(file.name, file_bytes, file.type, api_key, selected_model)

                    results.extend(parsed_invoices)
                except Exception as e:
                    st.error(f"Error processing **{file.name}**: {e}")
            
            if results:
                st.success(f"Successfully extracted {len(results)} invoice(s)!")
                
                df = pd.DataFrame(results)
                
                # Reorder columns to put File Name first
                if "File Name" in df.columns:
                    cols = ["File Name"] + [col for col in df.columns if col != "File Name"]
                    df = df[cols]
                else:
                    st.warning("Could not find 'File Name' in the extracted data. This might be due to a cached module. Please restart the app or clear cache.")
                
                st.subheader("Extracted Data")
                st.dataframe(df, width="stretch")
                
                # csv = df.to_csv(index=False).encode('utf-8')
                # st.download_button(
                #     label="Download Data as CSV",
                #     data=csv,
                #     file_name="extracted_document_data.csv",
                #     mime="text/csv",
                # )
