import subprocess
import sys
import shlex

def check_poetry_output(name: str, command: str, limit: int) -> bool:
    result = subprocess.run(
        shlex.split(command), 
        capture_output=True, text=True
    )
    outdated_packages = [package for package in result.stdout.strip().split("\n") if package != ""] 
    outdated_count = len(outdated_packages)

    print(f"Outdated {name} dependencies: {outdated_count}/{limit}")
    for package in outdated_packages:
        print(f"\t{package}")

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