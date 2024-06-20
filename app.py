from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from typing import List
import os
from utils import speech_to_text, text_to_speech, autoplay_audio, get_answer

app = FastAPI()

class InputAudio(BaseModel):
    file: bytes

class OutputAudio(BaseModel):
    file_path: str

@app.post("/process_audio/")
async def process_audio(input_audio: InputAudio):
    # Save the audio file temporarily
    audio_file_path = "temp_audio.mp3"
    with open(audio_file_path, "wb") as audio_file:
        audio_file.write(input_audio.file)

    # Convert audio to text
    text = speech_to_text(audio_file_path)

    # Process the text
    processed_text = get_answer(text)

    # Generate audio from processed text
    output_audio_path = "processed_audio.mp3"
    text_to_speech(processed_text, output_audio_path)

    return {"file_path": output_audio_path}

