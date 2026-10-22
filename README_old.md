# 🧾 Receipt OCR Engineered

A robust, test-driven Full-Stack application that extracts structured data from receipt images using OCR. Built with **FastAPI**, **SQLAlchemy**, and **Pytesseract**.

## 🚀 Features
- **Automated Parsing:** Extracts merchant, date, total, and line items from raw OCR text using robust regex patterns.
- **RESTful API:** High-performance backend built with FastAPI, featuring automatic Swagger/OpenAPI documentation.
- **Data Persistence:** Secure storage of parsed data using SQLite and SQLAlchemy ORM.
- **Test-Driven Development (TDD):** Comprehensive unit and integration tests using `pytest` and `unittest.mock` to ensure reliability.
- **Robust Error Handling:** Graceful handling of image processing failures, missing data, and database constraints.

## 🛠️ Tech Stack
- **Backend:** Python 3.10+, FastAPI, Uvicorn
- **Database:** SQLite, SQLAlchemy (ORM)
- **OCR Engine:** Tesseract OCR (via Pytesseract)
- **Image Processing:** Pillow (PIL)
- **Testing:** pytest, httpx, unittest.mock
- **Version Control:** Git, GitHub

## 📁 Project Structure
```text
receipt-ocr-engineered/
├── backend/
│   ├── main.py          # FastAPI entry point, routes, and middleware
│   ├── models.py        # SQLAlchemy database models (Receipt schema)
│   ├── database.py      # Database engine and session management
│   ├── ocr_parser.py    # Core logic for regex-based text parsing
│   └── tests/           # Unit and integration test suites
│       ├── test_ocr_parser.py
│       └── test_api.py
├── .gitignore           # Excludes venv, db files, and OS artifacts
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation

⚙️ Installation & Setup
1. Clone the repository
git clone https://github.com/Bindhusreepothapi/receipt-ocr-engineered.git
cd receipt-ocr-engineered
2. Create a virtual environment

python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On macOS/Linux

3. Install dependencies
pip install -r requirements.txt

4. Install Tesseract OCR

This project requires the Tesseract OCR engine to be installed on your system.
Windows: Download the installer from Tesseract Wiki.
Note: Ensure tesseract.exe is in your system PATH, or update the path in backend/main.py.
🏃‍♂️ Running the Application
Start the FastAPI development server: uvicorn backend.main:app --reload
The API will be available at http://127.0.0.1:8000.
Interactive API documentation (Swagger UI) is available at: http://127.0.0.1:8000/docs

🧪 Testing
This project follows Test-Driven Development (TDD). To run the full test suite: pytest backend/tests/ -v

Test Coverage:
Unit Tests: Verify individual parsing functions (merchant, total, date, items).
Integration Tests: Verify API endpoints, database interactions, and file handling using mocked OCR responses.
🤝 Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
📜 License
This project is licensed under the MIT License.
