

import google.generativeai as gemini
import json

# Initialize the Gemini API client
gemini.configure(api_key='AIzaSyDUjXn6GSd4acSPrBtCVQLDLlKHDiNfLq4')

# Input data in JSON format
input_data = {
    "id": "1497",
    "title": "Check If Array Pairs Are Divisible by k",
    "problemDescription": "<p>Given an array of integers <code>arr</code> of even length <code>n</code> and an integer <code>k</code>.</p>\n\n<p>We want to divide the array into exactly <code>n / 2</code> pairs such that the sum of each pair is divisible by <code>k</code>.</p>\n\n<p>Return <code>true</code><em> If you can find a way to do that or </em><code>false</code><em> otherwise</em>.</p>\n\n<p>&nbsp;</p>\n<p><strong class=\"example\">Example 1:</strong></p>\n\n<pre>\n<strong>Input:</strong> arr = [1,2,3,4,5,10,6,7,8,9], k = 5\n<strong>Output:</strong> true\n<strong>Explanation:</strong> Pairs are (1,9),(2,8),(3,7),(4,6) and (5,10).</pre>\n\n<p><strong class=\"example\">Example 2:</strong></p>\n\n<pre>\n<strong>Input:</strong> arr = [1,2,3,4,5,6], k = 7\n<strong>Output:</strong> true\n<strong>Explanation:</strong> Pairs are (1,6),(2,5) and(3,4).</pre>\n\n<p><strong class=\"example\">Example 3:</strong></p>\n\n<pre>\n<strong>Input:</strong> arr = [1,2,3,4,5,6], k = 10\n<strong>Output:</strong> false\n<strong>Explanation:</strong> You can try all possible pairs to see that there is no way to divide arr into 3 pairs each with sum divisible by 10.</pre>",
    "example_testcases": "[1,2,3,4,5,10,6,7,8,9]\n5\n[1,2,3,4,5,6]\n7\n[1,2,3,4,5,6]\n10",
    "topic_tags": ["Array", "Hash Table", "Counting"],
    "hints": ["Keep an array of the frequencies of ((x % k) + k) % k for each x in arr.", "for each i in [0, k - 1] we need to check if freq[i] == freq[k - i]", "Take care of the case when i == k - i and when i == 0"],
    "difficulty": "Medium",
    "submissions": [{
        "timestamp": "2024-10-05 19:41:37",
        "code": "class Solution(object):\n    def canArrange(self, arr, k):\n        # Array to store frequency of elements\n        n=len(arr)\n        rem_freq=[0]*k\n\n        for i in arr:\n            rem_freq[i%k]=rem_freq[i%k]+1\n        \n        if rem_freq[0]%2!=0:\n            return False\n\n        for i in range(1,(k//2)+1):\n            if rem_freq[i]!=rem_freq[k-i]:\n                return False\n        return True"
    }]
}

# The dynamic prompt
prompt = f'''
You are given the following input data for a coding problem:

Input Data:
```json
{json.dumps(input_data, indent=4)}
```

### Task:
Based on the input problem, generate the following:

1. **Problem Intuition:**  
   Provide an intuitive explanation of the problem's goal, explaining what needs to be achieved and any key observations about how the problem can be solved (specific to the problem’s context).

2. **Approach Breakdown:**
   - Explain the logical steps required to solve the problem.
   - Highlight important aspects, such as calculations, iterations, and conditions that need to be checked based on the problem’s constraints.
   - Discuss any data structures used or key steps to handle the problem’s requirements.

3. **Step-by-Step Explanation of the Example:**  
   For the given example test case, break it down step by step, showing how the solution would work. This should include:
   - Key computations or transformations.
   - Any important data structures or conditions being checked.
   - A clear explanation of how the example leads to the correct output.

4. **Brute Force Solution:**  
   Provide a brute force approach to solving the problem (even if inefficient). Describe how it works, its time and space complexity, and why it’s less efficient.

5. **Better Solution:**  
   Explain a more optimized solution, improving on the brute force approach. Discuss any improvements in terms of reducing time or space complexity.

6. **Optimal Solution:**  
   Provide the optimal solution, explaining:
   - Why it’s the most efficient approach.
   - Key techniques or optimizations used.
   - The time and space complexity breakdown.
   - Include the solution code, if provided, with a detailed explanation.

7. **Optimal Solution Revision Notes:**  
   Summarize the optimal solution in a revision-friendly format. Highlight:
   - Key concepts used to solve the problem.
   - Important edge cases.
   - Essential conditions or constraints that must be handled carefully.
'''

# Send the prompt to Gemini LLM
response = gemini.generate(prompt=prompt)

# Store the different sections of the response in separate variables
problem_intuition = response.get("Problem Intuition", "No intuition provided")
approach_breakdown = response.get(
    "Approach Breakdown", "No approach breakdown provided")
step_by_step_example = response.get(
    "Step-by-Step Explanation of the Example", "No step-by-step explanation provided")
brute_force_solution = response.get(
    "Brute Force Solution", "No brute force solution provided")
better_solution = response.get(
    "Better Solution", "No better solution provided")
optimal_solution = response.get(
    "Optimal Solution", "No optimal solution provided")
optimal_revision_notes = response.get(
    "Optimal Solution Revision Notes", "No revision notes provided")

# Output the responses
print("Problem Intuition:", problem_intuition)
print("Approach Breakdown:", approach_breakdown)
print("Step-by-Step Explanation of the Example:", step_by_step_example)
print("Brute Force Solution:", brute_force_solution)
print("Better Solution:", better_solution)
print("Optimal Solution:", optimal_solution)
print("Optimal Solution Revision Notes:", optimal_revision_notes)
