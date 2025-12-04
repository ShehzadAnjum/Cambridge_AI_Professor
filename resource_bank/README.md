# A-Level Past Papers Resource Bank

This directory contains past papers, mark schemes, and examiner reports for A-Level subjects.

## Directory Structure

```
resource_bank/
├── Accounting_9706/
│   ├── 2025/
│   │   ├── Past_Paper/
│   │   ├── Mark_Scheme/
│   │   └── Examiner_Report/
│   ├── 2024/
│   │   ├── Past_Paper/
│   │   ├── Mark_Scheme/
│   │   └── Examiner_Report/
│   └── ... (2023, 2022, 2021)
├── Economics_9708/
│   └── ... (same structure)
├── Mathematics_9709/
│   └── ... (same structure)
└── English_General_Paper_8021/
    └── ... (same structure)
```

## Subjects

- **Accounting (9706)**: https://gceguide.com/past-papers/A-AS-Level/Accounting-9706/
- **Economics (9708)**: https://gceguide.com/past-papers/A-AS-Level/Economics-9708/
- **Mathematics (9709)**: https://gceguide.com/past-papers/A-AS-Level/Mathematics-9709/
- **English General Paper (8021)**: https://gceguide.com/past-papers/A-AS-Level/English-General-Paper-8021/

## Downloading Past Papers

To download past papers, mark schemes, and examiner reports:

1. Ensure the website (gceguide.com) is accessible
2. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```
3. Run the download script:
   ```bash
   python3 download_past_papers.py
   ```

The script will:
- Download files for the last 5 years (2021-2025)
- Automatically categorize files as Past Papers, Mark Schemes, or Examiner Reports
- Organize them into the appropriate directories
- Skip files that already exist

## Notes

- The script includes retry logic for network issues
- Files are organized by subject, year, and type
- The script respects rate limits with delays between requests


