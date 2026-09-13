from tools.website_crawler import crawl_website


url = "https://example.com"

result = crawl_website(url)

print("\nSEO CRAWL RESULT")
print("=" * 60)

print(f"URL: {result['url']}")
print(f"Status Code: {result['status_code']}")
print(f"Title: {result['title']}")
print(f"Meta Description: {result['meta_description']}")
print(f"H1: {result['h1']}")
print(f"Canonical: {result['canonical']}")
print(f"Word Count: {result['word_count']}")

print("\nInternal Links:")
for link in result["internal_links"]:
    print(f"- {link}")

print("=" * 60)