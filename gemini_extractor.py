import google.generativeai as genai
import json
import re

def process_document_gemini(file_name, file_bytes, mime_type, api_key, model_name="gemini-1.5-flash"):
    """
    Process a document using the Gemini API.
    Returns a list of parsed dictionaries and the raw text response.
    """
    if not api_key:
        raise ValueError("Gemini API key is missing. Please provide it in the sidebar.")
        
    genai.configure(api_key=api_key)
    
    # Use the selected model
    model = genai.GenerativeModel(model_name)
    
    prompt = """
    You are an expert document data extractor. I have provided a document that may contain one or multiple invoices/packing slips/documents.
    Please extract the following information for EACH document you find in the image/PDF:
    1. Company Name (usually found under 'Invoice Address', 'Deliver to', or 'Bill to')
    2. Attention (usually found under 'Attention:' or similar)
    3. Delivery Address (usually found under 'Delivery Address' or 'Deliver to' or 'Ship to'. IMPORTANT: Do not include the postcode or the country name. E.g. '163 Tanglin Road, Unit, #03-128 Tanglin Mall')
    4. Invoice Number (usually found near 'Invoice Number', 'Duplicate Tax Invoice INV/...'. IMPORTANT: Extract ONLY the last 4 digits of the invoice number. E.g. if it is 'SPG-2821' or 'INV/2026/2819', return only '2821' or '2819')
    
    Return the result strictly as a JSON array of objects. 
    Each object must have exactly these keys: "Company Name", "Attention", "Delivery Address", "Invoice Number".
    Do not include markdown blocks like ```json in the output, just raw JSON.
    If you cannot find a field, use "Not Found".
    """
    
    try:
        # Generate content
        response = model.generate_content([
            {'mime_type': mime_type, 'data': file_bytes},
            prompt
        ])
        
        raw_output = response.text
        
        # Clean up the output in case the model wrapped it in markdown
        cleaned_json = re.sub(r'```(?:json)?\s*', '', raw_output)
        cleaned_json = re.sub(r'\s*```$', '', cleaned_json)
        
        try:
            parsed_invoices = json.loads(cleaned_json)
        except json.JSONDecodeError:
            # Fallback if the output isn't pure JSON
            raise ValueError(f"Failed to parse JSON from Gemini. Raw output: {raw_output}")
        
        # Ensure it's a list
        if isinstance(parsed_invoices, dict):
            parsed_invoices = [parsed_invoices]
            
        # Inject File Name into each parsed result
        for inv in parsed_invoices:
            inv["File Name"] = file_name
            
        return parsed_invoices, raw_output
        
    except Exception as e:
        raise Exception(f"Gemini API Error: {e}")
