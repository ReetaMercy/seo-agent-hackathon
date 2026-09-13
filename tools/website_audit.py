from typing import Dict, Any, List
from urllib.parse import urlparse

from strands import tool

from tools.website_crawler import crawl_website_pages
from tools.seo_issue_detector import detect_seo_issues


# ============================================================
# PAGE CLASSIFICATION
# ============================================================

def classify_page_type(url: str) -> str:
    """
    Classify a page based on its URL.
    """

    try:
        parsed = urlparse(url)
        path = parsed.path.lower().strip("/")

        if not path:
            return "Homepage"

        if path.startswith("blog"):
            return "Blog"

        if path.startswith("category"):
            return "Category"

        if path.startswith("product"):
            return "Product"

        if path.startswith("service"):
            return "Service"

        if path.startswith("contact"):
            return "Contact"

        if path.startswith("about"):
            return "About"

        return "Other"

    except Exception:
        return "Other"


# ============================================================
# PAGE PRIORITY
# ============================================================

def calculate_page_priority(page_type: str) -> int:
    """
    Give higher priority to commercially important pages.
    """

    priorities = {
        "Homepage": 10,
        "Service": 9,
        "Product": 9,
        "Category": 7,
        "About": 5,
        "Contact": 5,
        "Blog": 4,
        "Other": 3,
    }

    return priorities.get(
        page_type,
        3,
    )


# ============================================================
# NORMALIZE ISSUE
# ============================================================

def normalize_issue(issue: Any) -> Dict[str, Any]:
    """
    Convert different issue formats into a consistent structure.
    """

    if isinstance(issue, dict):

        return {
            "issue": str(
                issue.get("issue")
                or issue.get("message")
                or issue.get("description")
                or "SEO issue detected"
            ),

            "priority": str(
                issue.get(
                    "priority",
                    "Medium",
                )
            ),

            "action": str(
                issue.get(
                    "action",
                    "",
                )
            ),
        }

    return {
        "issue": str(issue),
        "priority": "Medium",
        "action": "",
    }


# ============================================================
# MAIN WEBSITE AUDIT
# ============================================================

@tool
def audit_website(
    url: str,
    max_pages: int = 10,
) -> Dict[str, Any]:
    """
    Crawl a website and perform an SEO audit.

    Returns page-level findings, site-wide issues,
    issue priorities, and page information.
    """

    # --------------------------------------------------------
    # Crawl website
    # --------------------------------------------------------

    pages = crawl_website_pages(
        start_url=url,
        max_pages=max_pages,
    )


    # --------------------------------------------------------
    # Safety check
    # --------------------------------------------------------

    if not pages:

        return {
            "website": url,
            "pages_crawled": 0,
            "pages_with_issues": 0,
            "total_issues": 0,
            "priority_counts": {
                "High": 0,
                "Medium": 0,
                "Low": 0,
            },
            "top_site_issues": [],
            "pages": [],
        }


    # --------------------------------------------------------
    # Store audit results
    # --------------------------------------------------------

    audit_pages = []

    priority_counts = {
        "High": 0,
        "Medium": 0,
        "Low": 0,
    }


    site_issue_map = {}


    # ========================================================
    # PROCESS EACH PAGE
    # ========================================================

    for page_result in pages:

        # ----------------------------------------------------
        # Support nested crawler structure
        # ----------------------------------------------------

        if (
            isinstance(page_result, dict)
            and isinstance(
                page_result.get("page"),
                dict,
            )
        ):

            page = page_result["page"]

            existing_issues = page_result.get(
                "issues",
                [],
            )

        else:

            page = page_result

            existing_issues = []


        # ----------------------------------------------------
        # Page URL
        # ----------------------------------------------------

        page_url = page.get(
            "url",
            "",
        )


        # ----------------------------------------------------
        # Page type
        # ----------------------------------------------------

        page_type = classify_page_type(
            page_url
        )


        # ----------------------------------------------------
        # Detect SEO issues
        # ----------------------------------------------------

        try:

            detected_issues = detect_seo_issues(
                page
            )

        except Exception:

            detected_issues = []


        # ----------------------------------------------------
        # Combine existing + detected issues
        # ----------------------------------------------------

        all_issues = []


        if existing_issues:

            all_issues.extend(
                existing_issues
            )


        if detected_issues:

            all_issues.extend(
                detected_issues
            )


        # ----------------------------------------------------
        # Normalize issues
        # ----------------------------------------------------

        issue_list = []


        for issue in all_issues:

            normalized = normalize_issue(
                issue
            )

            # Avoid duplicate issues on the same page
            duplicate = False

            for existing in issue_list:

                if (
                    existing["issue"].lower()
                    == normalized["issue"].lower()
                ):

                    duplicate = True
                    break


            if duplicate:
                continue


            issue_list.append(
                normalized
            )


        # ----------------------------------------------------
        # Count priorities
        # ----------------------------------------------------

        for issue in issue_list:

            priority = issue.get(
                "priority",
                "Medium",
            )


            if priority not in priority_counts:

                priority = "Medium"


            priority_counts[
                priority
            ] += 1


            # ------------------------------------------------
            # Site-wide issue aggregation
            # ------------------------------------------------

            issue_name = issue.get(
                "issue",
                "Unknown issue",
            )


            if issue_name not in site_issue_map:

                site_issue_map[
                    issue_name
                ] = {
                    "issue": issue_name,
                    "page_count": 0,
                    "score": 0,
                    "pages": [],
                }


            site_issue_map[
                issue_name
            ]["page_count"] += 1


            site_issue_map[
                issue_name
            ]["pages"].append(
                page_url
            )


            # Priority score
            if priority == "High":

                score = 5

            elif priority == "Medium":

                score = 2

            else:

                score = 1


            site_issue_map[
                issue_name
            ]["score"] += score


        # ----------------------------------------------------
        # Build page result
        # ----------------------------------------------------

        audit_pages.append(
            {
                "page": page,
                "page_type": page_type,
                "page_priority": calculate_page_priority(
                    page_type
                ),
                "issues": issue_list,
            }
        )


    # ========================================================
    # SITE-WIDE ISSUES
    # ========================================================

    top_site_issues = list(
        site_issue_map.values()
    )


    # Sort by score
    top_site_issues.sort(
        key=lambda item: (
            item.get("score", 0),
            item.get("page_count", 0),
        ),
        reverse=True,
    )


    # Keep the most important issues
    top_site_issues = top_site_issues[:10]


    # ========================================================
    # PAGE COUNT
    # ========================================================

    pages_with_issues = sum(
        1
        for page_result in audit_pages
        if page_result.get("issues")
    )


    total_issues = sum(
        len(
            page_result.get(
                "issues",
                [],
            )
        )
        for page_result in audit_pages
    )


    # ========================================================
    # RETURN AUDIT
    # ========================================================

    return {
        "website": url,
        "pages_crawled": len(audit_pages),
        "pages_with_issues": pages_with_issues,
        "total_issues": total_issues,
        "priority_counts": priority_counts,
        "top_site_issues": top_site_issues,
        "pages": audit_pages,
    }


# ============================================================
# AGENT-FRIENDLY AUDIT SUMMARY
# ============================================================

@tool
def get_agent_audit_summary(
    url: str,
    max_pages: int = 1,
) -> Dict[str, Any]:
    """
    Return a compact SEO audit summary suitable for an AI agent.
    """

    audit = audit_website(
        url=url,
        max_pages=max_pages,
    )


    page_summaries = []


    for page_result in audit.get(
        "pages",
        [],
    ):

        # ----------------------------------------------------
        # Extract actual page dictionary
        # ----------------------------------------------------

        if (
            isinstance(page_result, dict)
            and isinstance(
                page_result.get("page"),
                dict,
            )
        ):

            page = page_result["page"]

        else:

            page = page_result


        # ----------------------------------------------------
        # Extract issues
        # ----------------------------------------------------

        issues = page_result.get(
            "issues",
            [],
        )


        issue_list = []


        for issue in issues:

            if isinstance(
                issue,
                dict,
            ):

                issue_list.append(
                    {
                        "issue": issue.get(
                            "issue",
                            "",
                        ),
                        "priority": issue.get(
                            "priority",
                            "Medium",
                        ),
                        "action": issue.get(
                            "action",
                            "",
                        ),
                    }
                )

            else:

                issue_list.append(
                    {
                        "issue": str(issue),
                        "priority": "Medium",
                        "action": "",
                    }
                )


        # ----------------------------------------------------
        # H1
        # ----------------------------------------------------

        h1_values = page.get(
            "h1",
            [],
        )


        # ----------------------------------------------------
        # Page summary
        # ----------------------------------------------------

        page_summaries.append(
            {
                "url": page.get(
                    "url",
                    "Unknown URL",
                ),

                "page_type": page_result.get(
                    "page_type",
                    classify_page_type(
                        page.get(
                            "url",
                            "",
                        )
                    ),
                ),

                "status_code": page.get(
                    "status_code",
                    "Unknown",
                ),

                "title": page.get(
                    "title"
                ) or "Missing",

                "meta_description": page.get(
                    "meta_description"
                ) or "Missing",

                "h1": (
                    h1_values
                    if h1_values
                    else ["Missing"]
                ),

                "canonical": page.get(
                    "canonical"
                ) or "Missing",

                "word_count": page.get(
                    "word_count",
                    0,
                ),

                "issues": issue_list,
            }
        )


    # ========================================================
    # RETURN COMPACT SUMMARY
    # ========================================================

    return {
        "website": audit.get(
            "website",
            url,
        ),

        "pages_crawled": audit.get(
            "pages_crawled",
            0,
        ),

        "pages_with_issues": audit.get(
            "pages_with_issues",
            0,
        ),

        "total_issues": audit.get(
            "total_issues",
            0,
        ),

        "priority_counts": audit.get(
            "priority_counts",
            {
                "High": 0,
                "Medium": 0,
                "Low": 0,
            },
        ),

        "top_site_issues": audit.get(
            "top_site_issues",
            [],
        ),

        "pages": page_summaries,
    }