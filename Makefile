.DEFAULT_GOAL := pre-commit

clean:
	find ./ \
        \( \
        -iname '*.pyc' \
        -o -iname '*.pyo' \
        -o -iname __pycache__ \
        -o -iname .pytest_cache \
        -o -iname coverage \
        -o -iname .coverage \
        \) \
        -exec rm -rfv {} +

python-venv-setup:
	python3 -m venv venv
	source venv/bin/activate && pip install -r requirements.txt && pre-commit install

setup: python-venv-setup

pre-commit:
	pre-commit run --all-files --verbose --show-diff-on-failure

test:
	tox
