import os
from script_generator import generate_script

def generate_educational_video(topic: str):
    """
    Orchestrates the complete video generation workflow.
    """
    try:
        # 1. Generate scripts using LLM
        scripts = generate_script(topic)
        
        if not scripts.get('visualization_script') or not scripts.get('explanation_script'):
            raise ValueError("LLM failed to generate complete scripts")
        
        # 2. Save visualization script to file
        viz_file = f"{topic.lower().replace(' ', '_')}_viz.py"
        with open(viz_file, "w") as f:
            f.write(scripts["visualization_script"])
        
        # 3. Call video generation API
        import requests
        
        files = {
            'file': (viz_file, open(viz_file, 'rb')),
        }
        
        response = requests.post(
            'http://localhost:8000/generate-video/',
            files=files
        )
        
        if response.status_code != 200:
            raise ValueError(f"API call failed: {response.text}")
        
        # 4. Cleanup and return results
        os.remove(viz_file)
        
        return {
            "status": "success",
            "explanation_script": scripts["explanation_script"],
            "video_path": response.json()["video_path"]
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

# Example usage:
if __name__ == "__main__":
    # Import and initialize your client here
    result = generate_educational_video("binary search")
    
    if result["status"] == "success":
        print(f"Video generated successfully at: {result['video_path']}")
        print("\nExplanation script for voiceover:")
        print(result["explanation_script"])
    else:
        print(f"Error generating video: {result['error']}")