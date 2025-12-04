web: if [ -d "backend" ]; then cd backend; fi && python manage.py migrate && gunicorn core.wsgi:application --bind 0.0.0.0:$PORT

