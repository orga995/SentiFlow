# 1. מתחילים מגרסת פייתון קלה
FROM python:3.9-slim

# 2. מגדירים תיקיית עבודה
WORKDIR /app

# 3. מתקינים את הספריות
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. מעתיקים את כל הקוד (כולל תיקיית templates)
COPY . .

# 5. חושפים את הפורט של האתר
EXPOSE 5001

# 6. הגדרות כדי שפלאסק ירוץ חלק בתוך דוקר
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5001

# 7. פקודת ההרצה
CMD ["python", "app.py"]