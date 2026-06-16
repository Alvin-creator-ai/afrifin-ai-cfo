"""
Journal Entry Agent for AfriFin AI CFO.

Generates proper journal entries based on transaction categorization.
"""

import logging
from typing import Dict, Any, Optional
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

logger = logging.getLogger(__name__)


class JournalEntryAgent:
    """Agent for generating journal entries."""

    def __init__(self):
        """Initialize the journal entry agent."""
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4"

    def generate_journal_entry(
        self,
        description: str,
        amount: float,
        category: str,
        account_type: str,
    ) -> Dict[str, Any]:
        """
        Generate a journal entry for a transaction.

        Args:
            description: Transaction description
            amount: Transaction amount
            category: Transaction category
            account_type: Account type

        Returns:
            Dictionary with journal entry details
        """
        try:
            # Get debit and credit accounts based on category
            accounts = self._determine_accounts(category, account_type)

            if not accounts:
                return {
                    "error": "Unable to determine accounts",
                    "description": description,
                }

            # Create journal entry
            entry = {
                "debit_account": accounts["debit"],
                "debit_amount": amount,
                "credit_account": accounts["credit"],
                "credit_amount": amount,
                "description": description,
            }

            # Validate entry
            validation = self._validate_entry(entry)

            if not validation["is_valid"]:
                logger.warning(f"Invalid entry generated: {validation['message']}")
                return {
                    "error": validation["message"],
                    "entry": entry,
                }

            logger.info(f"Journal entry generated for: {description}")
            return {
                "success": True,
                "entry": entry,
                "formatted_entry": self._format_entry(entry),
                "validation": validation,
            }

        except Exception as e:
            logger.error(f"Error generating journal entry: {e}")
            return {"error": str(e)}

    def _determine_accounts(self, category: str, account_type: str) -> Optional[Dict[str, str]]:
        """
        Determine debit and credit accounts for transaction.

        Args:
            category: Transaction category
            account_type: Account type

        Returns:
            Dictionary with debit and credit accounts
        """
        # Expense accounts debit to expense, credit to bank/cash
        if "Expense" in account_type or "Expense" in category:
            return {
                "debit": category,  # Expense account
                "credit": "Bank",  # Assuming payment from bank
            }

        # Revenue accounts credit to revenue, debit to bank/cash
        elif "Revenue" in account_type or "Revenue" in category:
            return {
                "debit": "Bank",  # Money received
                "credit": category,  # Revenue account
            }

        else:
            return None

    def _validate_entry(self, entry: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate journal entry balance.

        Args:
            entry: Journal entry dictionary

        Returns:
            Validation result
        """
        debits = entry.get("debit_amount", 0)
        credits = entry.get("credit_amount", 0)

        is_balanced = abs(debits - credits) < 0.01

        return {
            "is_valid": is_balanced,
            "total_debits": debits,
            "total_credits": credits,
            "message": (
                "Entry is balanced" if is_balanced else f"Unbalanced: Dr {debits} != Cr {credits}"
            ),
        }

    def _format_entry(self, entry: Dict[str, Any]) -> str:
        """
        Format journal entry as string.

        Args:
            entry: Journal entry dictionary

        Returns:
            Formatted entry string
        """
        formatted = "Journal Entry:\n"
        formatted += f"  Dr {entry['debit_account']}  {entry['debit_amount']:,.2f}\n"
        formatted += f"    Cr {entry['credit_account']}  {entry['credit_amount']:,.2f}\n"
        formatted += f"\nDescription: {entry['description']}\n"

        return formatted

    def reverse_entry(self, original_entry: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a reversing entry.

        Args:
            original_entry: Original journal entry

        Returns:
            Reversing entry
        """
        reversed_entry = {
            "debit_account": original_entry["credit_account"],
            "debit_amount": original_entry["credit_amount"],
            "credit_account": original_entry["debit_account"],
            "credit_amount": original_entry["debit_amount"],
            "description": f"Reversal: {original_entry['description']}",
        }

        return {
            "success": True,
            "entry": reversed_entry,
            "formatted_entry": self._format_entry(reversed_entry),
        }

    def adjust_entry(
        self,
        entry: Dict[str, Any],
        adjustment_amount: float,
    ) -> Dict[str, Any]:
        """
        Create an adjustment entry.

        Args:
            entry: Original entry
            adjustment_amount: Amount to adjust (can be positive or negative)

        Returns:
            Adjustment entry
        """
        adjusted_entry = {
            "debit_account": entry["debit_account"],
            "debit_amount": adjustment_amount,
            "credit_account": entry["credit_account"],
            "credit_amount": adjustment_amount,
            "description": f"Adjustment: {entry['description']} (+{adjustment_amount})",
        }

        validation = self._validate_entry(adjusted_entry)

        return {
            "success": validation["is_valid"],
            "entry": adjusted_entry,
            "formatted_entry": self._format_entry(adjusted_entry),
            "validation": validation,
        }

    def batch_generate_entries(
        self, transactions: list
    ) -> Dict[str, Any]:
        """
        Generate journal entries for multiple transactions.

        Args:
            transactions: List of transaction dictionaries

        Returns:
            Results for all transactions
        """
        results = {
            "total": len(transactions),
            "successful": 0,
            "failed": 0,
            "entries": [],
            "errors": [],
        }

        for transaction in transactions:
            result = self.generate_journal_entry(
                description=transaction.get("description", ""),
                amount=transaction.get("amount", 0),
                category=transaction.get("category", ""),
                account_type=transaction.get("account_type", ""),
            )

            if "error" not in result:
                results["successful"] += 1
                results["entries"].append(result)
            else:
                results["failed"] += 1
                results["errors"].append(
                    {
                        "transaction": transaction,
                        "error": result.get("error", "Unknown error"),
                    }
                )

        logger.info(
            f"Batch processing complete: {results['successful']} successful, {results['failed']} failed"
        )

        return results
