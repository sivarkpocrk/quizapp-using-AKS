#!/bin/sh

set -e

echo "🚀 Starting Django QuizApp container..."

# ✅ Fix permissions (only needed if not already handled in Dockerfile)
chown -R django-user:django-user /vol/web/static /vol/web/media
chmod -R 755 /vol/web/static
chmod -R 777 /vol/web/media

# SQLite permission fix (only for SQLite users)
# if [ -f /quizapp/db.sqlite3 ]; then
#     chmod 666 /quizapp/db.sqlite3
# fi

# ✅ Collect static files
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

# ✅ Apply migrations
echo "🧱 Running migrations..."
python manage.py migrate

# ✅ (Optional) Load initial data
# python manage.py loaddata initial_data.json

echo "🚀 Starting Gunicorn..."
gunicorn quizapp.wsgi:application \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile - \
  --workers 4


#gunicorn --bind :9000 --workers 4 app.wsgi
