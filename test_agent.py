from seo_agent import seo_agent

prompt = """
You are an SEO Competitive Opportunity Agent.

Analyze ONLY the evidence provided below.

TARGET WEBSITE
mrmed.in

AUDIT EVIDENCE
Pages crawled: 10
Pages with issues: 6
Total SEO issues: 10

Priority:
High: 3
Medium: 7
Low: 0

Detected site-wide issues:
1. Missing H1 heading — 3 pages affected
2. Multiple H1 headings found (4) — 3 pages affected
3. Missing canonical tag — 2 pages affected
4. Limited visible page content — 1 page affected
5. Low visible HTML content detected; page may rely on JavaScript rendering — 1 page affected

IMPORTANT:
Do NOT claim that the homepage is missing a title, meta description, H1, or canonical tag unless the evidence explicitly says so.
Do NOT invent rankings, traffic, clicks, impressions, CTR, backlinks, or keywords.

Return exactly:

EXECUTIVE SUMMARY
- 2 concise bullets

TOP OPPORTUNITIES
1. Opportunity
   Evidence:
   Action:
2. Opportunity
   Evidence:
   Action:
3. Opportunity
   Evidence:
   Action:

Keep the answer concise and practical.
"""

response = seo_agent(prompt)

print("\n" + "=" * 60)
print("AI SEO OPPORTUNITY ANALYSIS")
print("=" * 60)
print(response)