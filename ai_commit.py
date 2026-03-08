import subprocess
import os
from google import genai
import threading
import itertools
import time
import sys
import re

def spinner(stop_event):
    for char in itertools.cycle(["|", "/", "-", "\\"]):
        if stop_event.is_set():
            break
        sys.stdout.write(f"\rGenerating commit message... {char}")
        sys.stdout.flush()
        time.sleep(0.1)


def get_staged_diff():  
    diff = subprocess.check_output(["git", "diff", "--staged", "--", ".", ":(exclude)package-lock.json", ":(exclude)*.map"], text=True, encoding="utf-8")

    if not diff.strip():
        print("No staged changes found. Run git add first.")
        exit()

    return diff[:4000]    

def is_first_commit():
    try:
        # If this fails, there are no commits yet
        subprocess.check_output(['git', 'rev-parse', 'HEAD'], stderr=subprocess.STDOUT)
        return False
    except subprocess.CalledProcessError:
        return True


def generate_commit_messages(diff):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("""
        No API key found.

        Please set your API key:

        Windows (PowerShell):
        setx GEMINI_API_KEY "your_key_here"

        Mac/Linux:
        export GEMINI_API_KEY="your_key_here"
        """)
        exit()

    client = genai.Client(api_key=api_key)

    first_commit_rule = ""
    if is_first_commit():
        first_commit_rule = "3. This is the FIRST commit of the project. Option 1 MUST be 'feat: initial commit'."
    else:
        first_commit_rule = "3. Be accurate to the specific logic changed in the diff."

    prompt = f"""
                You are an expert developer. Based on the following git diff, generate 3 concise conventional commit messages.

                Rules:
                1. Format: <type>(<scope>): <description>
                2. Types: feat, fix, refactor, docs, chore
                {first_commit_rule}
                4. Do not describe internal variable changes unless they represent a functional change.

                Git diff:
                {diff}
                """
    
    stop_event = threading.Event()
    spinner_thread = threading.Thread(target=spinner, args=(stop_event,))
    spinner_thread.start()
    
    response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=prompt,
            config={
                "temperature": 0.1,
            }
        )
    
    stop_event.set()
    spinner_thread.join()
    
    return [m.strip() for m in response.text.strip().split("\n") if m.strip()]

def choose_message(messages):
    print("\n\nSuggested Commit Messages:\n")

    cleaned_messages = []
    for msg in messages:
        # Strip leading "1. ", "2. ", "- ", etc.
        cleaned = re.sub(r'^[\d\-\s\.]+', '', msg).strip()
        if cleaned:
            cleaned_messages.append(cleaned)

    for i, msg in enumerate(cleaned_messages, 1):
        print(f"{i}. {msg}")

    choice = input("\nChoose commit message (1-3) or 'n' to cancel: ")

    if choice in ["1", "2", "3"]:
        index = int(choice) - 1
        selected = messages[index]
        # Clean up common AI prefixes like "1. " or "- "
        if ". " in selected:
            selected = selected.split(". ", 1)[1]
        elif "- " in selected:
            selected = selected.split("- ", 1)[1]
        return selected

    return None

def commit_message(message):
    subprocess.run(["git", "commit", "-m", message])
    print("Committed successfully.")


def main():
    if not os.path.exists(".git"):
        print("Error: This directory is not a git repository.")
        return
    
    diff = get_staged_diff()

    messages = generate_commit_messages(diff)

    selected = choose_message(messages)

    if not selected:
        print("Commit cancelled.")
        return

    commit_message(selected)


if __name__ == "__main__":
    main()
