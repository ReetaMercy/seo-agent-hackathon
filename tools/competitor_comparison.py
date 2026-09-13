from typing import Dict, Any, List

from strands import tool

from tools.website_crawler import crawl_website_pages
from tools.seo_issue_detector import detect_seo_issues


def calculate_average_word_count(
    pages: List[Dict[str, Any]]
) -> float:
    """Calculate average visible word count."""

    if not pages:
        return 0.0

    total_words = sum(
        int(page.get("word_count", 0) or 0)
        for page in pages
    )

    return round(total_words / len(pages), 1)


def count_pages_with_h1_issues(
    pages: List[Dict[str, Any]]
) -> int:
    """Count pages with missing or multiple H1 headings."""

    count = 0

    for page in pages:

        issues = detect_seo_issues(page)

        for issue in issues:

            if (
                "H1" in issue["issue"]
                and (
                    "Missing" in issue["issue"]
                    or "Multiple" in issue["issue"]
                )
            ):
                count += 1
                break

    return count


@tool
def compare_websites(
    target_website: str,
    competitors: List[str],
    max_pages: int = 10,
) -> Dict[str, Any]:
    """
    Crawl a target website and competitors and compare
    publicly observable technical SEO signals.
    """

    websites = [
        {
            "url": target_website,
            "type": "Target",
        }
    ]

    for competitor in competitors:

        websites.append(
            {
                "url": competitor,
                "type": "Competitor",
            }
        )

    comparison = []

    for website in websites:

        url = website["url"]
        website_type = website["type"]

        try:

            pages = crawl_website_pages(
                start_url=url,
                max_pages=max_pages,
            )

            total_issues = 0

            for page in pages:

                issues = detect_seo_issues(page)

                total_issues += len(issues)

            average_words = calculate_average_word_count(
                pages
            )

            h1_issue_pages = count_pages_with_h1_issues(
                pages
            )

            comparison.append(
                {
                    "website": url,
                    "type": website_type,
                    "pages_crawled": len(pages),
                    "average_word_count": average_words,
                    "h1_issue_pages": h1_issue_pages,
                    "total_seo_issues": total_issues,
                }
            )

        except Exception as error:

            comparison.append(
                {
                    "website": url,
                    "type": website_type,
                    "pages_crawled": 0,
                    "average_word_count": 0,
                    "h1_issue_pages": 0,
                    "total_seo_issues": 0,
                    "error": str(error),
                }
            )

    return {
        "target": target_website,
        "competitors": competitors,
        "comparison": comparison,
    }


def generate_executive_summary(
    comparison: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Generate an evidence-based executive SEO summary.

    The summary uses only publicly observable crawl signals.
    """

    if not comparison:

        return {
            "priorities": [],
            "message": "No comparison data available.",
        }

    target = next(
        (
            site
            for site in comparison
            if site["type"] == "Target"
        ),
        None,
    )

    competitors = [
        site
        for site in comparison
        if site["type"] == "Competitor"
    ]

    if not target:

        return {
            "priorities": [],
            "message": "Target website data is missing.",
        }

    priorities = []

    # ==================================================
    # 1. H1 STRUCTURE
    # ==================================================

    target_h1_issues = target["h1_issue_pages"]
    target_pages = target["pages_crawled"]

    target_h1_rate = 0.0

    if target_pages > 0:

        target_h1_rate = (
            target_h1_issues
            / target_pages
        ) * 100

    competitor_h1_rates = []

    for competitor in competitors:

        competitor_pages = competitor[
            "pages_crawled"
        ]

        if competitor_pages > 0:

            rate = (
                competitor["h1_issue_pages"]
                / competitor_pages
            ) * 100

            competitor_h1_rates.append(
                {
                    "website": competitor["website"],
                    "rate": rate,
                }
            )

    if competitor_h1_rates:

        best_competitor = min(
            competitor_h1_rates,
            key=lambda item: item["rate"],
        )

        if target_h1_rate > best_competitor["rate"]:

            priorities.append(
                {
                    "issue": "H1 structure",
                    "priority": "High",
                    "evidence": (
                        f"{target_h1_issues} of "
                        f"{target_pages} target pages "
                        f"have H1 issues, compared with "
                        f"{best_competitor['website']} "
                        f"at {best_competitor['rate']:.0f}%."
                    ),
                    "action": (
                        "Review missing and multiple H1 headings "
                        "on important SEO pages and establish "
                        "a clear heading hierarchy."
                    ),
                }
            )

    # ==================================================
    # 2. CONTENT DEPTH
    # ==================================================

    competitor_word_counts = [
        site
        for site in competitors
        if site["average_word_count"] > 0
    ]

    if competitor_word_counts:

        highest_content = max(
            competitor_word_counts,
            key=lambda item: item[
                "average_word_count"
            ],
        )

        target_words = target[
            "average_word_count"
        ]

        competitor_words = highest_content[
            "average_word_count"
        ]

        if competitor_words > target_words:

            difference = (
                competitor_words
                - target_words
            )

            priorities.append(
                {
                    "issue": "Visible content depth",
                    "priority": "Medium",
                    "evidence": (
                        f"Target average visible content is "
                        f"{target_words:.0f} words versus "
                        f"{highest_content['website']} "
                        f"at {competitor_words:.0f} words "
                        f"({difference:.0f} words higher)."
                    ),
                    "action": (
                        "Review important pages for content "
                        "coverage, search-intent alignment, "
                        "and useful topical depth. Do not add "
                        "content solely to increase word count."
                    ),
                }
            )

    # ==================================================
    # 3. TECHNICAL SEO CONSISTENCY
    # ==================================================

    if competitors:

        lowest_issue_competitor = min(
            competitors,
            key=lambda item: item[
                "total_seo_issues"
            ],
        )

        if (
            target["total_seo_issues"]
            > lowest_issue_competitor[
                "total_seo_issues"
            ]
        ):

            priorities.append(
                {
                    "issue": "Technical SEO consistency",
                    "priority": "Medium",
                    "evidence": (
                        f"Target has "
                        f"{target['total_seo_issues']} "
                        f"detected issues across "
                        f"{target['pages_crawled']} pages, "
                        f"while "
                        f"{lowest_issue_competitor['website']} "
                        f"has "
                        f"{lowest_issue_competitor['total_seo_issues']}."
                    ),
                    "action": (
                        "Review recurring technical and "
                        "on-page issues across important "
                        "SEO pages and address the "
                        "highest-impact patterns first."
                    ),
                }
            )

    # ==================================================
    # FALLBACK
    # ==================================================

    if not priorities:

        priorities.append(
            {
                "issue": "No major comparative signal detected",
                "priority": "Review",
                "evidence": (
                    "The crawled technical signals do not show "
                    "a clear priority difference from the "
                    "available sample."
                ),
                "action": (
                    "Expand the crawl and add search-performance "
                    "data before making broader SEO conclusions."
                ),
            }
        )

    # ==================================================
    # SORT PRIORITIES
    # ==================================================

    priority_order = {
        "High": 1,
        "Medium": 2,
        "Review": 3,
        "Low": 4,
    }

    priorities.sort(
        key=lambda item: priority_order.get(
            item["priority"],
            5,
        )
    )

    return {
        "priorities": priorities[:3],
        "message": (
            "Summary based only on publicly observable "
            "technical/on-page crawl signals."
        ),
    }