import re
import urllib.parse
from typing import Optional
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from pydantic import BaseModel


class ArxivPaper(BaseModel):
    """Data model representing a single arXiv paper entry."""
    paper_id: str
    title: str
    abstract: str


class ArxivSearchResults(BaseModel):
    """Container model for arXiv search results."""
    papers: list[ArxivPaper]


class ArxivPlaywrightAdvancedSearch:
    """Client for interacting with arXiv's advanced search functionality."""

    BASE_URL = "https://arxiv.org/search/advanced?"
    DEFAULT_PARAMS = {
        "advanced": "1",
        "terms-0-operator": "AND",
        "terms-0-field": "abstract",
        "classification-computer_science": "y",
        "classification-physics_archives": "all",
        "classification-include_cross_list": "include",
        "date-filter_by": "all_dates",
        "date-year": "",
        "date-from_date": "",
        "date-to_date": "",
        "date-date_type": "submitted_date",
        "abstracts": "show",
        "size": "200",
        "order": "-announced_date_first"
    }

    def __init__(self, headless: bool = True):
        """
        Initialize the arXiv client.

        :param headless: Whether to run browser in headless mode (True for production)
        """
        self.headless = headless

    def construct_search_url(self, query: str) -> str:
        """
        Build the advanced search URL for a given query.

        :param query: Search term for abstract field
        :return: Complete URL for arXiv advanced search
        """
        params = self.DEFAULT_PARAMS.copy()
        params["terms-0-term"] = query
        return self.BASE_URL + urllib.parse.urlencode(params)

    def fetch_search_results(self, query: str) -> Optional[str]:
        """
        Retrieve raw HTML content from arXiv for a given search query.

        :param query: Search term to look up
        :return: HTML content as string or None if retrieval fails
        """
        try:
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(headless=self.headless)
                page = browser.new_page()
                page.goto(self.construct_search_url(query))
                page.wait_for_load_state("networkidle")
                content = page.content()
                browser.close()
                return content
        except Exception as e:
            print(f"Error fetching results: {e}")
            return None

    @staticmethod
    def parse_search_results(html_content: str) -> ArxivSearchResults:
        """
        Parse raw HTML content into structured paper data.

        :param html_content: HTML string from arXiv search results
        :return: Structured search results container
        """
        soup = BeautifulSoup(html_content, "html.parser")
        results = []

        for entry in soup.find_all("li", class_="arxiv-result"):
            paper_id = entry.find("a", href=re.compile(r"arxiv\.org/abs/"))
            title = entry.find("p", class_="title is-5 mathjax")
            abstract = entry.find("span", class_="abstract-full")

            if not all([paper_id, title, abstract]):
                continue  # Skip incomplete entries

            # Clean up abstract content
            for element in abstract.find_all("a", class_="is-size-7"):
                element.decompose()

            results.append(ArxivPaper(
                paper_id=paper_id.text.replace("arXiv:", "").strip(),
                title=title.text.strip(),
                abstract=abstract.text.replace("Abstract:", "").strip()
            ))

        return ArxivSearchResults(papers=results)

    def execute_search(self, query: str) -> ArxivSearchResults:
        """
        Complete search workflow: fetch and parse results.

        :param query: Search term to process
        :return: Structured search results
        """
        html_content = self.fetch_search_results(query)
        if not html_content:
            return ArxivSearchResults(papers=[])
        return self.parse_search_results(html_content)

    def __call__(self, query: str) -> ArxivSearchResults:
        return self.execute_search(query)