import requests
import re
import subprocess

# URL of the external CSS
CSS_URL = "https://amar-louis.github.io/ticket-master/color.css"

# File inside your repo where you want to paste the root object
OUTPUT_FILE = "color.css"


def extract_root_block():
    # Download the CSS file
    response = requests.get(CSS_URL)
    css = response.text

    # Regex to extract everything inside :root { ... }
    match = re.search(r":root\s*\{[^}]*\}", css, re.DOTALL)

    if match:
        root_block = match.group(0)
        print("Found :root block:")
        print(root_block)
        return root_block
    else:
        print("No :root block found.")
        return None


def save_root_block(root_block):
    with open(OUTPUT_FILE, "w") as f:
        f.write(root_block)
    print(f"Saved root block to {OUTPUT_FILE}")


def git_commit_push():
    subprocess.run(["git", "add", "."], check=True)
     # Commit only if there is something to commit
    commit_status = subprocess.run(["git", "diff", "--cached", "--quiet"])
    if commit_status.returncode != 0:
        subprocess.run(["git", "commit", "-m", "Auto update"], check=True)
    else:
        print("No changes to commit.")

    # Try push
    result = subprocess.run(["git", "push"])
    if result.returncode == 0:
        print("Pushed to GitHub successfully!")
    else:
        print("❌ Push failed. Fix the GitHub email verification issue.")


if __name__ == "__main__":
    root_block = extract_root_block()
    if root_block:
        save_root_block(root_block)
        git_commit_push()
