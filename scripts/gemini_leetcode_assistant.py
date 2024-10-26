
import json
import google.generativeai as genai

# Install the google-generativeai package before running
# pip install google-generativeai

# Sample input data in JSON format
input_data = {
    "_id": {"$oid": "670196734f9c9445f573ba2e"},
    "id": "1497",
    "title": "Check If Array Pairs Are Divisible by k",
    "problemDescription": "<p>Given an array of integers <code>arr</code> of even length <code>n</code> and an integer <code>k</code>.</p>\n\n<p>We want to divide the array into exactly <code>n / 2</code> pairs such that the sum of each pair is divisible by <code>k</code>.</p>\n\n<p>Return <code>true</code><em> If you can find a way to do that or </em><code>false</code><em> otherwise</em>.</p>",
    "example_testcases": "[1,2,3,4,5,10,6,7,8,9]\n5\n[1,2,3,4,5,6]\n7\n[1,2,3,4,5,6]\n10",
    "topic_tags": ["Array", "Hash Table", "Counting"],
    "hints": ["Keep an array of the frequencies of ((x % k) + k) % k for each x in arr.", "for each i in [0, k - 1] we need to check if freq[i] == freq[k - i]", "Take care of the case when i == k - i and when i == 0"],
    "difficulty": "Medium",
    "submissions": [
        {
            "timestamp": "2024-10-05 19:41:37",
            "code": "class Solution(object):\n    def canArrange(self, arr, k):\n        \n: type arr: List[int]\n: type k: int\n: rtype: bool\n        \n        rem_freq = [0] * k\n        for i in arr:\n            rem_freq[i % k] += 1\n        if rem_freq[0] % 2 != 0:\n            return False\n        for i in range(1, (k // 2) + 1):\n            if rem_freq[i] != rem_freq[k - i]:\n                return False\n        return True"
        }
    ]
}

# Construct the prompt by embedding the input data
prompt_template = '''
You are given the following input data for a coding problem:

Input Data:
```json
{{input_data}}
```

### Task:
Based on the input problem, generate the following:

1. **Problem Intuition:**  
   Provide an intuitive explanation of the problem's goal, explaining what needs to be achieved and any key observations about how the problem can be solved.

2. **Approach Breakdown:**
   - Explain the logical steps required to solve the problem.
   - Highlight important aspects, such as calculations, iterations, and conditions that need to be checked.
   - Discuss any data structures used or key steps to handle the problem's requirements.

3. **Step-by-Step Explanation of the Example:**  
   For the given example test case, break it down step by step, showing how the solution would work.

4. **Brute Force Solution:**  
   Provide a brute force approach to solving the problem, including time and space complexity.

5. **Better Solution:**  
   Explain a more optimized solution, improving on the brute force approach.

6. **Optimal Solution:**  
   Provide the optimal solution with explanation and time/space complexity.

7. **Optimal Solution Revision Notes:**  
   Summarize the optimal solution in a revision-friendly format.
'''

# Replace placeholder with the actual input data
prompt = prompt_template.replace(
    '{{input_data}}', json.dumps(input_data, indent=4))

# Initialize the Gemini model
# Add your Gemini API key here
genai.configure(api_key="AIzaSyDUjXn6GSd4acSPrBtCVQLDLlKHDiNfLq4")
model = genai.GenerativeModel("gemini-1.5-flash")

# Send the prompt to the Gemini model and get the response
response = model.generate_content(prompt)

# Splitting the response into sections
sections = response.text.split("\n\n")

# Store separate sections for different part
problem_intuition = sections[1]
problem_intuition_data = sections[2]
approach_breakdown = sections[3]
approach_breakdown_data = sections[4]
step_by_step_explanation = sections[5]
step_by_step_explanation_data = sections[6]
brute_force_solution = sections[7]
brute_force_solution_data = sections[8]
better_solution = sections[9]
better_solution_data = sections[10]
optimal_solution = sections[11]
optimal_solution_data = sections[12]
revision_notes = sections[13]
revision_notes_data = sections[14]

# Print or store the responses
print("Problem Intuition:", problem_intuition, problem_intuition_data)
print()
print("Approach Breakdown:", approach_breakdown, approach_breakdown_data)
print()
print("Step-by-Step Explanation:", step_by_step_explanation,
      step_by_step_explanation_data)
print()
print("Brute Force Solution:", brute_force_solution, brute_force_solution_data)
print()
print("Better Solution:", better_solution, better_solution_data)
print()
print("Optimal Solution:", optimal_solution, optimal_solution_data)
print()
print("Optimal Solution Revision Notes:", revision_notes, revision_notes_data)
