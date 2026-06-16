"""
Financial reporting agent for AfriFin AI CFO.

Generates financial reports (P&L, Balance Sheet, Cash Flow).
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import pandas as pd

logger = logging.getLogger(__name__)


class ReportingAgent:
    """Agent for generating financial reports."""

    def __init__(self):
        """Initialize the reporting agent."""
        self.currency = "KES"

    def generate_profit_loss_statement(
        self, transactions: List[Dict[str, Any]], start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate Profit & Loss statement.

        Args:
            transactions: List of transaction dictionaries
            start_date: Start date for report period (YYYY-MM-DD)
            end_date: End date for report period (YYYY-MM-DD)

        Returns:
            P&L statement dictionary
        """
        try:
            df = pd.DataFrame(transactions)

            # Filter by date if provided
            if start_date:
                df = df[df["date"] >= start_date]
            if end_date:
                df = df[df["date"] <= end_date]

            # Calculate totals by category
            revenue = 0
            expenses = 0

            for _, row in df.iterrows():
                if "Revenue" in row.get("account_type", ""):
                    revenue += row.get("amount", 0)
                elif "Expense" in row.get("account_type", ""):
                    expenses += row.get("amount", 0)

            gross_profit = revenue - expenses
            net_profit = gross_profit  # Simplified; could include taxes

            report = {
                "type": "Profit & Loss Statement",
                "period_start": start_date or "Beginning",
                "period_end": end_date or "Current",
                "currency": self.currency,
                "revenue": revenue,
                "expenses": expenses,
                "gross_profit": gross_profit,
                "net_profit": net_profit,
                "generated_at": datetime.now().isoformat(),
            }

            logger.info("P&L statement generated")
            return report

        except Exception as e:
            logger.error(f"Error generating P&L statement: {e}")
            return {"error": str(e)}

    def generate_balance_sheet(
        self, transactions: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Generate Balance Sheet.

        Args:
            transactions: List of transaction dictionaries

        Returns:
            Balance Sheet dictionary
        """
        try:
            df = pd.DataFrame(transactions)

            assets = 0
            liabilities = 0
            equity = 0

            for _, row in df.iterrows():
                amount = row.get("amount", 0)
                account_type = row.get("account_type", "")

                if "Asset" in account_type:
                    assets += amount
                elif "Liability" in account_type:
                    liabilities += amount
                elif "Equity" in account_type:
                    equity += amount

            # Balance sheet equation
            total_assets = assets
            total_liabilities_equity = liabilities + equity

            report = {
                "type": "Balance Sheet",
                "as_of": datetime.now().strftime("%Y-%m-%d"),
                "currency": self.currency,
                "assets": {
                    "current_assets": assets * 0.7,  # Simplified
                    "fixed_assets": assets * 0.3,
                    "total_assets": total_assets,
                },
                "liabilities": {
                    "current_liabilities": liabilities,
                    "total_liabilities": liabilities,
                },
                "equity": {
                    "owner_capital": equity * 0.5,
                    "retained_earnings": equity * 0.5,
                    "total_equity": equity,
                },
                "total_liabilities_equity": total_liabilities_equity,
                "is_balanced": abs(total_assets - total_liabilities_equity) < 0.01,
                "generated_at": datetime.now().isoformat(),
            }

            logger.info("Balance sheet generated")
            return report

        except Exception as e:
            logger.error(f"Error generating balance sheet: {e}")
            return {"error": str(e)}

    def generate_cash_flow_statement(
        self, transactions: List[Dict[str, Any]], start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate Cash Flow statement.

        Args:
            transactions: List of transaction dictionaries
            start_date: Start date for report period
            end_date: End date for report period

        Returns:
            Cash Flow statement dictionary
        """
        try:
            df = pd.DataFrame(transactions)

            # Filter by date if provided
            if start_date:
                df = df[df["date"] >= start_date]
            if end_date:
                df = df[df["date"] <= end_date]

            operating_cash_flow = 0
            investing_cash_flow = 0
            financing_cash_flow = 0

            for _, row in df.iterrows():
                amount = row.get("amount", 0)
                category = row.get("category", "").lower()

                # Simplified categorization
                if any(word in category for word in ["expense", "revenue"]):
                    operating_cash_flow += amount
                elif "fixed" in category or "asset" in category:
                    investing_cash_flow -= amount
                elif "capital" in category or "debt" in category:
                    financing_cash_flow += amount

            net_cash_flow = operating_cash_flow + investing_cash_flow + financing_cash_flow

            report = {
                "type": "Cash Flow Statement",
                "period_start": start_date or "Beginning",
                "period_end": end_date or "Current",
                "currency": self.currency,
                "operating_activities": operating_cash_flow,
                "investing_activities": investing_cash_flow,
                "financing_activities": financing_cash_flow,
                "net_increase_in_cash": net_cash_flow,
                "generated_at": datetime.now().isoformat(),
            }

            logger.info("Cash flow statement generated")
            return report

        except Exception as e:
            logger.error(f"Error generating cash flow statement: {e}")
            return {"error": str(e)}

    def export_report_to_csv(self, report: Dict[str, Any], filename: str) -> str:
        """
        Export report to CSV file.

        Args:
            report: Report dictionary
            filename: Output filename

        Returns:
            Path to exported file
        """
        try:
            # Flatten report dictionary
            df = pd.DataFrame([report])

            output_path = f"reports/{filename}"
            df.to_csv(output_path, index=False)

            logger.info(f"Report exported to {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Error exporting report: {e}")
            return ""

    def get_summary_statistics(
        self, transactions: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Get summary statistics from transactions.

        Args:
            transactions: List of transactions

        Returns:
            Summary statistics
        """
        try:
            df = pd.DataFrame(transactions)

            total_revenue = df[df["account_type"].str.contains("Revenue", na=False)]["amount"].sum()
            total_expenses = df[df["account_type"].str.contains("Expense", na=False)]["amount"].sum()
            total_transactions = len(df)
            average_transaction = df["amount"].mean()

            return {
                "total_revenue": total_revenue,
                "total_expenses": total_expenses,
                "net_income": total_revenue - total_expenses,
                "total_transactions": total_transactions,
                "average_transaction": average_transaction,
                "largest_transaction": df["amount"].max(),
                "smallest_transaction": df["amount"].min(),
            }

        except Exception as e:
            logger.error(f"Error calculating statistics: {e}")
            return {}

    def format_report_for_display(self, report: Dict[str, Any]) -> str:
        """
        Format report for display.

        Args:
            report: Report dictionary

        Returns:
            Formatted report string
        """
        formatted = ""
        formatted += f"{'='*60}\n"
        formatted += f"{report.get('type', 'Report').upper()}\n"
        formatted += f"{'='*60}\n\n"

        for key, value in report.items():
            if key not in ["type", "generated_at"]:
                if isinstance(value, dict):
                    formatted += f"{key}:\n"
                    for sub_key, sub_value in value.items():
                        formatted += f"  {sub_key}: {sub_value:,.2f} {self.currency}\n"
                else:
                    if isinstance(value, float):
                        formatted += f"{key}: {value:,.2f} {self.currency}\n"
                    else:
                        formatted += f"{key}: {value}\n"

        formatted += f"\nGenerated: {report.get('generated_at', 'Unknown')}\n"
        formatted += f"{'='*60}\n"

        return formatted
