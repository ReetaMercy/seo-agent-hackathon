from tools.website_audit import audit_website


url = "https://www.mrmed.in/"

result = audit_website(
    url=url,
    max_pages=10,
)

print("\nSEO SITE AUDIT SUMMARY")
print("=" * 70)

print(f"Website: {result['website']}")
print(f"Pages Crawled: {result['pages_crawled']}")
print(f"Pages With Issues: {result['pages_with_issues']}")
print(f"Total Issues: {result['total_issues']}")

print("\nIssue Priority Summary:")
for priority, count in result["priority_counts"].items():
    print(f"- {priority}: {count}")

print("\nTop 3 Site-Wide Issues:")

if result["top_site_issues"]:
    for index, issue in enumerate(
        result["top_site_issues"],
        start=1,
    ):
        print(
            f"{index}. {issue['issue']} "
            f"({issue['page_count']} page(s))"
        )
else:
    print("No issues found.")

print("\nPage-Level Results")
print("-" * 70)

for index, page_result in enumerate(
    result["pages"],
    start=1,
):
    page = page_result["page"]
    issues = page_result["issues"]

    print(f"\n{index}. {page['url']}")
    print(f"   Page Type: {page_result['page_type']}")
    print(f"   Status: {page['status_code']}")
    print(f"   Title: {page['title'] or 'Missing'}")
    print(f"   H1 Count: {len(page['h1'])}")
    print(f"   Word Count: {page['word_count']}")
    print(f"   Issues: {len(issues)}")

    for issue in issues:
        print(
            f"      - {issue['issue']} "
            f"[{issue['priority']}]"
        )

print("\n" + "=" * 70)
print("Site audit complete.")