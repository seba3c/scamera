web: gunicorn wsgi --log-file -
worker: python manage.py runftpdserver
worker: python manage.py runtelegrambot -b scamera_bot