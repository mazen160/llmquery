.PHONY: clean build publish format

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

format:
	black .

build: clean format
	python -m build

publish: build
	python -m twine upload dist/*

test-publish: build
	python -m twine upload --repository testpypi dist/*
