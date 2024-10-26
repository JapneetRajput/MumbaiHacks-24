import os
import re
import json

problem_data = {
  "_id": {
    "$oid": "6701910aeaa81da1823b6166"
  },
  "id": "1",
  "title": "Two Sum",
  "titleSlug": "two-sum",
  "problemDescription": "<p>Given an array of integers <code>nums</code>&nbsp;and an integer <code>target</code>, return <em>indices of the two numbers such that they add up to <code>target</code></em>.</p>\n\n<p>You may assume that each input would have <strong><em>exactly</em> one solution</strong>, and you may not use the <em>same</em> element twice.</p>\n\n<p>You can return the answer in any order.</p>\n\n<p>&nbsp;</p>\n<p><strong class=\"example\">Example 1:</strong></p>\n\n<pre>\n<strong>Input:</strong> nums = [2,7,11,15], target = 9\n<strong>Output:</strong> [0,1]\n<strong>Explanation:</strong> Because nums[0] + nums[1] == 9, we return [0, 1].\n</pre>\n\n<p><strong class=\"example\">Example 2:</strong></p>\n\n<pre>\n<strong>Input:</strong> nums = [3,2,4], target = 6\n<strong>Output:</strong> [1,2]\n</pre>\n\n<p><strong class=\"example\">Example 3:</strong></p>\n\n<pre>\n<strong>Input:</strong> nums = [3,3], target = 6\n<strong>Output:</strong> [0,1]\n</pre>\n\n<p>&nbsp;</p>\n<p><strong>Constraints:</strong></p>\n\n<ul>\n\t<li><code>2 &lt;= nums.length &lt;= 10<sup>4</sup></code></li>\n\t<li><code>-10<sup>9</sup> &lt;= nums[i] &lt;= 10<sup>9</sup></code></li>\n\t<li><code>-10<sup>9</sup> &lt;= target &lt;= 10<sup>9</sup></code></li>\n\t<li><strong>Only one valid answer exists.</strong></li>\n</ul>\n\n<p>&nbsp;</p>\n<strong>Follow-up:&nbsp;</strong>Can you come up with an algorithm that is less than <code>O(n<sup>2</sup>)</code><font face=\"monospace\">&nbsp;</font>time complexity?",
  "example_testcases": "[2,7,11,15]\n9\n[3,2,4]\n6\n[3,3]\n6",
  "topic_tags": [
    "Array",
    "Hash Table"
  ],
  "hints": [
    "A really brute force way would be to search for all possible pairs of numbers but that would be too slow. Again, it's best to try out brute force solutions for just for completeness. It is from these brute force solutions that you can come up with optimizations.",
    "So, if we fix one of the numbers, say <code>x</code>, we have to scan the entire array to find the next number <code>y</code> which is <code>value - x</code> where value is the input parameter. Can we change our array somehow so that this search becomes faster?",
    "The second train of thought is, without changing the array, can we use additional space somehow? Like maybe a hash map to speed up the search?"
  ],
  "difficulty": "Easy",
  "submissions": [
    {
      "timestamp": "2024-10-09 09:57:20",
      "code": "class Solution:\n    def twoSum(self, nums: List[int], target: int) -> List[int]:\n        \n        map={}\n\n        for i in range(len(nums)):\n            if target-nums[i] in map.keys():\n                return [i,map[target-nums[i]]]\n                map[nums[i]]=i\n        \n        return [0,1]"
    }
  ]
}

from groq import Groq
from typing import Dict, List
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
        {problem_data['submissions'][0]['code']}
        
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
            max_tokens=1024,
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
        "analysis_timestamp": problem_data["submissions"][0]["timestamp"],
        "insights": insights
    }
    
    return analysis_result

print(analyze_problem(problem_data))

print('import numpy as np\nimport manim\n\n\nclass BinarySearch(Scene):\n def construct(self):\n # Create the array\n array = [3, 1, 4, 1, 5, 9, 2, 6]\n array_mob = VGroup(*[Text(str(i)) for i in array])\n array_mob.arrange(RIGHT, buff=0.5)\n self.add(array_mob)\n\n # Create the search value\n search_value = 5\n search_mob = Text(str(search_value))\n search_mob.to_edge(UP, buff=1.0)\n self.add(search_mob)\n\n # Perform the binary search\n low = 0\n high = len(array) - 1\n\n while low <= high:\n mid = (low + high) // 2\n mid_mob = array_mob[mid]\n mid_mob.set_color(YELLOW)\n self.wait(1.0)\n\n if array[mid] == search_value:\n self.wait(1.0)\n break\n elif array[mid] < search_value:\n low = mid + 1\n else:\n high = mid - 1\n\n mid_mob.set_color(WHITE)\n self.wait(1.0)\n\n # Highlight the found element\n mid_mob.set_color(GREEN)\n self.wait(2.0)\n\n # Clean up\n self.remove(array_mob)\n self.remove(search_mob)\n\n # Display the result\n result_mob = Text(f"Found {search_value} at index {mid}")\n result_mob.to_edge(DOWN, buff=1.0)\n self.add(result_mob)\n self.wait(2.0)\n\n # Clean up\n self.remove(result_mob)\n\n\nif name == "main":\n scene = BinarySearch()\n scene.render()", "audio_script": "In this visualization, we will perform a binary search on an array to find a specific value. The array is [3, 1, 4, 1, 5, 9, 2, 6]. We are looking for the value 5. Binary search works by repeatedly dividing the search interval in half. If the value of the search key is less than the item in the middle of the interval, narrow the interval to the lower half. Otherwise, narrow it to the upper half. Repeatedly check until the value is found or the interval is empty. In our case, we start by comparing the middle element of the array, which is 4, with our search value, 5. Since 5 is greater than 4, we narrow the interval to the upper half of the array. We continue this process until we find the value 5 at index 4. The binary search algorithm is efficient for large arrays because it reduces the number of comparisons required to find the target value.')