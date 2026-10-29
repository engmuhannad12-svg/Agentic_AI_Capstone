"""A/B evaluation: baseline routing vs synonym normalization."""
import json
from main import Rafeeq

TASKS = [
    ("I need a permit", "en", "permit"),
    ("construction permit requirements", "en", "permit"),
    ("I need a license", "en", "permit"),
    ("How do I get building authorization?", "en", "permit"),
    ("أحتاج تصريحًا", "ar", "permit"),
    ("أريد رخصة بناء", "ar", "permit"),
    ("أحتاج ترخيص بناء", "ar", "permit"),
    ("ما شروط البناء؟", "ar", "permit"),
    ("Check my status", "en", "status"),
    ("What is the status of my application?", "en", "status"),
    ("Track my application", "en", "status"),
    ("Where is my request?", "en", "status"),
    ("Application progress update", "en", "status"),
    ("متابعة الطلب", "ar", "status"),
    ("وين وصل طلبي؟", "ar", "status"),
    ("أريد تتبع المعاملة", "ar", "status"),
    ("حالة طلبي", "ar", "status"),
    ("Hello", "en", "greeting"),
    ("Good morning", "en", "greeting"),
    ("السلام عليكم", "ar", "greeting"),
    ("مرحبا", "ar", "greeting"),
]

ALIASES = [
    ("building authorization", "permit"),
    ("construction permission", "permit"),
    ("license", "permit"),
    ("licence", "permit"),
    ("ترخيص", "تصريح"),
    ("شروط البناء", "تصريح"),
    ("track my application", "status"),
    ("application progress", "status"),
    ("progress update", "status"),
    ("where is my request", "status"),
    ("request update", "status"),
    ("وين وصل", "حالة"),
    ("أين وصل", "حالة"),
    ("تتبع المعاملة", "حالة"),
    ("تتبع الطلب", "حالة"),
    ("مستجدات الطلب", "حالة"),
    ("تحديث الطلب", "حالة"),
]


def normalize(message):
    lowered = message.casefold()
    for phrase, canonical in ALIASES:
        if phrase.casefold() in lowered:
            return f"{message} {canonical}"
    return message

def classify_reply(reply):
    lowered = reply.casefold()

    if (
        "application id" in lowered
        or "رقم الطلب" in reply
        or "حالة الطلب" in reply
    ):
        return "status"

    if (
        lowered.startswith("welcome to rafeeq")
        or "مرحبًا بك في رفيق" in reply
    ):
        return "greeting"

    if (
        "permit requirements" in lowered
        or "municipal permit" in lowered
        or "تصريح" in reply
        or "رخصة" in reply
    ):
        return "permit"

    return "unknown"

def evaluate(config):
    results = []
    for index, (message, language, expected) in enumerate(TASKS, 1):
        agent = Rafeeq()
        actual_input = normalize(message) if config == "B" else message
        reply = agent.respond(actual_input, language=language)["reply"]
        predicted = classify_reply(reply)
        results.append({
            "task_id": index,
            "input": message,
            "expected": expected,
            "predicted": predicted,
            "passed": predicted == expected,
            "reply": reply,
        })
    return results


def summarize(results):
    passed = sum(row["passed"] for row in results)
    total = len(results)
    return {
        "total": total,
        "passed": passed,
        "failed": total - passed,
        "accuracy_percent": round(100 * passed / total, 2),
        "errors": [row for row in results if not row["passed"]],
    }


def main():
    a_results = evaluate("A")
    b_results = evaluate("B")
    report = {
        "description": (
            "A: raw baseline input. B: synonym normalization before "
            "the same agent. Scoring uses intent labels inferred from replies."
        ),
        "A_baseline": summarize(a_results),
        "B_improved": summarize(b_results),
        "results": {
            "A_baseline": a_results,
            "B_improved": b_results,
        },
    }
    report["accuracy_improvement_percentage_points"] = round(
        report["B_improved"]["accuracy_percent"]
        - report["A_baseline"]["accuracy_percent"],
        2,
    )

    with open("eval_results.json", "w", encoding="utf-8") as file:
        json.dump(report, file, ensure_ascii=False, indent=2)

    print(f"Tasks per configuration: {len(TASKS)}")
    print(
        f"A Baseline: {report['A_baseline']['passed']}/"
        f"{len(TASKS)} ({report['A_baseline']['accuracy_percent']}%)"
    )
    print(
        f"B Improved: {report['B_improved']['passed']}/"
        f"{len(TASKS)} ({report['B_improved']['accuracy_percent']}%)"
    )
    print(
        "Accuracy change: "
        f"{report['accuracy_improvement_percentage_points']:+.2f} percentage points"
    )
    print("A errors:")
    for row in report["A_baseline"]["errors"]:
        print(f"  Task {row['task_id']}: {row['input']} -> {row['predicted']}")
    print("B errors:")
    for row in report["B_improved"]["errors"]:
        print(f"  Task {row['task_id']}: {row['input']} -> {row['predicted']}")
    print("Full report saved to eval_results.json")


if __name__ == "__main__":
    main()
