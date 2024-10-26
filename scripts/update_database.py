import sys
import os
from pymongo import MongoClient
from datetime import datetime
import requests
from generate_insights import analyze_problem

# Import the fetch_single_problem function


def fetch_single_problem(problem_name):
    query = '''
    query selectProblem($titleSlug: String!) {
        question(titleSlug: $titleSlug) {
            questionFrontendId
            title
            titleSlug
            content
            exampleTestcases
            topicTags {
                name
            }
            hints
            difficulty
        }
    }'''

    title_slug = problem_name.lower().replace(
        " ", "-")  # Create slug from the problem name

    response = requests.post(
        'https://leetcode.com/graphql',
        json={
            'query': query,
            'variables': {'titleSlug': title_slug}
        },
        headers={'Content-Type': 'application/json'}
    )

    if response.status_code == 200:
        result = response.json()
        question_data = result['data']['question']

        if question_data:
            return {
                'questionFrontendId': question_data['questionFrontendId'],
                'title': question_data['title'],
                'titleSlug': question_data['titleSlug'],
                'content': question_data['content'],
                'exampleTestcases': question_data['exampleTestcases'],
                'topicTags': [tag['name'] for tag in question_data['topicTags']],
                'hints': question_data['hints'],
                'difficulty': question_data['difficulty'],
            }
        else:
            raise ValueError(
                f"Problem with titleSlug '{title_slug}' not found.")
    else:
        raise ValueError(
            f"Failed to fetch problem data: {response.status_code}")


# Get input parameters from GitHub Actions or CLI
problem_name = sys.argv[1]    # Problem name passed via sys args
solution = sys.argv[2]   # Solution link or code passed via sys args
notes = sys.argv[3] if len(sys.argv) > 3 else ""  # Optional notes

# MongoDB connection
# Fetch MongoDB URI from environment variable
MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("MONGO_URI environment variable is missing")

client = MongoClient(MONGO_URI)
db = client['leetcode']  # Database name
collection = db['problems']  # Collection name

# Fetch problem data using the problem_name
try:
    problem_data = fetch_single_problem(problem_name)
except ValueError as e:
    print(e)
    sys.exit(1)

# Prepare the submission object
timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
submission = {
    'timestamp': timestamp,
    'code': solution
}

# Check if the problem already exists in the database using the problem number (questionFrontendId)
existing_problem = collection.find_one(
    {"id": problem_data['questionFrontendId']})

if existing_problem:
    # If the problem exists, update the 'submissions' field by appending the new submission
    collection.update_one(
        {"id": problem_data['questionFrontendId']},
        {"$push": {"submissions": submission}}
    )
    print(
        f"Updated existing problem {problem_data['questionFrontendId']} with new submission.")
else:
    # If the problem does not exist, create a new document based on the fetched data
    new_problem = {
        'id': problem_data['questionFrontendId'],
        'title': problem_data['title'],
        'titleSlug': problem_data['titleSlug'],
        'problemDescription': problem_data['content'],
        'example_testcases': problem_data['exampleTestcases'],
        'topic_tags': problem_data['topicTags'],  # Use fetched tags
        'hints': problem_data['hints'],            # Use fetched hints
        'difficulty': problem_data['difficulty'],
        'submissions': [submission]  # Add first submission
    }
    collection.insert_one(new_problem)
    print(
        f"Inserted new problem {problem_data['questionFrontendId']} - {problem_data['title']} into the database.")

# Analyze the problem data for insights
analysis_result = analyze_problem(
    {'id': problem_data['questionFrontendId'], 'title': problem_data['title'], 'problemDescription': problem_data['content'], 'submission': submission})

# Update the MongoDB document with the analysis insights
collection.update_one(
    {"id": problem_data['questionFrontendId']},
    {"$set": {"insights": analysis_result['insights']}}
)
print(
    f"Analysis insights added for problem {problem_data['questionFrontendId']}.")
