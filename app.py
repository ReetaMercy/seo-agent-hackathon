import streamlit as st
from strands import Agent
from strands.models.ollama import OllamaModel

from tools.website_audit import audit_website
from tools.competitor_comparison import (
    compare_websites,
    generate_executive_summary,
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SEO Competitive Opportunity Agent",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# PREMIUM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ==============================
       GLOBAL
    ============================== */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 0%,
                rgba(37, 99, 235, 0.12),
                transparent 28%
            ),
            radial-gradient(
                circle at 90% 0%,
                rgba(124, 58, 237, 0.10),
                transparent 25%
            ),
            #080d18;
        color: #f8fafc;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 4rem;
        padding-left: 2.5rem;
        padding-right: 2.5rem;
    }


    /* ==============================
       TYPOGRAPHY
    ============================== */

    h1 {
        font-size: 2.7rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.045em !important;
    }

    h2 {
        font-size: 1.7rem !important;
        font-weight: 750 !important;
        letter-spacing: -0.025em !important;
        margin-top: 1rem !important;
    }

    h3 {
        font-size: 1.2rem !important;
        font-weight: 700 !important;
    }

    p {
        color: #cbd5e1;
    }


    /* ==============================
       HERO
    ============================== */

    .hero-box {
        padding: 2.3rem 2.5rem;
        margin-bottom: 2rem;

        border-radius: 22px;

        background:
            linear-gradient(
                135deg,
                rgba(30, 41, 59, 0.94),
                rgba(15, 23, 42, 0.92)
            );

        border: 1px solid rgba(148, 163, 184, 0.16);

        box-shadow:
            0 20px 60px rgba(0, 0, 0, 0.30),
            inset 0 1px 0 rgba(255, 255, 255, 0.035);
    }

    .hero-badge {
        display: inline-block;

        padding: 0.4rem 0.8rem;

        border-radius: 999px;

        background: rgba(59, 130, 246, 0.13);

        border: 1px solid rgba(96, 165, 250, 0.25);

        color: #93c5fd;

        font-size: 0.78rem;

        font-weight: 750;

        letter-spacing: 0.06em;

        text-transform: uppercase;

        margin-bottom: 1rem;
    }

    .hero-title {
        font-size: 2.8rem;

        font-weight: 850;

        line-height: 1.05;

        letter-spacing: -0.05em;

        color: #f8fafc;
    }

    .hero-subtitle {
        margin-top: 0.9rem;

        max-width: 900px;

        font-size: 1rem;

        line-height: 1.7;

        color: #94a3b8;
    }


    /* ==============================
       INPUTS
    ============================== */

    div[data-baseweb="input"] > div {
        background: rgba(15, 23, 42, 0.80) !important;

        border: 1px solid rgba(148, 163, 184, 0.18) !important;

        border-radius: 12px !important;

        min-height: 46px;
    }

    div[data-baseweb="input"] > div:focus-within {
        border-color: rgba(96, 165, 250, 0.75) !important;

        box-shadow:
            0 0 0 3px rgba(59, 130, 246, 0.12);
    }

    input {
        color: #f8fafc !important;
    }


    /* ==============================
       BUTTON
    ============================== */

    .stButton > button {
        width: 100%;

        min-height: 50px;

        border: none !important;

        border-radius: 12px !important;

        background:
            linear-gradient(
                135deg,
                #2563eb,
                #7c3aed
            ) !important;

        color: white !important;

        font-weight: 750 !important;

        box-shadow:
            0 10px 28px rgba(37, 99, 235, 0.28);

        transition:
            transform 0.16s ease,
            box-shadow 0.16s ease,
            filter 0.16s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);

        filter: brightness(1.06);

        box-shadow:
            0 15px 35px rgba(37, 99, 235, 0.38);
    }


    /* ==============================
       METRICS
    ============================== */

    div[data-testid="stMetric"] {
        background:
            linear-gradient(
                180deg,
                rgba(30, 41, 59, 0.88),
                rgba(15, 23, 42, 0.88)
            );

        border: 1px solid rgba(148, 163, 184, 0.14);

        border-radius: 16px;

        padding: 1.2rem;

        box-shadow:
            0 12px 30px rgba(0, 0, 0, 0.18);
    }

    div[data-testid="stMetricLabel"] {
        color: #94a3b8 !important;

        font-weight: 650;
    }

    div[data-testid="stMetricValue"] {
        color: #f8fafc !important;

        font-weight: 800;

        letter-spacing: -0.035em;
    }


    /* ==============================
       EXPANDERS
    ============================== */

    div[data-testid="stExpander"] {
        background: rgba(15, 23, 42, 0.68);

        border: 1px solid rgba(148, 163, 184, 0.14);

        border-radius: 14px;

        margin-bottom: 0.6rem;

        overflow: hidden;
    }

    div[data-testid="stExpander"] summary {
        font-weight: 650;

        color: #e2e8f0;
    }

    div[data-testid="stExpander"] summary:hover {
        background: rgba(51, 65, 85, 0.25);
    }


    /* ==============================
       ALERTS
    ============================== */

    div[data-testid="stAlert"] {
        border-radius: 12px !important;
    }


    /* ==============================
       TABLE
    ============================== */

    div[data-testid="stDataFrame"] {
        border-radius: 14px;

        overflow: hidden;

        border: 1px solid rgba(148, 163, 184, 0.14);
    }


    /* ==============================
       DIVIDERS
    ============================== */

    hr {
        border: none !important;

        height: 1px !important;

        background:
            linear-gradient(
                90deg,
                transparent,
                rgba(148, 163, 184, 0.22),
                transparent
            ) !important;

        margin: 2.2rem 0 !important;
    }


    /* ==============================
       SCROLLBAR
    ============================== */

    ::-webkit-scrollbar {
        width: 9px;
        height: 9px;
    }

    ::-webkit-scrollbar-track {
        background: #080d18;
    }

    ::-webkit-scrollbar-thumb {
        background: #334155;
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #475569;
    }


    /* ==============================
       MOBILE
    ============================== */

    @media (max-width: 900px) {

        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .hero-box {
            padding: 1.5rem;
        }

        .hero-title {
            font-size: 2rem;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero-box">

        <div class="hero-badge">
            SEO Intelligence Agent
        </div>

        <div class="hero-title">
            🔎 SEO Competitive Opportunity Agent
        </div>

        <div class="hero-subtitle">
            Crawl websites, detect technical SEO issues,
            prioritize opportunities, compare competitors,
            and transform verified crawl evidence into
            actionable SEO recommendations.
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# INPUT SECTION
# ============================================================

st.subheader("🌐 Website Analysis")

target_website = st.text_input(
    "Target Website",
    value="https://www.example.com",
)

st.subheader("🏆 Competitor Analysis")

col1, col2 = st.columns(2)

with col1:
    competitor_1 = st.text_input(
        "Competitor 1",
        value="https://competitor1.com",
    )

with col2:
    competitor_2 = st.text_input(
        "Competitor 2",
        value="https://competitor2.com",
    )


analyze_button = st.button(
    "🚀 Analyze Website",
    use_container_width=True,
)


# ============================================================
# ANALYSIS
# ============================================================

if analyze_button:

    target_website = target_website.strip()

    competitors = []

    if competitor_1.strip():
        competitors.append(competitor_1.strip())

    if competitor_2.strip():
        competitors.append(competitor_2.strip())


    if not target_website:

        st.error("Please enter a target website.")

        st.stop()


    # ========================================================
    # WEBSITE SEO AUDIT
    # ========================================================

    st.divider()

    st.header("📊 SEO Audit Overview")

    with st.spinner(
        "🔎 Crawling and analyzing the target website..."
    ):

        try:

            target_audit = audit_website(
                url=target_website,
                max_pages=10,
            )

        except Exception as error:

            st.error(
                "Website audit failed: " + str(error)
            )

            st.stop()


    # --------------------------------------------------------
    # AUDIT DATA
    # --------------------------------------------------------

    pages_crawled = target_audit.get(
        "pages_crawled",
        0,
    )

    pages_with_issues = target_audit.get(
        "pages_with_issues",
        0,
    )

    total_issues = target_audit.get(
        "total_issues",
        0,
    )

    priority_counts = target_audit.get(
        "priority_counts",
        {},
    )

    high_priority = priority_counts.get(
        "High",
        0,
    )

    medium_priority = priority_counts.get(
        "Medium",
        0,
    )

    low_priority = priority_counts.get(
        "Low",
        0,
    )


    # ========================================================
    # METRICS
    # ========================================================

    metric1, metric2, metric3, metric4 = st.columns(4)

    with metric1:
        st.metric(
            "Pages Crawled",
            pages_crawled,
        )

    with metric2:
        st.metric(
            "Pages With Issues",
            pages_with_issues,
        )

    with metric3:
        st.metric(
            "Total SEO Issues",
            total_issues,
        )

    with metric4:
        st.metric(
            "High Priority",
            high_priority,
        )


    # ========================================================
    # ISSUE PRIORITY
    # ========================================================

    st.subheader("🎯 Issue Priority")

    p1, p2, p3 = st.columns(3)

    with p1:
        st.metric(
            "🔴 High",
            high_priority,
        )

    with p2:
        st.metric(
            "🟠 Medium",
            medium_priority,
        )

    with p3:
        st.metric(
            "🟢 Low",
            low_priority,
        )


    # ========================================================
    # TOP SITE-WIDE ISSUES
    # ========================================================

    st.subheader("⚠️ Top Site-Wide Issues")

    top_site_issues = target_audit.get(
        "top_site_issues",
        [],
    )


    if not top_site_issues:

        st.info(
            "No site-wide SEO issues were detected."
        )

    else:

        for issue in top_site_issues:

            if not isinstance(issue, dict):
                continue


            issue_name = issue.get(
                "issue",
                "SEO Issue",
            )

            page_count = issue.get(
                "page_count",
                0,
            )

            score = issue.get(
                "score",
                0,
            )

            affected_pages = issue.get(
                "pages",
                [],
            )


            with st.expander(
                f"⚠️ {issue_name}"
            ):

                c1, c2 = st.columns(2)

                with c1:
                    st.write(
                        f"**Pages affected:** {page_count}"
                    )

                with c2:
                    st.write(
                        f"**Opportunity score:** {score}"
                    )


                if affected_pages:

                    st.write(
                        "**Affected pages:**"
                    )

                    for page_url in affected_pages:

                        st.markdown(
                            f"- [{page_url}]({page_url})"
                        )


    # ========================================================
    # PAGE LEVEL AUDIT
    # ========================================================

    st.divider()

    st.header("📄 Page-Level Audit")

    pages = target_audit.get(
        "pages",
        [],
    )


    if not pages:

        st.info(
            "No page-level data available."
        )

    else:

        for index, page_result in enumerate(
            pages,
            start=1,
        ):

            if not isinstance(
                page_result,
                dict,
            ):
                continue


            page = page_result.get(
                "page",
                {},
            )

            if not isinstance(
                page,
                dict,
            ):
                page = {}


            page_url = page.get(
                "url",
                page_result.get(
                    "url",
                    "Unknown URL",
                ),
            )

            title = page.get(
                "title",
                "Missing",
            )

            meta_description = page.get(
                "meta_description",
                "Missing",
            )

            h1 = page.get(
                "h1",
                [],
            )

            canonical = page.get(
                "canonical",
                "Missing",
            )

            word_count = page.get(
                "word_count",
                0,
            )

            status_code = page.get(
                "status_code",
                "Unknown",
            )

            issues = page_result.get(
                "issues",
                [],
            )


            with st.expander(
                f"{index}. {page_url}"
            ):

                st.write(
                    f"**URL:** {page_url}"
                )

                st.write(
                    f"**Status:** {status_code}"
                )

                st.write(
                    f"**Title:** {title}"
                )

                st.write(
                    f"**Meta Description:** "
                    f"{meta_description}"
                )

                st.write(
                    f"**H1:** {h1}"
                )

                st.write(
                    f"**Canonical:** {canonical}"
                )

                st.write(
                    f"**Word Count:** {word_count}"
                )


                if issues:

                    st.write(
                        "**Detected Issues:**"
                    )

                    for issue in issues:

                        if isinstance(
                            issue,
                            dict,
                        ):

                            issue_name = issue.get(
                                "issue",
                                "SEO Issue",
                            )

                            priority = issue.get(
                                "priority",
                                "Unknown",
                            )

                            action = issue.get(
                                "action",
                                "",
                            )

                            st.markdown(
                                f"- **{priority}** — "
                                f"{issue_name}"
                            )

                            if action:

                                st.caption(
                                    f"Action: {action}"
                                )

                        else:

                            st.write(
                                f"- {issue}"
                            )

                else:

                    st.success(
                        "No detected SEO issues on this page."
                    )


    # ========================================================
    # RULE-BASED SEO RECOMMENDATIONS
    # ========================================================

    st.divider()

    st.header(
        "🎯 SEO Recommendations & Action Plan"
    )

    st.caption(
        "Recommendations are generated from verified crawl evidence."
    )


    recommendation_items = []


    for issue in top_site_issues:

        if not isinstance(
            issue,
            dict,
        ):
            continue


        issue_name = issue.get(
            "issue",
            "SEO Issue",
        )

        page_count = issue.get(
            "page_count",
            0,
        )

        score = issue.get(
            "score",
            0,
        )


        issue_lower = issue_name.lower()


        if "missing h1" in issue_lower:

            action = (
                "Add one clear, descriptive H1 heading "
                "to each affected page."
            )

        elif "multiple h1" in issue_lower:

            action = (
                "Review the heading structure and "
                "keep one primary H1 per page."
            )

        elif "canonical" in issue_lower:

            action = (
                "Add an appropriate canonical URL "
                "to the affected indexable pages."
            )

        elif "limited visible" in issue_lower:

            action = (
                "Review the affected page content and "
                "ensure important SEO content is available "
                "in rendered HTML."
            )

        elif "javascript" in issue_lower:

            action = (
                "Review JavaScript rendering and verify "
                "important SEO content is accessible "
                "to search engines."
            )

        else:

            action = (
                "Review the affected pages and prioritize "
                "the issue according to its impact."
            )


        recommendation_items.append(
            {
                "issue": issue_name,
                "page_count": page_count,
                "score": score,
                "action": action,
            }
        )


    if recommendation_items:

        for index, item in enumerate(
            recommendation_items,
            start=1,
        ):

            with st.expander(
                f"{index}. {item['issue']}"
            ):

                st.write(
                    f"**Pages affected:** "
                    f"{item['page_count']}"
                )

                st.write(
                    f"**Opportunity score:** "
                    f"{item['score']}"
                )

                st.info(
                    "Recommended action: "
                    + item["action"]
                )

    else:

        st.success(
            "No actionable SEO issues were detected."
        )


    # ========================================================
    # AI SEO OPPORTUNITY ANALYSIS
    # ========================================================

    st.divider()

    st.header(
        "🤖 AI SEO Opportunity Analysis"
    )

    st.caption(
        "AI recommendations are constrained to verified crawl evidence."
    )


    # --------------------------------------------------------
    # Compact evidence for Ollama
    # --------------------------------------------------------

    compact_issues = []

    for item in recommendation_items:

        compact_issues.append(
            {
                "issue": item["issue"],
                "pages_affected": item["page_count"],
                "opportunity_score": item["score"],
                "recommended_action": item["action"],
            }
        )


    ai_prompt = f"""
You are an expert technical SEO analyst.

Analyze ONLY the verified crawl evidence below.

TARGET WEBSITE:
{target_website}

PAGES CRAWLED:
{pages_crawled}

PAGES WITH ISSUES:
{pages_with_issues}

TOTAL SEO ISSUES:
{total_issues}

PRIORITY:
High: {high_priority}
Medium: {medium_priority}
Low: {low_priority}

VERIFIED SEO OPPORTUNITIES:
{compact_issues}

Provide exactly:

EXECUTIVE SUMMARY

Write 2 concise sentences.

TOP AI-DRIVEN OPPORTUNITIES

Provide the top 3 opportunities.

For each opportunity include:

- Evidence
- AI Opportunity
- Recommended Action

RULES:

- Use ONLY the evidence provided.
- Do not invent rankings.
- Do not invent traffic.
- Do not invent impressions.
- Do not invent clicks.
- Do not invent CTR.
- Do not invent backlinks.
- Do not invent keyword data.
- Do not claim Google ranking improvements.
- Keep the answer concise and practical.
"""


    try:

        with st.spinner(
            "🤖 AI is analyzing the SEO opportunities..."
        ):

            # Create a fresh Ollama model
            ollama_model = OllamaModel(
                host="http://localhost:11434",
                model_id="llama3.1",
                temperature=0.2,
                max_tokens=900,
            )


            # Create a fresh Agent
            # This avoids the previous
            # "Concurrent invocations are not supported"
            # problem.

            ai_agent = Agent(
                model=ollama_model,
                tools=[],
            )


            ai_response = ai_agent(
                ai_prompt
            )


        st.success(
            "AI opportunity analysis completed successfully."
        )

        st.markdown(
            str(ai_response)
        )


    except Exception as error:

        st.error(
            "AI analysis could not be completed."
        )

        st.code(
            str(error)
        )


    # ========================================================
    # COMPETITIVE OPPORTUNITY ANALYSIS
    # ========================================================

    st.divider()

    st.header(
        "🏆 Competitive Opportunity Analysis"
    )


    if not competitors:

        st.info(
            "Add competitor URLs above to enable competitive analysis."
        )

    else:

        try:

            with st.spinner(
                "🔎 Comparing target website with competitors..."
            ):

                comparison_result = compare_websites(
                    target_website,
                    competitors,
                )


            st.success(
                "Competitive comparison completed successfully."
            )


            # ------------------------------------------------
            # COMPETITIVE SUMMARY
            # ------------------------------------------------

            st.subheader(
                "📋 Competitive Summary"
            )


            try:

                summary = generate_executive_summary(
                    comparison_result
                )

                if summary:

                    st.write(
                        summary
                    )

            except Exception:

                st.info(
                    "Competitive comparison completed. "
                    "Summary is available from the comparison data."
                )


            # ------------------------------------------------
            # COMPARISON DATA
            # ------------------------------------------------

            if isinstance(
                comparison_result,
                dict,
            ):

                comparison_rows = (
                    comparison_result.get(
                        "comparison",
                        [],
                    )
                )

            else:

                comparison_rows = []


            # ------------------------------------------------
            # COMPETITOR TABLE
            # ------------------------------------------------

            if comparison_rows:

                st.subheader(
                    "📊 Competitor Comparison"
                )

                table_rows = []


                for row in comparison_rows:

                    if not isinstance(
                        row,
                        dict,
                    ):
                        continue


                    website = row.get(
                        "website",
                        "Unknown",
                    )

                    website_type = row.get(
                        "type",
                        "Unknown",
                    )

                    crawled = row.get(
                        "pages_crawled",
                        0,
                    )

                    avg_words = row.get(
                        "average_word_count",
                        row.get(
                            "avg_word_count",
                            0,
                        ),
                    )

                    h1_issues = row.get(
                        "h1_issue_pages",
                        0,
                    )

                    seo_issues = row.get(
                        "total_seo_issues",
                        0,
                    )


                    table_rows.append(
                        {
                            "Website": website,
                            "Type": website_type,
                            "Pages Crawled": crawled,
                            "Avg. Word Count": avg_words,
                            "H1 Issue Pages": h1_issues,
                            "Total SEO Issues": seo_issues,
                        }
                    )


                if table_rows:

                    st.dataframe(
                        table_rows,
                        use_container_width=True,
                        hide_index=True,
                    )


            # ------------------------------------------------
            # TECHNICAL OPPORTUNITY SCORE
            # ------------------------------------------------

            st.subheader(
                "🎯 Technical Opportunity Score"
            )

            st.caption(
                "Higher scores indicate larger detected technical SEO "
                "opportunities based on audit findings. "
                "This is not a Google ranking or traffic metric."
            )


            score_rows = []


            for row in comparison_rows:

                if not isinstance(
                    row,
                    dict,
                ):
                    continue


                website = row.get(
                    "website",
                    "Unknown",
                )

                seo_issues = row.get(
                    "total_seo_issues",
                    0,
                )

                h1_pages = row.get(
                    "h1_issue_pages",
                    0,
                )

                avg_words = row.get(
                    "average_word_count",
                    row.get(
                        "avg_word_count",
                        0,
                    ),
                )


                score = (
                    int(seo_issues) * 5
                    + int(h1_pages) * 3
                )


                score_rows.append(
                    {
                        "Website": website,
                        "Technical Opportunity Score": score,
                        "SEO Issues": seo_issues,
                        "H1 Issue Pages": h1_pages,
                        "Avg. Word Count": avg_words,
                    }
                )


            if score_rows:

                st.dataframe(
                    score_rows,
                    use_container_width=True,
                    hide_index=True,
                )


            # ------------------------------------------------
            # COMPETITIVE OPPORTUNITIES
            # ------------------------------------------------

            st.subheader(
                "🚀 Competitive Opportunities"
            )


            opportunity_list = [
                (
                    "🔴 HIGH",
                    "Technical SEO remediation",
                    "Prioritize high-impact technical SEO issues "
                    "identified on the target website."
                ),
                (
                    "🟠 MEDIUM",
                    "Heading structure improvement",
                    "Improve H1 consistency where the target has "
                    "missing or multiple H1 headings."
                ),
                (
                    "🟡 MEDIUM",
                    "Competitive SEO gap analysis",
                    "Use differences in detected technical issues "
                    "and content volume to prioritize optimization."
                ),
                (
                    "🟢 LOW",
                    "Continuous SEO monitoring",
                    "Repeat the crawl periodically to measure whether "
                    "detected issues are being resolved."
                ),
            ]


            for index, (
                priority,
                title,
                description,
            ) in enumerate(
                opportunity_list,
                start=1,
            ):

                with st.expander(
                    f"{index}. {priority} — {title}"
                ):

                    st.write(
                        description
                    )


            # ------------------------------------------------
            # RAW DATA
            # ------------------------------------------------

            with st.expander(
                "🔍 View Raw Comparison Data"
            ):

                st.json(
                    comparison_result
                )


        except Exception as error:

            st.error(
                "Competitive analysis could not be completed."
            )

            st.code(
                str(error)
            )


    # ========================================================
    # FINAL STATUS
    # ========================================================

    st.divider()

    st.success(
        "✅ SEO analysis completed successfully."
    )