import asyncio
import unittest

from synth_ai.zyk import LM


class TestSonnetThinking(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lm = LM(
            model_name="claude-3-7-sonnet-latest",
            formatting_model_name="gpt-4o-mini",
            temperature=0,
        )
        # Set reasoning_effort in lm_config
        cls.lm.lm_config["reasoning_effort"] = "high"

    async def test_thinking_response(self):
        messages = [
            {"role": "system", "content": "You are a helpful AI assistant."},
            {
                "role": "user",
                "content": "Please solve this math problem step by step: If a train travels at 60 mph for 2.5 hours, how far does it travel?",
            },
        ]

        response = await self.lm.respond_async(messages=messages)
        print("\n=== Math Problem Test ===")
        print(f"Response:\n{response}\n")
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)

        # Test that the response includes numerical calculation
        self.assertTrue(any(char.isdigit() for char in response))

    async def test_thinking_structured_output(self):
        from pydantic import BaseModel

        class MathSolution(BaseModel):
            steps: list[str]
            final_answer: float
            units: str

        messages = [
            {"role": "system", "content": "You are a math problem solver."},
            {
                "role": "user",
                "content": "If a car travels at 30 mph for 45 minutes, how far does it travel? Provide steps.",
            },
        ]

        response = await self.lm.respond_async(
            messages=messages, response_model=MathSolution
        )

        print("\n=== Structured Math Problem Test ===")
        print(f"Steps:")
        for i, step in enumerate(response.steps, 1):
            print(f"{i}. {step}")
        print(f"Final Answer: {response.final_answer} {response.units}\n")

        self.assertIsInstance(response, MathSolution)
        self.assertGreater(len(response.steps), 0)
        self.assertIsInstance(response.final_answer, float)
        self.assertIsInstance(response.units, str)

    async def test_thinking_with_high_effort(self):
        messages = [
            {
                "role": "system",
                "content": "You are a problem-solving AI. Break down complex problems into detailed steps.",
            },
            {
                "role": "user",
                "content": "Design a system to automate a coffee shop's inventory management. Consider all aspects.",
            },
        ]

        print("\n=== High Effort Thinking Test ===")
        response = await self.lm.respond_async(messages=messages)
        print(f"High Effort Response:\n{response}\n")
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 100)  # Expecting detailed response

        # Test with medium effort
        lm_medium = LM(
            model_name="claude-3-7-sonnet-latest",
            formatting_model_name="gpt-4o-mini",
            temperature=0,
        )
        lm_medium.lm_config["reasoning_effort"] = "medium"
        print("\n=== Medium Effort Thinking Test ===")
        response_medium = await lm_medium.respond_async(messages=messages)
        print(f"Medium Effort Response:\n{response_medium}\n")
        self.assertIsInstance(response_medium, str)

    def test_all(self):
        print("\nStarting Claude 3.7 Sonnet Thinking Tests...")
        asyncio.run(self.test_thinking_response())
        asyncio.run(self.test_thinking_structured_output())
        asyncio.run(self.test_thinking_with_high_effort())
        print("\nAll tests completed successfully!")


if __name__ == "__main__":
    unittest.main()
