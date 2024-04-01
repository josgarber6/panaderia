mkdir -p logs
touch logs/gunicorn_access.log
touch logs/gunicorn_error.log

python3 ./manage.py makemigrations
python3 ./manage.py migrate

echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin123', 'admin@admin.com', 'adminSafePass123') if not User.objects.filter(username='admin123').exists() else None" | python manage.py shell

if [ ! -d "./media/products" ]; then
    python manage.py loaddata fixtures.json
fi

gunicorn backend.wsgi:application --config gunicorn.py
