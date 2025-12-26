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
    # Render monitor ke liye response
    return "✅ Disney Stream is Active on Render!"

def run_web_server():
    # Render ke liye 0.0.0.0 aur dynamic port zaroori hai
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def start_stream():
    # Forceful encoding to fix Black Screen issues
    command = [
        'ffmpeg', '-hide_banner', '-loglevel', 'info',
        '-reconnect', '1', '-reconnect_streamed', '1', '-reconnect_delay_max', '5',
        '-i', INPUT_URL,
        
        # Video encoding fix (Black Screen Solutions)
        '-c:v', 'libx264', 
        '-preset', 'ultrafast', 
        '-tune', 'zerolatency',
        '-vf', 'scale=854:480,format=yuv420p', 
        '-b:v', '800k', 
        '-maxrate', '850k', 
        '-bufsize', '1700k',
        '-g', '50', 
        
        # Audio sync fix
        '-c:a', 'aac', 
        '-b:a', '128k', 
        '-ar', '44100',
        '-af', 'aresample=async=1',
        
        '-f', 'flv', 
        RTMP_URL
    ]
    
    while True:
        try:
            print("🚀 Starting Stream on Render...")
            subprocess.run(command)
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("🔄 Reconnecting in 5 seconds...")
        time.sleep(5)

if __name__ == "__main__":
    t = threading.Thread(target=run_web_server)
    t.daemon = True
    t.start()
    
    start_stream()
        
