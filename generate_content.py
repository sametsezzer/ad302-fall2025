import csv
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from openai import OpenAI

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("Error: OPENAI_API_KEY environment variable is not set.")
    sys.exit(1)

client = OpenAI(api_key=OPENAI_API_KEY)
MODEL = "gpt-4o-search-preview"


def read_urls(filepath="sites.csv"):
    urls = []
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            url = row.get("url", "").strip()
            if url:
                urls.append(url)
    return urls


def clean_phone(text):
    """Extract just the phone number from a response that may contain markdown."""
    # Look for a phone number pattern in the text
    match = re.search(r'[\+\d][\d\s\-\(\)\.]{5,}', text)
    if match:
        return match.group(0).strip()
    if "not found" in text.lower():
        return "Not found"
    return text.strip()


def find_phone(url):
    prompt = (
        f"Visit this website and find the contact phone number: {url}. "
        "Return only the phone number or 'Not found' if unavailable."
    )
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            web_search_options={},
        )
        raw = response.choices[0].message.content.strip()
        result = clean_phone(raw)
        print(f"[phone] {url} -> {result}")
        return url, result
    except Exception as e:
        print(f"[error] {url} -> {e}")
        return url, "Not found"


def research_site(url):
    prompt = (
        f"Visit this website: {url}. "
        "Find out what the business does, their products/services, brand story, and any notable info. "
        "Write a clear 3-4 sentence English summary."
    )
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            web_search_options={},
        )
        summary = response.choices[0].message.content.strip()
        return summary
    except Exception as e:
        print(f"[error] research {url} -> {e}")
        return "Summary not available."


def main():
    urls = read_urls("sites.csv")
    if not urls:
        print("No URLs found in sites.csv.")
        sys.exit(1)

    print(f"Found {len(urls)} URLs. Starting parallel phone lookup...")

    results = [None] * len(urls)

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_index = {executor.submit(find_phone, url): i for i, url in enumerate(urls)}
        for future in as_completed(future_to_index):
            i = future_to_index[future]
            url, phone = future.result()
            results[i] = (url, phone)

    with open("phones.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["url", "phone"])
        for url, phone in results:
            writer.writerow([url, phone])

    print("Saved phones.csv")

    first_url = urls[0]
    print(f"\nResearching first site: {first_url} ...")
    summary = research_site(first_url)

    with open("content.txt", "w", encoding="utf-8") as f:
        f.write(summary)

    print("Saved content.txt")
    print("\nDone.")


if __name__ == "__main__":
    main()
