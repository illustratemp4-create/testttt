"""
RFP Document Information Extractor
Extracts structured information from HTML and PDF documents related to RFP processes.
"""

import os
import json
from typing import Dict, Any, Union
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
import fitz  # PyMuPDF
from bs4 import BeautifulSoup

load_dotenv()


class RFPExtractor:
    """
    Extracts structured RFP information from HTML and PDF documents using LLM.
    """
    
    # Define the expected fields to extract from RFP documents
    EXPECTED_FIELDS = [
        "Bid Number",
        "Title",
        "Due Date",
        "Bid Submission Type",
        "Term of Bid",
        "Pre Bid Meeting",
        "Installation",
        "Bid Bond Requirement",
        "Delivery Date",
        "Payment Terms",
        "Any Additional Documentation Required",
        "MFG for Registration",
        "Contract or Cooperative to use",
        "Model_no",
        "Part_no",
        "Product",
        "contact_info",
        "company_name",
        "Bid Summary",
        "Product Specification"
    ]
    
    def __init__(self, api_key: str = None):
        """
        Initialize the RFP Extractor with Groq API client.
        
        Args:
            api_key: Groq API key. If not provided, will use GROQ_API_KEY from environment.
        """
        self.api_key = api_key or os.environ.get('GROQ_API_KEY')
        if not self.api_key:
            raise ValueError("GROQ_API_KEY must be provided or set in environment variables")
        
        self.client = Groq(api_key=self.api_key)
    
    def extract_text_from_pdf(self, file_path: str) -> str:
        """
        Extract text content from a PDF file.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Extracted text as a string
        """
        try:
            doc = fitz.open(file_path)
            text = ""
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                text += page.get_text("text")
            
            doc.close()
            return text.strip()
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    def extract_text_from_html(self, file_path: str) -> str:
        """
        Extract text content from an HTML file.
        
        Args:
            file_path: Path to the HTML file
            
        Returns:
            Extracted text as a string
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            soup = BeautifulSoup(html_content, 'lxml')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text and clean it up
            text = soup.get_text()
            
            # Break into lines and remove leading/trailing space on each
            lines = (line.strip() for line in text.splitlines())
            
            # Break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            
            # Drop blank lines
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            return text
        except Exception as e:
            raise Exception(f"Error extracting text from HTML: {str(e)}")
    
    def extract_text_from_file(self, file_path: str) -> str:
        """
        Extract text from either PDF or HTML file based on extension.
        
        Args:
            file_path: Path to the document file
            
        Returns:
            Extracted text as a string
        """
        file_extension = Path(file_path).suffix.lower()
        
        if file_extension == '.pdf':
            return self.extract_text_from_pdf(file_path)
        elif file_extension in ['.html', '.htm']:
            return self.extract_text_from_html(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}. Only PDF and HTML are supported.")
    
    def extract_rfp_information(self, text: str) -> Dict[str, Any]:
        """
        Use LLM to extract structured RFP information from text.
        
        Args:
            text: Extracted text from the document
            
        Returns:
            Dictionary containing extracted RFP information
        """
        # Create a prompt for the LLM to extract structured information
        prompt = f"""You are an expert at extracting structured information from RFP (Request for Proposal) documents.

Extract the following information from the provided document text. For each field, provide the exact value found in the document. If a field is not found or not applicable, use "N/A" or "Not specified" as the value.

Required Fields:
1. Bid Number
2. Title
3. Due Date
4. Bid Submission Type
5. Term of Bid
6. Pre Bid Meeting
7. Installation
8. Bid Bond Requirement
9. Delivery Date
10. Payment Terms
11. Any Additional Documentation Required
12. MFG for Registration
13. Contract or Cooperative to use
14. Model_no
15. Part_no
16. Product
17. contact_info
18. company_name
19. Bid Summary
20. Product Specification

Document Text:
{text[:12000]}

Please provide the extracted information in the following JSON format:
{{
    "Bid Number": "value",
    "Title": "value",
    "Due Date": "value",
    "Bid Submission Type": "value",
    "Term of Bid": "value",
    "Pre Bid Meeting": "value",
    "Installation": "value",
    "Bid Bond Requirement": "value",
    "Delivery Date": "value",
    "Payment Terms": "value",
    "Any Additional Documentation Required": "value",
    "MFG for Registration": "value",
    "Contract or Cooperative to use": "value",
    "Model_no": "value",
    "Part_no": "value",
    "Product": "value",
    "contact_info": "value",
    "company_name": "value",
    "Bid Summary": "value",
    "Product Specification": "value"
}}

Return ONLY the JSON object without any additional text or explanation."""

        try:
            # Use Groq LLM to extract information
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at extracting structured information from documents. Always respond with valid JSON only."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                temperature=0.1,  # Low temperature for more consistent extraction
            )
            
            response_text = chat_completion.choices[0].message.content.strip()
            
            # Try to parse the JSON response
            # Sometimes LLMs add markdown code blocks, so we need to clean that
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            response_text = response_text.strip()
            
            extracted_data = json.loads(response_text)
            
            # Ensure all expected fields are present
            for field in self.EXPECTED_FIELDS:
                if field not in extracted_data:
                    extracted_data[field] = "Not specified"
            
            return extracted_data
            
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {str(e)}")
            print(f"Response text: {response_text}")
            # Return a template with "Error extracting" for all fields
            return {field: "Error extracting" for field in self.EXPECTED_FIELDS}
        except Exception as e:
            raise Exception(f"Error extracting information with LLM: {str(e)}")
    
    def process_document(self, file_path: str) -> Dict[str, Any]:
        """
        Process a single RFP document and extract structured information.
        
        Args:
            file_path: Path to the document file (PDF or HTML)
            
        Returns:
            Dictionary containing extracted RFP information with metadata
        """
        file_path = str(file_path)
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        print(f"Processing document: {file_path}")
        
        # Extract text from document
        print("  - Extracting text...")
        text = self.extract_text_from_file(file_path)
        
        print(f"  - Extracted {len(text)} characters")
        
        # Extract structured information using LLM
        print("  - Extracting structured information with LLM...")
        rfp_data = self.extract_rfp_information(text)
        
        # Add metadata
        result = {
            "document_name": Path(file_path).name,
            "document_type": Path(file_path).suffix.lower(),
            "extracted_fields": rfp_data
        }
        
        print("  - Extraction complete!")
        
        return result
    
    def process_multiple_documents(self, file_paths: list) -> list:
        """
        Process multiple RFP documents.
        
        Args:
            file_paths: List of paths to document files
            
        Returns:
            List of dictionaries containing extracted information for each document
        """
        results = []
        
        for file_path in file_paths:
            try:
                result = self.process_document(file_path)
                results.append(result)
            except Exception as e:
                print(f"Error processing {file_path}: {str(e)}")
                results.append({
                    "document_name": Path(file_path).name,
                    "error": str(e)
                })
        
        return results
    
    def save_results_to_json(self, results: Union[Dict, list], output_path: str):
        """
        Save extraction results to a JSON file.
        
        Args:
            results: Extracted data (single document or list of documents)
            output_path: Path where the JSON file will be saved
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\nResults saved to: {output_path}")


def main():
    """
    Example usage of the RFP Extractor.
    """
    print("RFP Document Information Extractor")
    print("=" * 50)
    
    # Initialize extractor
    try:
        extractor = RFPExtractor()
        print("✓ Groq API initialized successfully\n")
    except ValueError as e:
        print(f"✗ Error: {e}")
        print("Please set GROQ_API_KEY in your .env file or environment variables")
        return
    
    # Example: Process a single document
    # Uncomment and modify the path to test with your documents
    """
    file_path = "path/to/your/rfp_document.pdf"
    result = extractor.process_document(file_path)
    extractor.save_results_to_json(result, "rfp_output.json")
    """
    
    # Example: Process multiple documents
    """
    file_paths = [
        "path/to/document1.pdf",
        "path/to/document2.html",
        "path/to/document3.pdf"
    ]
    results = extractor.process_multiple_documents(file_paths)
    extractor.save_results_to_json(results, "rfp_batch_output.json")
    """
    
    print("\nTo use this extractor, uncomment the example code in the main() function")
    print("or import the RFPExtractor class in your own script.")


if __name__ == "__main__":
    main()
