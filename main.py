from flask import Flask, request, jsonify, render_template
import audio_manager

app = Flask(__name__)

@app.route('/')
def index():
    files = os.listdir(audio_manager.UPLOAD_FOLDER)
    return render_template('index.html', files=files, delay=audio_manager.delay_between_plays, duration=audio_manager.play_duration)

@app.route('/upload', methods=['POST'])
def upload_file():
    """Endpoint to upload a new audio file."""
    file = request.files['file']
    response = audio_manager.upload_audio_file(file)
    return jsonify(response)

@app.route('/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    """Endpoint to delete an audio file."""
    response = audio_manager.delete_audio_file(filename)
    return jsonify(response)

@app.route('/play', methods=['POST'])
def play_audio():
    """Endpoint to start playing an audio file with a delay and duration."""
    filename = request.json.get('filename')
    response = audio_manager.schedule_playback(filename)
    return jsonify(response)

@app.route('/set_timer', methods=['POST'])
def set_timer():
    """Endpoint to set delay and duration for playback."""
    delay = request.json.get('delay', audio_manager.delay_between_plays)
    duration = request.json.get('duration', audio_manager.play_duration)
    response = audio_manager.set_playback_timing(delay, duration)
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
