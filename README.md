# Receipt OCR Engine

A test-driven FastAPI application that extracts structured information from receipt images and stores the results in a SQLite database.

## Overview

**Receipt OCR Engine** is a backend-focused project that demonstrates an end-to-end receipt-processing workflow: image upload, optical character recognition (OCR), text parsing, validation, and persistence. It uses Tesseract through `pytesseract` to recognize text and Python parsing logic to identify receipt fields.

> **Project status:** Update this section to reflect the current implementation before publishing. Avoid claiming features or test coverage that have not been verified.

## Features

- **Receipt text extraction:** Uses Tesseract OCR through `pytesseract` to extract text from uploaded receipt images.
- **Structured parsing:** Uses parsing rules and regular expressions to identify fields such as merchant, date, total, and line items.
- **REST API:** Provides FastAPI endpoints and interactive OpenAPI documentation.
- **Database persistence:** Uses SQLAlchemy ORM with SQLite to store parsed receipt data.
- **Automated tests:** Uses `pytest`, `httpx`, and `unittest.mock` for parser and API tests.
- **Error handling:** Handles invalid input and processing failures with appropriate API errors.

## Technology Stack

| Area | Technologies |
| --- | --- |
| Language | Python 3.10+ |
| API | FastAPI, Uvicorn |
| Database | SQLite, SQLAlchemy |
| OCR | Tesseract OCR, `pytesseract` |
| Image processing | Pillow |
| Testing | `pytest`, `httpx`, `unittest.mock` |
| Version control | Git, GitHub |

## Architecture

```text
Receipt image
    |
    v
FastAPI upload endpoint
    |
    v
Image validation and preprocessing
    |
    v
Tesseract OCR (pytesseract)
    |
    v
Receipt text parser
    |
    v
Structured receipt data
    |
    v
SQLAlchemy ORM
    |
    v
SQLite database
```

## Repository Structure

```text
receipt-ocr-engineered/
├── backend/
│   ├── main.py              # FastAPI application and routes
│   ├── models.py            # SQLAlchemy models
│   ├── database.py          # Database engine and session setup
│   ├── ocr_parser.py        # Receipt text parsing logic
│   └── tests/
│       ├── test_ocr_parser.py
│       └── test_api.py
├── .gitignore
├── requirements.txt
└── README.md
```

The structure above reflects the intended layout. Adjust it if the repository differs.

## Prerequisites

- Python 3.10 or newer
- Git
- Tesseract OCR installed and accessible from your system `PATH`

### Install Tesseract OCR

Install the Tesseract OCR engine for your operating system:

- **Windows:** Use a trusted Windows Tesseract installer and ensure the directory containing `tesseract.exe` is added to `PATH`.
- **macOS:** Install with your preferred package manager, for example `brew install tesseract`.
- **Ubuntu/Debian:** Install with `sudo apt install tesseract-ocr` if you have the required system permissions.

Verify the installation:

```bash
tesseract --version
```

If Tesseract is installed but not on `PATH`, configure `pytesseract.pytesseract.tesseract_cmd` in the application configuration rather than hard-coding a machine-specific path throughout the code.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Bindhusreepothapi/receipt-ocr-engineered.git
cd receipt-ocr-engineered
```

### 2. Create and activate a virtual environment

**Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use Command Prompt instead:

```bat
venv\Scripts\activate.bat
```

**macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Python dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Start the API

From the repository root:

```bash
uvicorn backend.main:app --reload
```

The development server should be available at:

- API base URL: <http://127.0.0.1:8000>
- Swagger UI: <http://127.0.0.1:8000/docs>
- ReDoc: <http://127.0.0.1:8000/redoc>

Use `--reload` for local development only, not as a production server configuration.

## Testing

Run the test suite from the repository root:

```bash
pytest backend/tests/ -v
```

The intended test coverage includes:

- **Parser unit tests:** Check parsing behavior for merchant names, dates, totals, and line items.
- **API integration tests:** Check request validation, endpoint responses, database behavior, and file-handling paths.
- **Mocked OCR tests:** Replace the OCR call with predictable test responses so tests do not depend on OCR output for every case.

Only describe these tests as passing after running them in your environment. If coverage is measured, add the actual command and result, for example:

```bash
pytest --cov=backend --cov-report=term-missing backend/tests/
```

This coverage command requires `pytest-cov` to be installed.

## Example Workflow

1. Submit a receipt image to the relevant upload endpoint.
2. The application passes the image to the OCR engine.
3. The parser converts recognized text into structured fields.
4. The API validates and stores the result.
5. The client receives the API response.

Check `/docs` for the exact endpoint paths, request fields, and response schema implemented by this repository.

## Configuration and Troubleshooting

- **`tesseract is not installed or it's not in your PATH`:** Confirm `tesseract --version` works in the same terminal that runs the API.
- **Python import errors:** Activate the virtual environment and reinstall dependencies from `requirements.txt`.
- **Database or schema errors:** Confirm the database URL and table initialization match the current SQLAlchemy setup.
- **OCR returns incomplete text:** Try a clearer, well-lit image with the receipt fully visible and minimal skew. OCR accuracy depends on image quality, receipt layout, and language configuration.
- **Tests fail due to database state:** Ensure tests use an isolated test database or clean up records between runs.

## Engineering Notes

- Validate uploaded file type and size before processing.
- Avoid trusting the file extension alone; validate the actual image content.
- Keep database credentials and machine-specific configuration out of source control.
- Use parameterized ORM/database operations rather than building SQL strings from user input.
- Add tests for missing fields, ambiguous totals, invalid dates, malformed images, and duplicate submissions.
- Receipt parsing is heuristic: totals and dates may be ambiguous. Consider returning confidence or review indicators when fields cannot be identified reliably.

## Roadmap

Potential improvements, depending on project goals:

- [ ] Add configurable upload-size and image-format limits.
- [ ] Add stronger parsing for multiple date and currency formats.
- [ ] Add validation and confidence indicators for extracted fields.
- [ ] Add pagination and filtering for stored receipts.
- [ ] Add structured logging and request IDs.
- [ ] Add CI with automated tests on each pull request.
- [ ] Add Docker-based development setup.
- [ ] Add OCR accuracy evaluation using a small, documented sample dataset.

## Contributing

Contributions and bug reports are welcome. For substantial changes, open an issue first to discuss the proposed approach.

1. Create a feature branch.
2. Make a focused change.
3. Add or update tests.
4. Run the test suite.
5. Open a pull request with a clear summary.

## License

This project is licensed under the MIT License. See [`LICENSE`](LICENSE) for the full license text.

If the repository does not yet contain a `LICENSE` file, add the MIT license text before stating that the project is MIT-licensed.
