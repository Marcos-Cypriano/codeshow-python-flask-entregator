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
	pytest tests/ -v --cov=entregator

test:
	pytest tests/ -v --cov=entregator

hello:
	echo "Hello"
