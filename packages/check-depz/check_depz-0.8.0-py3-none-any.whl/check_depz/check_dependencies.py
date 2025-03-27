import subprocess
import sys
import shlex

def check_poetry_output(name: str, command: str, limit: int) -> bool:
    result = subprocess.run(
        shlex.split(command), 
        capture_output=True, text=True
    )
    outdated_packages = result.stdout.strip().split("\n")
    outdated_count = len(outdated_packages) - 1

    print(f"Outdated {name} dependencies: {outdated_count}")
    if len(result.stdout) > 0:
        print()
        print(result.stdout)

    if outdated_count > limit:
        print(f"Too many outdated {name} dependencies (limit is {limit}). Check failed.")
        return False
    else:
        return True

def main():
    top_level_result = check_poetry_output("top level", "poetry show --outdated --top-level", 10)
    all_result = check_poetry_output("all", "poetry show --outdated", 20)
    if top_level_result and all_result:
        print("All dependency checks passed.")
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()