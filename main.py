import os
import json
import hashlib

BASELINE_FILE = "baseline.json"

# ── 1. Compute SHA-256 hash for a file ───────────────────────────
def get_hash(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

# ── 2. Collect all files from a folder or single file ────────────
def get_files(path):
    if os.path.isfile(path):
        return [path]
    files = []
    for root, _, names in os.walk(path):
        for name in names:
            files.append(os.path.join(root, name))
    return files

# ── 3. Save baseline hashes ──────────────────────────────────────
def save_baseline(path):
    files = get_files(path)
    baseline = {}
    for f in files:
        baseline[f] = get_hash(f)
        print(f"  ✔ Recorded: {os.path.basename(f)}")
    with open(BASELINE_FILE, "w") as out:
        json.dump(baseline, out, indent=2)
    print(f"\n✅ Saved {len(baseline)} file(s) to {BASELINE_FILE}")

# ── 4. Check files against baseline ─────────────────────────────
def check_files(path):
    # Make sure baseline exists
    if not os.path.exists(BASELINE_FILE):
        print("❌ No baseline found! Run option 1 first.")
        return

    # Load stored hashes from disk
    with open(BASELINE_FILE) as f:
        baseline = json.load(f)

    files = get_files(path)
    tampered = []

    # Compare each current file against the stored hash
    for f in files:
        current_hash = get_hash(f)
        name = os.path.basename(f)

        if f not in baseline:
            # File was added after baseline was recorded
            print(f"  🔵 NEW      : {name}")
        elif current_hash == baseline[f]:
            # Hash matches — file is untouched
            print(f"  🟢 INTACT   : {name}")
        else:
            # Hash changed — file was modified
            print(f"  🔴 TAMPERED : {name}")
            tampered.append(name)

    # Detect files that existed in baseline but are now missing
    current_paths = set(files)
    for stored in baseline:
        if stored not in current_paths:
            print(f"  🟡 MISSING  : {os.path.basename(stored)}")

    # Final report
    print()
    if tampered:
        print(f"⚠️  Warning: {len(tampered)} file(s) may have been tampered with!")
    else:
        print("✅ All files are intact. No tampering detected.")

# ── 5. Delete the baseline ───────────────────────────────────────
def reset():
    if os.path.exists(BASELINE_FILE):
        os.remove(BASELINE_FILE)
        print("🗑️  Baseline deleted.")
    else:
        print("No baseline file found — nothing to delete.")

# ── Main menu ────────────────────────────────────────────────────
def main():
    print("=" * 40)
    print("   Log File Integrity Monitor")
    print("=" * 40)
    print("1. Record baseline (first time)")
    print("2. Check files for tampering")
    print("3. Delete baseline")
    print("4. Exit")
    print("=" * 40)

    choice = input("Choose: ").strip()

    if choice in ("1", "2"):
        path = input("Enter file or folder path: ").strip()
        if not os.path.exists(path):
            print("❌ Path not found!")
            return
        if choice == "1":
            save_baseline(path)
        else:
            check_files(path)
    elif choice == "3":
        reset()
    elif choice == "4":
        print("Goodbye!")
    else:
        print("❌ Invalid choice.")

if __name__ == "__main__":
    main()