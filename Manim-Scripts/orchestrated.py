# script_generator.py
from typing import Dict

def generate_script(topic: str) -> Dict[str, str]:
    """
    Generate an educational script based on the topic.
    Returns both explanation and visualization scripts.
    """
    # Dummy prompt for script generation
    prompt = f"""
    Create an educational script about {topic}. Focus on:
    1. Clear explanation of concepts
    2. Step by step breakdown
    3. Visual elements that can be animated
    4. Timing for each section
    """
    
    # For demonstration, returning dummy response
    # In practice, replace with actual LLM call
    return {
        "explanation_script": """
        Let's understand how Binary Search works.
        
        First, we'll look at a sorted array of numbers: [1, 3, 5, 7, 9, 11, 13].
        We want to find the number 7.
        
        Step 1: We start by checking the middle element.
        Step 2: Compare it with our target.
        Step 3: Eliminate half of the array based on comparison.
        Step 4: Repeat until we find our target.
        """,
        "visualization_script": """
        from manim import *

class BinarySearchVisualization(Scene):
    def construct(self):
        # Create title
        title = Text("Binary Search Visualization")
        self.play(Write(title), run_time=2)
        self.wait(2)  # Buffer for audio
        self.play(title.animate.scale(0.5).to_edge(UP))
        self.wait(1)

        # Create array
        numbers = [1, 3, 5, 7, 9, 11, 13]
        squares = VGroup(*[
            Square(side_length=1).set_fill(BLUE, opacity=0.5)
            for _ in numbers
        ]).arrange(RIGHT, buff=0.1)
        
        # Add numbers inside squares
        number_labels = VGroup(*[
            Text(str(num)).move_to(square)
            for num, square in zip(numbers, squares)
        ])
        
        # Show array
        self.play(Create(squares), run_time=2)
        self.play(Write(number_labels), run_time=2)
        self.wait(2)  # Buffer for audio explanation

        # Target number
        target_text = Text("Target: 7").next_to(squares, UP, buff=1)
        self.play(Write(target_text))
        self.wait(2)  # Buffer for audio

        # Binary search steps
        left, right = 0, len(numbers) - 1
        
        while left <= right:
            mid = (left + right) // 2
            
            # Highlight current range
            current_range = squares[left:right+1].copy()
            self.play(current_range.animate.set_fill(YELLOW, opacity=0.3))
            self.wait(1)
            
            # Highlight middle element
            self.play(squares[mid].animate.set_fill(RED, opacity=0.7))
            self.wait(2)  # Buffer for audio
            
            if numbers[mid] == 7:
                # Found target
                success_text = Text("Found 7!", color=GREEN).next_to(squares, DOWN)
                self.play(Write(success_text))
                self.wait(2)
                break
            elif numbers[mid] < 7:
                left = mid + 1
                # Show elimination of left half
                eliminate_range = squares[left:mid+1].copy()
                self.play(eliminate_range.animate.set_fill(GRAY, opacity=0.5))
            else:
                right = mid - 1
                # Show elimination of right half
                eliminate_range = squares[mid:right+1].copy()
                self.play(eliminate_range.animate.set_fill(GRAY, opacity=0.5))
            
            self.wait(2)  # Buffer for audio

        # Final buffer
        self.wait(3)
        """
    }

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
            command = f"manim -pql {file_path} BinarySearchVisualization"
        
        result = subprocess.run(
            command.split(),
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            return {"error": result.stderr}
            
        # Get the generated video path
        # Manim typically saves to media/videos/scene_name/quality/scene_name.mp4
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
def generate_educational_video(topic: str):
    """
    Orchestrates the complete video generation workflow.
    """
    # 1. Generate scripts
    scripts = generate_script(topic)
    
    # 2. Save visualization script to file
    viz_file = "binary_search_viz.py"
    with open(viz_file, "w") as f:
        f.write(scripts["visualization_script"])
    
    # 3. Call video generation API
    import requests
    
    files = {
        'file': ('binary_search_viz.py', open(viz_file, 'rb')),
    }
    
    response = requests.post(
        'http://localhost:8000/generate-video/',
        files=files
    )
    
    return {
        "status": "success",
        "explanation_script": scripts["explanation_script"],
        "video_path": response.json()["video_path"]
    }

generate_educational_video("Binary Search")