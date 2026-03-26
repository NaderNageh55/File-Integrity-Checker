# 🔐 Log File Integrity Monitor

A lightweight Python tool that detects unauthorized modifications to log files using **SHA-256 cryptographic hashing**.

---

## 📌 What It Does

Every time a file is modified — even by a single character — its SHA-256 hash changes completely.  
This tool records the original hashes of your log files (**baseline**), then lets you verify them at any time to detect tampering.

---

## ⚙️ How It Works

```
First run   →  compute SHA-256 for each file  →  save to baseline.json
Later runs  →  recompute hashes               →  compare with baseline
                                                        ↓
                                              🟢 INTACT   — file unchanged
                                              🔴 TAMPERED — file was modified
                                              🟡 MISSING  — file was deleted
                                              🔵 NEW      — file was added
```

---

## 🚀 Getting Started

### Requirements

- Python 3.6+
- No external libraries needed — uses only the standard library

### Installation

```bash
git clone https://github.com/NaderNageh55/log-integrity-monitor.git
cd log-integrity-monitor
```

### Run

```bash
python log_monitor.py
```

---

## 🖥️ Usage

When you run the program, you will see a simple menu:

```
========================================
   Log File Integrity Monitor
========================================
1. Record baseline (first time)
2. Check files for tampering
3. Delete baseline
4. Exit
========================================
Choose:
```

| Option | Description |
|--------|-------------|
| **1**  | Scan a file or folder and save all SHA-256 hashes |
| **2**  | Re-scan and compare against saved hashes |
| **3**  | Delete the baseline to start fresh |
| **4**  | Exit the program |

---

## 📁 Example

```
Enter file or folder path: /var/log/

  ✔ Recorded: app.log
  ✔ Recorded: error.log
  ✔ Recorded: access.log

✅ Saved 3 file(s) to baseline.json
```

After modifying a file:

```
Enter file or folder path: /var/log/

  🟢 INTACT   : app.log
  🔴 TAMPERED : error.log
  🟢 INTACT   : access.log

⚠️  Warning: 1 file(s) may have been tampered with!
```

---

## 📂 Project Structure

```
log-integrity-monitor/
│
├── log_monitor.py        # main program
├── baseline.json         # auto-generated — stores hashes (do not edit)
└── README.md             # this file
```

---


