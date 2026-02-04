import os
import time
import re
from flask import Flask, request, jsonify
from textblob import TextBlob
from deep_translator import GoogleTranslator
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError

app = Flask(__name__)

# הגדרת DB
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_text = db.Column(db.Text, nullable=False)
    sentiment = db.Column(db.String(50))
    score = db.Column(db.Float)
    suggestion = db.Column(db.Text, nullable=True)

# --- מנגנון המתנה לדאטה-בייס (מונע קריסה בהתחלה) ---
def init_db_connection():
    max_retries = 15
    print("⏳ Waiting for Database to wake up...")
    
    for i in range(max_retries):
        try:
            with app.app_context():
                db.create_all()
            print("✅ Database connected successfully!")
            return
        except OperationalError:
            print(f"⚠️ Database not ready yet... retrying ({i+1}/{max_retries})")
            time.sleep(3)
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            time.sleep(3)

init_db_connection()

# --- פונקציה לחילוץ הצעות ---
def extract_suggestion_from_text(text):
    keywords = [
        "should", "recommend", "suggest", "better if", "fix", "improve", "needs to", "please", 
        "כדאי", "מומלץ", "צריך", "לשפר", "הייתי מציע", "עדיף", "חבל ש", "תקנו", "חסר"
    ]
    # בדיקה פשוטה אם המשפט מכיל מילת מפתח
    if any(word in text.lower() for word in keywords):
        return text.strip()
    return None

# --- פונקציה לניתוח שורה בודדת ---
def analyze_single_line(text):
    if not text or not text.strip():
        return None

    # תרגום (אם צריך)
    try:
        translated = GoogleTranslator(source='auto', target='en').translate(text)
    except:
        translated = text

    # ניתוח סנטימנט
    analysis = TextBlob(translated)
    polarity = analysis.sentiment.polarity
    
    # חידוד הרגש
    if polarity > 0.05: sentiment = "Positive"
    elif polarity < -0.05: sentiment = "Negative"
    else: sentiment = "Neutral"
    
    # חיפוש הצעה
    suggestion = extract_suggestion_from_text(text)
    
    return {
        'translated': translated,
        'sentiment': sentiment,
        'score': round(polarity, 2),
        'suggestion': suggestion
    }

@app.route('/analyze_bulk', methods=['POST'])
def analyze_bulk():
    data = request.get_json()
    raw_text = data.get('text', '')
    
    # --- התיקון הגדול: פיצול לפי שורה בודדת ---
    # כל שורה תנותח בנפרד כדי להפריד בין "האוכל טוב" ל"השירות רע"
    lines = raw_text.split('\n')
    
    results = []
    positive_sum = 0
    negative_sum = 0
    valid_lines_count = 0
    
    for line in lines:
        # דילוג על שורות ריקות לגמרי
        if len(line.strip()) < 2: continue
        
        analysis = analyze_single_line(line)
        if not analysis: continue

        valid_lines_count += 1
        
        # שמירה ל-DB
        new_review = Review(
            original_text=line, 
            sentiment=analysis['sentiment'], 
            score=analysis['score'], 
            suggestion=analysis['suggestion']
        )
        db.session.add(new_review)
        
        # חישוב סכומים נפרדים
        if analysis['score'] > 0:
            positive_sum += analysis['score']
        elif analysis['score'] < 0:
            negative_sum += analysis['score'] # זה יצבור מינוסים (למשל -1.5)

        results.append({
            'original': line,
            'sentiment': analysis['sentiment'],
            'score': analysis['score'],
            'suggestion': analysis['suggestion']
        })
    
    db.session.commit()
    
    # מיון התוצאות
    sorted_reviews = sorted(results, key=lambda x: x['score'], reverse=True)
    
    return jsonify({
        'total_reviews': valid_lines_count, # עכשיו סופר שורות רלוונטיות
        'total_positive_score': round(positive_sum, 2),
        'total_negative_score': round(negative_sum, 2),
        'pros': sorted_reviews[:3], # יקח את השורות החיוביות ביותר
        'cons': sorted_reviews[-3:], # יקח את השורות השליליות ביותר
        'all_reviews': results
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)