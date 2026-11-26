clean_db: manage.py
	@echo "Cleaning the database..."
	rm -f db.sqlite3
	.venv/bin/python3 manage.py makemigrations
	.venv/bin/python3 manage.py migrate
	.venv/bin/python3 manage.py populate

run: manage.py
	@echo "Running the Django development server..."
	.venv/bin/python3 manage.py runserver

setup: requirements.txt
	@echo "Setting up the virtual environment..."
	rm -rf .venv
	python3 -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt
	make clean_db
