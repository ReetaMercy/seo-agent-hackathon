from typing import List, Dict, Any
from strands import tool


def identify_likely_issues(
    target_position: float,
    competitor_position: float,
    impressions: int,
    clicks: int,
) -> List[str]:
    """
    Identify up to 3 likely SEO issues based on available
    ranking, impression, click and competitor data.

    These are investigation areas, not confirmed technical issues.
    """

    issues = []

    ctr = 0.0
    if impressions > 0:
        ctr = (clicks / impressions) * 100

    ranking_gap = 0.0
    if competitor_position < target_position:
        ranking_gap = target_position - competitor_position

    # 1. Strong ranking but relatively low CTR
    if target_position <= 10 and impressions >= 500 and ctr < 3:
        issues.append(
            "Low CTR despite a Page 1 ranking — review the title tag, "
            "meta description, and search-result messaging."
        )

    # 2. Large competitor ranking gap
    if ranking_gap >= 5:
        issues.append(
            f"Large competitor gap of {int(ranking_gap)} positions — "
            "compare content relevance, search intent, topical coverage, "
            "internal linking, and authority signals."
        )

    # 3. Outside Page 1
    if 11 <= target_position <= 20:
        issues.append(
            "The page is ranking outside the top 10 — investigate "
            "search-intent alignment, content depth, topical coverage, "
            "and internal linking."
        )

    # 4. Very low ranking
    elif target_position > 20:
        issues.append(
            "The page is far from Page 1 — review overall page relevance, "
            "content quality, internal linking, and authority."
        )

    # 5. Strong impressions but weak traffic
    if impressions >= 1000 and ctr < 2:
        issues.append(
            "High impressions with low CTR — the page is receiving "
            "visibility but may not be compelling enough in search results."
        )

    # 6. Lower impressions
    if impressions < 500:
        issues.append(
            "Limited search visibility — review keyword relevance, "
            "content targeting, and overall topical coverage."
        )

    # 7. General competitive investigation
    if competitor_position < target_position and len(issues) < 3:
        issues.append(
            "Competitor ranks higher — compare the competing page's "
            "content structure, headings, relevance, and internal links."
        )

    # 8. Internal linking fallback
    if len(issues) < 3:
        issues.append(
            "Review internal linking and page relevance for this keyword."
        )

    # 9. Content fallback
    if len(issues) < 3:
        issues.append(
            "Review the page's content quality and alignment with search intent."
        )

    # 10. Final fallback
    if len(issues) < 3:
        issues.append(
            "Compare competitor content structure and topical coverage."
        )

    return issues[:3]


@tool
def analyze_competitive_opportunities(
    keyword_data: List[Dict[str, Any]],
    target_website: str,
    competitors: List[str],
) -> List[Dict[str, Any]]:
    """
    Compare a target website against competitor websites.

    Identifies:
    - Keyword gaps
    - Competitive opportunities
    - Target strengths
    - Top 3 likely SEO issues
    """

    target_website = target_website.lower().strip()
    competitors = [c.lower().strip() for c in competitors]

    keyword_groups: Dict[str, List[Dict[str, Any]]] = {}

    # Group all rows by keyword
    for row in keyword_data:
        keyword = str(row.get("keyword", "")).strip().lower()

        if keyword:
            keyword_groups.setdefault(keyword, []).append(row)

    opportunities = []

    for keyword, rows in keyword_groups.items():

        target_row = None
        competitor_rows = []

        for row in rows:
            website = str(row.get("website", "")).strip().lower()

            if website == target_website:
                target_row = row
            elif website in competitors:
                competitor_rows.append(row)

        # Find best-ranking competitor
        best_competitor = None

        if competitor_rows:
            best_competitor = min(
                competitor_rows,
                key=lambda row: float(row.get("position", 999) or 999),
            )

        # -----------------------------------------
        # KEYWORD GAP
        # -----------------------------------------
        if target_row is None and best_competitor:

            competitor_position = float(
                best_competitor.get("position", 0) or 0
            )

            opportunities.append(
                {
                    "keyword": keyword,
                    "type": "Keyword Gap",
                    "target_position": None,
                    "best_competitor_position": round(
                        competitor_position, 1
                    ),
                    "competitor": best_competitor.get("website"),
                    "priority": "High",
                    "top_3_issues": [
                        "Target website does not currently rank for this keyword.",
                        "Competitor already has search visibility for this keyword.",
                        "Search intent and content coverage should be investigated.",
                    ],
                    "action": (
                        "Create or optimize a relevant page targeting this "
                        "keyword and match the search intent."
                    ),
                }
            )

        # -----------------------------------------
        # COMPETITIVE OPPORTUNITY
        # -----------------------------------------
        elif target_row is not None and best_competitor:

            target_position = float(
                target_row.get("position", 0) or 0
            )

            competitor_position = float(
                best_competitor.get("position", 999) or 999
            )

            impressions = int(
                target_row.get("impressions", 0) or 0
            )

            clicks = int(
                target_row.get("clicks", 0) or 0
            )

            ranking_gap = target_position - competitor_position

            if ranking_gap >= 5:
                priority = "High"
            elif ranking_gap >= 2:
                priority = "Medium"
            else:
                priority = "Low"

            issues = identify_likely_issues(
                target_position,
                competitor_position,
                impressions,
                clicks,
            )

            opportunities.append(
                {
                    "keyword": keyword,
                    "type": "Competitive Opportunity",
                    "target_position": round(target_position, 1),
                    "best_competitor_position": round(
                        competitor_position, 1
                    ),
                    "competitor": best_competitor.get("website"),
                    "ranking_gap": round(ranking_gap, 1),
                    "priority": priority,
                    "top_3_issues": issues,
                    "action": (
                        "Review the competing page's content, search intent, "
                        "internal links, CTR signals, and authority signals."
                    ),
                }
            )

        # -----------------------------------------
        # TARGET STRENGTH
        # -----------------------------------------
        elif target_row is not None and not competitor_rows:

            target_position = float(
                target_row.get("position", 0) or 0
            )

            opportunities.append(
                {
                    "keyword": keyword,
                    "type": "Target Strength",
                    "target_position": round(target_position, 1),
                    "best_competitor_position": None,
                    "competitor": None,
                    "priority": "Low",
                    "top_3_issues": [
                        "No tracked competitor is currently outranking the target.",
                        "Continue monitoring the keyword ranking.",
                        "Strengthen the page with useful content and internal links.",
                    ],
                    "action": (
                        "Maintain the ranking and strengthen the page with "
                        "relevant internal links and useful content."
                    ),
                }
            )

    priority_order = {
        "High": 1,
        "Medium": 2,
        "Low": 3,
    }

    opportunities.sort(
        key=lambda item: (
            priority_order.get(item["priority"], 4),
            item.get("target_position") or 999,
        )
    )

    return opportunities