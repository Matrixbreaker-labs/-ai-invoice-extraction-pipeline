# 📄 Resilient AI Batch Invoice Extraction Pipeline

An automated data ingestion and auditing pipeline powered by **Google Gemini API** and **Python**. It extracts structured financial data from supplier PDF invoices, validates missing fields, and flags corrupted files for manual review without breaking the workflow.

## 🚀 Key Features
- **Automated Batch Processing:** Iterates through multiple PDF invoices seamlessly.
- **Fault-Tolerant Error Handling:** Flags corrupted or incomplete documents (`MANUAL REVIEW REQUIRED`) instead of crashing.
- **Structured CSV Export:** Outputs clean, audit-ready financial records into `supplier_invoices_extracted.csv`.

## 🛠️ Tech Stack
- Python 3.x
- Google Gemini API
- Pandas & Pydantic

## 📸 Execution Output
*(আপনার স্ক্রিনশটটি GitHub-এ আপলোড করার পর এখানে ইমেজ লিংক যুক্ত করে দিন)*

## ⚙️ How to Run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set your `GEMINI_API_KEY` in environment variables or Google Colab Secrets.
3. Run the script to generate the extracted CSV report.
