web: gunicorn adminB.adminB.wsgi:application --workers 2 --threads 4
release: python manage.py migrate && python manage.py collectstatic --noinput
