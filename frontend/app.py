from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)
BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:5000")

@app.route('/', methods=['GET', 'POST'])
def index():
    report = None
    
    if request.method == 'POST':
        bulk_text = request.form.get('bulk_text')
        
        if bulk_text:
            try:
                # שליחת הטקסט הגולמי לניתוח
                response = requests.post(f"{BACKEND_URL}/analyze_bulk", json={'text': bulk_text})
                if response.status_code == 200:
                    report = response.json()
            except Exception as e:
                print(f"Error: {e}")

    return render_template('index.html', report=report)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)