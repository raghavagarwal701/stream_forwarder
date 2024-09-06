import subprocess
import threading
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
RTMP_SERVER = "rtmp://localhost:1935/live"

# Dictionary to keep track of active streams
active_streams = {}


def stream_to_youtube(stream_name, youtube_url, stop_event):
    input_url = f"{RTMP_SERVER}/{stream_name}"
    print(input_url)
    # overlay_image = '/path/to/your/overlay/'+stream_name+'.png'  # Update this path to your overlay image
    overlay_image = 'sampleimage.png'

    ffmpeg_command = [
        'ffmpeg',
        '-i', input_url,
        '-i', overlay_image,
        '-filter_complex', '[0:v]transpose=1[v];[v][1:v]overlay=10:10',
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-strict', 'experimental',
        '-f', 'flv',
        youtube_url
    ]
    # ffmpeg_command = [
    #     'ffmpeg',
    #     '-i', input_url,
    #     '-i', overlay_image,
    #     '-filter_complex', 'overlay=350:550',
    #     '-c:v', 'libx264', 
    #     '-c:a', 'aac', 
    #     '-strict', 'experimental',
    #     '-f', 'flv',
    #     youtube_url
    # ]

    process = subprocess.Popen(ffmpeg_command)

    while not stop_event.is_set():
        if process.poll() is not None:
            print(f"FFmpeg process for stream {
                  stream_name} has ended unexpectedly.")
            break

    if process.poll() is None:
        process.terminate()
        process.wait()

    print(f"Stream {stream_name} stopped")


@app.route('/start_stream', methods=['POST'])
def start_stream():
    data = request.json
    youtube_url = data.get('youtube_url')
    stream_name = data.get('stream_name')
    print(youtube_url, stream_name)
    if not youtube_url or not stream_name:
        return jsonify({'error': 'Missing youtube_url or stream_name'}), 400

    if stream_name in active_streams:
        return jsonify({'error': 'Stream already active'}), 409

    stop_event = threading.Event()
    thread = threading.Thread(target=stream_to_youtube, args=(
        stream_name, youtube_url, stop_event))
    thread.start()

    active_streams[stream_name] = {
        'thread': thread,
        'stop_event': stop_event,
        'youtube_url': youtube_url
    }

    return jsonify({'message': f'Stream {stream_name} started successfully'}), 200


@app.route('/stop_stream', methods=['POST'])
def stop_stream():
    data = request.json
    stream_name = data.get('stream_name')
    if not stream_name:
        return jsonify({'error': 'Missing stream_name'}), 400

    if stream_name not in active_streams:
        return jsonify({'error': 'Stream not found'}), 404

    active_streams[stream_name]['stop_event'].set()
    active_streams[stream_name]['thread'].join()
    del active_streams[stream_name]

    return jsonify({'message': f'Stream {stream_name} stopped successfully'}), 200


@app.route('/list_streams', methods=['GET'])
def list_streams():
    return jsonify({name: {'youtube_url': info['youtube_url']} for name, info in active_streams.items()}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1233)
