import subprocess
import threading
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import time
from score_fetch import fetch_match_data
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)

# Configuration
RTMP_SERVER = "rtmp://localhost:1935/live"

# Dictionary to keep track of active streams
active_streams = {}

def stream_to_youtube(stream_name, youtube_url, stop_event):
    input_url = f"{RTMP_SERVER}/{stream_name}"
    print(input_url)

    while not stop_event.is_set():
        # Generate the overlay image
        main(stream_name)
        overlay_image = f"{stream_name}.png"

        ffmpeg_command = [
            'ffmpeg',
            '-i', input_url,
            '-i', overlay_image,
            '-filter_complex', '[0:v]transpose=2[v];[v][1:v]overlay=10:10',
            '-c:v', 'libx264',
            '-c:a', 'aac',
            '-strict', 'experimental',
            '-f', 'flv',
            youtube_url
        ]

        process = subprocess.Popen(ffmpeg_command)

        while not stop_event.is_set():
            if process.poll() is not None:
                print(f"FFmpeg process for stream {stream_name} has ended unexpectedly.")
                break
            time.sleep(1)  # Wait for 1 second before generating the next overlay image

        if process.poll() is None:
            process.terminate()
            process.wait()

    print(f"Stream {stream_name} stopped")

def main(stream_name):
    match_id = stream_name
    score = fetch_match_data(match_id)
    print(score)

    # Open the sample image
    img = Image.open('sampleimage.png')
    draw = ImageDraw.Draw(img)

    # Load custom font (if available, otherwise default font)
    font_path = "OpenSans-Regular.ttf"  # Change this to the path of a .ttf font file if you want to use one
    default_font_size = 20
    try:
        font = ImageFont.truetype(font_path, default_font_size)
    except IOError:
        font = ImageFont.load_default()

    # Define score details with their specific coordinates and font sizes
    score_elements = [
        {"text": f"{score['batting_team']}", "position": (230, 3), "font_size": 44},
        {"text": f"{score['bowling_team']}", "position": (1800, 3), "font_size": 44},
        {"text": f"{score['score']}", "position": (1000, 60), "font_size": 54},
        {"text": f"{score['overs_bowled']} ", "position": (1120, 80), "font_size": 34},
        {"text": f"{score['batter_one']}:  {score['batter_one_score']['runs']}({score['batter_one_score']['balls']})", "position": (85, 70), "font_size": 35},
        {"text": f"{score['batter_two']}:  {score['batter_two_score']['runs']}({score['batter_two_score']['balls']})", "position": (85, 130), "font_size": 35},
        {"text": f"{score['bowler']} - {score['bowler_figure']['runsGiven']}/{score['bowler_figure']['wickets']} in {score['bowler_figure']['ballsDelivered']} balls", "position": (1650, 100), "font_size": 40}
    ]

    # Loop through score elements and add each to the image
    for element in score_elements:
        # Adjust font size if specified
        font = ImageFont.truetype(font_path, element["font_size"]) if font_path else ImageFont.load_default()
        
        # Add the text to the image at the specified position
        draw.text(element["position"], element["text"], font=font, fill="white")

    # Save the modified image with match_id as the filename
    img.save(f'{match_id}.png')

    print(f"Image saved as {match_id}.png")