# 1. Base Image - אנחנו מתחילים ממערכת הפעלה קלה שכבר יש בה Python
FROM python:3.9-slim

# 2. Work Directory - מגדירים איפה נעבוד בתוך הקונטיינר
WORKDIR /app

# 3. Dependencies - מעתיקים קודם רק את רשימת המצרכים (בשביל Caching יעיל)
COPY requirements.txt .

# 4. Install - מתקינים את הספריות (Flask ו-TextBlob)
RUN pip install --no-cache-dir -r requirements.txt

# 5. NLP Data - מורידים את מאגר המילים של TextBlob לניתוח שפה
RUN python -m textblob.download_corpora

# 6. Copy Code - עכשיו מעתיקים את שאר הקוד שלנו (app.py)
COPY . .

# 7. Expose - מצהירים שהאפליקציה רצה בפורט 5000
EXPOSE 5000

# 8. Command - הפקודה שתרוץ כשהקונטיינר יעלה
CMD ["python", "app.py"]