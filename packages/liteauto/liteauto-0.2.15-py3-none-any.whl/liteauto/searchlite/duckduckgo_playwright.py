import json
from pathlib import Path

from playwright.sync_api import sync_playwright

import re
from bs4 import BeautifulSoup


class SearchResult:
    def __init__(self, url, title, description):
        self.url = url
        self.title = title
        self.description = description

    def __repr__(self):
        return f"SearchResult(url={self.url}, title={self.title}, description={self.description})"


def extract_search_results(html_content: str) -> list[SearchResult]:
    """
    Extracts search results from DuckDuckGo HTML content.

    Args:
        html_content: The HTML content of the DuckDuckGo search results page.

    Returns:
        A list of SearchResult objects.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    results = []

    # Find all result containers.  DuckDuckGo uses different classes over time,
    # so we look for article tags with specific data-testid.  This is more robust
    # than relying on specific class names that can change.
    result_elements = soup.find_all('article', {'data-testid': 'result'})

    for result_element in result_elements:
        # URL
        url_element = result_element.find('a', {'data-testid': 'result-extras-url-link'})
        url = url_element['href'] if url_element else None

        # Title
        title_element = result_element.find('a', {'data-testid': 'result-title-a'})
        title = title_element.get_text(strip=True) if title_element else None

        # Description (Snippet)
        # DuckDuckGo's snippet structure can vary. We try a couple of common patterns.
        description_element = result_element.find('div', {'data-result': 'snippet'})
        if description_element:
            # DuckDuckGo sometimes includes a date within the snippet.  We try to remove it.
            date_span = description_element.find('span', class_=re.compile(
                r'MILR5XIV'))  # Regex for various dynamic date classes.
            if date_span:
                date_span.decompose()  # Remove the date span from the description.
            description = description_element.get_text(strip=True)
        else:
            description = None

        if url and title:  # Discard the element if any is None.
            results.append(SearchResult(url, title, description))

    return results

def search_duckduckgo(query,headless=False):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)  # Set headless=True for production use
        page = browser.new_page()
        page.goto('https://duckduckgo.com/')
        search_box = page.locator('input[name="q"]')
        search_box.wait_for()
        search_box.fill(query)
        search_box.press('Enter')
        page.wait_for_load_state('networkidle')
        html = page.content()
        browser.close()
        return html


def duckduckgo_playwright(query):
    try:
        res = search_duckduckgo(query)
        response = extract_search_results(res)
        return response
    except Exception as e:
        return []