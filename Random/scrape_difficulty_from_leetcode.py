import pandas as pd
import time
from playwright.sync_api import sync_playwright, TimeoutError

INPUT_FILE = "Coding Patterns Practice.xlsx"
OUTPUT_FILE = "Coding Patterns Practice_withDifficulty.xlsx"

URL_COLUMN = "Problem Link"
DIFFICULTY_COLUMN = "Difficulty"
PUBLIC_COLUMN = "is_public"

DIFF_MAP = {
    "Easy": 1,
    "Medium": 2,
    "Hard": 3
}

def extract_difficulty(page):
    """
    Extract Easy/Medium/Hard from fully rendered page.
    """
    try:
        text = page.inner_text("body")

        for diff in DIFF_MAP:
            if diff in text:
                return DIFF_MAP[diff]

    except:
        return None

    return None  # difficulty not found


def is_problem_public(page):
    """
    Check whether the problem is accessible without subscription.
    A premium problem shows:
        - Messages like "Subscribe to unlock"
        - Locked content or paywall banners
        - Missing problem title or difficulty
    """
    try:
        text = page.inner_text("body")

        # Premium indicators
        locked_keywords = [
            "Subscribe to unlock", 
            "Unlock to see the solution",
            "LeetCode Premium",
            "To view this solution"
        ]

        for word in locked_keywords:
            if word.lower() in text.lower():
                return False  # locked problem

        # If problem title exists, usually public
        # LeetCode title often appears in h1 or spans
        try:
            title_elements = page.query_selector_all("h1, h2, span.text-title-large")
            if title_elements:
                return True
        except:
            pass

        # If difficulty is available → public
        for diff in DIFF_MAP:
            if diff in text:
                return True

    except:
        return False

    return False  # default to locked if unsure


def scrape():
    df = pd.read_excel(INPUT_FILE)

    # Add columns if missing
    if DIFFICULTY_COLUMN not in df.columns:
        df[DIFFICULTY_COLUMN] = ""

    if PUBLIC_COLUMN not in df.columns:
        df[PUBLIC_COLUMN] = ""

    with sync_playwright() as p:
        # Use headed mode for reliability
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        for i, url in enumerate(df[URL_COLUMN]):
            if not isinstance(url, str) or not url.startswith("http"):
                continue

            print(f"\n[{i+1}/{len(df)}] Opening {url} ...")

            try:
                page.goto(url, timeout=25000, wait_until="domcontentloaded")
                time.sleep(1.5)  # Let JS fully render

                # Determine if problem is public or locked
                public = is_problem_public(page)
                df.at[i, PUBLIC_COLUMN] = public

                if not public:
                    print("  → Locked / requires subscription.")
                    df.at[i, DIFFICULTY_COLUMN] = ""
                    continue

                # Extract difficulty for public problems
                difficulty = extract_difficulty(page)

                if difficulty is None:
                    print("  → Difficulty not found.")
                    df.at[i, DIFFICULTY_COLUMN] = ""
                else:
                    df.at[i, DIFFICULTY_COLUMN] = difficulty
                    print(f"  → Difficulty: {difficulty}")

            except TimeoutError:
                print("  → Timeout loading page.")
                df.at[i, DIFFICULTY_COLUMN] = ""
                df.at[i, PUBLIC_COLUMN] = False

            except Exception as e:
                print(f"  → Error: {e}")
                df.at[i, DIFFICULTY_COLUMN] = ""
                df.at[i, PUBLIC_COLUMN] = False

            time.sleep(1)

        browser.close()

    df.to_excel(OUTPUT_FILE, index=False)
    print(f"\nDONE! Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    scrape()