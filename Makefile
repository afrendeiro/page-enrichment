.DEFAULT_GOAL := pypitest

install:
	python -m \
		pip \
		install \
		git+https://github.com/afrendeiro/page-enrichment.git#egg=page \
		--user

test:
	python -m \
		pytest \
		--disable-warnings \
		--show-capture=no \
		--cov=page \
		--cov-report xml page/tests/test_*.py \
		--lf

coverage: test
	python -m codecov \
		-f coverage.xml
	python -m codacy \
		-r coverage.xml

docs:
	cd docs && $(MAKE) html
	xdg-open docs/build/html/index.html

build: test
	python setup.py sdist bdist_wheel

pypitest: build
	twine \
		upload \
		-r pypitest dist/*

pypi: build
	twine \
		upload \
		dist/*

gh:
	docker \
		build \
		-t page \
		.
	docker \
		tag \
		page \
		docker.pkg.github.com/afrendeiro/page-enrichment/page:latest
	docker \
		push \
		docker.pkg.github.com/afrendeiro/page-enrichment/page:latest

gh-release: install
	$(eval VERSION := \
		$(shell \
			python3 \
			-c 'from page import __version__ as v; print(v)'))
	docker \
		build \
		-t page:$(VERSION) \
		.
	docker \
		tag \
		page \
		docker.pkg.github.com/afrendeiro/page-enrichment/page:$(VERSION)
	docker \
		push \
		docker.pkg.github.com/afrendeiro/page-enrichment/page:$(VERSION)

clean_pyc:
	find . -name \*.pyc -delete

clean_mypy:
	rm -rf .mypy_cache/

clean_test:
	rm -rf .pytest_cache/
	rm -rf /tmp/pytest*
	find . -name "__pycache__" -exec rm -rf {} \;
	rm -rf .coverage*
	rm -rf .tox/

clean_cov: clean_test
	rm -fr coverage.xml htmlcov

clean_docs:
	rm -fr docs/build/

clean_dist:
	rm -fr dist/

clean_build:
	rm -fr build/
	rm -rf page/_version.py

clean_eggs:
	rm -fr page.egg-info
	rm -fr .eggs

clean: \
	clean_pyc \
	clean_mypy \
	clean_test \
	clean_cov \
	clean_docs \
	clean_dist \
	clean_build \
	clean_eggs

all: \
	test \
	coverage \
	docs \
	build \
	pypitest \
	pypi \
	clean

.PHONY: \
	test \
	coverage \
	docs \
	build \
	pypitest \
	pypi \
	clean_pyc \
	clean_mypy \
	clean_test \
	clean_cov \
	clean_docs \
	clean_dist \
	clean_build \
	clean_eggs \
	clean
