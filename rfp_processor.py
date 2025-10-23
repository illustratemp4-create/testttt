"""
RFP Processor - CLI Interface
Command-line interface for processing RFP documents and extracting structured information.
"""

import argparse
import sys
from pathlib import Path
from rfp_extractor import RFPExtractor


def main():
    parser = argparse.ArgumentParser(
        description='Extract structured information from RFP documents (PDF/HTML)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process a single document
  python rfp_processor.py -f document.pdf -o output.json

  # Process multiple documents
  python rfp_processor.py -f doc1.pdf doc2.html doc3.pdf -o results.json

  # Specify API key directly
  python rfp_processor.py -f document.pdf -o output.json -k YOUR_API_KEY
        """
    )
    
    parser.add_argument(
        '-f', '--files',
        nargs='+',
        required=True,
        help='Path(s) to RFP document file(s) (PDF or HTML)'
    )
    
    parser.add_argument(
        '-o', '--output',
        default='rfp_extracted_data.json',
        help='Output JSON file path (default: rfp_extracted_data.json)'
    )
    
    parser.add_argument(
        '-k', '--api-key',
        help='Groq API key (optional if GROQ_API_KEY is set in environment)'
    )
    
    args = parser.parse_args()
    
    # Validate input files
    print("\n" + "=" * 60)
    print("RFP Document Information Extractor")
    print("=" * 60)
    
    valid_files = []
    for file_path in args.files:
        path = Path(file_path)
        if not path.exists():
            print(f"✗ Error: File not found: {file_path}")
            continue
        
        if path.suffix.lower() not in ['.pdf', '.html', '.htm']:
            print(f"✗ Error: Unsupported file type: {file_path}")
            print("  Supported formats: PDF, HTML")
            continue
        
        valid_files.append(str(path))
    
    if not valid_files:
        print("\n✗ No valid files to process. Exiting.")
        sys.exit(1)
    
    print(f"\n✓ Found {len(valid_files)} valid file(s) to process")
    
    # Initialize extractor
    try:
        extractor = RFPExtractor(api_key=args.api_key)
        print("✓ Groq API initialized successfully")
    except ValueError as e:
        print(f"\n✗ Error: {e}")
        print("Please provide API key via -k flag or set GROQ_API_KEY in environment")
        sys.exit(1)
    
    print("\n" + "-" * 60)
    
    # Process documents
    if len(valid_files) == 1:
        # Single document
        print(f"Processing single document...\n")
        try:
            result = extractor.process_document(valid_files[0])
            extractor.save_results_to_json(result, args.output)
            print(f"\n✓ Successfully processed 1 document")
        except Exception as e:
            print(f"\n✗ Error processing document: {str(e)}")
            sys.exit(1)
    else:
        # Multiple documents
        print(f"Processing {len(valid_files)} documents...\n")
        results = extractor.process_multiple_documents(valid_files)
        extractor.save_results_to_json(results, args.output)
        
        # Summary
        successful = sum(1 for r in results if 'error' not in r)
        failed = len(results) - successful
        print(f"\n✓ Successfully processed: {successful}/{len(results)} documents")
        if failed > 0:
            print(f"✗ Failed: {failed} documents")
    
    print("\n" + "=" * 60)
    print(f"Results saved to: {args.output}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
