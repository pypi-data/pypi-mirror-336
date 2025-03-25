venv=. venv/bin/activate

makemigrations:
	$(venv); python makemigrations.py

build:
	$(venv); python -m build

publish:
	$(venv);\
		version=$$(cat pyproject.toml | grep 'version =' | cut -d' ' -f 3 | sed 's/"//g'); \
		python3 -m twine upload --repository pypi dist/*$${version}*

bp: build publish
