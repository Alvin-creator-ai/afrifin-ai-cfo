"""
Receipt Processing Agent for AfriFin AI CFO.

Handles extraction of information from receipts (PDF, PNG, JPG).
"""

import logging
from typing import Dict, Any, Optional
from pathlib import Path
import pytesseract
from PIL import Image
import PyPDF2

logger = logging.getLogger(__name__)


class ReceiptAgent:
    """Agent for processing and extracting data from receipts."""

    def __init__(self):
        """Initialize the receipt agent."""
        self.supported_formats = [".pdf", ".png", ".jpg", ".jpeg"]

    def process_receipt(self, file_path: str) -> Dict[str, Any]:
        """
        Process a receipt file and extract information.

        Args:
            file_path: Path to receipt file

        Returns:
            Dictionary with extracted information
        """
        try:
            file_path = Path(file_path)

            if not file_path.exists():
                return {"error": f"File not found: {file_path}"}

            if file_path.suffix.lower() not in self.supported_formats:
                return {"error": f"Unsupported file format: {file_path.suffix}"}

            if file_path.suffix.lower() == ".pdf":
                text = self._extract_from_pdf(str(file_path))
            else:
                text = self._extract_from_image(str(file_path))

            # Parse extracted text
            extracted_data = self._parse_receipt_text(text)
            extracted_data["raw_text"] = text
            extracted_data["file_path"] = str(file_path)

            logger.info(f"Receipt processed: {file_path.name}")
            return extracted_data

        except Exception as e:
            logger.error(f"Error processing receipt: {e}")
            return {"error": str(e), "file_path": str(file_path)}

    def _extract_from_pdf(self, pdf_path: str) -> str:
        """
        Extract text from PDF file.

        Args:
            pdf_path: Path to PDF file

        Returns:
            Extracted text
        """
        try:
            text = ""
            with open(pdf_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text()
            return text

        except Exception as e:
            logger.error(f"Error extracting text from PDF: {e}")
            return ""

    def _extract_from_image(self, image_path: str) -> str:
        """
        Extract text from image using OCR.

        Args:
            image_path: Path to image file

        Returns:
            Extracted text
        """
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image)
            return text

        except Exception as e:
            logger.error(f"Error extracting text from image: {e}")
            return ""

    def _parse_receipt_text(self, text: str) -> Dict[str, Any]:
        """
        Parse extracted receipt text to structured format.

        Args:
            text: Raw extracted text from receipt

        Returns:
            Parsed receipt data
        """
        import re

        parsed = {
            "vendor": None,
            "amount": None,
            "date": None,
            "items": [],
            "description": "",
        }

        lines = text.split("\n")

        # Try to find amount (common patterns: KES 1000, 1,000, etc.)
        amount_pattern = r"(?:KES\s*)?[\d,]+(?:\.\d{2})?"
        for line in lines:
            match = re.search(amount_pattern, line)
            if match and parsed["amount"] is None:
                try:
                    amount_str = match.group(0).replace("KES", "").replace(",", "").strip()
                    amount = float(amount_str)
                    if amount > 0:
                        parsed["amount"] = amount
                except ValueError:
                    pass

        # Try to find date
        date_pattern = r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}"
        for line in lines:
            match = re.search(date_pattern, line)
            if match and parsed["date"] is None:
                parsed["date"] = match.group(0)

        # Extract vendor name (usually first few words)
        if lines:
            parsed["vendor"] = lines[0].strip()[:50]

        # Extract items (lines with amounts)
        item_pattern = r"(.+?)\s+([\d,]+(?:\.\d{2})?)\s*$"
        for line in lines[1:]:
            line = line.strip()
            if line and len(line) > 5:
                match = re.match(item_pattern, line)
                if match:
                    parsed["items"].append(
                        {"description": match.group(1).strip(), "amount": match.group(2)}
                    )

        # Build description from vendor and first item if available
        if parsed["vendor"]:
            parsed["description"] = f"{parsed['vendor']}"
            if parsed["items"]:
                parsed["description"] += f" - {parsed['items'][0]['description']}"

        return parsed

    def validate_receipt_data(self, receipt_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate extracted receipt data.

        Args:
            receipt_data: Extracted receipt data

        Returns:
            Validation result
        """
        issues = []

        if not receipt_data.get("vendor"):
            issues.append("Vendor name not found")

        if not receipt_data.get("amount"):
            issues.append("Amount not found")
        elif receipt_data["amount"] <= 0:
            issues.append("Invalid amount (must be positive)")

        if not receipt_data.get("date"):
            issues.append("Date not found")

        return {
            "is_valid": len(issues) == 0,
            "issues": issues,
            "data": receipt_data,
        }

    def format_receipt_summary(self, receipt_data: Dict[str, Any]) -> str:
        """
        Format receipt data as summary string.

        Args:
            receipt_data: Extracted receipt data

        Returns:
            Formatted summary
        """
        summary = "Receipt Summary:\n"
        summary += f"Vendor: {receipt_data.get('vendor', 'Unknown')}\n"
        summary += f"Amount: KES {receipt_data.get('amount', 'Unknown'):,.2f}\n"
        summary += f"Date: {receipt_data.get('date', 'Unknown')}\n"

        if receipt_data.get("items"):
            summary += "\nItems:\n"
            for item in receipt_data["items"][:5]:  # Limit to 5 items
                summary += f"  - {item['description']}: {item['amount']}\n"

        return summary
