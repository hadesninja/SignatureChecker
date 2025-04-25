# SignatureChecker GUI Tool

A Python GUI application to run and parse [Microsoft Sysinternals](https://learn.microsoft.com/en-us/sysinternals/downloads/sigcheck) **sigcheck.exe** tool across selected files and folders. It displays the results in a user-friendly table format and provides options to export results to a CSV file.

---

## 📦 Features

- ✅ Download and use **sigcheck.exe** automatically
- ✅ Select **multiple files** for scanning
- ✅ Select **entire folders** (recursive scan)
- ✅ Display results with detailed metadata:
  - Verified
  - Signing Date
  - Publisher
  - Company
  - Description
  - Product
  - Product Version
  - File Version
  - MachineType
- ✅ Export output to a **CSV file**
- ✅ Error handling for invalid files or command failures
- ✅ File Menu and Help Menu with:
  - `Exit`
  - `Documentation`
  - `About (Version 1.0, Developer: Vaibhav Patil)`

---

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- PyQt5
- `requests` module

### Install dependencies

```bash
pip install pyqt5 requests
```

---

## ▶️ Run the Application

```bash
python SignatureChecker.py
```

---

## 📁 Usage

1. **Select Files** – Choose one or more files to scan.
2. **Select Folder** – Optionally select a folder to scan recursively.
3. Click **Run Sigcheck** to process the selected items.
4. Results will appear in the table.
5. Click **Save to CSV** to export the data.

---

## 📚 Menus

- **File > Exit**: Closes the application
- **Help > Doc**: Opens a message box explaining `sigcheck.exe`
- **Help > About**: Shows app version and developer info

---

## 🛠 Developer Info

- **Version**: 1.0  
- **Developer**: Vaibhav Patil

---

## 📜 License

This project uses [Sysinternals Sigcheck](https://learn.microsoft.com/en-us/sysinternals/downloads/sigcheck) under Microsoft's terms of use.

---
