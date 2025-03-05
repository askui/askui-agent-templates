from askui import VisionAgent
import fitz  # PyMuPDF
import pandas as pd
import os
import base64
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))  # Set your API key as environment variable

def encode_image_to_base64(image_path):
    """Convert image to base64 string for OpenAI API"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def extract_with_openai(image_path):
    """Extract data from an image using OpenAI vision capabilities"""
    base64_image = encode_image_to_base64(image_path)
    
    # Define what data to extract with a more specific prompt for invoice data
    prompt = """
    Please extract the following information from this invoice PDF:
    
    HEADER INFORMATION:
    1. Rechnungsnummer (Invoice number) - This appears once at the top of the invoice
    2. Rechnungsdatum (in format dd.MM.YYYY) - This appears once at the top of the invoice
    
    LINE ITEMS:
    For each product line/item in the invoice table, extract:
       - Menge (Quantity)
       - Nettogewicht (Net weight in kg)
       - Bruttogewicht (Gross weight in kg)
       - Article_nummer (Article number/product code)
       - Total_price (Total price for the item)
       - Description (Item description/Bezeichnung)
    
    Be thorough and extract EVERY line item in the table.
    
    Format your response as a structured JSON object with these fields.
    Include the header information at the top level, and all line items in an array called "items".
    If any field is not found, use null for the value.
    """
    
    # Call OpenAI API
    response = client.chat.completions.create(
        model="gpt-4.5-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}",
                            "detail": "high"
                        }
                    }
                ]
            }
        ],
        max_tokens=2000
    )
    
    # Extract the response
    return response.choices[0].message.content

def extract_data_from_pdf(pdf_path, use_openai=True):
    """Extract data from PDF using OpenAI or AskUI vision capabilities"""
    extracted_data = []
    
    # Open the PDF
    pdf_document = fitz.open(pdf_path)
    
    # Process with OpenAI
    if use_openai:
        # For each page in the PDF
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            
            # Get the page as an image
            pix = page.get_pixmap()
            img_path = f"temp_page_{page_num}.png"
            pix.save(img_path)
            
            # Extract data using OpenAI
            ai_response = extract_with_openai(img_path)
            
            # Add to our dataset
            extracted_data.append({
                "page": page_num + 1,
                "content": ai_response,
                "pdf_name": os.path.basename(pdf_path)
            })
            
            # Clean up the temporary image
            os.remove(img_path)
    
    
    return extracted_data

def process_ai_responses(extracted_data, use_openai=True):
    """Process AI responses into a structured format for Excel"""
    import json
    import re
    
    if use_openai:
        all_items = []
        pdf_data = {}  # Group data by PDF name
        
        for item in extracted_data:
            content = item["content"]
            pdf_name = item["pdf_name"]
            
            if pdf_name not in pdf_data:
                pdf_data[pdf_name] = []
            
            # Try to parse the content as JSON
            try:
                # Look for JSON in the text
                json_match = re.search(r'```json\s*([\s\S]*?)\s*```', content)
                if json_match:
                    content = json_match.group(1)
                
                # Parse the response
                data = json.loads(content)
                
                # Extract invoice details (header information)
                invoice_details = {
                    "Rechnungsnummer": data.get("Rechnungsnummer", ""),
                    "Date": data.get("date", "")
                }
                
                # Extract line items
                if "items" in data and isinstance(data["items"], list):
                    for line_item in data["items"]:
                        item_data = {
                            "Rechnungsnummer": invoice_details["Rechnungsnummer"],
                            "Date": invoice_details["Date"],
                            "Menge": line_item.get("Menge", ""),
                            "Nettogewicht": line_item.get("Nettogewicht", ""),
                            "Bruttogewicht": line_item.get("Bruttogewicht", ""),
                            "Article_nummer": line_item.get("Article_nummer", ""),
                            "Total_price": line_item.get("Total_price", ""),
                            "Description": line_item.get("description", "")
                        }
                        pdf_data[pdf_name].append(item_data)
                else:
                    # Fallback if no items array
                    item_data = {
                        "Rechnungsnummer": data.get("Rechnungsnummer", ""),
                        "Date": data.get("date", ""),
                        "Menge": data.get("Menge", ""),
                        "Nettogewicht": data.get("Nettogewicht", ""),
                        "Bruttogewicht": data.get("Bruttogewicht", ""),
                        "Article_nummer": data.get("Article_nummer", ""),
                        "Total_price": data.get("Total_price", ""),
                        "Description": data.get("description", "")
                    }
                    pdf_data[pdf_name].append(item_data)
                
            except (json.JSONDecodeError, AttributeError):
                # If JSON parsing fails, log the raw content
                print(f"Could not parse JSON from page {item['page']} of {pdf_name}. Using raw text.")
                pdf_data[pdf_name].append({
                    "Page": item["page"],
                    "Raw Content": content,
                    "Parsing Error": "Could not extract structured data"
                })
        
        return pdf_data
    else:
        # For AskUI processing
        pdf_data = {}
        for item in extracted_data:
            pdf_name = item["pdf_name"]
            if pdf_name not in pdf_data:
                pdf_data[pdf_name] = []
                
            pdf_data[pdf_name].append({
                "Page": item["page"],
                "Text": item.get("text", ""),
                "Tables": item.get("tables", ""),
            })
        return pdf_data

def save_to_excel(data, excel_path):
    """Save extracted data to Excel file with multiple sheets (one per PDF)"""
    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        for pdf_name, items in data.items():
            # Create a sheet name from the PDF filename (Excel has a 31 character limit for sheet names)
            sheet_name = os.path.splitext(pdf_name)[0]
            if len(sheet_name) > 31:
                sheet_name = sheet_name[:28] + "..."
            
            df = pd.DataFrame(items)
            
            # Reorder columns for better readability if using the structured format
            if 'Rechnungsnummer' in df.columns:
                column_order = [
                    'Rechnungsnummer', 'Date', 'Article_nummer', 'Description',
                    'Menge', 'Nettogewicht', 'Bruttogewicht', 'Total_price'
                ]
                # Only include columns that exist
                existing_columns = [col for col in column_order if col in df.columns]
                # Add any remaining columns that weren't in our preferred order
                remaining_columns = [col for col in df.columns if col not in column_order]
                final_column_order = existing_columns + remaining_columns
                
                df = df[final_column_order]
            
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    print(f"Data saved to {excel_path}")

def process_pdf_folder(folder_path, excel_path, use_openai=True):
    """Process all PDFs in a folder and save results to a single Excel file with multiple sheets"""
    all_data = {}
    
    # Get all PDF files in the folder
    pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print(f"No PDF files found in {folder_path}")
        return
    
    print(f"Found {len(pdf_files)} PDF files to process...")
    
    # Process each PDF
    for pdf_file in pdf_files:
        pdf_path = os.path.join(folder_path, pdf_file)
        print(f"Processing {pdf_file}...")
        
        # Extract data from the PDF
        extracted_data = extract_data_from_pdf(pdf_path, use_openai)
        
        # Process the extracted data
        processed_data = process_ai_responses(extracted_data, use_openai)
        
        # Add to our collection
        all_data.update(processed_data)
    
    # Save all data to Excel
    save_to_excel(all_data, excel_path)
    print(f"All {len(pdf_files)} PDFs processed and saved to {excel_path}")

# Main execution
if __name__ == "__main__":
    pdf_folder = "pdfs"  # Folder containing your PDF files
    excel_path = "extraction.xlsx"  # Output Excel file path
    use_openai = True  # Set to False to use AskUI instead
    
    # Process all PDFs in the folder
    process_pdf_folder(pdf_folder, excel_path, use_openai)

    

