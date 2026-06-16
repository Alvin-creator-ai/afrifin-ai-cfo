"""
Audit Agent for AfriFin AI CFO.

Detects anomalies and generates audit reports.
"""

import logging
from typing import Dict, List, Any
from datetime import datetime, timedelta
import pandas as pd

logger = logging.getLogger(__name__)


class AuditAgent:
    """Agent for auditing transactions and detecting anomalies."""

    def __init__(self):
        """Initialize the audit agent."""
        self.findings = []

    def audit_transactions(
        self, transactions: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Perform comprehensive audit on transactions.

        Args:
            transactions: List of transactions

        Returns:
            Audit report
        """
        self.findings = []

        # Run all audit checks
        self._check_duplicates(transactions)
        self._check_missing_classifications(transactions)
        self._check_suspicious_entries(transactions)
        self._check_unbalanced_entries(transactions)
        self._check_negative_balances(transactions)
        self._check_amount_anomalies(transactions)

        return self._generate_audit_report()

    def _check_duplicates(self, transactions: List[Dict[str, Any]]) -> None:
        """
        Check for duplicate transactions.

        Args:
            transactions: List of transactions
        """
        seen = {}

        for i, transaction in enumerate(transactions):
            key = (
                transaction.get("date"),
                transaction.get("description"),
                transaction.get("amount"),
            )

            if key in seen:
                self.findings.append(
                    {
                        "type": "duplicate_transaction",
                        "severity": "high",
                        "description": "Duplicate transaction detected",
                        "details": f"Transaction {i} matches transaction {seen[key]}",
                        "transaction_ids": [seen[key], i],
                    }
                )
            else:
                seen[key] = i

        logger.info(f"Duplicate check complete. Found {len([f for f in self.findings if f['type'] == 'duplicate_transaction'])} duplicates")

    def _check_missing_classifications(
        self, transactions: List[Dict[str, Any]]
    ) -> None:
        """
        Check for missing account classifications.

        Args:
            transactions: List of transactions
        """
        for i, transaction in enumerate(transactions):
            if not transaction.get("category") or transaction.get("category") == "Unknown":
                self.findings.append(
                    {
                        "type": "missing_classification",
                        "severity": "medium",
                        "description": "Missing transaction category",
                        "details": f"Transaction {i}: {transaction.get('description')}",
                        "transaction_id": i,
                    }
                )

        logger.info(
            f"Classification check complete. Found {len([f for f in self.findings if f['type'] == 'missing_classification'])} unclassified"
        )

    def _check_suspicious_entries(self, transactions: List[Dict[str, Any]]) -> None:
        """
        Check for suspicious or unusual entries.

        Args:
            transactions: List of transactions
        """
        if not transactions:
            return

        df = pd.DataFrame(transactions)
        amounts = df["amount"].numeric() if "amount" in df.columns else pd.Series()

        if len(amounts) > 0:
            mean = amounts.mean()
            std = amounts.std()

            for i, transaction in enumerate(transactions):
                amount = transaction.get("amount", 0)

                # Flag amounts more than 3 standard deviations from mean
                if std > 0 and abs(amount - mean) > 3 * std:
                    self.findings.append(
                        {
                            "type": "suspicious_amount",
                            "severity": "low",
                            "description": "Unusual transaction amount",
                            "details": f"Amount {amount:,.2f} is {((amount - mean) / std):.1f}σ from mean",
                            "transaction_id": i,
                            "amount": amount,
                        }
                    )

        logger.info(
            f"Suspicious entry check complete. Found {len([f for f in self.findings if f['type'] == 'suspicious_amount'])} anomalies"
        )

    def _check_unbalanced_entries(
        self, transactions: List[Dict[str, Any]]
    ) -> None:
        """
        Check for unbalanced journal entries.

        Args:
            transactions: List of transactions
        """
        for i, transaction in enumerate(transactions):
            # Check if transaction has matching debit/credit
            debit = transaction.get("debit_amount", 0)
            credit = transaction.get("credit_amount", 0)

            if debit != 0 and credit != 0 and abs(debit - credit) > 0.01:
                self.findings.append(
                    {
                        "type": "unbalanced_entry",
                        "severity": "high",
                        "description": "Unbalanced journal entry",
                        "details": f"Debits {debit} != Credits {credit}",
                        "transaction_id": i,
                    }
                )

        logger.info(
            f"Balance check complete. Found {len([f for f in self.findings if f['type'] == 'unbalanced_entry'])} unbalanced entries"
        )

    def _check_negative_balances(
        self, transactions: List[Dict[str, Any]]
    ) -> None:
        """
        Check for negative account balances.

        Args:
            transactions: List of transactions
        """
        account_balances = {}

        for transaction in transactions:
            account = transaction.get("account_code", "Unknown")
            amount = transaction.get("amount", 0)

            if account not in account_balances:
                account_balances[account] = 0

            account_balances[account] += amount

        for account, balance in account_balances.items():
            # Asset accounts shouldn't have negative balances
            if balance < 0 and account in ["1010", "1020", "1030"]:  # Asset accounts
                self.findings.append(
                    {
                        "type": "negative_balance",
                        "severity": "high",
                        "description": "Negative asset account balance",
                        "details": f"Account {account} has balance {balance:,.2f}",
                        "account": account,
                        "balance": balance,
                    }
                )

        logger.info(
            f"Balance check complete. Found {len([f for f in self.findings if f['type'] == 'negative_balance'])} negative balances"
        )

    def _check_amount_anomalies(self, transactions: List[Dict[str, Any]]) -> None:
        """
        Check for amount-related anomalies.

        Args:
            transactions: List of transactions
        """
        for i, transaction in enumerate(transactions):
            amount = transaction.get("amount", 0)

            # Check for zero amount
            if amount == 0:
                self.findings.append(
                    {
                        "type": "zero_amount",
                        "severity": "low",
                        "description": "Transaction with zero amount",
                        "details": transaction.get("description", "Unknown"),
                        "transaction_id": i,
                    }
                )

            # Check for extremely large amounts
            elif amount > 1000000:
                self.findings.append(
                    {
                        "type": "large_amount",
                        "severity": "low",
                        "description": "Unusually large transaction amount",
                        "details": f"Amount: {amount:,.2f}",
                        "transaction_id": i,
                    }
                )

    def _generate_audit_report(self) -> Dict[str, Any]:
        """
        Generate final audit report.

        Returns:
            Audit report
        """
        severity_counts = {
            "high": len([f for f in self.findings if f.get("severity") == "high"]),
            "medium": len([f for f in self.findings if f.get("severity") == "medium"]),
            "low": len([f for f in self.findings if f.get("severity") == "low"]),
        }

        report = {
            "audit_date": datetime.now().isoformat(),
            "total_findings": len(self.findings),
            "severity_summary": severity_counts,
            "findings": sorted(
                self.findings, key=lambda x: {"high": 0, "medium": 1, "low": 2}.get(x.get("severity", "low"), 3)
            ),
            "status": "PASS" if len(self.findings) == 0 else "FAIL",
        }

        logger.info(f"Audit report generated with {len(self.findings)} findings")

        return report

    def format_audit_report(self, report: Dict[str, Any]) -> str:
        """
        Format audit report for display.

        Args:
            report: Audit report dictionary

        Returns:
            Formatted report string
        """
        formatted = "=" * 70 + "\n"
        formatted += "AUDIT REPORT\n"
        formatted += "=" * 70 + "\n\n"

        formatted += f"Audit Date: {report.get('audit_date', 'Unknown')}\n"
        formatted += f"Status: {report.get('status', 'UNKNOWN')}\n"
        formatted += f"Total Findings: {report.get('total_findings', 0)}\n\n"

        severity = report.get("severity_summary", {})
        formatted += "Severity Summary:\n"
        formatted += f"  🔴 High: {severity.get('high', 0)}\n"
        formatted += f"  🟠 Medium: {severity.get('medium', 0)}\n"
        formatted += f"  🟡 Low: {severity.get('low', 0)}\n\n"

        if report.get("findings"):
            formatted += "Findings:\n"
            formatted += "-" * 70 + "\n"

            for i, finding in enumerate(report.get("findings", []), 1):
                severity_icon = {
                    "high": "🔴",
                    "medium": "🟠",
                    "low": "🟡",
                }.get(finding.get("severity", "unknown"), "❓")

                formatted += f"\n{i}. {severity_icon} {finding.get('description', 'Unknown')}\n"
                formatted += f"   Type: {finding.get('type', 'Unknown')}\n"
                formatted += f"   Details: {finding.get('details', 'N/A')}\n"
        else:
            formatted += "✅ No findings - All checks passed!\n"

        formatted += "\n" + "=" * 70 + "\n"

        return formatted

    def export_audit_report(self, report: Dict[str, Any], filename: str) -> str:
        """
        Export audit report to file.

        Args:
            report: Audit report
            filename: Output filename

        Returns:
            Path to exported file
        """
        try:
            import json
            output_path = f"reports/{filename}"
            with open(output_path, "w") as f:
                json.dump(report, f, indent=2)
            logger.info(f"Audit report exported to {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Error exporting audit report: {e}")
            return ""
