import os
from git import Repo
from rich.table import Table
from rich.console import Console

console = Console()

def find_large_files(threshold, unit="MB"):
    try:
        repo = Repo(os.getcwd(), search_parent_directories=True)
    except Exception:
        console.print("Error: Not a git repository (or any of the parent directories).")
        return
    unit = unit.upper()
    if unit not in ("KB", "MB", "GB"):
        console.print(f"Error: Unsupported unit '{unit}'. Use KB, MB, or GB.")
        return
    if threshold <= 0:
        console.print("Error: Threshold must be greater than zero.")
        return
    if not repo.head.is_valid():
        console.print("Error: No commits found in this repository.")
        return
    if unit == "KB":
        threshold_bytes = threshold * 1024
    elif unit == "MB":
        threshold_bytes = threshold * 1024 * 1024
    elif unit == "GB":
        threshold_bytes = threshold * 1024 * 1024 * 1024
    found = []
    total_files = 0

    console.print(f"Scanning for files larger than [bold]{threshold}{unit}[/bold] in Git history\n")

    try:
        for commit in repo.iter_commits():
            for item in commit.tree.traverse():
                if item.type == "blob":
                    total_files += 1
                    if item.size > threshold_bytes:
                        size_in_unit = item.size / (1024 if unit == "KB" else 1024*1024 if unit == "MB" else 1024*1024*1024)
                        found.append((item.path, size_in_unit, commit.hexsha[:7], item.size))
    except Exception as e:
        console.print(f"Error while scanning commits: {e}")
        return
    if not found:
        console.print("No large files found.")
        console.print(f"Total files scanned: {total_files}")
        return

    console.print(f"Large Files Found-\n")
    for path, size, commit, _ in found:
        console.print(f"- File: {path}")
        console.print(f"  Size: {size:.2f} {unit}")
        console.print(f"  Commit: {commit}\n")
    # Summary statistics
    largest = max(found, key=lambda x: x[3])
    smallest = min(found, key=lambda x: x[3])
    console.print(f"[bold]Summary:[/bold]")
    console.print(f"  Total files scanned: {total_files}")
    console.print(f"  Large files found: {len(found)}")
    console.print(f"  Largest file: {largest[0]} ({largest[1]:.2f} {unit})")
    console.print(f"  Smallest large file: {smallest[0]} ({smallest[1]:.2f} {unit})")

def find_large_files_in_dir(threshold, unit="MB"):
    import os
    unit = unit.upper()
    if unit not in ("KB", "MB", "GB"):
        console.print(f"Error: Unsupported unit '{unit}'. Use KB, MB, or GB.")
        return
    if threshold <= 0:
        console.print("Error: Threshold must be greater than zero.")
        return
    if unit == "KB":
        threshold_bytes = threshold * 1024
    elif unit == "MB":
        threshold_bytes = threshold * 1024 * 1024
    elif unit == "GB":
        threshold_bytes = threshold * 1024 * 1024 * 1024
    found = []
    total_files = 0
    console.print(f"Scanning working directory for files larger than [bold]{threshold}{unit}[/bold]...\n")
    try:
        for root, dirs, files in os.walk(os.getcwd()):
            for file in files:
                total_files += 1
                file_path = os.path.join(root, file)
                try:
                    size = os.path.getsize(file_path)
                except Exception:
                    continue
                if size > threshold_bytes:
                    size_in_unit = size / (1024 if unit == "KB" else 1024*1024 if unit == "MB" else 1024*1024*1024)
                    found.append((file_path, size_in_unit, size))
    except Exception as e:
        console.print(f"Error while scanning directory: {e}")
        return
    if not found:
        console.print("No large files found in working directory.")
        console.print(f"Total files scanned: {total_files}")
        return
    console.print(f"Large Files Found in Working Directory-\n")
    for path, size, _ in found:
        console.print(f"- File: {path}")
        console.print(f"  Size: {size:.2f} {unit}\n")
    # Summary statistics
    largest = max(found, key=lambda x: x[2])
    smallest = min(found, key=lambda x: x[2])
    console.print(f"[bold]Summary:[/bold]")
    console.print(f"  Total files scanned: {total_files}")
    console.print(f"  Large files found: {len(found)}")
    console.print(f"  Largest file: {largest[0]} ({largest[1]:.2f} {unit})")
    console.print(f"  Smallest large file: {smallest[0]} ({smallest[1]:.2f} {unit})")

def generate_pre_commit_hook(threshold, unit="MB"):
    import os
    import stat
    unit = unit.upper()
    if unit not in ("KB", "MB", "GB"):
        console.print(f"Error: Unsupported unit '{unit}'. Use KB, MB, or GB.")
        return
    if threshold <= 0:
        console.print("Error: Threshold must be greater than zero.")
        return
    if unit == "KB":
        threshold_bytes = threshold * 1024
    elif unit == "MB":
        threshold_bytes = threshold * 1024 * 1024
    elif unit == "GB":
        threshold_bytes = threshold * 1024 * 1024 * 1024
    hook_path = os.path.join(os.getcwd(), ".git", "hooks", "pre-commit")
    script = f'''#!/bin/sh
# Auto-generated by gitrim
THRESHOLD={int(threshold_bytes)}

fail=0

# Check all staged files
for file in $(git diff --cached --name-only); do
    if [ -f "$file" ]; then
        size=$(stat -c%s "$file")
        if [ "$size" -gt "$THRESHOLD" ]; then
            echo "[gitrim] ERROR: $file is $(echo "scale=2; $size / {1024 if unit == 'KB' else 1024*1024 if unit == 'MB' else 1024*1024*1024}" | bc) {unit} (limit: {threshold} {unit})"
            fail=1
        fi
    fi
done

if [ $fail -ne 0 ]; then
    echo "[gitrim] Commit aborted due to large files."
    exit 1
fi
'''
    try:
        with open(hook_path, "w") as f:
            f.write(script)
        os.chmod(hook_path, os.stat(hook_path).st_mode | stat.S_IEXEC)
        console.print(f"[green]Pre-commit hook generated at {hook_path}[/green]")
    except Exception as e:
        console.print(f"Error writing pre-commit hook: {e}")

def remove_large_files_in_dir(threshold, unit="MB", dry_run=True, yes=False):
    import os
    unit = unit.upper()
    if unit not in ("KB", "MB", "GB"):
        console.print(f"Error: Unsupported unit '{unit}'. Use KB, MB, or GB.")
        return
    if threshold <= 0:
        console.print("Error: Threshold must be greater than zero.")
        return
    if unit == "KB":
        threshold_bytes = threshold * 1024
    elif unit == "MB":
        threshold_bytes = threshold * 1024 * 1024
    elif unit == "GB":
        threshold_bytes = threshold * 1024 * 1024 * 1024
    found = []
    total_files = 0
    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            total_files += 1
            file_path = os.path.join(root, file)
            try:
                size = os.path.getsize(file_path)
            except Exception:
                continue
            if size > threshold_bytes:
                size_in_unit = size / (1024 if unit == "KB" else 1024*1024 if unit == "MB" else 1024*1024*1024)
                found.append((file_path, size_in_unit, size))
    if not found:
        console.print("No large files found in working directory.")
        console.print(f"Total files scanned: {total_files}")
        return
    console.print(f"Large files to be removed (>{threshold}{unit}):\n")
    for path, size, _ in found:
        console.print(f"- File: {path}")
        console.print(f"  Size: {size:.2f} {unit}")
    if dry_run:
        console.print("\n[bold yellow]Dry run:[/bold yellow] No files were deleted.")
    # Summary statistics
    largest = max(found, key=lambda x: x[2])
    smallest = min(found, key=lambda x: x[2])
    console.print(f"[bold]Summary:[/bold]")
    console.print(f"  Total files scanned: {total_files}")
    console.print(f"  Large files found: {len(found)}")
    console.print(f"  Largest file: {largest[0]} ({largest[1]:.2f} {unit})")
    console.print(f"  Smallest large file: {smallest[0]} ({smallest[1]:.2f} {unit})")
    if dry_run:
        return
    if not yes:
        try:
            confirm = input("\nAre you sure you want to delete these files? (y/N): ").strip().lower()
        except Exception:
            confirm = "n"
        if confirm != "y":
            console.print("Aborted. No files were deleted.")
            return
    deleted = 0
    for path, _, _ in found:
        try:
            os.remove(path)
            deleted += 1
        except Exception as e:
            console.print(f"Error deleting {path}: {e}")
    console.print(f"\n[green]Deleted {deleted} file(s) larger than {threshold}{unit}.[/green]")