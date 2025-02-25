from flask import Flask, render_template
from datetime import datetime, timezone

app = Flask(__name__)

@app.route('/')
def index():
    # Calculate time remaining until April 20th
    shutdown_date = datetime(2024, 4, 20, tzinfo=timezone.utc)
    current_date = datetime.now(timezone.utc)
    time_remaining = shutdown_date - current_date
    days_remaining = max(0, time_remaining.days)
    
    return render_template('index.html', days_remaining=days_remaining)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8080) 