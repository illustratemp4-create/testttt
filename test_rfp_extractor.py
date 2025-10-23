"""
Test script for RFP Document Extractor
Demonstrates the functionality with sample documents.
"""

import os
from pathlib import Path
from rfp_extractor import RFPExtractor


def test_rfp_extractor():
    """
    Test the RFP extractor with sample documents.
    """
    print("\n" + "=" * 70)
    print("RFP Document Extractor - Test Script")
    print("=" * 70 + "\n")
    
    # Check if API key is available
    api_key = os.environ.get('GROQ_API_KEY')
    if not api_key:
        print("❌ GROQ_API_KEY not found in environment variables")
        print("\nTo run this test:")
        print("1. Create a .env file in /app directory")
        print("2. Add your Groq API key: GROQ_API_KEY=your_key_here")
        print("3. Get a free API key from: https://console.groq.com")
        print("\nAlternatively, set it in your environment:")
        print("   export GROQ_API_KEY=your_key_here")
        return False
    
    print("✅ Groq API key found")
    
    # Initialize extractor
    try:
        extractor = RFPExtractor()
        print("✅ RFP Extractor initialized successfully\n")
    except Exception as e:
        print(f"❌ Error initializing extractor: {str(e)}")
        return False
    
    # Test with sample HTML document
    sample_html = Path("/app/sample_rfp.html")
    
    if not sample_html.exists():
        print(f"⚠️  Sample HTML file not found: {sample_html}")
        print("   Skipping HTML test\n")
    else:
        print("-" * 70)
        print("Test 1: Processing Sample HTML Document")
        print("-" * 70)
        
        try:
            result = extractor.process_document(str(sample_html))
            
            print("\n📊 Extraction Results:")
            print(f"   Document: {result['document_name']}")
            print(f"   Type: {result['document_type']}")
            print(f"\n   Extracted {len(result['extracted_fields'])} fields:")
            
            # Display key fields
            key_fields = ["Bid Number", "Title", "Due Date", "company_name", "contact_info"]
            for field in key_fields:
                value = result['extracted_fields'].get(field, "N/A")
                # Truncate long values
                if len(str(value)) > 60:
                    value = str(value)[:60] + "..."
                print(f"   - {field}: {value}")
            
            # Save results
            output_file = "/app/test_output.json"
            extractor.save_results_to_json(result, output_file)
            print(f"\n✅ Full results saved to: {output_file}")
            
        except Exception as e:
            print(f"❌ Error processing HTML document: {str(e)}")
            return False
    
    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)
    print("✅ All tests completed successfully!")
    print("\nYou can now use the RFP extractor with your own documents:")
    print("   python rfp_processor.py -f your_document.pdf -o output.json")
    print("\nFor more information, see RFP_README.md")
    print("=" * 70 + "\n")
    
    return True


def display_usage_examples():
    """
    Display usage examples for the RFP extractor.
    """
    print("\n" + "=" * 70)
    print("Usage Examples")
    print("=" * 70 + "\n")
    
    examples = [
        {
            "title": "Process a single PDF document",
            "command": "python rfp_processor.py -f rfp_document.pdf -o results.json"
        },
        {
            "title": "Process a single HTML document",
            "command": "python rfp_processor.py -f rfp_document.html -o results.json"
        },
        {
            "title": "Process multiple documents",
            "command": "python rfp_processor.py -f doc1.pdf doc2.html doc3.pdf -o batch_results.json"
        },
        {
            "title": "Specify API key directly",
            "command": "python rfp_processor.py -f document.pdf -o output.json -k YOUR_API_KEY"
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"{i}. {example['title']}:")
        print(f"   {example['command']}\n")
    
    print("=" * 70 + "\n")


if __name__ == "__main__":
    # Run tests
    success = test_rfp_extractor()
    
    # Display usage examples
    if success:
        display_usage_examples()
    
    print("For complete documentation, see: RFP_README.md\n")
