# 📄 Document Processing Suite

This repository contains two powerful document processing tools:

## 🎯 1. RFP Document Extractor (NEW!)

**Extract structured information from RFP documents (PDF & HTML)**

A standalone Python program that intelligently extracts 20 key fields from Request for Proposal documents using AI-powered analysis.

### ✨ Features
- 📑 Process PDF and HTML RFP documents
- 🤖 AI-powered extraction using Groq LLM
- 📊 Structured JSON output with 20 predefined fields
- 🔄 Batch processing support
- 💻 Easy-to-use CLI interface

### 🚀 Quick Start
```bash
# Process a single RFP document
python rfp_processor.py -f your_rfp.pdf -o results.json

# Process multiple documents
python rfp_processor.py -f doc1.pdf doc2.html doc3.pdf -o batch_results.json
```

### 📚 Documentation
- **[Complete Documentation](RFP_README.md)** - Full usage guide
- **[Project Overview](PROJECT_OVERVIEW.md)** - Architecture and examples
- **[Test Script](test_rfp_extractor.py)** - Demonstration and testing

---

## 🧠 2. PDF Chatbot – Search Answers from PDFs

**Interactive chatbot for querying PDF documents**

A chatbot that can search a PDF and return accurate answers to any user query.  
It processes the document, understands the context, and gives concise, relevant responses.

### 🚀 Features
- 📂 Upload any PDF document
- 🔍 Ask questions in natural language
- 🤖 AI-powered search to find the exact answers
- ⚡ Fast and accurate results

### 📽️ Demo:
![Demo](images/demo_new.gif)


