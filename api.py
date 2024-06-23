from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from audiocheck import audiocheck,audiosend
import uvicorn
import json
import os

app = FastAPI()
# Allow all origins for demonstration purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):
    global file_location
    try:
        
        file_location = rf"Input/temp_{file.filename}"
        
        with open(file_location, "wb") as buffer:
            buffer.write(file.file.read())
        
        return audiocheck(file_location,file)
    
    except Exception as e:
        return {"error": str(e)}
    # os.remove(file_location)
    # return JSONResponse(content=file_info)

@app.get("/get-audio")
async def send_audio():
    global file_location
    wav = audiosend(file_location)
    return FileResponse(path=wav, filename=os.path.basename(wav))
    
@app.get("/get-data")
async def send_data():
    
    file_path = 'Output/data.json'
    
    try:
        
        if os.path.exists(file_path):
        
            with open(file_path, 'r', encoding='utf-8') as file:
        
                data = json.load(file)
                return JSONResponse(content=data)
    
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Data file not found")
    
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Error parsing JSON data")

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)