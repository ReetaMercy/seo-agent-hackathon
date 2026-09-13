from tools.competitor_comparison import (
    compare_websites,
    generate_executive_summary,
)


target = "https://www.mrmed.in/"

competitors = [
    "https://www.1mg.com/",
    "https://www.netmeds.com/",
]

result = compare_websites(
    target_website=target,
    competitors=competitors,
    max_pages=5,
)

summary = generate_executive_summary(
    result["comparison"]
)

print("\nCOMPETITOR SEO COMPARISON")
print("=" * 70)

for website in result["comparison"]:

    print(f"\nWebsite: {website['website']}")
    print(f"Type: {website['type']}")
    print(f"Pages Crawled: {website['pages_crawled']}")
    print(
        f"Average Word Count: "
        f"{website['average_word_count']}"
    )
    print(
        f"H1 Issue Pages: "
        f"{website['h1_issue_pages']}"
    )
    print(
        f"Total SEO Issues: "
        f"{website['total_seo_issues']}"
    )

    if website.get("error"):
        print(f"Error: {website['error']}")

print("\n" + "=" * 70)
print("Competitor comparison complete.")

print("\nEXECUTIVE SEO SUMMARY")
print("=" * 70)

print(summary["message"])

for index, priority in enumerate(
    summary["priorities"],
    start=1,
):
    print(f"\n{index}. {priority['issue']}")
    print(f"   Priority: {priority['priority']}")
    print(f"   Evidence: {priority['evidence']}")
    print(f"   Recommended Action: {priority['action']}")

print("\n" + "=" * 70)
print("Executive summary complete.")