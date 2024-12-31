web: gunicorn adminB.adminB.wsgi:application --workers 2 --threads 4
release: python adminB/manage.py migrate && python adminB/manage.py collectstatic --noinput
