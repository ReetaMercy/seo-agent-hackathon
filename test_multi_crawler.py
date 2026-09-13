from tools.website_crawler import crawl_website_pages


url = "https://www.mrmed.in/"

pages = crawl_website_pages(
    start_url=url,
    max_pages=10,
)

print("\nMULTI-PAGE SEO CRAWL")
print("=" * 60)

print(f"Pages crawled: {len(pages)}")

for index, page in enumerate(pages, start=1):
    print(f"\n{index}. {page['url']}")
    print(f"   Status: {page['status_code']}")
    print(f"   Title: {page['title'] or 'Missing'}")
    print(f"   H1 count: {len(page['h1'])}")
    print(f"   Word count: {page['word_count']}")
    print(
        "   JS rendering likely: "
        f"{page['possible_javascript_rendering']}"
    )

print("\n" + "=" * 60)
print("Multi-page crawl complete.")