"""
Database module for AfriFin AI CFO.

Handles SQLite database operations for transactions, accounts, clients,
invoices, bills, rules, and audit logs.
"""

import sqlite3
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any

logger = logging.getLogger(__name__)


class Database:
    """SQLite database manager for AfriFin AI CFO."""

    def __init__(self, db_path: str = "data/afrifin.db"):
        """
        Initialize database connection.

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self.init_database()

    def get_connection(self) -> sqlite3.Connection:
        """
        Get database connection.

        Returns:
            SQLite connection object
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_database(self) -> None:
        """Initialize database schema."""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            # Accounts table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS accounts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    code TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    type TEXT NOT NULL,
                    category TEXT NOT NULL,
                    description TEXT,
                    balance REAL DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Transactions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    description TEXT NOT NULL,
                    amount REAL NOT NULL,
                    category TEXT NOT NULL,
                    account_type TEXT NOT NULL,
                    account_code TEXT,
                    reference_id TEXT,
                    receipt_path TEXT,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Journal Entries table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS journal_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    transaction_id INTEGER,
                    debit_account_code TEXT NOT NULL,
                    debit_amount REAL NOT NULL,
                    credit_account_code TEXT NOT NULL,
                    credit_amount REAL NOT NULL,
                    description TEXT,
                    entry_date TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (transaction_id) REFERENCES transactions(id)
                )
            """)

            # Clients table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS clients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT,
                    phone TEXT,
                    address TEXT,
                    pin TEXT,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Invoices table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS invoices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    invoice_number TEXT UNIQUE NOT NULL,
                    client_id INTEGER,
                    amount REAL NOT NULL,
                    date TEXT NOT NULL,
                    due_date TEXT,
                    status TEXT DEFAULT 'pending',
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (client_id) REFERENCES clients(id)
                )
            """)

            # Bills table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS bills (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    bill_number TEXT UNIQUE NOT NULL,
                    vendor_name TEXT NOT NULL,
                    amount REAL NOT NULL,
                    date TEXT NOT NULL,
                    due_date TEXT,
                    status TEXT DEFAULT 'unpaid',
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Rules table (for transaction categorization)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS rules (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    keyword TEXT NOT NULL,
                    category TEXT NOT NULL,
                    account_code TEXT NOT NULL,
                    priority INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Audit Logs table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS audit_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    action TEXT NOT NULL,
                    entity_type TEXT NOT NULL,
                    entity_id INTEGER,
                    old_value TEXT,
                    new_value TEXT,
                    user_id TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            conn.commit()
            logger.info("Database initialized successfully")

        except sqlite3.Error as e:
            logger.error(f"Database initialization error: {e}")
            conn.rollback()
        finally:
            conn.close()

    def insert_transaction(
        self,
        date: str,
        description: str,
        amount: float,
        category: str,
        account_type: str,
        account_code: Optional[str] = None,
        reference_id: Optional[str] = None,
        receipt_path: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> int:
        """
        Insert a transaction into the database.

        Args:
            date: Transaction date (YYYY-MM-DD format)
            description: Transaction description
            amount: Transaction amount
            category: Expense/Revenue category
            account_type: GL account type
            account_code: Chart of accounts code
            reference_id: External reference ID
            receipt_path: Path to receipt file
            notes: Additional notes

        Returns:
            Transaction ID
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO transactions
                (date, description, amount, category, account_type, account_code,
                 reference_id, receipt_path, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    date,
                    description,
                    amount,
                    category,
                    account_type,
                    account_code,
                    reference_id,
                    receipt_path,
                    notes,
                ),
            )
            conn.commit()
            transaction_id = cursor.lastrowid
            logger.info(f"Transaction inserted with ID: {transaction_id}")
            return transaction_id

        except sqlite3.Error as e:
            logger.error(f"Error inserting transaction: {e}")
            conn.rollback()
            raise
        finally:
            conn.close()

    def get_transactions(
        self, limit: int = 100, offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Retrieve transactions from database.

        Args:
            limit: Number of transactions to retrieve
            offset: Number of transactions to skip

        Returns:
            List of transaction dictionaries
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT * FROM transactions
                ORDER BY date DESC
                LIMIT ? OFFSET ?
                """,
                (limit, offset),
            )
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

        except sqlite3.Error as e:
            logger.error(f"Error retrieving transactions: {e}")
            return []
        finally:
            conn.close()

    def get_transactions_by_category(self, category: str) -> List[Dict[str, Any]]:
        """
        Get transactions filtered by category.

        Args:
            category: Transaction category

        Returns:
            List of transactions in the category
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT * FROM transactions
                WHERE category = ?
                ORDER BY date DESC
                """,
                (category,),
            )
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

        except sqlite3.Error as e:
            logger.error(f"Error retrieving transactions by category: {e}")
            return []
        finally:
            conn.close()

    def get_account_balances(self) -> Dict[str, float]:
        """
        Calculate current account balances from transactions.

        Returns:
            Dictionary of account codes and their balances
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT account_code, SUM(amount) as balance
                FROM transactions
                GROUP BY account_code
                """
            )
            rows = cursor.fetchall()
            return {row["account_code"]: row["balance"] for row in rows}

        except sqlite3.Error as e:
            logger.error(f"Error calculating account balances: {e}")
            return {}
        finally:
            conn.close()

    def insert_journal_entry(
        self,
        transaction_id: int,
        debit_account_code: str,
        debit_amount: float,
        credit_account_code: str,
        credit_amount: float,
        description: str,
        entry_date: str,
    ) -> int:
        """
        Insert a journal entry.

        Args:
            transaction_id: Associated transaction ID
            debit_account_code: Debit account code
            debit_amount: Debit amount
            credit_account_code: Credit account code
            credit_amount: Credit amount
            description: Journal entry description
            entry_date: Date of entry

        Returns:
            Journal entry ID
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO journal_entries
                (transaction_id, debit_account_code, debit_amount,
                 credit_account_code, credit_amount, description, entry_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    transaction_id,
                    debit_account_code,
                    debit_amount,
                    credit_account_code,
                    credit_amount,
                    description,
                    entry_date,
                ),
            )
            conn.commit()
            entry_id = cursor.lastrowid
            logger.info(f"Journal entry inserted with ID: {entry_id}")
            return entry_id

        except sqlite3.Error as e:
            logger.error(f"Error inserting journal entry: {e}")
            conn.rollback()
            raise
        finally:
            conn.close()

    def get_journal_entries(
        self, limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Retrieve journal entries.

        Args:
            limit: Number of entries to retrieve

        Returns:
            List of journal entry dictionaries
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT * FROM journal_entries
                ORDER BY entry_date DESC
                LIMIT ?
                """,
                (limit,),
            )
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

        except sqlite3.Error as e:
            logger.error(f"Error retrieving journal entries: {e}")
            return []
        finally:
            conn.close()

    def insert_client(
        self,
        name: str,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        address: Optional[str] = None,
        pin: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> int:
        """
        Insert a client record.

        Args:
            name: Client name
            email: Client email
            phone: Client phone
            address: Client address
            pin: Client PIN
            notes: Additional notes

        Returns:
            Client ID
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO clients
                (name, email, phone, address, pin, notes)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (name, email, phone, address, pin, notes),
            )
            conn.commit()
            return cursor.lastrowid

        except sqlite3.Error as e:
            logger.error(f"Error inserting client: {e}")
            conn.rollback()
            raise
        finally:
            conn.close()

    def get_clients(self) -> List[Dict[str, Any]]:
        """
        Retrieve all clients.

        Returns:
            List of client dictionaries
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM clients ORDER BY name")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

        except sqlite3.Error as e:
            logger.error(f"Error retrieving clients: {e}")
            return []
        finally:
            conn.close()

    def log_audit_event(
        self,
        action: str,
        entity_type: str,
        entity_id: int,
        old_value: Optional[str] = None,
        new_value: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> int:
        """
        Log an audit event.

        Args:
            action: Action performed
            entity_type: Type of entity affected
            entity_id: ID of entity
            old_value: Previous value
            new_value: New value
            user_id: User performing action

        Returns:
            Audit log ID
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO audit_logs
                (action, entity_type, entity_id, old_value, new_value, user_id)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (action, entity_type, entity_id, old_value, new_value, user_id),
            )
            conn.commit()
            return cursor.lastrowid

        except sqlite3.Error as e:
            logger.error(f"Error logging audit event: {e}")
            conn.rollback()
            raise
        finally:
            conn.close()

    def get_audit_logs(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Retrieve audit logs.

        Args:
            limit: Number of logs to retrieve

        Returns:
            List of audit log dictionaries
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT * FROM audit_logs
                ORDER BY timestamp DESC
                LIMIT ?
                """,
                (limit,),
            )
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

        except sqlite3.Error as e:
            logger.error(f"Error retrieving audit logs: {e}")
            return []
        finally:
            conn.close()

    def init_default_accounts(self) -> None:
        """Initialize default chart of accounts."""
        conn = self.get_connection()
        cursor = conn.cursor()

        default_accounts = [
            ("1010", "Cash", "Asset", "Current Asset", "Physical currency"),
            (
                "1020",
                "Bank",
                "Asset",
                "Current Asset",
                "Bank account balances",
            ),
            (
                "1030",
                "Accounts Receivable",
                "Asset",
                "Current Asset",
                "Money owed by customers",
            ),
            (
                "2010",
                "Accounts Payable",
                "Liability",
                "Current Liability",
                "Money owed to suppliers",
            ),
            (
                "3010",
                "Owner's Capital",
                "Equity",
                "Owner Equity",
                "Owner investment",
            ),
            (
                "3020",
                "Retained Earnings",
                "Equity",
                "Owner Equity",
                "Accumulated profits",
            ),
            ("4010", "Service Revenue", "Revenue", "Operating Revenue", "Service fees"),
            (
                "4020",
                "Product Revenue",
                "Revenue",
                "Operating Revenue",
                "Product sales",
            ),
            ("5010", "Fuel Expense", "Expense", "Operating Expense", "Fuel costs"),
            (
                "5020",
                "Internet Expense",
                "Expense",
                "Operating Expense",
                "Internet bills",
            ),
            (
                "5030",
                "Utilities Expense",
                "Expense",
                "Operating Expense",
                "Electricity, water",
            ),
            ("5040", "Rent Expense", "Expense", "Operating Expense", "Office rent"),
            ("5050", "Salary Expense", "Expense", "Operating Expense", "Employee salaries"),
            (
                "5060",
                "Office Supplies Expense",
                "Expense",
                "Operating Expense",
                "Office supplies",
            ),
        ]

        try:
            for code, name, acc_type, category, description in default_accounts:
                cursor.execute(
                    """
                    INSERT OR IGNORE INTO accounts
                    (code, name, type, category, description)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (code, name, acc_type, category, description),
                )
            conn.commit()
            logger.info("Default accounts initialized")

        except sqlite3.Error as e:
            logger.error(f"Error initializing default accounts: {e}")
            conn.rollback()
        finally:
            conn.close()
