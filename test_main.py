import unittest
from main import Rafeeq


class TestRafeeq(unittest.TestCase):
    def setUp(self):
        self.agent = Rafeeq()

    def test_arabic_permit_request(self):
        result = self.agent.respond("أحتاج تصريحًا", language="ar")
        self.assertIn("تصريح", result["reply"])
        self.assertEqual(len(result["tools"]), 3)

    def test_english_permit_request(self):
        result = self.agent.respond("I need a permit", language="en")
        self.assertIn("permit", result["reply"].lower())

    def test_requirements_tool(self):
        result = self.agent.permit_requirements("construction")
        self.assertIn("required_documents", result)
        self.assertTrue(result["required_documents"])

    def test_status_not_found(self):
        result = self.agent.check_status("UNKNOWN-001")
        self.assertEqual(result["status"], "not_found_in_demo_data")

    def test_human_approval_required(self):
        result = self.agent.prepare_application("construction", "Demo User")
        self.assertEqual(result["status"], "approval_required")
        self.assertEqual(len(self.agent.permits), 0)

    def test_approved_demo_submission(self):
        result = self.agent.prepare_application(
            "construction", "Demo User", approved=True
        )
        self.assertEqual(result["status"], "submitted_demo")
        self.assertEqual(len(self.agent.permits), 1)

    def test_memory_is_bounded(self):
        for i in range(15):
            self.agent.respond(f"message {i}")
        self.assertEqual(len(self.agent.memory), 10)


if __name__ == "__main__":
    unittest.main()
