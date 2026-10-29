"""Lightweight evaluation suite for Rafeeq."""
import json
from main import Rafeeq

TASKS = [
    {"input": "I need a permit", "lang": "en", "expected": "permit"},
    {"input": "أحتاج تصريحًا", "lang": "ar", "expected": "تصريح"},
    {"input": "ما هي متطلبات التصريح؟", "lang": "ar", "expected": "تصريح"},
    {"input": "Check my status", "lang": "en", "expected": "application ID"},
    {"input": "متابعة الطلب", "lang": "ar", "expected": "رقم الطلب"},
    {"input": "Hello", "lang": "en", "expected": "Welcome"},
    {"input": "مرحبا", "lang": "ar", "expected": "مرحبًا"},
    {"input": "Tell me about construction permits", "lang": "en", "expected": "permit"},
    {"input": "أريد رخصة بناء", "lang": "ar", "expected": "تصريح"},
    {"input": "Where is my application status?", "lang": "en", "expected": "application ID"},
    {"input": "ما حالة طلبي؟", "lang": "ar", "expected": "رقم الطلب"},
    {"input": "Help me with a municipal permit", "lang": "en", "expected": "permit"},
    {"input": "أحتاج رخصة", "lang": "ar", "expected": "تصريح"},
    {"input": "Good morning", "lang": "en", "expected": "Welcome"},
    {"input": "السلام عليكم", "lang": "ar", "expected": "مرحبًا"},
]


def run_evaluation():
    agent = Rafeeq()
    results = []

    for index, task in enumerate(TASKS, start=1):
        response = agent.respond(task["input"], language=task["lang"])
        reply = response["reply"]
        passed = task["expected"].casefold() in reply.casefold()
        results.append({
            "task_id": index,
            "input": task["input"],
            "expected": task["expected"],
            "actual": reply,
            "passed": passed,
        })

    passed_count = sum(item["passed"] for item in results)
    report = {
        "configuration": "A - baseline",
        "total": len(results),
        "passed": passed_count,
        "failed": len(results) - passed_count,
        "pass_rate_percent": round(100 * passed_count / len(results), 2),
        "results": results,
    }

    with open("eval_results.json", "w", encoding="utf-8") as file:
        json.dump(report, file, ensure_ascii=False, indent=2)

    print(f"Evaluation: {passed_count}/{len(results)} passed")
    print(f"Pass rate: {report['pass_rate_percent']}%")
    print("Detailed report saved to eval_results.json")
    for item in results:
        if not item["passed"]:
            print(f"FAIL task {item['task_id']}: {item['input']}")


if __name__ == "__main__":
    run_evaluation()
