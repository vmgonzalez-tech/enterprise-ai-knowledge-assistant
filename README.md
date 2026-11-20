
# Enterprise AI Knowledge Assistant

A local Retrieval-Augmented Generation (RAG) prototype designed to answer questions about internal company documentation using an open-source language model.

This project demonstrates practical AI engineering concepts, including semantic retrieval, grounded answer generation, factual review, automated evaluation, and security-aware development.

## Business Problem

Employees often spend significant time searching through internal policies, handbooks, and knowledge bases.

Traditional keyword searches may not easily surface the information needed, particularly when questions are expressed in natural language.

This prototype explores how Retrieval-Augmented Generation can make company information easier to access while reducing reliance on unsupported model knowledge.

## Solution

An AI-powered knowledge assistant that:

- Accepts natural-language questions.
- Retrieves relevant passages from a vector database.
- Generates answers using a locally hosted language model.
- Performs a second LLM-based factual review.
- Displays retrieved source passages for transparency.
- Supports automated evaluation against predefined test cases.

The system uses fictional company documentation and runs locally without requiring a paid cloud LLM API.

## Technology Stack

- **Python 3.12** — Application development
- **Streamlit** — Interactive chat interface
- **Ollama** — Local LLM inference
- **Llama 3.2 (3B)** — Language model
- **ChromaDB** — Vector database
- **RAG** — Retrieval-Augmented Generation
- **Git and GitHub** — Version control
- **Gitleaks** — Secret scanning
- **pip-audit** — Dependency vulnerability scanning

## Features

- Natural-language question answering
- Semantic document retrieval
- Source-grounded answer generation
- Secondary LLM-based factual review
- Display of retrieved source passages
- Abstention when information is unavailable
- Local inference without paid cloud APIs
- Automated RAG evaluation with five test cases
- Individual PASS/FAIL evaluation results
- Basic factual completeness and abstention scoring

## Architecture

The application separates the user interface from the RAG processing logic.

```text
User Question
     |
     v
Streamlit Interface
(app/ui.py)
     |
     v
RAG Engine
(app/assistant.py)
     |
     v
ChromaDB Semantic Retrieval
     |
     v
Retrieved Document Context
     |
     v
Llama 3.2 Answer Generation
     |
     v
Llama 3.2 Factual Review
     |
     v
Final Answer + Retrieved Sources
```

The evaluation framework calls the same RAG engine used by the Streamlit application.

```text
Evaluation Cases (JSON)
         |
         v
Evaluation Runner
(tests/evaluate_rag.py)
         |
         v
RAG Engine
(app/assistant.py)
         |
         v
Answer Comparison
         |
         v
PASS / FAIL + Overall Score
```

This separation reduces duplicated logic and allows the application and evaluation framework to use the same answer-generation pipeline.

## Project Structure

```text
enterprise-ai-knowledge-assistant/
|
|-- app/
|   |-- assistant.py
|   |-- rag.py
|   |-- ui.py
|
|-- data/
|   |-- employee_handbook.txt
|
|-- tests/
|   |-- evaluate_rag.py
|   |-- rag_eval_cases.json
|
|-- .gitignore
|-- README.md
|-- requirements.txt
```

The project also creates a local ChromaDB database during document indexing. This database is excluded from Git version control.

## Run Locally

### Prerequisites

- Python 3.12
- Ollama
- Git (optional)

### Installation

1. Clone the repository:

```powershell
git clone https://github.com/vmgonzalez-tech/enterprise-ai-knowledge-assistant.git
cd enterprise-ai-knowledge-assistant
```

2. Create a virtual environment:

```powershell
python -m venv .venv
```

3. Activate the virtual environment in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

4. Install the project dependencies:

```powershell
pip install -r requirements.txt
```

5. Download the language model:

```powershell
ollama pull llama3.2:3b
```

6. Ensure Ollama is running locally.

7. Index the fictional employee handbook:

```powershell
python app/rag.py
```

If the command-line assistant starts after indexing, exit it before proceeding.

8. Launch the Streamlit interface, restricted to localhost:

```powershell
streamlit run app/ui.py --server.address 127.0.0.1
```

9. Open the application:

http://127.0.0.1:8501

The application is intended for local demonstration only.

## RAG Evaluation

The project includes an automated evaluation framework with five predefined test cases.

The evaluation checks two key behaviours:

**Factual completeness**

For questions supported by the source documentation, the answer must contain the expected factual elements.

**Abstention**

For questions where the source does not provide an answer, the assistant should acknowledge that the information is unavailable rather than inventing a policy.

### Evaluation Cases

| Test Case | Evaluation Objective |
|-----------|----------------------|
| Annual leave | Correct entitlement and UK bank holidays |
| Remote work | Weekly limit and manager approval |
| Expenses | Approval requirements above GBP 500 |
| Unknown sick leave | Appropriate abstention |
| Unknown salary policy | Appropriate abstention |

### Evaluation Results

| Metric | Initial Baseline | Latest Observed |
|--------|------------------|-----------------|
| Tests passed | 4/5 | 5/5 |
| Pass rate | 80% | 100% |

### Identified Failure and Improvement

The initial evaluation identified an incomplete answer to the remote work policy question.

The assistant correctly stated that employees could work remotely for up to three days per week but omitted the requirement for manager approval.

Investigation confirmed that:

1. ChromaDB retrieved the correct policy passage.
2. The initial LLM response omitted the approval requirement.
3. Prompt refinement enabled the initial response to identify the requirement.
4. The second LLM review still removed the requirement.
5. Refining the factual review prompt resolved the omission in the observed evaluation run.

This demonstrated that correct retrieval alone does not guarantee complete answers and that an additional LLM review can itself introduce information loss.

### Run the Evaluation

```powershell
python tests/evaluate_rag.py
```

The evaluation prints each question, the generated answer, its PASS/FAIL status, missing expected facts where applicable, and an overall score.

### Evaluation Limitations

The current framework uses predefined expected phrases and basic abstention detection.

It does not yet provide:

- Comprehensive semantic equivalence scoring
- Independent verification of every factual claim
- Retrieval precision or recall measurements
- Statistical reliability across repeated runs
- Comprehensive adversarial or prompt-injection testing

A 100% result on five cases does not establish production-level accuracy or reliability.

## Security & Privacy Considerations

Security and data privacy have been considered during the development of this prototype.

### Current Security Measures

- **Local inference:** Ollama runs the language model locally without requiring an external paid LLM API.
- **Fictional documentation:** The employee handbook contains demonstration data rather than confidential corporate information.
- **Git exclusions:** The `.gitignore` file excludes local environments, vector database files, common credential files, and temporary backups.
- **Secret scanning:** Gitleaks has been used to scan staged changes for potential credential exposure.
- **Dependency auditing:** pip-audit has been used to identify known vulnerabilities.
- **Restricted application access:** The documented Streamlit command binds the interface to `127.0.0.1`.
- **Transparent limitations:** Known security risks are documented rather than presented as resolved.

These controls reduce some development risks but do not constitute a comprehensive security assessment.

### Current Security Limitations

The prototype does not yet implement:

- User authentication
- Role-based access control
- Document-level permissions
- Comprehensive prompt-injection defences
- Enterprise secrets management
- Production monitoring and audit logging
- Production-grade deployment security

These capabilities would require further design and validation before using the system with real enterprise information.

### Dependency Security Review

A dependency audit using `pip-audit` reported five vulnerability findings associated with ChromaDB 1.5.9.

The audit output included a repeated vulnerability identifier. These are five reported findings, not necessarily five distinct vulnerabilities.

No corrected package version was identified in the displayed audit output.

**Current risk considerations:**

- The application uses ChromaDB through an embedded local `PersistentClient`.
- The project does not intentionally launch a ChromaDB HTTP server.
- The documented Streamlit launch command restricts the application to localhost.
- The vulnerabilities remain unresolved and require further assessment.

**Mitigation approach:**

- Restrict use to local demonstrations.
- Do not ingest confidential enterprise documents.
- Do not expose the application or database to untrusted network clients.
- Monitor upstream security updates.
- Repeat dependency audits when updating packages.
- Reassess risks before any production deployment.

The presence of known dependency vulnerabilities means this prototype must not be represented as production-ready.

This security review is documentation of development practices and known limitations, not a security certification.

## Current Status

The project currently includes:

- A functional local RAG assistant
- An interactive Streamlit interface
- A reusable RAG processing module
- Source passage visibility
- A two-stage LLM answer-generation and review pipeline
- Five automated evaluation cases
- A latest observed evaluation result of 5/5
- Documented dependency security findings

The system remains a local portfolio prototype.

## Planned Improvements

- Expanded evaluation datasets
- Semantic answer-quality evaluation
- Retrieval quality metrics
- Improved source attribution and citations
- PDF document ingestion
- Prompt-injection testing and defensive controls
- FastAPI endpoints
- Automated CI/CD checks with GitHub Actions
- Authentication and access-control architecture
- Azure deployment architecture and security design

## Disclaimer

All company policies in this repository are fictional demonstration data.

This project is intended to demonstrate AI engineering concepts and development practices. It is not a production deployment and must not be used to process confidential enterprise information without substantial additional security, reliability, and governance work.
