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

    async def test_thinking_blocks_attributes(self):
        """Test to verify thinking blocks have the correct attributes and structure"""
        messages = [
            {"role": "system", "content": "You are a helpful AI assistant."},
            {
                "role": "user",
                "content": "Please solve this math problem step by step: If a train travels at 60 mph for 2.5 hours, how far does it travel?",
            },
        ]

        print("\n=== Testing Thinking Blocks Structure ===")
        try:
            response = await self.lm.respond_async(messages=messages)
            print(f"Response received successfully: {response[:100]}...")
            self.assertIsInstance(response, str)
            self.assertGreater(len(response), 0)
        except AttributeError as e:
            if "'TextBlock' object has no attribute 'value'" in str(e):
                self.fail(
                    "TextBlock missing 'value' attribute - API response structure may have changed"
                )
            raise

    async def test_thinking_blocks_with_structured_output(self):
        """Test thinking blocks with structured output to verify attribute handling"""
        from pydantic import BaseModel

        class SimpleResponse(BaseModel):
            answer: str
            explanation: str

        messages = [
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": "What is 2+2? Provide answer and explanation."},
        ]

        print("\n=== Testing Thinking Blocks with Structured Output ===")
        try:
            response = await self.lm.respond_async(
                messages=messages, response_model=SimpleResponse
            )
            print(f"Structured response received: {response}")
            self.assertIsInstance(response, SimpleResponse)
            self.assertTrue(hasattr(response, "answer"))
            self.assertTrue(hasattr(response, "explanation"))
        except AttributeError as e:
            if "'TextBlock' object has no attribute 'value'" in str(e):
                self.fail("TextBlock missing 'value' attribute in structured output")
            raise

    async def test_thinking_blocks_raw_response(self):
        """Test to examine the raw response structure from the API"""
        messages = [
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": "Count from 1 to 3."},
        ]

        print("\n=== Testing Raw Response Structure ===")
        try:
            # Access the raw response if possible
            response = await self.lm.respond_async(messages=messages)
            print(f"Raw response type: {type(response)}")
            print(f"Raw response content: {response}")

            # Add detailed response structure inspection
            print("\nResponse Structure Details:")
            print(f"Is string: {isinstance(response, str)}")
            if hasattr(response, "content"):
                for i, block in enumerate(response.content):
                    print(f"\nBlock {i}:")
                    print(f"Type: {block.type}")
                    print(f"Available attributes: {dir(block)}")
                    if hasattr(block, "text"):
                        print(f"Has .text: {block.text}")
                    if hasattr(block, "value"):
                        print(f"Has .value: {block.value}")

            self.assertIsInstance(response, str)
        except Exception as e:
            print(f"Exception type: {type(e)}")
            print(f"Exception message: {str(e)}")
            print(f"Full exception details: {dir(e)}")
            raise

    async def test_thinking_blocks_structure(self):
        """Test specifically for thinking blocks structure"""
        messages = [
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": "What is 2+2?"},
        ]

        print("\n=== Testing Thinking Blocks Structure ===")
        try:
            # Set high reasoning effort to trigger thinking
            self.lm.lm_config["reasoning_effort"] = "high"
            response = await self.lm.respond_async(messages=messages)
            print(f"Response with thinking:\n{response}")
            self.assertIsInstance(response, str)
            self.assertGreater(len(response), 0)
        except AttributeError as e:
            print(f"Attribute Error Details:")
            print(f"Error message: {str(e)}")
            print(f"Error type: {type(e)}")
            if hasattr(e, "__context__"):
                print(f"Context: {e.__context__}")
            raise

    def test_all(self):
        print("\nStarting Claude 3.7 Sonnet Thinking Tests...")
        asyncio.run(self.test_thinking_response())
        asyncio.run(self.test_thinking_structured_output())
        asyncio.run(self.test_thinking_with_high_effort())
        asyncio.run(self.test_thinking_blocks_attributes())
        asyncio.run(self.test_thinking_blocks_with_structured_output())
        asyncio.run(self.test_thinking_blocks_raw_response())
        asyncio.run(self.test_thinking_blocks_structure())
        print("\nAll tests completed successfully!")


if __name__ == "__main__":
    unittest.main()
