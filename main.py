import asyncio
from flask import Flask, request, jsonify, render_template
import audio_manager
import command_listener  # Import the command_listener module

app = Flask(__name__)

# Flask routes for audio management
@app.route('/')
def index():
    files = os.listdir(audio_manager.UPLOAD_FOLDER)
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    response = audio_manager.upload_audio_file(file)
    return jsonify(response)

@app.route('/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    response = audio_manager.delete_audio_file(filename)
    return jsonify(response)

@app.route('/play', methods=['POST'])
def play_audio():
    filename = request.json.get('filename')
    response = audio_manager.schedule_playback(filename)
    return jsonify(response)

# Run the command listener asynchronously
async def run_command_listener():
    await asyncio.to_thread(command_listener.command_listener)

# Main async function to run Flask and command listener concurrently
async def main():
    # Start Flask app in a separate thread
    loop = asyncio.get_running_loop()
    flask_thread = asyncio.to_thread(app.run, host='0.0.0.0', port=5000)
    
    # Run command listener concurrently with Flask
    await asyncio.gather(run_command_listener(), flask_thread)

if __name__ == '__main__':
    asyncio.run(main())
