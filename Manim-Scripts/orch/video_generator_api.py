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