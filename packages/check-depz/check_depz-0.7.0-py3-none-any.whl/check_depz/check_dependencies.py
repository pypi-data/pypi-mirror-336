import subprocess
import sys
import shlex

def main():
    result = subprocess.run(
        shlex.split("poetry show  --outdated --top-level"), 
        capture_output=True, text=True
    )
    outdated_packages = result.stdout.strip().split("\n")
    outdated_count = len(outdated_packages) - 1

    print(f"Number of outdated dependencies: {outdated_count}")
    print()
    print(result.stdout)

    limit = 10
    if outdated_count > limit:
        print(f"Too many outdated dependencies (limit is {limit}). Check failed.")
        sys.exit(1)
    else:
        print("Dependency check passed.")
        sys.exit(0)


if __name__ == "__main__":
    main()