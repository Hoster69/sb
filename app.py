from flask import Flask, render_template, jsonify, url_for
from datetime import datetime, timezone
import threading
import time
import urllib.request

app = Flask(__name__, static_url_path='/static')

def keep_alive():
    while True:
        try:
            urllib.request.urlopen("https://slapbattles.onrender.com/health")
            print("Server pinged successfully")
        except Exception as e:
            print(f"Failed to ping server: {e}")
        time.sleep(840)  # 14 minutes, just under Render's 15-minute sleep threshold

@app.route('/health')
def health_check():
    return jsonify({"status": "alive", "timestamp": datetime.now(timezone.utc).isoformat()})

@app.route('/')
def index():
    # Calculate time remaining until April 20th 2025
    shutdown_date = datetime(2025, 4, 20, tzinfo=timezone.utc)
    current_date = datetime.now(timezone.utc)
    time_remaining = shutdown_date - current_date
    
    days_remaining = time_remaining.days
    hours = time_remaining.seconds // 3600
    minutes = (time_remaining.seconds % 3600) // 60
    seconds = time_remaining.seconds % 60
    
    return render_template('index.html', 
                         days_remaining=max(0, days_remaining),
                         hours_remaining=hours,
                         minutes_remaining=minutes,
                         seconds_remaining=seconds)

if __name__ == '__main__':
    # Start the keep-alive thread
    ping_thread = threading.Thread(target=keep_alive, daemon=True)
    ping_thread.start()
    
    app.run(debug=False, host='0.0.0.0', port=8080) 