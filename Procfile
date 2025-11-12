web: python manage.py migrate && python manage.py collectstatic --noinput && gunicorn control_asistencia.wsgi --bind 0.0.0.0:$PORT
