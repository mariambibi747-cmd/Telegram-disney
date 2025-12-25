import subprocess
import time
import threading
import os
from flask import Flask

# --- CONFIGURATION ---
INPUT_URL = "http://103.182.170.32:8888/play/a04g"
SERVER_URL = "rtmps://dc5-1.rtmp.t.me/s/"
STREAM_KEY = "3519271296:HrkJNqE1ZRx7Xl6TB2d2zQ"
RTMP_URL = f"{SERVER_URL}{STREAM_KEY}"

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Stream is Running 24/7"

def run_web_server():
    # Render default port 10000 use karta hai
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def start_stream():
    command = [
        'ffmpeg',
        '-hide_banner', '-loglevel', 'info',
        '-reconnect', '1', '-reconnect_streamed', '1', '-reconnect_delay_max', '5',
        '-i', INPUT_URL,
        '-c:v', 'libx264', '-preset', 'ultrafast', '-tune', 'zerolatency',
        '-b:v', '700k', '-s', '854x480', '-r', '24', '-g', '48', '-pix_fmt', 'yuv420p',
        '-c:a', 'aac', '-b:a', '96k', '-ar', '44100', '-af', 'aresample=async=1',
        '-f', 'flv', RTMP_URL
    ]
    
    while True:
        try:
            print("🚀 Starting Stream...")
            subprocess.run(command)
        except Exception as e:
            print(f"❌ Error: {e}")
        time.sleep(5)

if __name__ == "__main__":
    t = threading.Thread(target=run_web_server)
    t.daemon = True
    t.start()
    start_stream()
