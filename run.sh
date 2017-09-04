pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
gunicorn -w 1 -t 180 -b 0.0.0.0:8000 wellcoders_backend.wsgi
