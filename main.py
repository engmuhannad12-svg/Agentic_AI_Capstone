"""Rafeeq: a minimal bilingual municipal permit assistant."""
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Rafeeq:
    max_steps: int = 5
    memory: list[str] = field(default_factory=list)
    permits: list[dict[str, Any]] = field(default_factory=list)

    def tools(self):
        return {
            "permit_requirements": self.permit_requirements,
            "check_status": self.check_status,
            "prepare_application": self.prepare_application,
        }

    def permit_requirements(self, permit_type: str) -> dict:
        """Demo data only; not official municipal guidance."""
        return {
            "permit_type": permit_type,
            "required_documents": [
                "Applicant ID",
                "Property ownership or lease proof",
                "Site plan",
            ],
            "notice": "Demonstration data. Verify actual requirements with the municipality.",
        }

    def check_status(self, application_id: str) -> dict:
        for permit in self.permits:
            if permit["application_id"] == application_id:
                return {"application_id": application_id, "status": permit["status"]}
        return {
            "application_id": application_id,
            "status": "not_found_in_demo_data",
        }

    def prepare_application(self, permit_type: str, applicant_name: str,
                            approved: bool = False) -> dict:
        if not approved:
            return {
                "status": "approval_required",
                "message": "Human approval is required before submitting an application.",
            }
        application_id = f"DEMO-{len(self.permits) + 1:04d}"
        record = {
            "application_id": application_id,
            "permit_type": permit_type,
            "applicant_name": applicant_name,
            "status": "submitted_demo",
        }
        self.permits.append(record)
        return record

    def respond(self, message: str, language: str = "en") -> dict:
        self.memory.append(message)
        if len(self.memory) > 10:
            self.memory = self.memory[-10:]

        text = message.lower()
        if any(word in text for word in ["status", "حالة", "متابعة"]):
            return {
                "reply": (
                    "Please provide an application ID to check demo status."
                    if language == "en"
                    else "يرجى إدخال رقم الطلب للتحقق من الحالة التجريبية."
                ),
                "tools": list(self.tools()),
            }

        if any(word in text for word in ["permit", "تصريح", "رخصة"]):
            return {
                "reply": (
                    "I can explain demo permit requirements or help prepare an application."
                    if language == "en"
                    else "يمكنني شرح متطلبات التصريح التجريبية أو مساعدتك في تجهيز طلب."
                ),
                "tools": list(self.tools()),
            }

        return {
            "reply": (
                "Welcome to Rafeeq. How can I help with a municipal permit?"
                if language == "en"
                else "مرحبًا بك في رفيق. كيف يمكنني مساعدتك في التصاريح البلدية؟"
            ),
            "tools": list(self.tools()),
        }


if __name__ == "__main__":
    agent = Rafeeq()
    print(agent.respond("أحتاج تصريحًا", language="ar"))
    print(agent.permit_requirements("construction"))
    print(agent.prepare_application("construction", "Demo User"))
