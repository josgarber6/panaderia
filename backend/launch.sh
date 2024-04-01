python3 ./manage.py makemigrations
python3 ./manage.py migrate
python3 ./manage.py createsuperuser --noinput
python3 ./manage.py loaddata fixtures.json