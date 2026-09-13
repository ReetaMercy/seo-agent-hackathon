import csv
import json

from tools.keyword_analyzer import analyze_competitive_opportunities


with open("data/competitor_keywords.csv", encoding="utf-8") as file:
    keyword_data = list(csv.DictReader(file))


with open("data/project_config.json", encoding="utf-8") as file:
    config = json.load(file)


results = analyze_competitive_opportunities(
    keyword_data=keyword_data,
    target_website=config["target_website"],
    competitors=config["competitors"],
)


for index, result in enumerate(results, start=1):
    print("=" * 70)
    print(f"{index}. {result['keyword'].title()}")
    print(f"Type: {result['type']}")

    if result["target_position"] is not None:
        print(f"Your Position: #{int(result['target_position'])}")
    else:
        print("Your Position: Not Ranking")

    if result["best_competitor_position"] is not None:
        print(
            f"Best Competitor Position: "
            f"#{int(result['best_competitor_position'])}"
        )

    if result.get("competitor"):
        print(f"Competitor: {result['competitor']}")

    print(f"Priority: {result['priority']}")

    print("\nTop 3 Issues:")
    for issue_number, issue in enumerate(
        result["top_3_issues"], start=1
    ):
        print(f"{issue_number}. {issue}")

    print(f"\nAction: {result['action']}")
    print()


print("=" * 70)
print("Competitive SEO analysis complete.")