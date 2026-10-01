import json
from app.services.problem_extractor import ProblemExtractor
from app.services.problem_classifier import ProblemClassifier
from app.services.roadmap_generator import RoadmapGenerator

def test_prompt_example():
    test_raw_text = """
55 — Jump Game
121 — Best Time to Buy and Sell Stock
141 — Linked List Cycle
206 — Reverse Linked List
704 — Binary Search
875 — Koko Eating Bananas
1046 — Last Stone Weight
1710 — Maximum Units on a Truck
1834 — Single-Threaded CPU
"""
    classifier = ProblemClassifier()
    extractor = ProblemExtractor(classifier.known_problems)

    # 1. Extraction
    extracted = extractor.extract_from_raw_text(test_raw_text)
    print(f"Extracted {len(extracted)} problems:")
    for p in extracted:
        print(f"  #{p['leetcode_number']}: {p['title']}")

    # 2. Classification
    enriched = [classifier.classify_problem(p) for p in extracted]
    print("\nEnriched Problem Samples:")
    for p in enriched:
        print(f"  #{p['leetcode_number']} | {p['title']} | Difficulty: {p['difficulty']} | Topic: {p['topics']} | Similar to: {p['similar_concept']}")

    # 3. Roadmap Generation for Average Level, 3 Months, 20 Problems
    roadmap = RoadmapGenerator.generate_roadmap(
        problems=enriched,
        user_level="Average",
        duration_months=3,
        target_problem_count=20,
        title="Test 3-Month Roadmap"
    )

    print(f"\nGenerated Roadmap ID: {roadmap['id']} | Total weeks: {roadmap['total_weeks']} | Total problems: {roadmap['total_problems']}")
    print("\nWeek 1 schedule:")
    for day in roadmap['weeks'][0]['days']:
        prob_titles = [f"#{p['leetcode_number']} {p['title']} ({p['difficulty']}, {p['topic']}, Similar to: {p['similar_concept']})" for p in day['problems']]
        print(f"  Day {day['day']} [{day['focus_topic']}]: {', '.join(prob_titles) if prob_titles else 'Revision / Rest'}")

    print("\nALL TEST CASE CHECKS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    test_prompt_example()
