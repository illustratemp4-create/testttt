# 📄 RFP Document Information Extractor

A Python program that extracts structured information from Request for Proposals (RFP) documents in PDF and HTML formats using AI-powered extraction with Groq LLM.

## 🎯 Overview

This tool processes RFP documents and automatically extracts 20 key fields into a structured JSON format, making it easy to analyze and compare multiple proposals.

## ✨ Features

- 📑 **Multi-format Support**: Process both PDF and HTML documents
- 🤖 **AI-Powered Extraction**: Uses Groq's LLM for intelligent information extraction
- 📊 **Structured Output**: Generates clean JSON files with standardized fields
- 🔄 **Batch Processing**: Handle multiple documents at once
- 🎯 **Comprehensive Field Extraction**: Extracts 20 predefined RFP-related fields
- 💻 **CLI Interface**: Easy-to-use command-line tool

## 📋 Extracted Fields

The program extracts the following information from RFP documents:

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

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- Groq API key (get one from https://console.groq.com)

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Dependencies

The program requires the following Python packages:

- `beautifulsoup4` - HTML parsing
- `lxml` - HTML/XML processing
- `PyMuPDF` (fitz) - PDF text extraction
- `groq` - Groq API client for LLM
- `python-dotenv` - Environment variable management

## ⚙️ Configuration

### Set up your Groq API Key

**Option 1: Environment Variable (Recommended)**

Create a `.env` file in the project directory:

```bash
GROQ_API_KEY=your_groq_api_key_here
```

**Option 2: Command Line**

Pass the API key directly when running the program:

```bash
python rfp_processor.py -f document.pdf -o output.json -k YOUR_API_KEY
```

## 💻 Usage

### Command Line Interface

#### Process a Single Document

```bash
python rfp_processor.py -f rfp_document.pdf -o extracted_data.json
```

#### Process Multiple Documents

```bash
python rfp_processor.py -f doc1.pdf doc2.html doc3.pdf -o batch_results.json
```

#### Specify API Key

```bash
python rfp_processor.py -f document.pdf -o output.json -k YOUR_GROQ_API_KEY
```

### Command Line Arguments

- `-f, --files`: Path(s) to RFP document file(s) (required)
- `-o, --output`: Output JSON file path (default: `rfp_extracted_data.json`)
- `-k, --api-key`: Groq API key (optional if set in environment)

### Programmatic Usage

You can also use the `RFPExtractor` class directly in your Python code:

```python
from rfp_extractor import RFPExtractor

# Initialize the extractor
extractor = RFPExtractor()

# Process a single document
result = extractor.process_document("path/to/rfp_document.pdf")

# Save results to JSON
extractor.save_results_to_json(result, "output.json")

# Process multiple documents
file_paths = ["doc1.pdf", "doc2.html", "doc3.pdf"]
results = extractor.process_multiple_documents(file_paths)
extractor.save_results_to_json(results, "batch_output.json")
```

## 📤 Output Format

### Single Document Output

```json
{
  "document_name": "rfp_document.pdf",
  "document_type": ".pdf",
  "extracted_fields": {
    "Bid Number": "RFP-2025-001",
    "Title": "IT Infrastructure Upgrade",
    "Due Date": "2025-08-15",
    "Bid Submission Type": "Electronic",
    "Term of Bid": "90 days",
    "Pre Bid Meeting": "2025-07-01 at 10:00 AM",
    "Installation": "Within 30 days of award",
    "Bid Bond Requirement": "5% of bid amount",
    "Delivery Date": "2025-09-30",
    "Payment Terms": "Net 30",
    "Any Additional Documentation Required": "Company certifications, references",
    "MFG for Registration": "Not specified",
    "Contract or Cooperative to use": "State Contract ABC-123",
    "Model_no": "XYZ-5000",
    "Part_no": "P123456",
    "Product": "Network switches and routers",
    "contact_info": "procurement@example.com, (555) 123-4567",
    "company_name": "Example Corporation",
    "Bid Summary": "Comprehensive network infrastructure upgrade...",
    "Product Specification": "Detailed specs available in attachment A"
  }
}
```

### Multiple Documents Output

```json
[
  {
    "document_name": "rfp1.pdf",
    "document_type": ".pdf",
    "extracted_fields": { ... }
  },
  {
    "document_name": "rfp2.html",
    "document_type": ".html",
    "extracted_fields": { ... }
  }
]
```

## 🔧 Technical Details

### Architecture

1. **Document Parser**
   - PDF: Uses PyMuPDF (fitz) for text extraction
   - HTML: Uses BeautifulSoup4 with lxml parser

2. **LLM Integration**
   - Model: `meta-llama/llama-4-scout-17b-16e-instruct` via Groq
   - Temperature: 0.1 (for consistent extraction)
   - Context window: Up to 12,000 characters

3. **Extraction Process**
   - Text extraction from document
   - Structured prompt to LLM with predefined fields
   - JSON parsing and validation
   - Error handling and fallback mechanisms

### Supported File Formats

- **PDF**: `.pdf`
- **HTML**: `.html`, `.htm`

## 🐛 Troubleshooting

### Common Issues

**Issue**: `GROQ_API_KEY not found`
**Solution**: Make sure you have set the API key in your `.env` file or pass it via `-k` flag

**Issue**: `Error extracting text from PDF`
**Solution**: Ensure the PDF is not password-protected or corrupted

**Issue**: `Unsupported file format`
**Solution**: Only PDF and HTML files are supported. Check your file extension

**Issue**: JSON parsing error
**Solution**: The LLM response might need adjustment. The program will return "Error extracting" for failed fields

## 📝 Examples

### Example 1: Single RFP Document

```bash
# Process a single RFP PDF
python rfp_processor.py -f examples/rfp_sample.pdf -o results/sample_output.json
```

### Example 2: Batch Processing

```bash
# Process multiple RFP documents from a directory
python rfp_processor.py -f rfp_docs/*.pdf -o results/batch_results.json
```

### Example 3: Mixed Formats

```bash
# Process both PDF and HTML documents
python rfp_processor.py -f rfp1.pdf rfp2.html rfp3.pdf -o mixed_results.json
```

## 🔒 Security Notes

- API keys should never be committed to version control
- Use `.env` files or environment variables for sensitive information
- The `.env` file is included in `.gitignore`

## 📚 Project Structure

```
/app/
├── rfp_extractor.py       # Core extraction logic
├── rfp_processor.py       # CLI interface
├── RFP_README.md          # This documentation
├── requirements.txt       # Python dependencies
├── .env                   # API keys (not in git)
└── examples/              # Sample documents (optional)
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📄 License

This project is provided as-is for educational and commercial use.

## 🙏 Acknowledgments

- Built with [Groq](https://groq.com) for fast LLM inference
- Uses [PyMuPDF](https://pymupdf.readthedocs.io/) for PDF processing
- HTML parsing with [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/)

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the examples
3. Open an issue in the repository

---

**Happy Extracting! 🚀**
