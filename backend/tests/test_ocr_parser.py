"""
Tests for OCR text parsing functions.

These tests verify that we can extract structured data from raw OCR text.
We use known sample texts to ensure consistent behavior.
"""

import pytest
from backend.ocr_parser import parse_receipt_text


class TestParseReceiptText:
    """Test suite for the parse_receipt_text function."""
    
    def test_parses_merchant_name(self):
        """Test that merchant name is extracted from first non-empty line."""
        ocr_text = """
        WALMART STORE #1234
        123 Main Street
        Date: 01/15/2024
        
        Milk          $3.99
        Bread         $2.49
        Total:        $6.48
        """
        result = parse_receipt_text(ocr_text)
        assert result["merchant"] == "WALMART STORE #1234"
    
    def test_parses_total_amount(self):
        """Test that total amount is correctly extracted."""
        ocr_text = """
        Some Store
        Item 1    $10.00
        Item 2    $5.50
        Total:    $15.50
        """
        result = parse_receipt_text(ocr_text)
        assert result["total"] == 15.50
    
    def test_parses_date_in_mm_dd_yyyy_format(self):
        """Test date extraction in MM/DD/YYYY format."""
        ocr_text = """
        Store Name
        Date: 03/25/2024
        Total: $20.00
        """
        result = parse_receipt_text(ocr_text)
        assert result["date"] == "03/25/2024"
    
    def test_handles_missing_total(self):
        """Test that missing total defaults to 0.0."""
        ocr_text = """
        Store Name
        Some random text without amounts
        """
        result = parse_receipt_text(ocr_text)
        assert result["total"] == 0.0
    
    def test_handles_missing_date(self):
        """Test that missing date defaults to 'Unknown'."""
        ocr_text = """
        Store Name
        Total: $10.00
        """
        result = parse_receipt_text(ocr_text)
        assert result["date"] == "Unknown"
    
    def test_extracts_multiple_items(self):
        """Test that line items are extracted."""
        ocr_text = """
        GROCERY STORE
        Milk        3.99
        Bread       2.49
        Eggs        4.99
        Total:      11.47
        """
        result = parse_receipt_text(ocr_text)
        assert len(result["items"]) == 3
        assert "Milk" in result["items"]
        assert "Bread" in result["items"]