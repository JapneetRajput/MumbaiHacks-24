# script_generator.py
from typing import Dict
import json
from groq import Groq

def generate_script(topic: str, client) -> Dict[str, str]:
    """
    Generate an educational script based on the topic using LLM.
    Returns both explanation and visualization scripts.
    """
    prompt = f"""
    Create an educational video script about {topic}. Return a JSON object with two keys:
    1. 'explanation_script': A detailed script that can be used for voiceover, including timing markers
    2. 'visualization_script': A complete Python script using manim for visualization
    
    The visualization script should:
    - Include proper timing for audio sync
    - Add buffer pauses after animations for audio
    - Show data structures clearly
    - Include step-by-step animations
    
    Follow these guidelines:
    - Don't use LaTeX
    - Create a single merged output video
    - Add pauses after text display for audio sync
    - Show data structures alongside test cases
    - Include buffer time after animations for explanations
    
    Format the response as a valid JSON object with the two scripts as strings.
    """
    
    # Generate content using the provided LLM function
    response = generate_content(prompt)
    
    # Parse the JSON response
    try:
        scripts = json.loads(response)
        return scripts
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse LLM response as JSON: {e}")

# video_generator_api.py
from fastapi import FastAPI, File, UploadFile
from pathlib import Path
import subprocess
import os

app = FastAPI()

@app.post("/generate-video/")
async def generate_video(file: UploadFile = File(...), command: str = None):
    # Save uploaded Python file
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    try:
        # Execute manim command
        if not command:
            # Extract class name from the file
            with open(file_path, 'r') as f:
                content = f.read()
                import re
                class_match = re.search(r'class\s+(\w+)\(Scene\)', content)
                if class_match:
                    class_name = class_match.group(1)
                else:
                    raise ValueError("Could not find Scene class in the Python file")
            
            command = f"manim -pqh {file_path} {class_name}"
        
        result = subprocess.run(
            command.split(),
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            return {"error": result.stderr}
            
        # Get the generated video path
        video_path = list(Path("media").rglob("*.mp4"))[0]
        
        return {
            "status": "success",
            "video_path": str(video_path),
            "command_output": result.stdout
        }
        
    except Exception as e:
        return {"error": str(e)}
    
    finally:
        # Cleanup
        if os.path.exists(file_path):
            os.remove(file_path)

# workflow_orchestrator.py
def generate_educational_video(topic: str, client):
    """
    Orchestrates the complete video generation workflow.
    """
    try:
        # 1. Generate scripts using LLM
        scripts = generate_script(topic, client)
        
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
    
def generate_content(prompt):
  response=client.chat.completions.create(
      messages=[{
          "role":"user",
          "content":prompt
      }],
      model="llama-3.1-8b-instant",
      response_format={"type": "json_object"}
  )
  return response['choices'][0]['message']['content']

# Example usage:
if __name__ == "__main__":
    # Import and initialize your client here
    os.environ['GROQ_API_KEY'] = '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'
    client = Groq()
    result = generate_educational_video("binary search", client)
    
    if result["status"] == "success":
        print(f"Video generated successfully at: {result['video_path']}")
        print("\nExplanation script for voiceover:")
        print(result["explanation_script"])
    else:
        print(f"Error generating video: {result['error']}")