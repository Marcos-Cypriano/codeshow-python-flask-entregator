install:
	pip install -e .['dev']

clean:
	@find ./ -name '*.py' -exec rm -f {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
	rm -rf .cache
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -rf htmlcov
	rm -rf	.tox/
	rm -rf docs/_build
	pip install -e .['dev'] --upgrade --no-cache
	
test:
	FLASK_ENV=test pytest tests/ -v --cov=entregator

test:
	FLASK_ENV=test pytest tests/ -v --cov=entregator

init_db:
	FLASK_APP=entregator/app.py flask create-db
	FLASK_APP=entregator/app.py flask db upgrade

format:
	isort **/*.py
	black -l 79 **/*.py

run:
	FLASK_APP=entregator/app.py FLASK_ENV=development flask run
	