import sounddevice as sd
import numpy as np
import audio_manager  # Assuming your playback functions are here

# Audio settings
sample_rate = 44100  # Samples per second
duration = 1  # Duration to listen per check (in seconds)
volume_threshold = 0.3  # Adjust this value based on noise levels in your environment

def is_squawk_below_threshold(volume):
    """Return True if the volume is below the defined threshold."""
    return volume < volume_threshold

def detect_squawk():
    """Detect squawks and trigger responses if volume is below threshold."""
    # Start listening to audio data
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()  # Block until recording is finished
    
    # Calculate volume by finding the root mean square of the audio data
    volume = np.sqrt(np.mean(np.square(recording)))
    
    if is_squawk_below_threshold(volume):
        print("Squawk detected below threshold. Triggering response.")
        audio_manager.play_audio_file("positive_response.mp3", 2)  # Example response
    else:
        print("Squawk too loud. Ignoring.")

# Example loop to check continuously
while True:
    detect_squawk()
