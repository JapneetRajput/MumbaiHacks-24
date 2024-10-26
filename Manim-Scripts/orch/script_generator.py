from groq import Groq
from typing import Dict
import json
import os

def generate_script(topic: str, client: Groq) -> Dict:
    """
    Generate an educational script for a given topic using Groq LLM.
    Returns a JSON object containing the narrative script and timing information.
    
    Args:
        topic (str): The topic to create a script for
        client (Groq): Initialized Groq client
    
    Returns:
        Dict: JSON object containing script sections and timing
    """
    
    system_prompt = """You are an expert educational content creator who specializes in creating clear, 
    engaging video scripts. Your task is to create a detailed script for an educational video.
    
    IMPORTANT: You must enclose your entire response between %%%script%%% delimiters.
    
    The script should include:
    1. A clear title
    2. Total duration (in seconds)
    3. Multiple sections, each containing:
        - Section title
        - Content to be explained
        - Visualization notes
        - Duration in seconds
        - Pause duration needed after this section
    
    Guidelines:
    1. Each section should be 15-30 seconds
    2. Include clear visualization notes for each section
    3. Add appropriate pauses between sections
    4. Total duration should be 2-3 minutes
    5. Make the content engaging and educational
    6. Include specific timing for animations and transitions
    7. ENSURE your response is enclosed in %%%script%%% delimiters"""

    user_prompt = f"""Create an educational video script about {topic}.
    The script should:
    1. Start with a brief introduction
    2. Break down the concept step by step
    3. Include practical examples
    4. End with a summary
    
    Make sure each section has clear visualization notes that can be animated later.
    Remember to enclose your entire response in %%%script%%% delimiters."""

    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            temperature=1,
            max_tokens=131072,
            top_p=1,
            stream=False,
            stop=None,
        )
        
        # Extract the content from the response
        raw_content = completion.choices[0].message.content
        
        # Extract content between delimiters
        start_token = "%%%script%%%"
        end_token = "%%%script%%%"
        
        try:
            # Find the content between delimiters
            start_idx = raw_content.find(start_token) + len(start_token)
            end_idx = raw_content.rfind(end_token)
            
            if start_idx == -1 or end_idx == -1:
                raise ValueError("Delimiter tokens not found in response")
                
            script_content = raw_content[start_idx:end_idx].strip()
            
            # Create a dictionary to store the parsed content
            script_dict = {
                "raw_content": script_content
            }

            return script_dict

        except ValueError as e:
            raise ValueError(f"Failed to extract content between delimiters: {e}")
            
    except Exception as e:
        raise Exception(f"Error generating script: {str(e)}")

# Example usage
if __name__ == "__main__":
    os.environ['GROQ_API_KEY'] = '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'
    # Initialize Groq client
    client = Groq()
    
    # Example topics to test
    test_topics = [
        "binary search algorithm"
    ]
    
    # Test the function
    try:
        for topic in test_topics:
            print(f"\nGenerating script for: {topic}")
            script = generate_script(topic, client)
            
            print("\nGenerated Script:")
            print(script["raw_content"])
            
    except Exception as e:
        print(f"Error: {str(e)}")