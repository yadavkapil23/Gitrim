# Gitrim

**Keep your git repositories clean and lean!**

Gitrim is a powerful, user-friendly CLI tool to help you detect, block, and remove large files from your git repositories and working directories. It also helps you prevent accidental commits of oversized files with a pre-commit hook.

---

## 🚀 Features
- 🔍 Scan git history for large files
- 📂 Scan working directory for large files
- 🗑️ Remove large files from the working directory (with dry-run and confirmation)
- 🛡️ Generate a pre-commit hook to block large files from being committed
- 📏 Flexible size threshold (KB, MB, GB)
- 📊 Summary statistics after each operation
- 🤝 User-friendly CLI with helpful usage info
- ⚠️ Clear error handling and confirmation prompts

---

## 🛠️ Installation

1. **Clone this repository:**
   ```sh
   git clone https://github.com/yadavkapil23/Gitrim.git
   cd Gitrim
   ```

2. **(Recommended) Create and activate a virtual environment:**
   ```sh
   python -m venv gitrim-env
   # On Windows:
   gitrim-env\Scripts\activate
   # On macOS/Linux:
   source gitrim-env/bin/activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **(Optional) Install in editable/development mode:**
   ```sh
   pip install -e .
   ```

5. **Verify installation:**
   ```sh
   gitrim --help
   ```

---

## ⚡ Usage

Run `gitrim` to see all commands and examples:
```sh
$ gitrim
```

### 1. 🔍 Scan git history for large files
```sh
$ gitrim large-files --threshold 5 --unit MB
```
- Scans the entire git history for files larger than 5 MB.

### 2. 📂 Scan working directory for large files
```sh
$ gitrim scan-working-dir --threshold 500 --unit KB
```
- Scans only the current working directory (not git history) for files larger than 500 KB.

### 3. 🗑️ Remove large files from working directory
- **Dry run (no deletion):**
  ```sh
  $ gitrim remove-large-files --threshold 2 --unit MB --dry-run
  ```
- **Actually delete (with confirmation):**
  ```sh
  $ gitrim remove-large-files --threshold 2 --unit MB
  ```
- **Actually delete (no confirmation):**
  ```sh
  $ gitrim remove-large-files --threshold 2 --unit MB --yes
  ```

### 4. 🛡️ Generate a pre-commit hook
```sh
$ gitrim generate-pre-commit-hook --threshold 1 --unit MB
```
- Creates a `.git/hooks/pre-commit` script that blocks commits containing files above the threshold.

### 5. Get help for any command
```sh
$ gitrim --help
# or
$ gitrim <command> --help
```

---

## 📦 Components

- **gitrim/cli.py**
  - The main CLI entry point. Defines all commands and options using Click.
  - Handles user input, help messages, and command dispatch.

- **gitrim/cleaner.py**
  - Contains all core logic for scanning, reporting, removing large files, and generating pre-commit hooks.
  - Handles both git history and working directory operations.
  - Provides summary statistics and user feedback.

- **requirements.txt**
  - Lists all Python dependencies: `click`, `rich`, `GitPython`.

- **README.md**
  - This file! Explains installation, usage, and features.

- **pyproject.toml**
  - Used for editable installs and packaging.

---

## 📝 Example Workflow

1. **Scan your repo for large files:**
   ```sh
   $ gitrim large-files --threshold 10 --unit MB
   ```
2. **Scan your working directory:**
   ```sh
   $ gitrim scan-working-dir --threshold 500 --unit KB
   ```
3. **Remove large files (with confirmation):**
   ```sh
   $ gitrim remove-large-files --threshold 5 --unit MB
   ```
4. **Block large files from being committed:**
   ```sh
   $ gitrim generate-pre-commit-hook --threshold 2 --unit MB
   ```

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.