from fastapi import HTTPException
from pydub import AudioSegment
from pydub.utils import mediainfo
import os

def get_mime_type(file_path: str) -> str:
    try:
        info = mediainfo(file_path)
        return f"audio/{info['format_name']}"
    except Exception:
        return "unknown"

def convert_to_wav(file_path: str) -> str:
    try:
        audio = AudioSegment.from_file(file_path)
        wav_path = file_path.rsplit(".", 1)[0] + ".wav"
        audio.export(wav_path, format="wav")
        return wav_path
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to convert audio to WAV: {e}")

def audiocheck(file_location: str, file) -> dict[str, any]:
    
    file_mime_type = get_mime_type(file_location)

    if not file_mime_type.startswith("audio/"):
        os.remove(file_location)
        raise HTTPException(status_code=400, detail="Uploaded file is not an audio file")

    file_info = {
        "filename": file.filename,
        "content_type": file.content_type,
        "mime_type": file_mime_type,
        "original_size": os.path.getsize(file_location),
    }

    return file_info

def audiosend(file_location: str) -> str:
    
    wav_file_location = convert_to_wav(file_location)
    return wav_file_location