run:
	python manage.py collectstatic --no-input
	python manage.py makemigrations --noinput
	python manage.py migrate --noinput
	python manage.py loaddata tag.json
	python manage.py loaddata ingredient.json
	python manage.py createsuperuser --username admin --email admin@foodgram.com