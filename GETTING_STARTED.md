# GETTING STARTED

## 🎯 5-Minute Quick Start

### 1. Start the Application
```bash
streamlit run app.py
```

### 2. Navigate to "Transaction Analyzer"

### 3. Enter Your First Transaction
**Example:**
- Date: Today
- Description: "Paid Safaricom KES 15,000 for office internet"
- Amount: 15000

### 4. Click "Analyze Transaction"

The AI will automatically:
- ✅ Categorize as "Internet Expense"
- ✅ Assign account type "Operating Expense"
- ✅ Generate journal entry
- ✅ Provide IFRS compliance explanation

### 5. Click "Save Transaction"

That's it! Your first transaction is recorded.

---

## 📊 Features Overview

### 🏠 Home Page
- **Total Revenue**: Sum of all revenue transactions
- **Total Expenses**: Sum of all expense transactions
- **Net Income**: Revenue minus expenses
- **Recent Transactions**: Your last 10 entries

### 📊 Transaction Analyzer
Main feature for categorizing transactions.

**How it works:**
1. Enter transaction description
2. Enter amount
3. AI analyzes and suggests category
4. Review journal entry
5. Save to database

**Smart Features:**
- Keyword-based quick categorization
- AI fallback for complex transactions
- Historical consistency checking
- Journal entry validation

**Example Transactions:**
```
"Paid employee salary 50,000 KES"
"Received invoice payment from client 150,000 KES"
"Bought office supplies for 5,000 KES"
"Paid electricity bill 12,000 KES"
"Purchased fuel 8,500 KES"
"Monthly rent 50,000 KES"
```

### 📸 Receipt Upload
Upload receipts (PDF, PNG, JPG) for automatic processing.

**What happens:**
1. Upload receipt file
2. System extracts text using OCR
3. AI identifies: vendor, amount, date
4. Preview extracted information
5. Save as transaction

**Supported Formats:**
- PDF files
- PNG images
- JPG/JPEG images

### 📋 Reports
Generate professional financial statements.

**Available Reports:**
1. **Profit & Loss Statement**
   - Total revenue
   - Total expenses
   - Gross profit
   - Net profit

2. **Balance Sheet**
   - Assets (current + fixed)
   - Liabilities
   - Equity
   - Verification of accounting equation

3. **Cash Flow Statement**
   - Operating activities
   - Investing activities
   - Financing activities
   - Net cash increase/decrease

**Export Options:**
- CSV format for Excel
- Print-friendly view

### 🔍 Audit
Automatic validation and anomaly detection.

**Checks Performed:**
- 🔴 **High Severity:**
  - Duplicate transactions
  - Unbalanced entries
  - Negative asset balances

- 🟠 **Medium Severity:**
  - Missing classifications
  - Incomplete information

- 🟡 **Low Severity:**
  - Unusual amounts (3σ from mean)
  - Zero amount entries
  - Unusually large amounts

**Audit Report Includes:**
- Total findings count
- Severity breakdown
- Detailed issue descriptions
- Exportable JSON report

### ⚙️ Settings
Configure your business information.

**Options:**
- Business name
- Currency (KES, USD, GBP, EUR)
- Accounting standard (IFRS, US GAAP)
- Preferences

---

## 💡 Usage Examples

### Example 1: Record Operating Expense
```
Date: 2024-06-16
Description: "Paid Safaricom KES 15,000 for office internet"
Amount: 15,000

Result:
Category: Internet Expense
Account: Operating Expense
Entry:
  Dr Internet Expense    15,000
  Cr Bank                     15,000
```

### Example 2: Record Revenue
```
Date: 2024-06-16
Description: "Received payment from ABC Corp for consulting services"
Amount: 50,000

Result:
Category: Service Revenue
Account: Operating Revenue
Entry:
  Dr Bank                50,000
  Cr Service Revenue          50,000
```

### Example 3: Process Receipt
```
1. Upload receipt image
2. System extracts:
   - Vendor: "Nakumatt Supermarket"
   - Amount: KES 8,500
   - Date: 2024-06-16
   - Items: Office supplies
3. Save as transaction
```

### Example 4: Generate Monthly Report
```
1. Click "Reports"
2. Select "Profit & Loss Statement"
3. Click "Generate Report"
4. View summary of revenue and expenses
5. Export as CSV
```

---

## 🚀 Best Practices

### 1. Daily Transaction Entry
- Record transactions daily
- Use consistent descriptions
- Include all relevant details

### 2. Regular Audits
- Run audit weekly
- Address high-severity findings immediately
- Review unusual amounts

### 3. Monthly Reporting
- Generate P&L statement monthly
- Review revenue and expenses
- Compare with previous months

### 4. Receipt Management
- Store receipts for 7 years (tax requirement)
- Process receipts within 48 hours
- Keep digital copies

### 5. Account Reconciliation
- Reconcile bank account monthly
- Match transactions with receipts
- Resolve discrepancies promptly

---

## 📝 Supported Transaction Categories

| Category | Account Type | GL Code |
|----------|-------------|---------|
| Internet Expense | Operating Expense | 5020 |
| Fuel Expense | Operating Expense | 5010 |
| Utilities Expense | Operating Expense | 5030 |
| Rent Expense | Operating Expense | 5040 |
| Salary Expense | Operating Expense | 5050 |
| Office Supplies Expense | Operating Expense | 5060 |
| Service Revenue | Operating Revenue | 4010 |
| Product Revenue | Operating Revenue | 4020 |

---

## 🔐 Data Security

### API Key Protection
- Never share your OpenAI API key
- Store in `.env` file (not in code)
- Regenerate key if exposed
- Use separate keys for dev/prod

### Database Security
- Database stored locally
- Encrypted when backed up
- Regular backups recommended
- Access controlled

### Transaction Privacy
- All data stays on your device
- No cloud storage by default
- Audit logs track all changes

---

## 🆘 Getting Help

### Common Issues

**Q: AI categorization seems incorrect**
A: 
1. Check transaction description is clear
2. Run audit to review pattern
3. Add custom categorization rule in settings
4. Retrain on similar transactions

**Q: Report shows unexpected numbers**
A:
1. Verify all transactions were saved
2. Check for duplicate entries
3. Run audit to identify issues
4. Reconcile manually

**Q: Receipt upload fails**
A:
1. Ensure file is PDF, PNG, or JPG
2. Check file size < 10MB
3. Verify tesseract is installed
4. Try with clearer image

**Q: Can't connect to OpenAI**
A:
1. Verify API key in .env
2. Check internet connection
3. Ensure API key is active
4. Check OpenAI account quota

---

## 📖 Next Steps

1. ✅ Complete installation ([INSTALLATION.md](INSTALLATION.md))
2. ✅ Record your first transaction
3. ✅ Upload a receipt
4. ✅ Generate your first report
5. ✅ Run an audit
6. ✅ Customize settings
7. ✅ Explore advanced features

---

## 💬 Support & Feedback

- GitHub Issues: Report bugs and request features
- Documentation: Check README.md for detailed guides
- Community: Share best practices with other users

**Need help?** Check the [README.md](README.md) or [INSTALLATION.md](INSTALLATION.md)

Happy bookkeeping! 🎉
