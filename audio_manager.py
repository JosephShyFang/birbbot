from playsound import playsound
import os
import time
from threading import Timer

UPLOAD_FOLDER = 'audio_files/'

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Default playback settings
delay_between_plays = 10  # seconds
play_duration = 5  # seconds

def play_audio_file(file_path, duration):
    """Play an audio file for a specified duration."""
    try:
        Timer(0, playsound, args=[file_path]).start()  # Asynchronous play
        time.sleep(duration)  # Control playback duration
    except Exception as e:
        print(f"Error playing audio: {e}")

def upload_audio_file(file):
    """Save the uploaded audio file."""
    if file.filename.endswith(('wav', 'mp3')):
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        return {"status": "success", "message": "File uploaded successfully"}
    return {"status": "error", "message": "Invalid file format"}

def delete_audio_file(filename):
    """Delete an audio file."""
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return {"status": "success", "message": f"{filename} deleted"}
    return {"status": "error", "message": "File not found"}

def set_playback_timing(delay, duration):
    """Set delay and duration for audio playback."""
    global delay_between_plays, play_duration
    delay_between_plays = delay
    play_duration = duration
    return {"status": "success", "message": "Playback timing updated"}

def schedule_playback(filename):
    """Schedule playback of an audio file."""
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(file_path):
        return {"status": "error", "message": "File not found"}

    def play_loop():
        play_audio_file(file_path, play_duration)
        Timer(delay_between_plays, play_loop).start()

    Timer(delay_between_plays, play_loop).start()
    return {"status": "success", "message": "Audio playback started"}
