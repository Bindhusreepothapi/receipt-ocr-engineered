"""
FastAPI Application Entry Point.

Defines the API endpoints for uploading receipts and retrieving data.
"""

from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os
from backend import models, database, ocr_parser

import pytesseract
# UPDATE THIS PATH to where Tesseract is installed on your temporary system
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Initialize the database tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Receipt OCR API")

# Allow CORS so our frontend can talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploaded_receipts"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Receipt OCR API"}

@app.post("/upload/")
def upload_receipt(file: UploadFile = File(...), db: Session = Depends(database.get_db)):
    """
    Endpoint to upload a receipt image, parse it, and store the data.
    """
    # 1. Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    # 2. Save the file locally
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    try:
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    
    # 3. Read the image and extract text using Tesseract
    from PIL import Image
    import pytesseract
    
    try:
        image = Image.open(file_path)
        ocr_text = pytesseract.image_to_string(image)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing image: {str(e)}")

    # 4. Parse the text into structured data
    parsed_data = ocr_parser.parse_receipt_text(ocr_text)
    
    # 5. Store in database
    try:
        db_receipt = models.Receipt(
            merchant=parsed_data["merchant"],
            date=parsed_data["date"],
            total=parsed_data["total"],
            items=str(parsed_data["items"])
        )
        db.add(db_receipt)
        db.commit()
        db.refresh(db_receipt)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    return {"message": "Receipt processed successfully", "data": parsed_data}

@app.get("/receipts/")
def get_receipts(db: Session = Depends(database.get_db)):
    """Retrieve all stored receipts."""
    return db.query(models.Receipt).all()