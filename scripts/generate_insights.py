from typing import Dict, List
from groq import Groq
import os
import re
import json


class CodeAnalyzer:
    def __init__(self):
        os.environ['GROQ_API_KEY'] = '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'
        self.client = Groq()

    def get_system_prompt(self) -> str:
        return """
        You are an expert code analyzer focusing on algorithmic patterns and implementation techniques.
        Analyze the given code submission and provide key insights in the following structured format:

        {
        "Algorithm Pattern": {
            "Description": "Briefly describe the overall algorithmic approach.",
            "Approach": "Explain the main steps taken by the algorithm."
        },
        "Time & Space Complexity": {
            "Time Complexity": "Describe the time complexity, including the variable used and why.",
            "Space Complexity": "Describe the space complexity and the reason for it."
        },
        "Data Structures": {
            "Key Data Structures": "List the data structures used in the code and their purposes."
        },
        "Implementation Technique": {
            "Key Techniques": "Highlight coding techniques like hashing, iteration, early return, or other specific implementations."
        },
        "Potential Improvements": {
            "Suggesting Improvements": [
            "List suggestions to enhance code readability or functionality if any."
            ],
            "Optimization Suggestions": [
            "List potential optimizations if any, even if the code is already efficient."
            ]
        }
        }

        Format your response *exactly* in this JSON structure, and do not include any additional commentary or explanation outside the JSON block.
        """

    def get_user_prompt(self, problem_data: Dict) -> str:
        return f"""
        Analyze the following code submission for the problem '{problem_data['title']}':
        
        Problem Description:
        {problem_data['problemDescription']}
        
        Submitted Code:
        {problem_data['submission']}
        
        Provide detailed insights about the implementation approach and patterns used.
        """

    def analyze_code(self, problem_data: Dict) -> Dict:
        accumulated_response = ""

        completion = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": self.get_system_prompt()
                },
                {
                    "role": "user",
                    "content": self.get_user_prompt(problem_data)
                }
            ],
            temperature=1,
            max_tokens=8000,
            top_p=1,
            stream=True,
            stop=None
        )

        # Accumulate streamed response
        for chunk in completion:
            delta_content = chunk.choices[0].delta.content or ""
            accumulated_response += delta_content

        insights = self.clean_and_parse_response(accumulated_response)

        return insights

    def clean_and_parse_response(self, raw_response: str) -> dict:
        try:
            # Find the JSON part within the raw response using regex
            json_match = re.search(r'{.*}', raw_response, re.DOTALL)

            # If JSON-like structure is found, attempt to parse it
            if json_match:
                json_str = json_match.group(0)
                return json.loads(json_str)
            else:
                # Return error if no JSON structure is detected
                return {"error": "No JSON object found in response", "raw_response": raw_response}

        except json.JSONDecodeError as e:
            # Return error details if JSON decoding fails
            return {"error": "Failed to parse JSON", "raw_response": raw_response, "exception": str(e)}

# Example usage


def analyze_problem(problem_data: Dict) -> Dict:
    analyzer = CodeAnalyzer()
    insights = analyzer.analyze_code(problem_data)

    # Store results in a structured format
    analysis_result = {
        "problem_id": problem_data["id"],
        "problem_title": problem_data["title"],
        "analysis_timestamp": problem_data["submission"],
        "insights": insights
    }

    return analysis_result
