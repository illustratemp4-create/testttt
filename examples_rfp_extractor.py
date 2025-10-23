"""
Advanced Examples for RFP Extractor
Demonstrates programmatic usage patterns and integration scenarios.
"""

from rfp_extractor import RFPExtractor
from pathlib import Path
import json


def example_1_basic_extraction():
    """
    Example 1: Basic extraction from a single document
    """
    print("\n" + "=" * 70)
    print("Example 1: Basic Extraction")
    print("=" * 70 + "\n")
    
    # Initialize extractor
    extractor = RFPExtractor()
    
    # Process document
    result = extractor.process_document("sample_rfp.html")
    
    # Access extracted data
    print(f"Document: {result['document_name']}")
    print(f"Bid Number: {result['extracted_fields']['Bid Number']}")
    print(f"Title: {result['extracted_fields']['Title']}")
    print(f"Due Date: {result['extracted_fields']['Due Date']}")
    
    # Save results
    extractor.save_results_to_json(result, "example1_output.json")


def example_2_batch_processing():
    """
    Example 2: Process multiple documents and generate a summary report
    """
    print("\n" + "=" * 70)
    print("Example 2: Batch Processing with Summary Report")
    print("=" * 70 + "\n")
    
    extractor = RFPExtractor()
    
    # List of documents to process
    documents = [
        "sample_rfp.html",
        # Add more document paths here
    ]
    
    # Process all documents
    results = extractor.process_multiple_documents(documents)
    
    # Generate summary report
    print("\nBatch Processing Summary:")
    print("-" * 70)
    
    successful = 0
    failed = 0
    
    for result in results:
        if 'error' in result:
            print(f"❌ {result['document_name']}: FAILED")
            print(f"   Error: {result['error']}")
            failed += 1
        else:
            print(f"✅ {result['document_name']}: SUCCESS")
            bid_num = result['extracted_fields'].get('Bid Number', 'N/A')
            print(f"   Bid Number: {bid_num}")
            successful += 1
    
    print(f"\nTotal: {successful} successful, {failed} failed")
    
    # Save batch results
    extractor.save_results_to_json(results, "example2_batch_output.json")


def example_3_filtered_extraction():
    """
    Example 3: Extract and filter specific fields of interest
    """
    print("\n" + "=" * 70)
    print("Example 3: Filtered Field Extraction")
    print("=" * 70 + "\n")
    
    extractor = RFPExtractor()
    
    # Process document
    result = extractor.process_document("sample_rfp.html")
    
    # Define fields of interest
    important_fields = [
        'Bid Number',
        'Title',
        'Due Date',
        'company_name',
        'contact_info',
        'Bid Summary'
    ]
    
    # Create filtered output
    filtered_data = {
        'document_name': result['document_name'],
        'key_information': {}
    }
    
    for field in important_fields:
        filtered_data['key_information'][field] = result['extracted_fields'].get(field, 'N/A')
    
    # Display filtered data
    print("Key Information Extracted:")
    print("-" * 70)
    for field, value in filtered_data['key_information'].items():
        # Truncate long values
        display_value = str(value)[:80] + "..." if len(str(value)) > 80 else value
        print(f"{field:30}: {display_value}")
    
    # Save filtered results
    with open("example3_filtered_output.json", 'w') as f:
        json.dump(filtered_data, f, indent=2)
    
    print("\nFiltered results saved to: example3_filtered_output.json")


def example_4_comparison_report():
    """
    Example 4: Compare multiple RFP documents side-by-side
    """
    print("\n" + "=" * 70)
    print("Example 4: RFP Comparison Report")
    print("=" * 70 + "\n")
    
    extractor = RFPExtractor()
    
    # Process multiple documents
    documents = [
        "sample_rfp.html",
        # Add more documents to compare
    ]
    
    results = extractor.process_multiple_documents(documents)
    
    # Fields to compare
    comparison_fields = [
        'Bid Number',
        'Title',
        'Due Date',
        'Bid Bond Requirement',
        'Payment Terms'
    ]
    
    # Create comparison table
    print("RFP Comparison Table:")
    print("=" * 70)
    
    for field in comparison_fields:
        print(f"\n{field}:")
        print("-" * 70)
        for result in results:
            if 'error' not in result:
                doc_name = result['document_name']
                value = result['extracted_fields'].get(field, 'N/A')
                # Truncate for display
                display_value = str(value)[:50] + "..." if len(str(value)) > 50 else value
                print(f"  {doc_name:30}: {display_value}")


def example_5_export_to_csv():
    """
    Example 5: Export extracted data to CSV format
    """
    print("\n" + "=" * 70)
    print("Example 5: Export to CSV")
    print("=" * 70 + "\n")
    
    import csv
    
    extractor = RFPExtractor()
    
    # Process documents
    documents = ["sample_rfp.html"]
    results = extractor.process_multiple_documents(documents)
    
    # Prepare CSV data
    csv_file = "example5_rfp_data.csv"
    
    # Get all field names
    all_fields = ['Document Name'] + extractor.EXPECTED_FIELDS
    
    # Write to CSV
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=all_fields)
        writer.writeheader()
        
        for result in results:
            if 'error' not in result:
                row = {'Document Name': result['document_name']}
                row.update(result['extracted_fields'])
                writer.writerow(row)
    
    print(f"✅ Data exported to: {csv_file}")


def example_6_custom_processing():
    """
    Example 6: Custom post-processing of extracted data
    """
    print("\n" + "=" * 70)
    print("Example 6: Custom Post-Processing")
    print("=" * 70 + "\n")
    
    from datetime import datetime
    
    extractor = RFPExtractor()
    result = extractor.process_document("sample_rfp.html")
    
    # Custom processing: Check if deadline is approaching
    extracted = result['extracted_fields']
    
    print("Custom Analysis:")
    print("-" * 70)
    
    # 1. Check for urgent deadlines (simplified - just check if "August" is in date)
    due_date = extracted.get('Due Date', '')
    if due_date and due_date != 'N/A':
        print(f"⏰ Due Date: {due_date}")
        # In real implementation, parse date and compare with current date
    
    # 2. Check if bid bond is required
    bid_bond = extracted.get('Bid Bond Requirement', 'N/A')
    if bid_bond and bid_bond != 'N/A' and bid_bond != 'Not specified':
        print(f"💰 Bid Bond Required: {bid_bond}")
        print("   → Action: Prepare financial guarantee")
    
    # 3. Check if pre-bid meeting scheduled
    pre_bid = extracted.get('Pre Bid Meeting', 'N/A')
    if pre_bid and pre_bid != 'N/A' and pre_bid != 'Not specified':
        print(f"📅 Pre-Bid Meeting: {pre_bid}")
        print("   → Action: Add to calendar")
    
    # 4. Identify required documentation
    additional_docs = extracted.get('Any Additional Documentation Required', 'N/A')
    if additional_docs and additional_docs != 'N/A' and additional_docs != 'Not specified':
        print(f"📄 Additional Documents: {additional_docs}")
        print("   → Action: Prepare required documentation")


def main():
    """
    Run all examples (uncomment individual examples to run them)
    """
    print("\n" + "=" * 70)
    print("RFP Extractor - Advanced Examples")
    print("=" * 70)
    
    # Uncomment the examples you want to run:
    
    # example_1_basic_extraction()
    # example_2_batch_processing()
    # example_3_filtered_extraction()
    # example_4_comparison_report()
    # example_5_export_to_csv()
    # example_6_custom_processing()
    
    print("\n" + "=" * 70)
    print("To run examples, uncomment them in the main() function")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
