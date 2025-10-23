# 🎯 RFP Document Extractor - Project Overview

## 📁 Project Structure

```
/app/
├── rfp_extractor.py          # Core extraction logic and RFPExtractor class
├── rfp_processor.py          # Command-line interface
├── RFP_README.md             # Complete documentation
├── test_rfp_extractor.py     # Test and demonstration script
├── sample_rfp.html           # Sample RFP document for testing
├── .env.template             # Environment variables template
├── requirements.txt          # Python dependencies
└── existing files...         # Original PDF chatbot files
```

## 🚀 Quick Start Guide

### 1. Setup Environment

```bash
# Copy the environment template
cp .env.template .env

# Edit .env and add your Groq API key
# Get a free API key from: https://console.groq.com
nano .env
```

Edit the .env file:
```
GROQ_API_KEY=your_actual_groq_api_key_here
```

### 2. Verify Installation

```bash
# Test that all dependencies are installed
python test_rfp_extractor.py
```

### 3. Process Your Documents

#### Single Document
```bash
python rfp_processor.py -f your_rfp.pdf -o results.json
```

#### Multiple Documents
```bash
python rfp_processor.py -f rfp1.pdf rfp2.html rfp3.pdf -o batch_results.json
```

#### Test with Sample
```bash
python rfp_processor.py -f sample_rfp.html -o sample_output.json
```

## 📋 Features

### ✅ What the Program Does

1. **Accepts Input**: PDF and HTML files containing RFP documents
2. **Extracts Text**: Uses PyMuPDF for PDFs and BeautifulSoup for HTML
3. **AI Processing**: Leverages Groq's LLM (Llama 4 Scout) to intelligently extract information
4. **Structured Output**: Generates JSON files with 20 predefined fields
5. **Batch Processing**: Handle multiple documents in one command
6. **Error Handling**: Graceful handling of missing fields or parsing errors

### 📊 Extracted Information (20 Fields)

| Field | Description |
|-------|-------------|
| Bid Number | Unique identifier for the RFP |
| Title | RFP title/project name |
| Due Date | Submission deadline |
| Bid Submission Type | How to submit (email, portal, etc.) |
| Term of Bid | How long the bid is valid |
| Pre Bid Meeting | Date/time of pre-bid conference |
| Installation | Installation requirements/timeline |
| Bid Bond Requirement | Required bond amount or percentage |
| Delivery Date | Expected delivery/completion date |
| Payment Terms | Payment schedule and terms |
| Any Additional Documentation Required | List of required documents |
| MFG for Registration | Manufacturer registration requirements |
| Contract or Cooperative to use | Applicable contracts (e.g., GSA Schedule) |
| Model_no | Product model number |
| Part_no | Part number |
| Product | Product/service description |
| contact_info | Contact person and details |
| company_name | Issuing organization name |
| Bid Summary | Executive summary of the RFP |
| Product Specification | Detailed technical specifications |

## 🔧 Technical Architecture

### Component Breakdown

```
┌─────────────────────────────────────────────────┐
│           rfp_processor.py (CLI)                │
│         Command-line Interface                  │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│         rfp_extractor.py (Core Logic)           │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │  Document Parser                        │   │
│  │  - PDF: PyMuPDF (fitz)                 │   │
│  │  - HTML: BeautifulSoup + lxml          │   │
│  └─────────────────────────────────────────┘   │
│                  │                              │
│                  ▼                              │
│  ┌─────────────────────────────────────────┐   │
│  │  Text Extraction                        │   │
│  │  - Clean and normalize text             │   │
│  │  - Remove boilerplate                   │   │
│  └─────────────────────────────────────────┘   │
│                  │                              │
│                  ▼                              │
│  ┌─────────────────────────────────────────┐   │
│  │  LLM Processing (Groq API)              │   │
│  │  - Model: Llama 4 Scout 17B             │   │
│  │  - Structured extraction prompt         │   │
│  │  - Temperature: 0.1 (consistent)        │   │
│  └─────────────────────────────────────────┘   │
│                  │                              │
│                  ▼                              │
│  ┌─────────────────────────────────────────┐   │
│  │  JSON Output Generator                  │   │
│  │  - Validate fields                      │   │
│  │  - Format response                      │   │
│  └─────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```

### Key Classes and Functions

#### `RFPExtractor` Class

**Methods:**
- `__init__(api_key)` - Initialize with Groq API key
- `extract_text_from_pdf(file_path)` - Extract text from PDF
- `extract_text_from_html(file_path)` - Extract text from HTML
- `extract_text_from_file(file_path)` - Auto-detect format and extract
- `extract_rfp_information(text)` - Use LLM to extract structured data
- `process_document(file_path)` - Process single document
- `process_multiple_documents(file_paths)` - Batch processing
- `save_results_to_json(results, output_path)` - Save to JSON file

## 📦 Dependencies

### Core Libraries
- **beautifulsoup4** (4.14.2) - HTML parsing
- **lxml** (6.0.2) - XML/HTML processing engine
- **PyMuPDF** (1.26.5) - PDF text extraction
- **groq** (0.33.0) - Groq API client for LLM
- **python-dotenv** (1.1.1) - Environment variable management

### Supporting Libraries
- **pydantic** (2.12.3) - Data validation
- **requests** (2.32.4) - HTTP library
- **numpy** - Numerical operations (from existing project)
- **sentence-transformers** - Embeddings (from existing project)

## 🎓 Usage Examples

### Example 1: Basic Usage
```bash
# Process a single RFP PDF
python rfp_processor.py -f rfp_document.pdf -o results.json
```

### Example 2: Programmatic Usage
```python
from rfp_extractor import RFPExtractor

# Initialize
extractor = RFPExtractor()

# Process a document
result = extractor.process_document("rfp_document.pdf")

# Access extracted data
bid_number = result['extracted_fields']['Bid Number']
title = result['extracted_fields']['Title']
due_date = result['extracted_fields']['Due Date']

print(f"RFP: {bid_number} - {title}")
print(f"Due: {due_date}")

# Save to JSON
extractor.save_results_to_json(result, "output.json")
```

### Example 3: Batch Processing
```python
from rfp_extractor import RFPExtractor

extractor = RFPExtractor()

# Process multiple documents
documents = [
    "rfp_project_a.pdf",
    "rfp_project_b.html",
    "rfp_project_c.pdf"
]

results = extractor.process_multiple_documents(documents)

# Save batch results
extractor.save_results_to_json(results, "batch_output.json")

# Analyze results
for result in results:
    if 'error' not in result:
        print(f"✓ {result['document_name']}: Success")
    else:
        print(f"✗ {result['document_name']}: {result['error']}")
```

## 🧪 Testing

### Run the Test Script
```bash
python test_rfp_extractor.py
```

This will:
1. ✅ Check for API key
2. ✅ Initialize the extractor
3. ✅ Process the sample HTML document
4. ✅ Display extracted fields
5. ✅ Save results to `test_output.json`
6. ✅ Show usage examples

### Test with Sample Document
```bash
# Process the included sample
python rfp_processor.py -f sample_rfp.html -o sample_results.json

# View the results
cat sample_results.json | python -m json.tool
```

## 🔍 Output Format

### Single Document Output
```json
{
  "document_name": "sample_rfp.html",
  "document_type": ".html",
  "extracted_fields": {
    "Bid Number": "RFP-2025-IT-456",
    "Title": "Cloud Infrastructure Migration and Management Services",
    "Due Date": "August 30, 2025, 5:00 PM EST",
    "Bid Submission Type": "Electronic submission via email",
    "Term of Bid": "120 days from submission date",
    "Pre Bid Meeting": "July 20, 2025, 2:00 PM EST via Zoom",
    "Installation": "Cloud migration to be completed within 90 days",
    "Bid Bond Requirement": "10% of total bid amount or $50,000",
    "Delivery Date": "Services to commence within 45 days",
    "Payment Terms": "Net 45 days, with milestone-based payments",
    "Any Additional Documentation Required": "Financial statements, ISO 27001, references",
    "MFG for Registration": "Amazon Web Services (AWS), Microsoft Azure certified",
    "Contract or Cooperative to use": "GSA Schedule 70 - IT Services",
    "Model_no": "AWS EC2 t3.xlarge instances",
    "Part_no": "AWS-EC2-T3XL-2025",
    "Product": "Cloud infrastructure services",
    "contact_info": "procurement@techcorp.com, (555) 987-6543",
    "company_name": "TechCorp Solutions Inc.",
    "Bid Summary": "TechCorp Solutions is seeking qualified vendors...",
    "Product Specification": "Minimum 4 vCPUs, 16GB RAM, 500GB SSD storage..."
  }
}
```

## 🛠️ Troubleshooting

### Common Issues

**Problem**: "GROQ_API_KEY not found"
**Solution**: 
```bash
# Create .env file from template
cp .env.template .env
# Edit and add your API key
nano .env
```

**Problem**: "Module not found" errors
**Solution**:
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

**Problem**: "Error extracting text from PDF"
**Solutions**:
- Check if PDF is password-protected
- Verify file is not corrupted
- Ensure file path is correct

**Problem**: JSON parsing errors
**Solution**: The LLM sometimes returns malformed JSON. The program handles this gracefully and returns "Error extracting" for problematic fields.

## 📚 Additional Resources

- **Full Documentation**: See `RFP_README.md`
- **API Documentation**: https://console.groq.com/docs
- **Groq Console**: https://console.groq.com
- **BeautifulSoup Docs**: https://www.crummy.com/software/BeautifulSoup/
- **PyMuPDF Docs**: https://pymupdf.readthedocs.io/

## 💡 Tips for Best Results

1. **Document Quality**: Higher quality PDFs with selectable text work best
2. **HTML Structure**: Well-structured HTML with proper tags improves extraction
3. **Field Names**: The program looks for common RFP terminology
4. **Batch Processing**: Process similar documents together for consistency
5. **API Limits**: Groq has rate limits; add delays for large batches if needed

## 🤝 Support

For issues or questions:
1. Check the documentation in `RFP_README.md`
2. Review the troubleshooting section
3. Run the test script to verify setup
4. Check Groq API status and limits

## ✨ Next Steps

1. **Set up your API key** in the `.env` file
2. **Run the test script** to verify everything works
3. **Try the sample document** to see the output format
4. **Process your own RFP documents**
5. **Integrate into your workflow**

---

**Built with ❤️ using Groq's Fast LLM Inference**
