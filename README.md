# Enterprise AI Knowledge Assistant

A locally deployed Retrieval-Augmented Generation (RAG) prototype designed to answer questions about internal company documentation.

## Business Problem
Employees often spend time searching through internal policies and knowledge bases. This prototype explores how AI-powered retrieval can make company information easier to access.

## Solution
An AI assistant that retrieves relevant document sections and uses a local language model to generate context-grounded answers.

## Technology Stack
- Python 3.12
- Streamlit - Web interface
- Ollama - Local LLM inference
- Llama 3.2 (3B) - Language model
- ChromaDB - Vector database
- RAG - Document retrieval and answer generation

## Features
- Natural-language question answering
- Semantic document retrieval
- Display of retrieved source passages
- Local inference without paid cloud APIs
- Initial testing of unsupported questions

## Architecture
User -> Streamlit -> ChromaDB -> Retrieved Context -> Ollama / Llama 3.2 -> Answer

## Run Locally
1. Install Python 3.12 and Ollama.
2. Download the model: `ollama pull llama3.2:3b`
3. Create and activate a Python virtual environment.
4. Install dependencies: `pip install -r requirements.txt`
5. Index the sample document: `python app/rag.py`
6. Exit the command-line assistant.
7. Launch the interface: `streamlit run app/ui.py`

## Current Status
Functional local prototype. Initial manual tests passed for factual retrieval and identifying missing policy information.

## Planned Improvements
- PDF ingestion
- Automated evaluation and testing
- FastAPI endpoints
- CI/CD with GitHub Actions
- Improved source attribution
- Azure deployment architecture

## Disclaimer
All company policies in this repository are fictional demonstration data.
This is a portfolio prototype, not a production deployment.

## Security & Privacy Considerations

Security and data privacy have been considered throughout the development of this prototype.

The project includes the following measures and development practices:

- **Local LLM inference:** Ollama runs the language model locally, without requiring a paid external LLM API.
- **Demo-only documentation:** The sample employee handbook contains fictional company policies, not real corporate information.
- **Git exclusions:** The `.gitignore` file excludes virtual environments, local vector database files, environment configuration files and common credential formats.
- **Secret scanning:** Gitleaks has been used during pre-publication checks to identify potential exposed credentials.
- **Source review:** Application code, sample data and repository contents have been reviewed for accidental disclosure of sensitive information.
- **Transparency:** The project is explicitly identified as a prototype rather than a production-ready enterprise system.

### Current Security Limitations

This prototype does not yet implement user authentication, role-based access control, document-level permissions or comprehensive prompt-injection defenses.

These would be essential considerations before deploying the application with real enterprise data.

**Security approach:** Documented controls, transparent limitations and incremental improvements.

### Dependency Security Review

A pre-publication dependency audit was performed using `pip-audit`.

The audit identified five vulnerability findings associated with ChromaDB 1.5.9, including code-injection and authorization issues.

**Risk assessment:**
- The prototype uses ChromaDB through an embedded local `PersistentClient`.
- It does not intentionally expose a ChromaDB HTTP server.
- A local check found no services listening on ports 8000 or 8501 at the time of testing.
- The identified vulnerabilities remain unresolved and require reassessment before any production deployment.

**Mitigation approach:**
- Keep the application restricted to local demonstration use.
- Do not ingest confidential enterprise documents.
- Avoid exposing ChromaDB to untrusted network clients.
- Monitor upstream security fixes and repeat dependency audits.

This review documents known risks; it does not constitute a security certification.