"""
OCR Text Parsing Module.

This module contains functions to extract structured data from raw OCR text
extracted from receipt images. It uses regex patterns to identify common
receipt fields like merchant name, total amount, date, and line items.
"""

import re
from typing import Dict, List


def parse_receipt_text(ocr_text: str) -> Dict[str, object]:
    """
    Parse raw OCR text from a receipt image into structured data.
    
    Args:
        ocr_text: Raw text extracted from receipt image using Tesseract OCR.
        
    Returns:
        A dictionary with keys:
            - merchant (str): Name of the store/vendor
            - date (str): Date of purchase (MM/DD/YYYY format or 'Unknown')
            - total (float): Total amount paid
            - items (List[str]): List of item names purchased
    """
    # Extract merchant name (first non-empty line)
    merchant = extract_merchant(ocr_text)
    
    # Extract total amount
    total = extract_total(ocr_text)
    
    # Extract date
    date = extract_date(ocr_text)
    
    # Extract line items
    items = extract_items(ocr_text)
    
    return {
        "merchant": merchant,
        "date": date,
        "total": total,
        "items": items
    }


def extract_merchant(text: str) -> str:
    """
    Extract merchant name from OCR text.
    
    Assumes the merchant name is on the first non-empty line of the receipt.
    
    Args:
        text: Raw OCR text from receipt.
        
    Returns:
        Merchant name as string, or 'Unknown' if not found.
    """
    lines = text.strip().split('\n')
    for line in lines:
        line = line.strip()
        if line:  # First non-empty line
            return line
    return "Unknown"


def extract_total(text: str) -> float:
    """
    Extract total amount from OCR text.
    
    Searches for patterns like "Total: $15.50" or "Total 15.50".
    
    Args:
        text: Raw OCR text from receipt.
        
    Returns:
        Total amount as float, or 0.0 if not found.
    """
    # Pattern matches: Total: $15.50, Total $15.50, Total: 15.50, etc.
    pattern = r'Total[:\s]*\$?(\d+[.,]?\d*)'
    match = re.search(pattern, text, re.IGNORECASE)
    
    if match:
        total_str = match.group(1).replace(',', '')
        return float(total_str)
    
    return 0.0


def extract_date(text: str) -> str:
    """
    Extract date from OCR text.
    
    Searches for MM/DD/YYYY format dates.
    
    Args:
        text: Raw OCR text from receipt.
        
    Returns:
        Date string in MM/DD/YYYY format, or 'Unknown' if not found.
    """
    # Pattern matches: 01/15/2024, 1/5/2024, etc.
    pattern = r'(\d{1,2}/\d{1,2}/\d{4})'
    match = re.search(pattern, text)
    
    if match:
        return match.group(1)
    
    return "Unknown"


def extract_items(text: str) -> List[str]:
    """
    Extract line items from OCR text.
    
    Identifies lines that contain both text and numbers (likely item + price).
    
    Args:
        text: Raw OCR text from receipt.
        
    Returns:
        List of item name strings.
    """
    items = []
    lines = text.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        # Skip empty lines, merchant name (first line), and total/date lines
        if not line or line == extract_merchant(text):
            continue
        
        # Check if line contains both letters and digits (likely an item)
        has_letters = any(c.isalpha() for c in line)
        has_digits = any(c.isdigit() for c in line)
        
        # Skip lines that are just "Total:" or "Date:"
        if re.match(r'^(Total|Date|Subtotal|Tax)', line, re.IGNORECASE):
            continue
        
        if has_letters and has_digits:
            # Extract just the item name (part before the price)
            # Remove trailing numbers and currency symbols
            item_name = re.sub(r'[\d$.,\s]+$', '', line).strip()
            if item_name:
                items.append(item_name)
    
    return items