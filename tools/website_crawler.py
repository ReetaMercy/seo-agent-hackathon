import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

from playwright.sync_api import sync_playwright
from strands import tool


USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0 Safari/537.36"
)


def normalize_url(url: str) -> str:
    """Ensure the URL has a scheme."""
    url = url.strip()

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    return url


def extract_page_data(
    html: str,
    page_url: str,
) -> dict:
    """Extract basic SEO information from HTML."""

    soup = BeautifulSoup(html, "html.parser")

    # Title
    title = ""

    if soup.title:
        title = soup.title.get_text(
            " ",
            strip=True,
        )

    # Meta description
    meta_description = ""

    meta_tag = soup.find(
        "meta",
        attrs={
            "name": lambda value: (
                value
                and value.lower() == "description"
            )
        },
    )

    if meta_tag:
        meta_description = meta_tag.get(
            "content",
            "",
        ).strip()

    # H1
    h1_tags = [
        h1.get_text(
            " ",
            strip=True,
        )
        for h1 in soup.find_all("h1")
    ]

    # Canonical
    canonical = ""

    canonical_tag = soup.find(
        "link",
        rel=lambda value: (
            value
            and "canonical" in value
        ),
    )

    if canonical_tag:
        canonical = canonical_tag.get(
            "href",
            "",
        ).strip()

    # Script count
    script_count = len(
        soup.find_all("script")
    )

    # Check for common JS app roots
    javascript_framework_detected = any(
        [
            soup.find(
                "div",
                id="root",
            )
            is not None,

            soup.find(
                "div",
                id="app",
            )
            is not None,

            soup.find(
                "div",
                id="__next",
            )
            is not None,
        ]
    )

    # Visible text
    text_soup = BeautifulSoup(
        html,
        "html.parser",
    )

    for element in text_soup(
        [
            "script",
            "style",
            "noscript",
            "svg",
        ]
    ):
        element.decompose()

    visible_text = text_soup.get_text(
        " ",
        strip=True,
    )

    word_count = len(
        visible_text.split()
    )

    possible_javascript_rendering = (
        word_count < 100
        and (
            script_count >= 10
            or javascript_framework_detected
        )
    )

    return {
        "url": page_url,
        "title": title,
        "meta_description": meta_description,
        "h1": h1_tags,
        "canonical": canonical,
        "word_count": word_count,
        "script_count": script_count,
        "javascript_framework_detected": (
            javascript_framework_detected
        ),
        "possible_javascript_rendering": (
            possible_javascript_rendering
        ),
    }


@tool
def crawl_website(url: str) -> dict:
    """
    Crawl a single webpage using a real browser.
    JavaScript is rendered before extracting SEO data.
    """

    url = normalize_url(url)

    with sync_playwright() as playwright:

        browser = playwright.chromium.launch(
            headless=True,
        )

        page = browser.new_page(
            user_agent=USER_AGENT,
        )

        response = page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=30000,
        )

        # Give client-side JavaScript time to render.
        page.wait_for_timeout(2000)

        final_url = page.url
        html = page.content()

        status_code = (
            response.status
            if response
            else 0
        )

        browser.close()

    page_data = extract_page_data(
        html=html,
        page_url=final_url,
    )

    page_data["status_code"] = status_code

    return page_data


@tool
def crawl_website_pages(
    start_url: str,
    max_pages: int = 10,
) -> list[dict]:
    """
    Discover and crawl up to max_pages internal pages
    using a real browser.
    """

    start_url = normalize_url(start_url)

    parsed_start = urlparse(start_url)

    start_domain = parsed_start.netloc.lower()

    visited = set()
    queue = [start_url]
    results = []

    with sync_playwright() as playwright:

        browser = playwright.chromium.launch(
            headless=True,
        )

        page = browser.new_page(
            user_agent=USER_AGENT,
        )

        while queue and len(results) < max_pages:

            current_url = queue.pop(0)

            if current_url in visited:
                continue

            visited.add(current_url)

            try:

                response = page.goto(
                    current_url,
                    wait_until="domcontentloaded",
                    timeout=30000,
                )

                page.wait_for_timeout(2000)

                final_url = page.url

                if (
                    urlparse(final_url).netloc.lower()
                    != start_domain
                ):
                    continue

                html = page.content()

                status_code = (
                    response.status
                    if response
                    else 0
                )

                page_data = extract_page_data(
                    html=html,
                    page_url=final_url,
                )

                page_data["status_code"] = (
                    status_code
                )

                results.append(page_data)

                # ------------------------------------------
                # Discover internal links from rendered DOM
                # ------------------------------------------

                links = page.locator(
                    "a[href]"
                ).evaluate_all(
                    """
                    elements => elements.map(
                        element => element.href
                    )
                    """
                )

                for link in links:

                    if not link:
                        continue

                    parsed_link = urlparse(link)

                    if (
                        parsed_link.netloc.lower()
                        != start_domain
                    ):
                        continue

                    clean_link = link.split("#")[0]

                    if clean_link not in visited:
                        queue.append(
                            clean_link
                        )

            except Exception:
                continue

        browser.close()

    return results