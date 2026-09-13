from typing import Dict, Any, List

from strands import tool


@tool
def detect_seo_issues(
    page_data: Dict[str, Any],
) -> List[Dict[str, str]]:
    """
    Analyze crawled page data and identify basic SEO issues.
    """

    issues: List[Dict[str, str]] = []

    title = str(page_data.get("title", "")).strip()
    meta_description = str(
        page_data.get("meta_description", "")
    ).strip()

    h1 = page_data.get("h1", [])
    canonical = str(page_data.get("canonical", "")).strip()

    word_count = int(
        page_data.get("word_count", 0) or 0
    )

    status_code = int(
        page_data.get("status_code", 0) or 0
    )

    possible_javascript_rendering = bool(
        page_data.get(
            "possible_javascript_rendering",
            False,
        )
    )

    # ---------------------------------------------
    # HTTP status
    # ---------------------------------------------

    if status_code != 200:
        issues.append(
            {
                "issue": (
                    f"Page returned HTTP status {status_code}."
                ),
                "priority": "High",
                "action": (
                    "Investigate the HTTP response and ensure "
                    "the page returns the appropriate status code."
                ),
            }
        )

    # ---------------------------------------------
    # Title
    # ---------------------------------------------

    if not title:
        issues.append(
            {
                "issue": "Missing title tag.",
                "priority": "High",
                "action": (
                    "Add a unique and descriptive title tag "
                    "that reflects the primary topic of the page."
                ),
            }
        )

    # ---------------------------------------------
    # Meta description
    # ---------------------------------------------

    if not meta_description:
        issues.append(
            {
                "issue": "Missing meta description.",
                "priority": "Medium",
                "action": (
                    "Add a unique, relevant meta description "
                    "that clearly summarizes the page."
                ),
            }
        )

    # ---------------------------------------------
    # H1
    # ---------------------------------------------

    if len(h1) == 0:

        issues.append(
            {
                "issue": "Missing H1 heading.",
                "priority": "High",
                "action": (
                    "Add one clear H1 heading that describes "
                    "the main topic of the page."
                ),
            }
        )

    elif len(h1) > 1:

        issues.append(
            {
                "issue": (
                    f"Multiple H1 headings found ({len(h1)})."
                ),
                "priority": "Medium",
                "action": (
                    "Review the heading structure and ensure "
                    "the page has a clear primary heading."
                ),
            }
        )

    # ---------------------------------------------
    # Canonical
    # ---------------------------------------------

    if not canonical:

        issues.append(
            {
                "issue": "Missing canonical tag.",
                "priority": "Medium",
                "action": (
                    "Add a canonical URL where appropriate "
                    "to clarify the preferred version of the page."
                ),
            }
        )

    # ---------------------------------------------
    # Content
    # ---------------------------------------------

    if word_count < 300:

        if possible_javascript_rendering:

            issues.append(
                {
                    "issue": (
                        "Low visible HTML content detected; "
                        "the page may rely on JavaScript rendering."
                    ),
                    "priority": "Review",
                    "action": (
                        "Verify the rendered page content with "
                        "a browser-based crawler before concluding "
                        "that the page has thin content."
                    ),
                }
            )

        else:

            issues.append(
                {
                    "issue": "Limited visible page content.",
                    "priority": "Medium",
                    "action": (
                        "Review whether the page provides enough "
                        "useful content to satisfy the intended "
                        "search query."
                    ),
                }
            )

    # ---------------------------------------------
    # ALWAYS RETURN THE LIST
    # ---------------------------------------------

    return issues