migrations:
	python donateasyouread/manage.py makemigrations

migrate:
	python donateasyouread/manage.py migrate

runserver:
	python donateasyouread/manage.py runserver 8001

collectstatic:
	python donateasyouread/manage.py collectstatic



